# Information hiding in tracce MP3

L'obiettivo di questo progetto è trovare ed implementare una o più tecniche in grado di poter nascondere informazioni all'interno di tracce MP3.

Questa operazione è resa difficile dal fatto che le informazioni all'interno di tracce MP3 sono segnali che hanno frequenze comprese tra i 20Hz ed i 25-26KHz (tutte frequenze udibili dall'orecchio umano).

La problematica principale è riuscire ad inserire queste informazioni senza che l'utente  che riproduce la traccia sia in grado di distinguerle da quella originale.

## Stato dell'arte

Ad oggi sono presenti due tecniche per nascondere informazioni all'interno di tracce MP3:

- Echo Hiding

- Amplitude Hiding

### Echo Hiding

Il processo di echo hiding funziona utilizzando un algoritmo matematico per "inserire" i dati nascosti nel file audio. L'algoritmo analizza l'audio e inserisce i dati in modo tale da non essere facilmente individuati dall'orecchio umano. Di seguito è riportato un esempio di pseudocodice del funzionamento dell'algoritmo:

// Pseudocodice dell'algoritmo per l'occultamento dell'eco

// Input: File audio e dati da nascondere

// Output: File audio con dati incorporati

1. Analizzare il file audio per determinare la frequenza e l'ampiezza delle onde sonore.
2. Calcolare l'ampiezza media del file audio
3. Calcolare l'intervallo di frequenza per nascondere l'eco
4. Generare una serie di frequenze all'interno dell'intervallo calcolato al punto 3.
5. Inserire i dati da nascondere nel file audio alle frequenze calcolate al punto 4.
6. Regolare l'ampiezza delle frequenze calcolate nel passaggio 4 in modo che corrisponda all'ampiezza media del file audio.
7. Emettere il file audio con i dati incorporati

### Amplitude Hiding

Nell'amplitude hiding, il messaggio viene incorporato manipolando l'ampiezza di alcuni campioni audio.

L'algoritmo per l'occultamento dell'ampiezza è il seguente:

1. Prendere l'ampiezza dei campioni audio
2. Scegliere un certo valore di soglia 
3. Se l'ampiezza del campione è superiore alla soglia, impostarla sull'ampiezza massima.
4. Se l'ampiezza del campione è inferiore alla soglia, impostarla sull'ampiezza minima.
5. Incorporare il messaggio nell'audio manipolando l'ampiezza dei campioni.
6. Emettere il file audio modificato

Pseudocodice:

// Input: audio file, message

FOR each sample in audio file
    IF sample amplitude > threshold
        Set sample amplitude to maximum
    ELSE
        Set sample amplitude to minimum
    END IF
END FOR

Embed message into audio by manipulating amplitude of samples

Output modified audio file
