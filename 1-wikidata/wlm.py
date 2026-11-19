import csv
import os
import time
from urllib.parse import quote, unquote

import requests

API = "https://commons.wikimedia.org/w/api.php"
# Commons chiede un User-Agent descrittivo: inserisci il tuo contatto
HEADERS = {"User-Agent": "corso-bauer/0.1 (contatto: tua@email.it)"}


def valore(info, chiave):
    """Restituisce il valore di un campo dei metadati, o stringa vuota se manca."""
    return info.get(chiave, {}).get("value", "")


def chiave_file(nome):
    """Forma uniforme del nome di un file, per collegare i due CSV."""
    return nome.removeprefix("File:").replace("_", " ")


def crediti(titoli, file_csv, collegamenti):
    """Scrive un CSV con titolo, link, autore, licenza, data e monumento di ogni file.

    collegamenti: dizionario da nome del file al Q-number del monumento su Wikidata.
    """
    with open(file_csv, "w", newline="", encoding="utf-8") as f:
        scrittore = csv.writer(f)
        scrittore.writerow([
            "file", "pagina", "autore", "licenza", "link_licenza",
            "credit", "data", "monumento_wikidata",
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
                monumenti = collegamenti.get(chiave_file(nome), [])
                scrittore.writerow([
                    nome,
                    link,
                    valore(info, "Artist"),
                    valore(info, "LicenseShortName"),
                    valore(info, "LicenseUrl"),
                    valore(info, "Credit"),
                    valore(info, "DateTimeOriginal") or valore(info, "DateTime"),
                    ";".join(monumenti),
                ])
            time.sleep(1)  # una pausa tra una richiesta e l'altra


def scarica(titoli, cartella, larghezza=800):
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
    # il CSV esportato dalla query su query.wikidata.org
    with open("risultati_wikidata.csv", encoding="utf-8") as f:
        righe = list(csv.DictReader(f))

    COLONNA = "immagine" if "immagine" in righe[0] else "immagine1"

    # per ogni file, i monumenti di Wikidata a cui è collegato (es. Q839012)
    collegamenti = {}
    for r in righe:
        if r[COLONNA]:
            # il valore è un link tipo .../Special:FilePath/Nome%20file.jpg
            nome = unquote(r[COLONNA].split("/Special:FilePath/")[1].split("?")[0])
            q = r["monumento"].rsplit("/", 1)[-1]
            lista = collegamenti.setdefault(chiave_file("File:" + nome), [])
            if q not in lista:
                lista.append(q)

    # un file può comparire più volte nella query: lo teniamo una sola volta
    titoli = sorted(set("File:" + k for k in collegamenti))
    print(len(titoli), "immagini trovate")

    crediti(titoli, "crediti.csv", collegamenti)
    print("crediti scritti in crediti.csv")
    scarica(titoli, "immagini", larghezza=800)
