import csv
import os
import re
import time
import unicodedata
from urllib.parse import quote

import requests

API = "https://commons.wikimedia.org/w/api.php"
# Commons chiede un User-Agent descrittivo: inserisci il tuo contatto
HEADERS = {"User-Agent": "corso-bauer/0.1 (contatto: tua@email.it)"}

# --- impostazioni: modifica solo queste righe ---
CATEGORIA = "Media from Archivio Storico Touring Club Italiano"
CARTELLA = "immagini"
CSV_CREDITI = "crediti.csv"
SCARICA_TUTTE = False   # False = prova con i primi 10 file, True = tutti
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


def chiave_file(nome):
    """Forma uniforme del nome di un file, per collegare i dati."""
    return nome.removeprefix("File:").replace("_", " ")


def nome_sicuro(nome):
    """Nome senza accenti, spazi o simboli: solo lettere, cifre, underscore e estensione minuscola."""
    base, ext = os.path.splitext(nome)
    base = unicodedata.normalize("NFKD", base).encode("ascii", "ignore").decode("ascii")
    base = re.sub(r"[^A-Za-z0-9]+", "_", base).strip("_") or "file"
    ext = re.sub(r"[^a-z0-9]", "", ext.lower())
    return base + ("." + ext if ext else "")


def assegna_nomi(originali):
    """Un nome sicuro per ogni file originale, senza due file con lo stesso nome."""
    sicuri, usati = {}, set()
    for chiave in sorted(originali):
        base = nome_sicuro(originali[chiave])
        candidato, n = base, 2
        while candidato in usati:
            radice, ext = os.path.splitext(base)
            candidato = f"{radice}_{n}{ext}"
            n += 1
        usati.add(candidato)
        sicuri[chiave] = candidato
    return sicuri


def crediti(titoli, file_csv, sicuri):
    """Scrive un CSV con file, file originale, link, autore, licenza e data di ogni file."""
    with open(file_csv, "w", newline="", encoding="utf-8") as f:
        scrittore = csv.writer(f)
        scrittore.writerow([
            "file", "file_originale", "pagina", "autore", "licenza",
            "link_licenza", "credit", "data",
        ])
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
                    sicuri[chiave_file(nome)],
                    nome.removeprefix("File:"),
                    link,
                    valore(info, "Artist"),
                    valore(info, "LicenseShortName"),
                    valore(info, "LicenseUrl"),
                    valore(info, "Credit"),
                    valore(info, "DateTimeOriginal") or valore(info, "DateTime"),
                ])
            time.sleep(1)  # una pausa tra una richiesta e l'altra


def scarica(elenco, cartella, larghezza):
    """Scarica ogni file da Commons e lo salva con il nome sicuro."""
    os.makedirs(cartella, exist_ok=True)
    for originale, sicuro in elenco:
        url = f"https://commons.wikimedia.org/wiki/Special:FilePath/{quote(originale)}?width={larghezza}"
        r = requests.get(url, headers=HEADERS, timeout=60)
        r.raise_for_status()
        with open(os.path.join(cartella, sicuro), "wb") as f:
            f.write(r.content)
        print("scaricato:", sicuro)
        time.sleep(1)  # una pausa tra un download e l'altro


if __name__ == "__main__":
    titoli = sorted(set(file_ricorsivo(CATEGORIA)))
    print(len(titoli), "file trovati in", CATEGORIA, "e nelle sottocategorie")

    originali = {chiave_file(t): t.removeprefix("File:") for t in titoli}
    sicuri = assegna_nomi(originali)

    crediti(titoli, CSV_CREDITI, sicuri)
    print("crediti scritti in", CSV_CREDITI)

    elenco = [(originali[k], sicuri[k]) for k in sorted(originali)]
    da_scaricare = elenco if SCARICA_TUTTE else elenco[:10]
    scarica(da_scaricare, CARTELLA, LARGHEZZA)
