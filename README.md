##Astro Server

Per comunicare via socket con processing

##Requirements

```bash
pip install telepot
```

##RUN

Definire `TOKEN`, `host`, `port` nella funzione main.

Testato con Python 2.7 su un mac

```bash
python astro_server.py
```

##Utilizzo

Una volta lanciato il programma e il server processing, il bot risponderà ai comandi

- `/register`: registra l'utente e gli invierà i dati mandati da processing
- `/unregister`
