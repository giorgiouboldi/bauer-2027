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

Con Anaconda Navigator crei un ambiente dedicato al corso, e con il terminale di Anaconda lanci gli script. Lo ambiente si crea una sola volta.

1. Scarica Anaconda Distribution dal sito [anaconda.com](https://www.anaconda.com). Su Mac scegli la versione per il tuo chip: Apple silicon per i Mac con chip M, Intel per gli altri. Il tipo di chip si legge in «Informazioni su questo Mac».
2. Installa con le impostazioni predefinite.
3. Apri Anaconda Navigator e vai nella sezione **Environments**. Premi **Create**, scrivi `bauer-2027` come nome e scegli una versione di Python, per esempio 3.11. Premi **Create** e aspetta che l'ambiente sia pronto.
4. Sempre in **Environments**, seleziona `bauer-2027`. Nel menu sopra la lista dei pacchetti scegli **Not installed**, cerca `requests`, selezionalo e premi **Apply**.

Per lanciare uno script:

1. Apri Anaconda Prompt (Windows) o il Terminale (Mac).
2. Attiva l'ambiente con `conda activate bauer-2027`.
3. Vai nella cartella del workflow con `cd`, per esempio `cd 1-wikidata`.
4. Lancia lo script con `python wlm.py`, oppure `python categoria.py` nella cartella `2-commons`.

Lo script legge e scrive i file nella cartella da cui lo lanci, quindi il CSV `risultati_wikidata.csv` del workflow 1 va messo lì.
