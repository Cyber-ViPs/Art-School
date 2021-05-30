import sqlite3
from sqlite3.dbapi2 import Cursor, connect

class Conexao:
   
    def conectar(self):
        conexao = None
        db_path = 'school.db'
        try:
            conexao = sqlite3.connect(db_path, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)

        except sqlite3.DatabaseError as err:
            print(f"Erro ao conectar o banco de dados {db_path}.")
        return conexao

    def search(nome="", idade="", cpf="", matricula="", email="", endereco=""):
        conexao = Conexao()
        conexao.conectar()
        conexao.execute("SELECT * FROM aluno WHERE nome=? or idade=? or cpf=? or matricula=? or email=? or endereco=?", (nome,idade,cpf,matricula,email, endereco))
        rows = conexao.fetchall()
        conexao.disconnect()
        return rows

    def createTablealuno(self,conexao,cursor):
        cursor.execute('DROP TABLE IF EXISTS aluno')
    
        sql = """CREATE TABLE IF NOT EXISTS aluno (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome varchar NOT NULL,
                    idade varchar NOT NULL,
                    cpf bigint NOT NULL UNIQUE,
                    matricula int NOT NULL,
                    email varchar NOT NULL,
                    endereco varchar NOT NULL);"""
        
        cursor.execute(sql)
        conexao.commit()

    def createTabledisciplina(self,conexao,cursor):
        cursor.execute('DROP TABLE IF EXISTS disciplina')
        
        sql = """CREATE TABLE IF NOT EXISTS disciplina(
            id INTEGER PRIMARY KEY,
            disciplina varchar NOT NULL 
        );"""
        
        cursor.execute(sql)
        conexao.commit()

    def createTablenota(self,conexao,cursor):
        cursor.execute('DROP TABLE IF EXISTS nota')
        
        sql = """CREATE TABLE IF NOT EXISTS nota(
            fk_aluno_id int,
            fk_disciplina_id int,
            av1 double NOT NULL,
            av2 double NOT NULL,
            av3 double NOT NULL,
            media DOUBLE NOT NULL,
            PRIMARY KEY (fk_aluno_id),
            FOREIGN KEY (fk_Aluno_id) REFERENCES aluno (id)
            FOREIGN KEY (fk_disciplina_id) REFERENCES disciplina (id));"""
        
        cursor.execute(sql)
        conexao.commit()    

    def createTables(self):
        
        conexao = self.conectar()
        cursor = conexao.cursor()
        self.createTablealuno(conexao,cursor)
        self.createTabledisciplina(conexao,cursor)
        self.createTablenota(conexao,cursor)
       