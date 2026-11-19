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

Anaconda installa Python e Spyder. Prima di lanciare gli script crea un ambiente dedicato al corso, con dentro Python e la libreria `requests`. Lo fai una sola volta.

1. Scarica Anaconda Distribution dal sito [anaconda.com](https://www.anaconda.com). Su Mac scegli la versione per il tuo chip: Apple silicon per i Mac con chip M, Intel per gli altri. Il tipo di chip si legge in «Informazioni su questo Mac».
2. Installa con le impostazioni predefinite.
3. Apri Anaconda Prompt (Windows) o il Terminale (Mac) e crea l'ambiente:

```
conda create -n bauer-2027 python requests -y
```

4. Attiva l'ambiente:

```
conda activate bauer-2027
```

5. Vai nella cartella dello script con `cd`, per esempio `cd 1-wikidata`, e lancialo:

```
python wlm.py
```

oppure `python categoria.py` nella cartella `2-commons`.

Se preferisci Spyder, apri Anaconda Navigator, scegli l'ambiente `bauer-2027` nella colonna «Environments», premi «Launch» sotto Spyder, apri il file con File > Apri e premi il pulsante verde Esegui, oppure il tasto F5.

In entrambi i casi, lo script legge e scrive i file nella cartella in cui si trova, quindi il CSV `risultati_wikidata.csv` del workflow 1 va messo lì.
