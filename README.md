# Toponiemresolutie op Grafstenen via de Coördinaten in jpg-metadata

Alle bestanden zijn aanwezig om zowel evaluation.py als toponiemresolutie.py te runnen

## Instructies

Uncomment de regel van de methode (baseline 1, baseline 2, eindresultaat) die je wilt printen als output in toponiemresolutie.py

```python3 toponiemresolutie.py > results.txt```


Als je daarna evaluation.py wilt gebruiken:

```cat results.txt | grep -w "geo" > results_codes.txt```


Dan kan evaluation.py gerund worden die de precision, recall en f-score geeft

