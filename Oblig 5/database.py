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
    #create utleie
    def add_utleie(self): # not working yet
        self.cursor.execute("")
    #edit utleie
    def update_utleie(self): # not working yet
        self.cursor.execute("")
    


    
    #Visninger
    #A
    #B
    #C
    #D
    #E

