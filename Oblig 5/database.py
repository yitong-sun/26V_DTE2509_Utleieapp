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
    def get_all_kunder(self): # not working yet
        self.cursor.execute("")
        return self.cursor.fetchall()
    #edit kunde
    def update_kunde(self): # not working yet
        self.cursor.execute("")

    #create kunde
    def add_kunde(self): # not working yet
        self.cursor.execute("")

    #delete kunde
    def delete_kunde(self, kundenr): # not working yet
        self.cursor.execute("DELETE FROM Kunde WHERE KundeNr = %s", (kundenr))
    



    #utleie
    #read utleie
    def get_all_utleie(self):
        self.cursor.execute("""SELECT utl.UtleieId, utl.UtstyrId, utl.InstansId, utl.KundeNr, utl.UtleidDato, utl.InnlevertDato, 
                                concat(kb.Fornavn,' ', kb.Etternavn), utl.LeveresKunde, bm.Beskrivelse, utl.LeveringsKostnad, utl.TotalPris 
                                FROM utleie AS utl, kundebehandler AS kb, betalingsmåte AS bm 
                                WHERE utl.KundebehandlerId = kb.KundebehandlerId AND utl.BetalingsmåteId = bm.BetalingsmåteId""")
        return self.cursor.fetchall()
    
    #create utleie
    def add_utleie(self, kundebehandler_id, kunde_nr, utstyr_id, instans_id, leveres_kunde, betalingsmåte_id, start_dato): # not working yet
        self.cursor.execute("INSERT INTO utleie (KundebehandlerId, KundeNr, UtstyrId, InstansId, LeveresKunde, BetalingsmåteId, UtleidDato) VALUES (%s, %s, %s,%s,%s,%s,%s)", 
                            (kundebehandler_id, kunde_nr, utstyr_id, instans_id, leveres_kunde, betalingsmåte_id, start_dato))

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
    def update_utleie(self): # not working yet
        self.cursor.execute("")
        pass
    
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
