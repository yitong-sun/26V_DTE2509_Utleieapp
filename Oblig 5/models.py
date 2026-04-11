from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, name, email, role):
        self.id = id
        self.name = name
        self.email = email
        self.role = role

class Kunde(): #can edit this, 
    def __init__(self, kundenr, navn, epost, mobil, fakt_adresse ,levering_adresse):
        self.kundenr = kundenr
        self.navn = navn
        self.epost = epost
        self.mobil = mobil
        self.fakt_Adresse = fakt_adresse 
        self.levering_Adresse  = levering_adresse

class Utstyr():
    def __init__(self, UtstyrId, UtstyrsType, UtstyrsMerke, UtstyrsModell, Beskrivelse, UtstyrsKategori, leieprisdøgn, AntallUtstyr, AntallPåLager):
        self.UtstyrId = UtstyrId
        self.UtstyrsType = UtstyrsType
        self.UtstyrsMerke = UtstyrsMerke
        self.UtstyrsModell = UtstyrsModell
        self.Beskrivelse = Beskrivelse
        self.UtstyrsKategori= UtstyrsKategori
        self.leieprisdøgn = "Utiljengelig" if leieprisdøgn == None else leieprisdøgn
        self.AntallUtstyr= AntallUtstyr
        self.AntallPåLager= AntallPåLager

class Utleie():
    def __init__(self, UtleieId, UtstyrsId, InstansId, KundeNr, UtleidDato, InlevertDato, KundebehandlerId,Levereskunde,BetalingsmåteId, Leveringskostnad, Totalpris ):
        self.UtleieId = UtleieId
        self.UtstyrsId = UtstyrsId
        self.InstansId = InstansId
        self.KundeNr = KundeNr
        self.UtleidDato = UtleidDato
        self.InlevertDato = InlevertDato
        self.KundebehandlerId = KundebehandlerId
        self.Levereskunde = Levereskunde
        self.BetalingsmåteId = BetalingsmåteId
        self.Leveringskostnad = Leveringskostnad
        self.Totalpris = Totalpris