# UtleieApp – Oblig5

Webapplikasjon for håndtering av kunder, utstyr og utleie.

## Krav

Følgende må være installert:

- Python 3.x
- MySQL
- pip

## Installering

1. Klon eller last ned prosjektet.

2. Opprett virtual environment:

```bash
python -m venv venv
```

3. Aktiver miljøet:

Windows:
```bash
venv\Scripts\activate
```

Mac/Linux:
```bash
source venv/bin/activate
```

4. Installer nødvendige pakker:

```bash
pip install -r requirements.txt
```

## Database

1. Opprett en database i MySQL med navn:

`utstyrsutleiedb`

2. Importer SQL-scriptet som følger prosjektet.

3. Opprett en `.env` fil i prosjektmappen med:

```env
DB_PASSWORD=din_mysql_passord
```

## Kjør applikasjonen

Start applikasjonen:

```bash
python app.py
```

Åpne i nettleser:

`http://127.0.0.1:8000`

## Innlogging

Bruk følgende testbruker:

- E-post: `hildep@utstyr.no`
- Passord: `Utstyr11`

Innlogging skjer med e-post og passord.

## Funksjonalitet

- Hjem-side som viser:
Antall aktive utleier (ikke innlevert)
Antall tilgjengelige utstyr
Siste utleier (f.eks. siste 5)

- Logge inn og ut, samt beskyttede sider
- Opprette ny og redigere kunder
- Registrere og vise utstyr
- Administrere utleie
- Se statistikk
