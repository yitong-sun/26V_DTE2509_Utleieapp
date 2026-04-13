import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

class Database():
    def __init__(self):
        self.mysqlConnection = mysql.connector.connect(
        host="localhost",
        user="root",
        password=os.getenv("DB_PASSWORD"),
        database= "utstyrsutleiedb")

    def __enter__(self):
        try:
            self.cursor = self.mysqlConnection.cursor()
            return self
        except mysql.connector.Error as error:
            print("Error while connecting to MySQL", error)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.mysqlConnection.commit()
        self.cursor.close()
        self.mysqlConnection.close()




    #user
    def load_user(self, user_id):
        self.cursor.execute("SELECT * FROM user WHERE id = %s", (user_id,))
        return self.cursor.fetchone()
    
    def create_user(self, name, email, password):
        self.cursor.execute("INSERT INTO user (name, email, password_hash, role) VALUES (%s, %s, %s, 'user')", (name, email, password))
        return 
        
    def load_user_by_email(self, email):
        self.cursor.execute("SELECT * FROM user WHERE email = %s;", (email,))
        return self.cursor.fetchone()
    

    
    #utstyr
    def get_all_utstyr(self):
        self.cursor.execute("SELECT ut.UtstyrId, ut.UtstyrsType, ut.UtstyrsMerke, ut.UtstyrsModell, ut.Beskrivelse, kat.Beskrivelse, ut.LeiePrisDøgn, ut.AntallUtstyr, ut.AntallPåLager FROM utstyr as ut, utstyrskategori as kat WHERE ut.UtstyrsKatId = kat.UtstyrsKatId  ")
        return self.cursor.fetchall()
    


    
    #kunder
    def get_all_kunder(self):
        self.cursor.execute("""
                            SELECT KundeNr, KundeEpost, Fakt_AdresseId, Levering_AdresseId
                            FROM kunde
                            """)
        return self.cursor.fetchall()

    def get_kunde_by_kundenr(self, kundenr):
        self.cursor.execute("""
                            SELECT KundeNr, KundeEpost, Fakt_AdresseId, Levering_AdresseId
                            FROM kunde
                            WHERE KundeNr = %s
                            """, (kundenr,))
        return self.cursor.fetchone()


    #kundetelefon
    def get_telefoner_for_kunde(self, kundenr):
        self.cursor.execute("""
                            SELECT TelefonNr
                            FROM kundetelefon
                            WHERE KundeNr = %s
                            """, (kundenr,))
        return self.cursor.fetchall()

    #privatkunde
    def get_privatkunde_navn(self, kundenr):
        self.cursor.execute("""
                            SELECT Fornavn, Etternavn
                            FROM privatkunde
                            WHERE KundeNr = %s
                            """, (kundenr,))
        return self.cursor.fetchone()

    #bedriftkunde
    def get_bedriftkunde_navn(self, kundenr):
        self.cursor.execute("""
                            SELECT Kundenavn
                            FROM bedriftkunde
                            WHERE KundeNr = %s
                            """, (kundenr,))
        return self.cursor.fetchone()

    #adresse
    def get_adresse_by_id(self, adresse_id):
        self.cursor.execute("""
                            SELECT a.AdrGate, a.AdrGateNr, a.PostNr, p.PostSted
                            FROM adresse AS a,
                                 poststed AS p
                            WHERE a.PostNr = p.PostNr
                              AND a.AdresseId = %s
                            """, (adresse_id,))
        return self.cursor.fetchone()





    #create kunde
    def add_kunde(self, kundenr, epost, fakt_adresse_id, levering_adresse_id):
        self.cursor.execute("""
                            INSERT INTO kunde (KundeNr, KundeEpost, Fakt_AdresseId, Levering_AdresseId)
                            VALUES (%s, %s, %s, %s)
                            """, (kundenr, epost, fakt_adresse_id, levering_adresse_id))


    def add_kundetelefon(self, kundenr, telefonnr):
        self.cursor.execute("""
                            INSERT INTO kundetelefon (KundeNr, TelefonNr)
                            VALUES (%s, %s)
                            """, (kundenr, telefonnr))

    def add_privatkunde(self, kundenr, fornavn, etternavn):
        self.cursor.execute("""
                            INSERT INTO privatkunde (KundeNr, Fornavn, Etternavn)
                            VALUES (%s, %s, %s)
                            """, (kundenr, fornavn, etternavn))

    def add_bedriftkunde(self, kundenr, kundenavn):
        self.cursor.execute("""
                            INSERT INTO bedriftkunde (KundeNr, Kundenavn)
                            VALUES (%s, %s)
                            """, (kundenr, kundenavn))


    #add adresse
    def get_max_adresse_id(self):
        self.cursor.execute("SELECT MAX(AdresseId) FROM adresse")
        return self.cursor.fetchone()

    def add_adresse(self, adresse_id, adresse_type_id, postnr, adrgate, adrgatenr):
        self.cursor.execute("""
                            INSERT INTO adresse (AdresseId, AdresseTypeID, PostNr, AdrGate, AdrGateNr)
                            VALUES (%s, %s, %s, %s, %s)
                            """, (adresse_id, adresse_type_id, postnr, adrgate, adrgatenr))







    #edit kunde
    def update_kunde(self, kundenr, epost, fakt_adresse_id, levering_adresse_id):
        self.cursor.execute("""
                            UPDATE kunde
                            SET KundeEpost         = %s,
                                Fakt_AdresseId     = %s,
                                Levering_AdresseId = %s
                            WHERE KundeNr = %s
                            """, (epost, fakt_adresse_id, levering_adresse_id, kundenr))

    def update_kundetelefon(self, kundenr, telefonnr):
        self.cursor.execute("""
                            UPDATE kundetelefon
                            SET TelefonNr = %s
                            WHERE KundeNr = %s
                            """, (telefonnr, kundenr))

    def update_privatkunde(self, kundenr, fornavn, etternavn):
        self.cursor.execute("""
                            UPDATE privatkunde
                            SET Fornavn   = %s,
                                Etternavn = %s
                            WHERE KundeNr = %s
                            """, (fornavn, etternavn, kundenr))

    def update_bedriftkunde(self, kundenr, kundenavn):
        self.cursor.execute("""
                            UPDATE bedriftkunde
                            SET Kundenavn = %s
                            WHERE KundeNr = %s
                            """, (kundenavn, kundenr))

    def update_adresse(self, adresse_id, postnr, adrgate, adrgatenr):
        self.cursor.execute("""
                            UPDATE adresse
                            SET PostNr    = %s,
                                AdrGate   = %s,
                                AdrGateNr = %s
                            WHERE AdresseId = %s
                            """, (postnr, adrgate, adrgatenr, adresse_id))



    # #delete kunde
    # def delete_kunde(self, kundenr): # not working yet
    #     self.cursor.execute("DELETE FROM kunde WHERE KundeNr = %s", (kundenr,))






    #utleie
    #create utleie
    def add_utleie(self): # not working yet
        self.cursor.execute("")
    #edit utleie
    def update_utleie(self): # not working yet
        self.cursor.execute("")
    


    
    #Visninger
    #A Kundeliste
    def all_bedriftskunder(self):
        self.cursor.execute(""" SELECT bk.KundeNr, bk.Kundenavn, k.KundeEpost, adr.AdrGate AS FakturaAdrGate, adr.AdrGateNr AS FakturaAdrGateNr, adr.postnr AS FakturaAdrPostNr
                                FROM bedriftkunde AS bk, adresse AS adr, kunde as k
                                WHERE k.KundeNr = bk.KundeNr and k.Fakt_AdresseId = adr.AdresseId  """)
        return self.cursor.fetchall()
    
    #B  Aktive utleier ("Ikke innlevert", filtrer på inlogget ansatt)
    def aktive_utleier(self, KundeBehandlerId):
        self.cursor.execute(""" SELECT utl.UtleidDato, utl.InnlevertDato, utl.KundeNr, ut.UtstyrId, ut.UtstyrsMerke, ut.UtstyrsModell, ut.UtstyrsType
                                FROM utleie as utl, Utstyr AS ut, kundebehandler AS kb
                                WHERE utl.UtstyrId = ut.utstyrid AND utl.KundebehandlerId = kb.KundebehandlerId 
                                AND kb.KundebehandlerId = %s AND utl.Innlevertdato is null; """, (KundeBehandlerId,))
        return self.cursor.fetchall()
    
    #C Statistikk: Teller opp antall komplette utleier i valgt periode 
    def komplette_utleier(self):
        self.cursor.execute("""SELECT count(*)
                                FROM utleie
                                WHERE Innlevertdato IS NOT NULL 
                                AND utleiddato BETWEEN "2019-01-01" AND "2020-02-10" 
                                AND Innlevertdato BETWEEN "2019-01-01" AND "2020-02-10";""")
        return self.cursor.fetchone()

    #D Inntekt per utstyr: (liste/tabell, sorter synkende)Viser hvor mye det er tjent på hvert utstyr (uavhengig av instansId).
    def tjent_per_utstyr(self):
        self.cursor.execute("""SELECT utl.utstyrid AS UtstyrsMal_ID, SUM(utl.Totalpris - utl.Leveringskostnad) AS SumPerUtstyr, ut.UtstyrsMerke, ut.UtstyrsModell, ut.UtstyrsType
                                FROM utstyr AS ut INNER JOIN utleie AS utl 
                                ON ut.Utstyrid = utl.Utstyrid AND utl.Totalpris IS NOT NULL
                                GROUP BY utl.Utstyrid
                                ORDER BY SumPerUtstyr DESC;""")
        return self.cursor.fetchall()
    
    #E Mest utleid utstyr: (Highlight topresultatet)Vis det utstyret som er leid ut flest ganger, dvs. uavhengig av instansId.
    def flest_utleid_utstyr(self):
        self.cursor.execute("""SELECT AU.AntUtleid, Ut.UtstyrsMerke, Ut.UtstyrsModell, Ut.UtstyrsType, utkat.Beskrivelse AS Kategori
                                FROM utstyr AS Ut, (SELECT COUNT(*) AS AntUtleid, Utstyrid FROM Utleie GROUP BY utstyrid ORDER BY Antutleid DESC LIMIT 1) as AU, utstyrskategori AS utkat
                                WHERE Ut.utstyrid = AU.UtstyrId AND Ut.UtstyrsKatId = utkat.UtstyrsKatId;""")
        return self.cursor.fetchall()
