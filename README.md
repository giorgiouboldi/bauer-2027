# bauer-2027
A repository of tools for the data visualization course at cfp Bauer about data visualization using content from wikidata and commons

## Workflow

### `1-wikidata/`: monumenti di Wiki Loves Monuments

Parte da una query su Wikidata che elenca i monumenti di Milano con un identificativo Wiki Loves Monuments. Lo script `wlm.py`:

- legge il CSV esportato dalla query e trova l'immagine di ogni monumento;
- scrive `risultati_wikidata_pulito.csv`, con il Q-number del monumento e il nome sicuro del file;
- scrive `crediti.csv`, con autore, licenza, link e data di ogni immagine;
- scarica le immagini nella cartella `immagini`, con nomi senza accenti né spazi.

Il collegamento tra i due CSV è nelle colonne `monumento` e `file`.

### `2-commons/`: file di una categoria di Commons

Scarica i file di una categoria di Wikimedia Commons, comprese le sottocategorie. Lo script `categoria.py`:

- raccoglie tutti i file della categoria e delle sottocategorie;
- scrive `crediti.csv`, con il nome sicuro del file, il nome originale, autore, licenza, link e data;
- scarica le immagini nella cartella `immagini`, con nomi sicuri.

Ogni cartella contiene un README con i passi del workflow.

## Come far girare gli script con Anaconda

Anaconda installa Python e Spyder. Con Anaconda Navigator crei un ambiente dedicato al corso e lanci gli script. Lo fai una sola volta.

1. Scarica Anaconda Distribution dal sito [anaconda.com](https://www.anaconda.com). Su Mac scegli la versione per il tuo chip: Apple silicon per i Mac con chip M, Intel per gli altri. Il tipo di chip si legge in «Informazioni su questo Mac».
2. Installa con le impostazioni predefinite.
3. Apri Anaconda Navigator e vai nella sezione **Environments**. Premi **Create**, scrivi `bauer-2027` come nome e scegli una versione di Python, per esempio 3.11. Premi **Create** e aspetta che l'ambiente sia pronto.
4. Sempre in **Environments**, seleziona `bauer-2027`. Nel menu sopra la lista dei pacchetti scegli **Not installed**, cerca `requests`, selezionalo e premi **Apply**.
5. Con `bauer-2027` selezionato, premi **Launch** sotto Spyder.
6. In Spyder apri lo script con File > Apri: `wlm.py` in `1-wikidata/`, oppure `categoria.py` in `2-commons/`. Premi il pulsante verde Esegui, oppure il tasto F5. Il risultato compare nella console in basso.

Spyder usa come cartella di lavoro quella del file aperto, quindi il CSV `risultati_wikidata.csv` del workflow 1 va messo nella stessa cartella dello script.
