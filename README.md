# bauer-2027
A repository of tools for the data visualization course at cfp Bauer about data visualization using content from wikidata and commons

## Workflow

- `1-wikidata/`: query Wikidata per i monumenti di Wiki Loves Monuments, crediti e download delle immagini (`wlm.py`).
- `2-commons/`: download e crediti di una categoria di Wikimedia Commons, con le sottocategorie (`categoria.py`).

Ogni cartella ha un file `.md` con i passi del workflow.

## Come far girare gli script con Anaconda

Anaconda installa Python e le librerie più comuni, tra cui `requests`, e include Spyder, un editor con un pulsante per eseguire il file.

1. Scarica Anaconda Distribution da [anaconda.com](https://www.anaconda.com). Su Mac scegli la versione per il tuo chip: Apple silicon per i Mac con chip M, Intel per gli altri. Il tipo di chip si legge in «Informazioni su questo Mac».
2. Installa con le impostazioni predefinite.
3. Apri Anaconda Navigator dal menu Start (Windows) o dalla cartella Applicazioni (Mac). Premi «Launch» sotto Spyder.
4. In Spyder apri lo script con File > Apri: `wlm.py` in `1-wikidata/`, oppure `categoria.py` in `2-commons/`.
5. Per il workflow 1, metti prima nella stessa cartella dello script il file `risultati_wikidata.csv`, esportato dalla query su query.wikidata.org. Spyder usa come cartella di lavoro quella del file aperto, quindi i file vengono letti e scritti lì.
6. Premi il pulsante verde Esegui, oppure il tasto F5. Il risultato compare nella console in basso.

Se compare l'errore «No module named requests», apri Anaconda Prompt (Windows) o il Terminale (Mac) e scrivi:

```
conda install requests
```

Poi riavvia Spyder e lancia di nuovo lo script.
