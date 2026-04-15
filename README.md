# UtleieApp – Oblig5

Webapplikasjon for håndtering av kunder, utstyr og utleie.

## Krav

Følgende må være installert:

- Python 3.x
- MySQL
- pip
- støtte for virtual environment (`venv`)

## Installering

1. Klon eller last ned prosjektet.

2. Gå inn i prosjektmappen "Oblig 5":

```bash
cd "Oblig 5"
```

3. Opprett virtual environment:
```bash
python -m venv venv
```

4. Aktiver miljøet (fra samme mappe):

Windows:
```bash
venv\Scripts\activate
```

Mac/Linux:
```bash
source venv/bin/activate
```

5. Installer nødvendige Python-pakker:

```bash
pip install -r requirements.txt
```


## Database

Applikasjonen bruker en lokal MySQL-database.

### Oppsett

1. Opprett en database i MySQL med navn:

`utstyrsutleiedb`

2. Importer SQL-scriptet `Utstyrutleie_webbapp.sql` i databasen.


### Miljøvariabler

Opprett en `.env` fil i prosjektmappen (`Oblig 5`) og sett ditt eget MySQL-passord:

```env
DB_PASSWORD=din_egen_mysql_passord
```

### Tilkobling

Applikasjonen kobler til databasen med følgende innstillinger:

- Host: `localhost`
- Bruker: `root`
- Database: `utstyrsutleiedb`
- Passord: hentes fra `.env` (variabel: `DB_PASSWORD`)

## Kjør applikasjonen

Sørg for at du er i prosjektmappen (`Oblig 5`), og kjør:

```bash
python app.py
```

Åpne i nettleser:

`http://127.0.0.1:8000`



## Prosjektstruktur

```text
.
├── app.py
├── database.py
├── models.py
├── requirements.txt
├── .env (ikke inkludert i repository)
├── Utstyrutleie_webbapp.sql
├── routes
│   ├── kunder_bp.py
│   ├── statistikk_bp.py
│   ├── utleie_bp.py
│   ├── utstyr_bp.py
│   └── user_manager.py
└── templates
    ├── base.html
    ├── index.html
    ├── Kunder
    │   ├── read.html
    │   ├── create.html
    │   └── add_edit.html
    ├── Statistikk
    │   └── read.html
    ├── Users
    │   ├── login.html
    │   ├── register.html
    │   └── profile.html
    ├── Utleie
    │   ├── read.html
    │   ├── create.html
    │   └── add_edit.html
    └── Utstyr
        └── read.html
```

## Innlogging

Bruk følgende testbruker:

- E-post: `hildep@utstyr.no`
- Passord: `Utstyr11`

Innlogging skjer med e-post og passord.

## Funksjonalitet

Applikasjonen består av følgende hovedmoduler:

### Hjem-side (Dashboard)
- Oversikt over aktive utleier (ikke innlevert)
- Antall tilgjengelig utstyr
- Siste 5 utleier

### Kunder
- Vise kundeliste
- Legge til og redigere kunder

### Utstyr
- Vise alt utstyr
- Filtrere på type og kategori
- Vise status basert på utleid d.v.s Tilgjengelig / Utleid

### Utleie
- Registrere ny utleie (valg av kunde, tilgjengelig utstyr, dato, om det skal leveres til kunde og leveringskostnad)
- Pålogget ansatt automatisk valgt som kundebehandler
- Registrere innlevering dato

### Statistikk
Basert på tidligere SQL-spørringer:

- Kundeliste
- Aktive utleier (filtrert på innlogget ansatt)
- Antall komplette utleier i perioden 2019-01-01 til 2020-02-10
- Inntekt per utstyr (sortert synkende)
- Mest utleid utstyr (toppresultat markert)