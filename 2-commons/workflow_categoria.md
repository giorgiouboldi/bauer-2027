# Workflow: immagini e metadati di una categoria di Commons

Questo workflow scarica i file di una categoria di Wikimedia Commons, comprese le sottocategorie, e crea un CSV con i crediti di ogni file. Lo script si chiama `categoria.py` ed è in questa cartella.

## Passo 1: scegliere la categoria

Apri la categoria su Commons e copia il nome esatto, per esempio `Media provided by Touring Club Italiano in 2024`. Il nome va scritto senza il prefisso `Category:`.

## Passo 2: impostare lo script

Apri `categoria.py` e modifica solo le righe in alto, tra le impostazioni:

- `CATEGORIA`: il nome della categoria.
- `CARTELLA`: la cartella in cui scaricare le immagini.
- `CSV_CREDITI`: il nome del CSV dei crediti.
- `SCARICA_TUTTE`: `False` per una prova con 10 file, `True` per scaricare tutto.
- `LARGHEZZA`: la larghezza in pixel delle immagini.

## Passo 3: installare requests

Una sola volta, dal terminale:

- Windows: `py -m pip install requests`
- Mac: `python3 -m pip install requests`

## Passo 4: prima prova

- Windows: `py categoria.py`
- Mac: `python3 categoria.py`

Imposta `SCARICA_TUTTE = False` per una prova con solo 10 file. Controlla che compaiano il CSV dei crediti e la cartella delle immagini.

## Passo 5: scaricare tutto

Imposta `SCARICA_TUTTE = True` e lancia di nuovo lo script. Per la collezione del Touring 2024, con circa 912 file, il download richiede tempo e spazio, perché ogni file pesa diversi megabyte.

## Note

- Lo script include anche le sottocategorie, quindi il numero di file può essere più alto di quello mostrato nella pagina della categoria principale.
- Il campo autore può contenere codice HTML: va ripulito a mano nel CSV.
- Il workflow non è ancora stato eseguito. Il controllo più utile è confrontare il numero di righe del CSV con il numero di file trovati.
