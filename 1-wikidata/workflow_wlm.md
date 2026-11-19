# Workflow: monumenti WLM con immagini e crediti

Questo workflow parte dalla query su Wikidata, raccoglie i crediti delle immagini su Wikimedia Commons e scarica le immagini. Lo script si chiama `wlm.py` ed è in questa cartella.

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

La colonna `immagine1` contiene il link al file su Commons, e lo script la legge da lì.

## Passo 2: preparare la cartella

Metti nella stessa cartella il file `risultati_wikidata.csv` e lo script `wlm.py`.

## Passo 3: installare requests

Una sola volta, dal terminale:

- Windows: `py -m pip install requests`
- Mac: `python3 -m pip install requests`

## Passo 4: lanciare lo script

- Windows: `py wlm.py`
- Mac: `python3 wlm.py`

Lo script legge il CSV, elimina i duplicati, scrive `crediti.csv` e scarica le immagini nella cartella `immagini`. Il CSV dei crediti ha una colonna `monumento_wikidata` con il Q-number del monumento, così ogni riga rimanda al monumento da cui viene l'immagine.

## Passo 5: verificare i risultati

Controlla che compaiano `crediti.csv` e la cartella `immagini`. Il numero di righe del CSV deve corrispondere al numero di file scaricati.

## Note

- Il workflow non è ancora stato eseguito. Va provato prima della lezione.
- Se un monumento non ha P18, la riga non ha immagine e viene saltata.
