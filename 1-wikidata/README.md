# Workflow: monumenti WLM con immagini e crediti

Questo workflow parte dalla query su Wikidata, raccoglie i crediti delle immagini su Wikimedia Commons e scarica le immagini. Lo script si chiama `wlm.py` ed è in questa cartella. Per lanciarlo serve l'ambiente `bauer-2027` creato con Anaconda, come descritto nel README principale del repo.

## Passo 1: eseguire la query su Wikidata

Apri query.wikidata.org, incolla la query qui sotto ed eseguila. La query raggruppa i risultati per monumento, così ogni monumento compare una sola volta. Poi scarica il risultato in CSV con il nome `risultati_wikidata.csv`.

```sparql
SELECT ?monumento ?monumentoLabel
  (SAMPLE(?indirizzo) AS ?indirizzo1)
  (SAMPLE(?lat) AS ?lat1)
  (SAMPLE(?lon) AS ?lon1)
  (SAMPLE(?immagine) AS ?immagine1)
  (GROUP_CONCAT(DISTINCT ?architettoNome; separator=" ; ") AS ?architetti)
  (MIN(?anno) AS ?annoPrimo)
WHERE {
  ?monumento wdt:P131 wd:Q490 ;
             wdt:P2186 ?idWLM .
  OPTIONAL { ?monumento wdt:P6375 ?indirizzo . }
  OPTIONAL {
    ?monumento wdt:P625 ?coord .
    BIND(geof:latitude(?coord) AS ?lat)
    BIND(geof:longitude(?coord) AS ?lon)
  }
  OPTIONAL { ?monumento wdt:P18 ?immagine . }
  OPTIONAL {
    ?monumento wdt:P84 ?architetto .
    OPTIONAL { ?architetto rdfs:label ?architettoIT . FILTER(LANG(?architettoIT) = "it") }
    OPTIONAL { ?architetto rdfs:label ?architettoEN . FILTER(LANG(?architettoEN) = "en") }
    BIND(COALESCE(?architettoIT, ?architettoEN, STR(?architetto)) AS ?architettoNome)
  }
  OPTIONAL { ?monumento wdt:P571 ?data . BIND(YEAR(?data) AS ?anno) }
  SERVICE wikibase:label { bd:serviceParam wikibase:language "it,en". }
}
GROUP BY ?monumento ?monumentoLabel
LIMIT 200
```

## Passo 2: preparare la cartella

Metti nella stessa cartella il file `risultati_wikidata.csv` e lo script `wlm.py`.

## Passo 3: lanciare lo script

Apri Anaconda Prompt (Windows) o il Terminale (Mac), attiva l'ambiente, vai nella cartella del workflow e lancia lo script:

```
conda activate bauer-2027
cd 1-wikidata
python wlm.py
```

Lo script produce tre risultati:

- `risultati_wikidata_pulito.csv`: la copia del CSV di Wikidata con due colonne comuni, `monumento` (il Q-number, per esempio `Q839012`) e `file` (il nome sicuro dell'immagine).
- `crediti.csv`: una riga per ogni coppia monumento-file, con le colonne `monumento` e `file`, più autore, licenza, link e data.
- la cartella `immagini`, con le immagini scaricate con nomi sicuri.

Le due colonne `monumento` e `file` servono per collegare i due CSV con un vlookup, usando come chiave la colonna `monumento` o la colonna `file`.

## Passo 4: verificare i risultati

Controlla che compaiano i tre risultati. Il numero di righe di `crediti.csv` deve essere almeno il numero di file scaricati, perché un file collegato a più monumenti compare su più righe.

## Note

- Il nome sicuro contiene solo lettere, cifre, underscore e l'estensione in minuscolo: niente accenti, spazi o apostrofi. Se due file avrebbero lo stesso nome, il secondo riceve il suffisso `_2`.
- Se un monumento non ha P18, la riga non ha immagine e viene saltata.
