# Workflow: immagini e metadati di una categoria di Commons

Questo workflow scarica i file di una categoria di Wikimedia Commons, comprese le sottocategorie, e crea un CSV con i crediti di ogni file. Lo script si chiama `categoria.py` ed è in questa cartella. Per lanciarlo serve l'ambiente `bauer-2027` creato con Anaconda, come descritto nel README principale del repo.

## Passo 1: scegliere la categoria

Apri la categoria su Commons e copia il nome esatto, per esempio `Media provided by Touring Club Italiano in 2024`. Il nome va scritto senza il prefisso `Category:`.

## Passo 2: impostare lo script

Apri `categoria.py` e modifica solo le righe in alto, tra le impostazioni:

- `CATEGORIA`: il nome della categoria.
- `CARTELLA`: la cartella in cui scaricare le immagini.
- `CSV_CREDITI`: il nome del CSV dei crediti.
- `SCARICA_TUTTE`: `False` per scaricare solo una prova di 10 file (è il valore di partenza).
- `LARGHEZZA`: la larghezza in pixel delle immagini.

Nel campo `HEADERS` inserisci il tuo contatto al posto del segnaposto.

## Passo 3: lanciare lo script

Apri Anaconda Prompt (Windows) o il Terminale (Mac), attiva l'ambiente, vai nella cartella del workflow e lancia lo script:

```
conda activate bauer-2027
cd 2-commons
python categoria.py
```

Il primo messaggio dice quanti file ci sono in totale, comprese le sottocategorie. Con `SCARICA_TUTTE = False` vengono scaricati solo 10 file. Il CSV dei crediti viene scritto per tutti i file trovati, non solo per quelli scaricati.

## Passo 4: decidere quante immagini scaricare

Il numero di file trovato al Passo 3 è il riferimento per la scelta:

- `SCARICA_TUTTE = False`: scarica 10 file, utile per una prova.
- `SCARICA_TUTTE = True`: scarica tutti i file. Per la collezione del Touring 2024, con circa 912 file, il download richiede tempo e spazio, perché ogni file pesa diversi megabyte.
- Per una quantità intermedia, con `SCARICA_TUTTE = False` cambia nello script il numero 10 in `elenco[:10]` con il numero che ti serve, per esempio `elenco[:50]`.

## Note

- Il CSV dei crediti ha la colonna `file` con il nome sicuro dell'immagine, usata per il vlookup, e la colonna `file_originale` con il nome come è su Commons.
- Il nome sicuro contiene solo lettere, cifre, underscore e l'estensione in minuscolo: niente accenti, spazi o apostrofi. Se due file avrebbero lo stesso nome, il secondo riceve il suffisso `_2`.
- Lo script include anche le sottocategorie, quindi il numero di file può essere più alto di quello mostrato nella pagina della categoria principale.
- Il campo autore può contenere codice HTML: va ripulito a mano nel CSV.
- Il controllo più utile è confrontare il numero di righe del CSV con il numero di file trovati.
