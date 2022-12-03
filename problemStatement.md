# Data hiding in tracce audio

L'obiettivo di questo progetto è analizzare ed implementare una tecnica in grado di poter nascondere informazioni all'interno di tracce audio.

La problematica principale è riuscire ad inserire queste informazioni senza che l'utente che riproduce la traccia sia in grado di distinguerle da quella originale.

## Stato dell'arte

Ad oggi sono state proposte due tecniche per nascondere informazioni all'interno di tracce audio:

- Echo Hiding

- Amplitude Hiding

Allo scopo di questo progetto, si è deciso di implementare la prima tecnica

### Echo Hiding

Il processo di echo hiding funziona utilizzando un algoritmo matematico per "inserire" i dati nascosti nel file audio. \
L'algoritmo analizza l'audio e inserisce i dati in modo tale da non essere facilmente individuati dall'orecchio umano andando ad inserire un echo nella traccia. 

### Lavoro proposto

Questa tecnica è stata presa in considerazione dagli studenti "Zullo Alessandra, Lombardi Gabriele, Villani Marco" che ne hanno fornito un'implementazione parziale non funzionante. \
Lo scopo di questo lavoro consiste principalmente in 3 punti:

1. Implementazione concreta e funzionante dell'Echo Hiding
2. Aggiunta di un ulteriore layer di sicurezza tramite crittografia del messaggio (AES)
3. Embedding dei dati su tutta la traccia e non solo nella parte iniziale
