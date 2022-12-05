# Data Echo Hiding - Statement of Work

## Introduzione
L'obiettivo di questo progetto consiste nell'analizzare ed implementare una tecnica di **steganografia audio**, che permette quindi di nascondere informazioni all'interno di tracce audio.

La problematica principale risulta essere  l'effettivo inserimento di informazioni senza che l'utente che riproduce la traccia modificata sia in grado di distinguerla da quella originale.

## Stato dell'arte
Negli anni, diversi sono stati gli studi che hanno messo a punto tecniche di steganografia audio. In particolare, menzioniamo:

- Echo Hiding (H. B. Dieu, **An Improvement for Hiding Data in Audio Using Echo Modulation**, ICIES 2013)
- Amplitude Hiding (Wen-Nung Lie; Li-Chun Chang, **Robust and High-Quality Time-Domain Audio Watermarking Based on Low-Frequency Amplitude Modification**, IEEE Transactions on Multimedia 2006)

Allo scopo di questo progetto, si è deciso di implementare e migliorare la tecnica di *Echo Hiding*.

## Echo Hiding: una breve panoramica

La tecnica proposta da Dieu prevede l'embedding di messaggi binari all'interno di tracce audio andando ad aggiungere una certa quantità di eco alla traccia stessa.

### La codifica
Il codificatore riceve in input la traccia originale, il messaggio da nascondere ed una coppia di interi (la *chiave*). Attraverso la chiave viene generata una sequenza binaria ausiliaria. Sulla base di questa sequenza, sfruttando alcune regole precise viene effettuato l'embedding.

### La decodifica
Il decodificatore riceve in input la traccia originale, la lunghezza del messaggio, la traccia modificata e **la stessa chiave** utilizzata per la codifica, per generare la stessa sequenza ausiliaria. Il decodificatore confronta le due tracce audio e se nota differenze allora sulla base della sequenza binaria ausiliaria estrae i bit del messaggio.

## Il punto di partenza
La tecnica di Data Echo Hiding è stata presa in considerazione dagli studenti Alessandra Zullo, Gabriele Lombardi e Marco Villani il cui progetto, **Data Audio Hiding**, risulta essere la base del lavoro che andremo a svolgere. 

## Lavoro proposto
Gli autori del lavoro originale hanno concentrato i loro sforzi sull'implementazione della tecnica di Amplitude Hiding, fornendo per l'**Echo Hiding** solamente un'implementazione **incompleta** e **non funzionante**.

Lo scopo del nostro lavoro consiste principalmente nella re-implementazione della tecnica di **Echo Hiding** così come appare nello studio originale di H. B. Dieu, con le seguenti integrazioni:

1. Cifratura preliminare del messaggio da nascondere per migliorare ulteriormente la sicurezza dello schema;
2. Studio del comportamento dello schema in termini di disturbi percepibili dall'orecchio umano nel caso di embedding di messaggi più lunghi.

Lo schema da noi proposto consiste in due moduli:

- Modulo **codificatore**: effettua l'embedding del messaggio binario mediante aggiunta di eco alla traccia audio;
- Modulo **decodificatore**: effettua l'estrazione del messaggio dalla traccia audio andando a considerare le differenze che intercorrono tra la traccia audio originale e quella modificata.

Si prevede di utilizzare il linguaggio di programamzione **Python** e la libreria *pydub* che permette di manipolare file audio in maniera immediata.