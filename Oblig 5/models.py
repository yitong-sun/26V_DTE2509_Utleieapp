from flask_login import UserMixin
from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, DateField
from wtforms.validators import DataRequired 

# Tabeller i databasen:

class User(UserMixin):
    def __init__(self, id, fornavn, etternavn, email, role):
        self.id = id
        self.fornavn = fornavn
        self.etternavn = etternavn
        self.email = email
        self.role = role

class Kunde():
    def __init__(
        self,
        kundenr,
        epost,
        fakt_adresse_id,
        levering_adresse_id,
        telefoner=None,
        navn="",
        fakt_adresse="",
        levering_adresse=""
    ):
        self.kundenr = kundenr
        self.epost = epost
        self.fakt_adresse_id = fakt_adresse_id
        self.levering_adresse_id = levering_adresse_id
        self.telefoner = telefoner if telefoner is not None else []

        self.navn = navn
        self.mobil = ", ".join(self.telefoner) if self.telefoner else ""
        self.fakt_adresse = fakt_adresse
        self.levering_adresse = levering_adresse

class Utstyr():
    def __init__(self, utstyr_id, utstyrs_type, utstyrs_merke, utstyrs_modell, beskrivelse, utstyrs_kategori, leie_pris_døgn, antall_utstyr, antall_på_lager):
        self.utstyr_id = utstyr_id
        self.utstyrs_type = utstyrs_type
        self.utstyrs_merke = utstyrs_merke
        self.utstyrs_modell = utstyrs_modell
        self.beskrivelse = beskrivelse
        self.utstyrs_kategori= utstyrs_kategori
        self.leie_pris_døgn = "Utiljengelig" if leie_pris_døgn == None else leie_pris_døgn
        self.antall_utstyr= antall_utstyr
        self.antall_på_lager= antall_på_lager

class Utleie():
    def __init__(self, utleie_id, utstyrs_id, instans_id , kunde_nr, utleid_dato, innlevert_dato, kundebehandler, leveres_kunde, betalingsmåte, leverings_kostnad, total_pris ):
        self.utleie_id = utleie_id
        self.utstyrs_id = utstyrs_id
        self.instans_id = instans_id 
        self.kunde_nr = kunde_nr
        self.utleid_dato = utleid_dato
        self.innlevert_dato = innlevert_dato if innlevert_dato else "Ikke levert"
        self.kundebehandler = kundebehandler
        self.leveres_kunde = leveres_kunde
        self.betalingsmåte = betalingsmåte
        self.leverings_kostnad = leverings_kostnad if leverings_kostnad else "0.00"
        self.total_pris = total_pris if total_pris else "Uberegnet"

class Adresse():
    def __init__(self, adresse_id, adresse_type_id, post_nr, adr_gate, adr_gate_nr):
        self.adresse_id = adresse_id
        self.adresse_type_id = adresse_type_id
        self.post_nr = post_nr
        self.adr_gate = adr_gate
        self.adr_gate_nr = adr_gate_nr

class AdresseType():
    def __init__(self, adresse_type_id, beskrivelse):
        self.adresse_type_id = adresse_type_id
        self.beskrivelse = beskrivelse


class BedrifKunde():
    def __init__(self, kunde_nr, kunde_navn):
        self.kunde_nr = kunde_nr
        self.kunde_navn = kunde_navn


class Betalingsmåte():
    def __init__(self, betalingsmåte_id, beskrivelse):
        self.betalingsmåte_id = betalingsmåte_id
        self.beskrivelse = beskrivelse

class Instans():
    def __init__(self, instans_id, utstyr_id, siste_vedlikehold, neste_vedlikehold):
        self.instans_id = instans_id
        self.utstyr_id = utstyr_id
        self.siste_vedlikehold = siste_vedlikehold
        self.neste_vedlikehold = neste_vedlikehold

class Kundebehandler():
    def __init__(self, kundebehandler_id, fornavn, etternavn, telefon_nr):
        self.kundebehandler_id = kundebehandler_id
        self.fornavn = fornavn
        self.etternavn = etternavn
        self.telefon_nr = telefon_nr

class KundeTelefon():
    def __init__(self, kunde_nr, telefon_nr):
        self.kunde_nr = kunde_nr
        self.telefon_nr = telefon_nr


class Poststed():
    def __init__(self, post_nr, post_sted):
        self.post_nr = post_nr
        self.post_sted = post_sted


class PrivatKunde():
    def __init__(self, kunde_nr, fornavn, etternavn):
        self.kunde_nr = kunde_nr
        self.fornavn = fornavn
        self.etternavn = etternavn


class UtstyrsKategori():
    def __init__(self, utstyrs_kat_id, beskrivelse):
        self.utstyrs_kat_id = utstyrs_kat_id
        self.beskrivelse = beskrivelse

#Forms

class FilterUtstyrForm(FlaskForm):
    utstyr_type = SelectField('Utstyr type:', choices=[], coerce=str)
    kategori = SelectField('Utstyr kategori:', choices=[], coerce=str)
    filter = SubmitField('Filter')

class AddUtleieForm(FlaskForm):
    kunde_nr = SelectField('KundeNr:', choices=[], coerce=str)
    avail_utstyr = SelectField('Tilgjengelig Utstyr:', choices=[], coerce=str)
    betalings_måte = SelectField('Betalingsmåte:', choices=[], coerce=str )
    leveres_kunde = SelectField('Leveres kunde?:', choices=[], coerce=str )
    start_dato = DateField('Start Dato:', format='%Y-%m-%d')
    submit = SubmitField('Legg til Utleie')

class UpdateUtleieForm(FlaskForm):
    slutt_dato = DateField('Slutt Dato:', format='%Y-%m-%d')
    submit = SubmitField('Oppdater')

#visninger:

#A，see class Kunde():


#B
class Utleie_Aktiv(): 
    def __init__(self, UtleidDato, InlevertDato, KundeNr, UtstyrsId, UtstyrsMerke, UtstyrsModell, UtstyrsType):
        self.UtleidDato = UtleidDato
        self.InlevertDato = "Ikke levert" if InlevertDato == None else InlevertDato
        self.KundeNr = KundeNr        
        self.UtstyrsId = UtstyrsId 
        self.UtstyrsMerke = UtstyrsMerke
        self.UtstyrsModell = UtstyrsModell
        self.UtstyrsType = UtstyrsType
#D
class Utstyr_Inntekt():
    def __init__(self, UtstyrId, SumPerUtstyr, UtstyrsMerke, UtstyrsModell, UtstyrsType):
        self.UtstyrId = UtstyrId
        self.SumPerUtstyr = SumPerUtstyr
        self.UtstyrsMerke = UtstyrsMerke
        self.UtstyrsModell = UtstyrsModell
        self.UtstyrsType = UtstyrsType
