# ProgettoCompressioneDati
## Struttura del progetto
- [ProgettoCompressioneDati](https://github.com/h3rm4nn-99/ProgettoCompressioneDati)
    - [Codice](https://github.com/h3rm4nn-99/ProgettoCompressioneDati/tree/main/code)
    - [Documentazione](https://github.com/h3rm4nn-99/ProgettoCompressioneDati/tree/main/docs)
## Dipendenze
#### Per installare le dipendenze, eseguire il seguente comando:
```
pip install -r requirements.txt
```

## Scaletta presentazione iniziale:
- Introduzione teorica: 
    - Teorema del Campionamento di Shannon;
    - FFT (*Fast Fourier Transform*)
- *Psicoacustica*
- Compressione MP3
- Steganografia
- Tool di steganografia audio (stato dell'arte)
- Implementazione progetto precedente
- Migliorie da apportare (eventuale)

## Basics

### Segnale audio
L'*audio* è un segnale analogico continuo che assume un'infinità di valori (in un intervallo) nel tempo. Per essere memorizzato su un supporto deve essere trasformato in digitale mediante un processo di *campionamento*, che può avvenire ad una determinata frequenza, detta *frequenza di campionamento*. Mediante il campionamento, si produce un segnale che assume valori *discreti* al costo di un determinato *rumore* di campionamento, effetto collaterale del processo. Un segnale audi reso digitale ma non compresso viene memorizzato e trasmesso mediante la modulazione **PCM** (pulse code modulation). Per valutare la qualità di una traccia audio modulata tramite PCM è necessario andare a considerare il sample rate (la frequenza di campionamento) ed il bitrate (quantità di dati necessaria per codificare ogni secondo di riproduzione)

### Steganografia
Le curve analogiche vengono sfruttate come segnale cover per nascondere un messaggio segreto, mediante tecniche di *steganografia*. Due tecniche di steganografia sono:
- Crittografia, per rendere segreti messaggi usando algoritmi a chiave privata o pubblica
- Watermarking, in cui si vanno ad inserire delle informazioni all'interno di un segnale. Il watermarking può essere realizzato mediante:
    - Echo data hiding, ovvero andando ad inserire i dati sotto forma di eco all'interno del file audio
    - Amplitude data hiding, modificando l'ampiezza del segnale audio.

Nel caso particolare dei file audio si possono utilizzare differeti tecniche di steganografia:

- Codifica dei bit bassi: in ogni campione del segnale (prodotto dal campionamento) si sostituiscono i bit meno significativi con delle informazioni che di base non c'entrano nulla con il segnale (ovvero ciò che vogliamo nascondere);
- Codifica delle fasi: si sostituisce la fase del segmento iniziale di un file audio con una fase che rappresenta i dati (mi fido di quello che hanno scritto);
- Spread spectrum: diffonde i dati all'interno dello spettro delle frequenze. Per decodificarli, è necessario conoscere la permutazione pseudocasuale che rappresenta l'ordine delle frequenze con cui vengono distribuiti i dati. Questo metodo viene usato come misura di sicurezza anche in altri ambiti;
- Echo hiding: viene aggiunto uun segnale ospite che introduce un'eco all'interno del segnale audio. Devono essere stabiliti tre parametri per la realizzazione dell'echo hiding:
    - Ampiezza iniziale del segnale;
    - Tasso di indebolimento del suono;
    - Ritardo
Introducendo due diversi ritardi è possibile codificare le cifre binarie 0 ed 1. Se è necessario codfificare più di un bit, il segnale viene diviso in parti, a cui veraanno introdotte diverse eco


## Compressione audio

### Psicoacustica

La psicoacustica è la scienza che si occupa di stabilire il rapporto che intercorre tra l'orecchio (che si occupa di percepire uno stimolo acustico) ed il cervello umano (che elabora questo stimolo). 

### Il corpo umano
È stato dimostrato che il cervello umano riesce ad elaborare frequenze audio che vanno dai 20 Hz ai 20 kHz, con una sensibilità che diventa massima tra i 2 kHz ai 4 kHz. Man mano che si esce da questa "regione", diventa più difficile perceprire suoni. Il corpo umano quindi funge da "filtro", che taglia tutte le frequenze non elaborabili dal corpo umano

### Taglio delle frequenze
I codec audio (come MP3) fanno la stessa cosa, in modo tale da diminuire lo spazio necessario per la memorizzazione e la trasmissione di tracce audio.

### *Critical bands* e *masking*
L'orecchio umano lavora con bande di 24 frequenze. Esistono delle *bande critiche* che sono suscettibili ad un particolare fenomeno detto *masking*, in cui l'eventuale presenza di un segnale di disturbo va a "mascherare" le frequenze presenti nelle bande critiche

### Simultaneous masking e temporal masking
Il mascheramento di tipo simultaneo (o frequency masking) avviene nel dominio delle frequenze. Il mascheramento di tipo temporale avviene (come suggerisce la definizione) nel dominio del tempo. Nel primo caso, il segnale "masker" si presenta allo stesso momento del segnale "maskee". Esiste quindi una soglia (threshold) di mascheramento tale che tutte le frequenze che la superano sono "tagliate fuori". Nel secondo caso, invece, la presenza di un segnale masker ad un certo punto del tempo rende inudibile il segnale maskee.

(Ho fatto del mio meglio su questa parte ma dalla tesina non è molto chiaro e su internet non si trova molto).

### MP3
La codifica *MP3* (MPEG-{1,2} Audio Layer III) è un formato di compressione di tipo *lossy*, ovvero che prevede una perdita (accettabile) di informazioni. Si basa sull' "incapacità" dell'orecchio umano di percepire determinate frequenze audio, che vengono "tagliate", ottenendo un buon rapporto di compressione, che può arrivare a circa 12:1.

### Come ottenere la compressione di un fattore 12?

Dato che l'essere umano non riesce a percepire tutte le frequenze presenti in natura, si provvede a tagliarle. Si sfrutta il concetto di banda critica, che ogni essere umano possiede, che viene approssimata tramite una *scalefactor band*. 

Successivamente, viene calcolata una soglia di mascheramento (oltre la quale l'essere umano non può percepire) e le bande vengono scalate usando un fattore adeguato, per ridurre il rumore di quantizzazione. 

Viene, infine, utilizzata la codifica di Huffman per aumentare ulteriormente il compression rate.

MP3 dunque ha un ottimo fattore di compressione ed una qualità comunque buona.

### MP3: caratteristiche

MP3 supporta due tipi di bitrate:
- Costante: necessario per lo streaming dei contenuti
- Variabile: il bitrate varia e si adatta al contesto. Porta problemi di timing della traccia

Lo standard MPEG1, di cui MP3 fa parte, prevede frequenze di campionamento di 32 kHz, 44.1 kHz e 48 kHz.

MP3 funziona in quattro diversi *channel modes* (che differiscono appunto dall'organizzazione dei canali audio):
- Single Channel
- Dual Channel (Single Channel + Single Channel)
- Stereo
- Joint Stereo

La modalità operativa più interessante è quella Joint Stereo, che viene usata per ottimizzare la codifica sfruttando la ridondanza tra i canali left e right della traccia audio.

È possibile approcciarsi a questa modalità in due modi:
- Middle/Side Stereo (o MS Stereo), in cui i canali vengono sommati e sottratti e la somma e la differenza vengono trasmessi, sfruttando il fatto che tipicamente i due canali sono uguali per la maggior parte dei casi e la loro somma porta più informazione. Questa è una codifica lossless

- Intensity Stereo Mode, che utilizza una tecnica detta "Joint Frequency Encoding", basata sul principio di localizzazione sonora. L'udito umano è, in maniera preponderante, meno capace di localizzare la provenienza di determinate frequenze, rispetto ad altri animali. Nello specifico, per la localizzazione delle frequenze, gli umani si affidano alle differenze di tempo e di ampiezza inter-aurali. La capacità di distinguere le differenze di tempo inter-aurali è presente solo per le basse frequenze, di conseguenza l'unico modo per localizzare le frequenze alte è sfruttare la sola ampiezza. Sfruttando questa caratteristica è possibile ridurre le dimensioni di un file audio o di uno stream, senza cambiamenti sostanziali nella qualità percepita. Tuttavia, questa tecnica prevede di unire la parte inferiore dello spettro sonoro in un canale unico (riducendo le differenze tra i vari canali) e trasmettere dell'informazione aggiuntiva per consentire a certe regioni dello spettro di ripristinare la differenza di ampiezza inter-aurale (e quindi ottenere di nuovo una localizzazione abbastanza accurata). Tutto ciò può portare a piccolissime distorsioni nell'audio risultante, ma per bitrate bassi si può addirittura ottenere un miglioramento nella qualità percepita. Proprio per via di questo miglioramento, Intensity stereo mode è supportato da diversi codec, tra cui MP3, Opus, Vorbis e AAC.

## MP3
### Anatomia di un file
Un file mp3 è suddiviso in frame di 1152 samples ciascuno. Ogni frame ha una durata di 26 ms, quindi circa 38 fps. I frame sono suddivisi in granules da 576 samples ciascuno.

A seconda del bitrate e della frequenza di campionamento, avremo samples più o meno grandi. Nello specifico, la taglia è data da ((144 * bitrate) / (freq. campionamento)) + padding.
Il padding corrisponde ad 1 byte per frame, inserito per mantenere costante il bitrate. Se questo byte viene inserito, avremo un bit speciale nell'header settato ad 1.

### Layout di un frame
Un frame è suddiviso in.
- Header;
- CRC;
- Informazione aggiuntiva;
- Dati principali;
- Dati accessori.

### Header
L'header mp3 è lungo 32 bit ed è così strutturato:
- Informazioni di sincronizzazione (12 bit), utilizzate per poter riprodurre il contenuto senza partire dall'inizio o per sincronizzare l'audio con il flusso video di uno stream;
- ID (1 bit), identifica la versione di MPEG usata, 1 per MPEG-1, 0 per MPEG-2. Alcune versioni utilizzano 1 bit in meno per la sincronizzazione, in modo da poter distinguere ulteriori versioni di MPEG;
- Layer (2 bit), indica il layer utilizzato;
- Bit di protezione (1 bit), se impostato a 0, il frame è protetto da un CRC di 16 bit;
- Bitrate (4 bit), indica con quanti bit è codificato il frame;
- Frequenza (2 bit), indica la frequenza di campionamento;
- Bit di padding (1 bit), indica se è presente o meno 1 byte di padding;
- Private bit (1 bit), se settato a 1 si utilizza CRC;
- Modalità  del canale(2 bit), indica la modalità utilizzata;
- Estensione modalità (solo joint stereo) (2 bit), indicano se Intensity stereo e MS stereo sono attivi o meno;
- Copyright (1 bit), indica se è possibile copiare il contenuto;
- Original o Home (1 bit), indica se il frame è nel media originale;
- Enfasi (2 bit), indica al decodificatore se è necessario de-enfatizzare (re-equalizzare) il suono;

### Informazioni aggiuntive
Questa parte del frame contiene informazioni circa la decodifica dei dati principali. La taglia dipende dalla modalità del canale.

Sono suddivise come segue: 
- main_data-begin (9 bit), indica dove cominciano i main data da decodificare. Ciò è necessario, poichè se si utilizza il layer 3, si possono utilizzare eventuali bit liberi per contenere i main data dei frame successivi. Il valore massimo è 4088 bit, utilizzato come offset negativo per ritrovare l'inizio dei main data nei frame precedenti.
- SCaleFactor Selection Information (scfsi)(4-8 bit), indica se gli scale factors sono utilizzati per tutti i granule di un certo gruppo.
- side_info_gr0 e side_info_gr1, campi identici utilizzati per le informazioni dei due granule.

(direi che questo livello di dettaglio va bene per i nostri appunti)

### Main data

[WIP]


