import csv
import os
import re
import time
import unicodedata
from urllib.parse import quote, unquote

import requests

API = "https://commons.wikimedia.org/w/api.php"
# Commons chiede un User-Agent descrittivo: inserisci il tuo contatto
HEADERS = {"User-Agent": "corso-bauer/0.1 (contatto: tua@email.it)"}


def valore(info, chiave):
    """Restituisce il valore di un campo dei metadati, o stringa vuota se manca."""
    return info.get(chiave, {}).get("value", "")


def chiave_file(nome):
    """Forma uniforme del nome di un file, per collegare i dati di Wikidata e di Commons."""
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


def crediti(titoli, file_csv, collegamenti, sicuri):
    """Scrive un CSV con una riga per ogni coppia monumento-file, con autore, licenza e data."""
    with open(file_csv, "w", newline="", encoding="utf-8") as f:
        scrittore = csv.writer(f)
        scrittore.writerow([
            "monumento", "file", "file_originale", "pagina", "autore",
            "licenza", "link_licenza", "credit", "data",
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
                chiave = chiave_file(nome)
                link = "https://commons.wikimedia.org/wiki/" + quote(nome.replace(" ", "_"))
                for monumento in collegamenti.get(chiave, []):
                    scrittore.writerow([
                        monumento,
                        sicuri[chiave],
                        nome.removeprefix("File:"),
                        link,
                        valore(info, "Artist"),
                        valore(info, "LicenseShortName"),
                        valore(info, "LicenseUrl"),
                        valore(info, "Credit"),
                        valore(info, "DateTimeOriginal") or valore(info, "DateTime"),
                    ])
            time.sleep(1)  # una pausa tra una richiesta e l'altra


def scarica(elenco, cartella, larghezza=800):
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
    # il CSV esportato dalla query su query.wikidata.org
    with open("risultati_wikidata.csv", encoding="utf-8") as f:
        lettore = csv.DictReader(f)
        righe = list(lettore)
        campi = lettore.fieldnames

    COLONNA = "immagine" if "immagine" in campi else "immagine1"

    # per ogni file originale, i monumenti di Wikidata a cui è collegato
    collegamenti, originali = {}, {}
    for r in righe:
        if r[COLONNA]:
            # il valore è un link tipo .../Special:FilePath/Nome%20file.jpg
            nome = unquote(r[COLONNA].split("/Special:FilePath/")[1].split("?")[0])
            chiave = chiave_file("File:" + nome)
            originali.setdefault(chiave, nome)
            q = r["monumento"].rsplit("/", 1)[-1]
            lista = collegamenti.setdefault(chiave, [])
            if q not in lista:
                lista.append(q)

    sicuri = assegna_nomi(originali)
    print(len(originali), "immagini trovate")

    # copia del CSV di Wikidata con le due colonne comuni: monumento e file
    with open("risultati_wikidata_pulito.csv", "w", newline="", encoding="utf-8") as f:
        scrittore = csv.DictWriter(f, fieldnames=campi + ["file"])
        scrittore.writeheader()
        for r in righe:
            file_sicuro = ""
            if r[COLONNA]:
                nome = unquote(r[COLONNA].split("/Special:FilePath/")[1].split("?")[0])
                file_sicuro = sicuri[chiave_file("File:" + nome)]
            r["monumento"] = r["monumento"].rsplit("/", 1)[-1]
            r["file"] = file_sicuro
            scrittore.writerow(r)
    print("risultati scritti in risultati_wikidata_pulito.csv")

    titoli = ["File:" + originali[k] for k in sorted(originali)]
    crediti(titoli, "crediti.csv", collegamenti, sicuri)
    print("crediti scritti in crediti.csv")

    elenco = [(originali[k], sicuri[k]) for k in sorted(originali)]
    scarica(elenco, "immagini", larghezza=800)
