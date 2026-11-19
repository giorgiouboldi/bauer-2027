import csv
import os
import time
from urllib.parse import quote

import requests

API = "https://commons.wikimedia.org/w/api.php"
# Commons chiede un User-Agent descrittivo: inserisci il tuo contatto
HEADERS = {"User-Agent": "corso-bauer/0.1 (contatto: giorgio@calib.ro)"}

# --- impostazioni: modifica solo queste righe ---
CATEGORIA = "Media from Archivio Storico Touring Club Italiano"
CARTELLA = "immagini"
CSV_CREDITI = "crediti.csv"
SCARICA_TUTTE = True   # False = prova con i primi 10 file, True = tutti
LARGHEZZA = 1000        # larghezza in pixel delle immagini scaricate


def membri(categoria, tipo):
    """Restituisce tutti i membri di tipo 'file' o 'subcat', seguendo la paginazione."""
    risultati, cont = [], None
    while True:
        params = {
            "action": "query",
            "list": "categorymembers",
            "cmtitle": f"Category:{categoria}",
            "cmtype": tipo,
            "cmlimit": "500",
            "format": "json",
        }
        if cont:
            params["cmcontinue"] = cont
        r = requests.get(API, params=params, headers=HEADERS, timeout=30)
        r.raise_for_status()
        dati = r.json()
        risultati += [m["title"] for m in dati["query"]["categorymembers"]]
        if "continue" not in dati:
            return risultati
        cont = dati["continue"]["cmcontinue"]


def file_ricorsivo(categoria, visitate=None):
    """Raccoglie i file della categoria e di tutte le sottocategorie."""
    if visitate is None:
        visitate = set()
    if categoria in visitate:
        return []
    visitate.add(categoria)
    trovati = membri(categoria, "file")
    for sotto in membri(categoria, "subcat"):
        trovati += file_ricorsivo(sotto.removeprefix("Category:"), visitate)
    return trovati


def valore(info, chiave):
    """Restituisce il valore di un campo dei metadati, o stringa vuota se manca."""
    return info.get(chiave, {}).get("value", "")


def crediti(titoli, file_csv):
    """Scrive un CSV con titolo, link, autore, licenza e data di ogni file."""
    with open(file_csv, "w", newline="", encoding="utf-8") as f:
        scrittore = csv.writer(f)
        scrittore.writerow(["file", "pagina", "autore", "licenza", "link_licenza", "credit", "data"])
        # l'API accetta al massimo 50 titoli per richiesta
        for i in range(0, len(titoli), 50):
            params = {
                "action": "query",
                "prop": "imageinfo",
                "iiprop": "extmetadata",
                "titles": "|".join(titoli[i:i + 50]),
                "format": "json",
            }
            r = requests.get(API, params=params, headers=HEADERS, timeout=30)
            r.raise_for_status()
            for pagina in r.json()["query"]["pages"].values():
                if "imageinfo" not in pagina:
                    continue  # file non trovato
                info = pagina["imageinfo"][0]["extmetadata"]
                nome = pagina["title"]
                link = "https://commons.wikimedia.org/wiki/" + quote(nome.replace(" ", "_"))
                scrittore.writerow([
                    nome,
                    link,
                    valore(info, "Artist"),
                    valore(info, "LicenseShortName"),
                    valore(info, "LicenseUrl"),
                    valore(info, "Credit"),
                    valore(info, "DateTimeOriginal") or valore(info, "DateTime"),
                ])
            time.sleep(1)  # una pausa tra una richiesta e l'altra


def scarica(titoli, cartella, larghezza):
    """Scarica ogni file nella cartella, con il nome originale e la larghezza indicata."""
    os.makedirs(cartella, exist_ok=True)
    for titolo in titoli:
        nome = titolo.removeprefix("File:")
        url = f"https://commons.wikimedia.org/wiki/Special:FilePath/{quote(nome)}?width={larghezza}"
        r = requests.get(url, headers=HEADERS, timeout=60)
        r.raise_for_status()
        with open(os.path.join(cartella, nome), "wb") as f:
            f.write(r.content)
        print("scaricato:", nome)
        time.sleep(1)  # una pausa tra un download e l'altro


if __name__ == "__main__":
    titoli = sorted(set(file_ricorsivo(CATEGORIA)))
    print(len(titoli), "file trovati in", CATEGORIA, "e nelle sottocategorie")

    crediti(titoli, CSV_CREDITI)
    print("crediti scritti in", CSV_CREDITI)

    da_scaricare = titoli if SCARICA_TUTTE else titoli[:10]
    scarica(da_scaricare, CARTELLA, LARGHEZZA)
