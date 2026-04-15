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
        database= "utstyrsutleiedb",
        buffered=True)

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
    
    def create_user(self, id, fornavn, etternavn, email, password):
        self.cursor.execute("INSERT INTO user (id, fornavn, etternavn, email, password_hash, role) VALUES (%s, %s, %s, %s, %s, 'user')", (id, fornavn, etternavn, email, password))
        return 
        
    def load_user_by_email(self, email):
        self.cursor.execute("SELECT * FROM user WHERE email = %s;", (email,))
        return self.cursor.fetchone()
    
    def create_kundebehandler(self, id, fornavn, etternavn):
        self.cursor.execute("INSERT INTO kundebehandler (KundebehandlerId, Fornavn, Etternavn) VALUES (%s, %s, %s)", (id, fornavn, etternavn))

    def check_id_in_use(self, id):
        self.cursor.execute("SELECT EXISTS(SELECT id FROM user WHERE id = %s)", (id,))
        return self.cursor.fetchone()
    
    
    #Dashboard
    def get_total_antall_aktiv_utleie(self):
        self.cursor.execute(""" SELECT COUNT(*)
                                FROM utleie 
                                WHERE Innlevertdato is null
                                GROUP BY InnlevertDato; """)
        return self.cursor.fetchone()
    
    def get_antall_tilgjengelinge_utstyr(self):
        self.cursor.execute(""" SELECT COUNT(*)
                                FROM instans 
                                WHERE concat(Utstyrid,'.',InstansId) 
                                NOT IN (SELECT concat(UtstyrId,'.',InstansId) FROM utleie WHERE InnlevertDato IS Null)""")
        return self.cursor.fetchone()
    
    def get_fem_siste_utleier(self):
        self.cursor.execute("""SELECT utl.UtleieId, utl.UtstyrId, utl.InstansId, utl.KundeNr, utl.UtleidDato, utl.InnlevertDato, 
                                concat(kb.Fornavn,' ', kb.Etternavn), utl.LeveresKunde, bm.Beskrivelse, utl.LeveringsKostnad, utl.TotalPris 
                                FROM utleie AS utl, kundebehandler AS kb, betalingsmåte AS bm 
                                WHERE utl.KundebehandlerId = kb.KundebehandlerId AND utl.BetalingsmåteId = bm.BetalingsmåteId
                                ORDER BY UtleidDato DESC LIMIT 5
                                """)
        return self.cursor.fetchall()

    #utstyr
    def check_status_utstyr_id(self, utstyr_id):
        self.cursor.execute("""SELECT UtstyrId
                                FROM instans 
                                WHERE UtstyrId = %s AND
                                concat(Utstyrid,'.',InstansId) 
                                NOT IN (SELECT concat(UtstyrId,'.',InstansId) FROM utleie WHERE InnlevertDato IS Null)""",
                                (utstyr_id))
        return self.cursor.fetchone()
    
    def get_utstyr_id(self):
        self.cursor.execute("SELECT UtstyrId FROM Utstyr")
        return self.cursor.fetchall()

    def get_all_utstyr(self):
        self.cursor.execute("""SELECT ut.UtstyrId, ut.UtstyrsType, ut.UtstyrsMerke, ut.UtstyrsModell, ut.Beskrivelse, 
                            kat.Beskrivelse, ut.LeiePrisDøgn, ut.AntallUtstyr, ut.AntallPåLager 
                            FROM utstyr as ut, utstyrskategori as kat 
                            WHERE ut.UtstyrsKatId = kat.UtstyrsKatId """)
        
        return self.cursor.fetchall()
    
    def get_filtered_utstyr(self, utstyr_type = None, kategori = None):
        
        query = """SELECT ut.UtstyrId, ut.UtstyrsType, ut.UtstyrsMerke, ut.UtstyrsModell, ut.Beskrivelse, kat.Beskrivelse, 
                    ut.LeiePrisDøgn, ut.AntallUtstyr, ut.AntallPåLager 
                    FROM utstyr as ut, utstyrskategori as kat 
                    WHERE ut.UtstyrsKatId = kat.UtstyrsKatId"""

        paramaters = []

        if utstyr_type:
            query += " AND ut.UtstyrsType= %s "
            paramaters.append(utstyr_type)

        if kategori:
            query += " AND kat.Beskrivelse = %s "
            paramaters.append(kategori)

        self.cursor.execute(query, paramaters)
        
        return self.cursor.fetchall()
    
    def get_utstyr_typer(self):
        self.cursor.execute("SELECT DISTINCT UtstyrsType FROM utstyr ORDER BY UtstyrsType")
        return self.cursor.fetchall()
    
    def get_utstyr_kategorier(self):
        self.cursor.execute("SELECT DISTINCT Beskrivelse FROM utstyrskategori ORDER BY Beskrivelse")
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
    #read utleie
    def get_all_utleie(self):
        self.cursor.execute("""SELECT utl.UtleieId, utl.UtstyrId, utl.InstansId, utl.KundeNr, utl.UtleidDato, utl.InnlevertDato, 
                                concat(kb.Fornavn,' ', kb.Etternavn), utl.LeveresKunde, bm.Beskrivelse, utl.LeveringsKostnad, utl.TotalPris 
                                FROM utleie AS utl, kundebehandler AS kb, betalingsmåte AS bm 
                                WHERE utl.KundebehandlerId = kb.KundebehandlerId AND utl.BetalingsmåteId = bm.BetalingsmåteId
                                ORDER BY utl.UtleieId ASC""")
        return self.cursor.fetchall()
    
    #create utleie
    def add_utleie(self, kundebehandler_id, kunde_nr, utstyr_id, instans_id, leveres_kunde, betalingsmåte_id, start_dato, leveringskostnad): # not working yet
        self.cursor.execute("INSERT INTO utleie (KundebehandlerId, KundeNr, UtstyrId, InstansId, LeveresKunde, BetalingsmåteId, UtleidDato, LeveringsKostnad) VALUES (%s, %s, %s,%s,%s,%s,%s,%s)", 
                            (kundebehandler_id, kunde_nr, utstyr_id, instans_id, leveres_kunde, betalingsmåte_id, start_dato, leveringskostnad))

    def get_kunde_nr(self):
        self.cursor.execute("SELECT KundeNr FROM kunde")
        return self.cursor.fetchall()
    
    def get_utstyr_if_available(self):
        self.cursor.execute("""SELECT concat(Utstyrid,'.',InstansId) 
                                FROM instans 
                                WHERE concat(Utstyrid,'.',InstansId) 
                                NOT IN (SELECT concat(UtstyrId,'.',InstansId) FROM utleie WHERE InnlevertDato IS Null)""")
        return self.cursor.fetchall()
    
    def get_betalingsmåter(self):
        self.cursor.execute("SELECT Beskrivelse FROM betalingsmåte")
        return self.cursor.fetchall()
    
    def get_betalingsmåte_id(self, betalingsmåte):
        self.cursor.execute("SELECT BetalingsmåteId FROM betalingsmåte WHERE Beskrivelse = %s", (betalingsmåte,))
        return self.cursor.fetchone()
    
    #edit utleie
    def edit_innlevert_utleie(self, slutt_dato, utleie_id): # not working yet
        self.cursor.execute("UPDATE utleie SET InnlevertDato=%s WHERE UtleieId=%s ", (slutt_dato, utleie_id))

    def calculate_totalpris(self, utleie_id):
        self.cursor.execute("""SELECT SUM(ut.LeiePrisDøgn*IF(DATEDIFF(utl.InnlevertDato, utl.UtleidDato)=0, 1, DATEDIFF(utl.InnlevertDato, utl.UtleidDato)) + utl.LeveringsKostnad) 
                                FROM utstyr as ut, utleie as utl 
                                WHERE ut.UtstyrId=utl.UtstyrId AND utl.UtleieId = %s""", (utleie_id,))
        return self.cursor.fetchone()
        
    def edit_totalpris_utleie(self,totalpris ,utleie_id):
        self.cursor.execute("UPDATE utleie SET TotalPris=%s WHERE UtleieId=%s ", (totalpris, utleie_id))

    def get_utleid_dato(self, utleie_id):
        self.cursor.execute(""" SELECT UtleidDato 
                                FROM Utleie
                                WHERE UtleieId = %s
                                """, (utleie_id,))
        return self.cursor.fetchone()
    


    #Registrere utleie
        #Velg kunde
        #Velg Utstyr(kun tilgjengelig)
        #Sett dato
        #Automatisk registrer hvilken ansatt som ekspederer

    #Registrer innlevering
        #Marker utleie som levert
        #Sett innleveringsdato  


    
    #Visninger
    #A Kundeliste
    def all_bedriftskunder(self):
        self.cursor.execute(""" SELECT bk.KundeNr, bk.Kundenavn, k.KundeEpost, adr.AdrGate AS FakturaAdrGate, adr.AdrGateNr AS FakturaAdrGateNr, adr.postnr AS FakturaAdrPostNr
                                FROM bedriftkunde AS bk, adresse AS adr, kunde as k
                                WHERE k.KundeNr = bk.KundeNr and k.Fakt_AdresseId = adr.AdresseId  """)
        return self.cursor.fetchall()
    
    #B  Aktive utleier ("Ikke innlevert", filtrer på inlogget ansatt)
    def aktive_utleier(self, kundebehandler_id):
        self.cursor.execute(""" SELECT utl.UtleidDato, utl.InnlevertDato, utl.KundeNr, ut.UtstyrId, ut.UtstyrsMerke, ut.UtstyrsModell, ut.UtstyrsType
                                FROM utleie as utl, Utstyr AS ut, kundebehandler AS kb
                                WHERE utl.UtstyrId = ut.utstyrid AND utl.KundebehandlerId = kb.KundebehandlerId 
                                AND kb.KundebehandlerId = %s AND utl.Innlevertdato is null; """, (kundebehandler_id,))
        return self.cursor.fetchall()
    
    def get_kundebehandler_navn(self, kundebehandler_id):
        self.cursor.execute("SELECT concat(Fornavn,' ', Etternavn) FROM kundebehandler WHERE KundebehandlerId = %s", (kundebehandler_id,))
        return self.cursor.fetchone()
    
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
                                FROM utstyr AS Ut, 
                                (SELECT COUNT(*) AS AntUtleid, Utstyrid FROM Utleie GROUP BY utstyrid ORDER BY Antutleid DESC) as AU, utstyrskategori AS utkat
                                WHERE Ut.utstyrid = AU.UtstyrId AND Ut.UtstyrsKatId = utkat.UtstyrsKatId
                                ORDER BY AU.AntUtleid DESC;""")
        return self.cursor.fetchall()
    
    def get_top_flest_utleid_utstyr_antall(self):        
        self.cursor.execute("""SELECT COUNT(*) AS AntUtleid 
                            FROM Utleie 
                            GROUP BY utstyrid 
                            ORDER BY Antutleid DESC LIMIT 1""")
        return self.cursor.fetchone()

