import sqlite3
from sqlite3.dbapi2 import Error
from tkinter.constants import NONE
from conexao import Conexao

class Nota:

    def cadastrar(self,fk_aluno_id,fk_disciplina_id,av1,av2,av3,media):
        try:
            conn = Conexao()
            conexao = conn.conectar()
            cursor = conexao.cursor()

            sql = 'INSERT INTO nota (fk_aluno_id,fk_disciplina_id,av1,av2,av3,media) VALUES (?,?,?,?,?,?)'
            cursor.execute(sql,(fk_aluno_id,fk_disciplina_id,av1,av2,av3,media))
           
            conexao.commit()
            cursor.close()
            conexao.close()

            return True
        except sqlite3.OperationalError as e:
            print("Erro no cadastro de aluno: {}".format(e))
            return False
        except sqlite3.IntegrityError as e:
            print("Erro de integridade: {}".format(e))
            return False

    
    def consultar(self):
        conn = Conexao()
        conexao = conn.conectar()
        cursor = conexao.cursor()
         
        
        try:
            resultset = cursor.execute('SELECT * FROM nota ORDER BY fk_aluno_id').fetchall()
        except Error as e:
            print(f"O erro '{e}' ocorreu.")
            
        cursor.close()
        conexao.close()
        return resultset

    def atualizar(self,fk_aluno_id,fk_disciplina_id,av1,av2,av3,media):
        try:
            conn = Conexao()
            conexao = conn.conectar()
            cursor = conexao.cursor()

            sql = 'UPDATE nota SET fk_aluno_id = ?, fk_disciplina_id = ?, av1 = ?, av2 = ?, av3 = ?, media = ? WHERE fk_aluno_id = (?)'
            cursor.execute(sql,(fk_aluno_id,fk_disciplina_id,av1,av2,av3,media))
           
            conexao.commit()
            cursor.close()
            conexao.close()

            return True
        except sqlite3.OperationalError as e:
            print("Erro na atualização de aluno: {}".format(e))
            return False
        except sqlite3.IntegrityError as e:
            print("Erro de integridade: {}".format(e))
            return False


    def excluir(self,fk_aluno_id):
        try:
            conn = Conexao()
            conexao = conn.conectar()
            cursor = conexao.cursor()

            sql = 'DELETE FROM nota WHERE fk_aluno_id = (?)'
            cursor.execute(sql,[fk_aluno_id])
           
            conexao.commit()
            cursor.close()
            conexao.close()

            return True
        except sqlite3.OperationalError as e:
            print("Erro na exclusão de aluno: {}".format(e))
            return False
        except sqlite3.IntegrityError as e:
            print("Erro de integridade: {}".format(e))
            return False

    def consultar_por_matricula(self,matri):
        conn = Conexao()
        conexao = conn.conectar()
        cursor = conexao.cursor()

        sql = """SELECT n.fk_aluno_id, n.fk_disciplina_id, n.av1, n.av2, n.av3, n.media
                FROM nota as n
                WHERE fk_aluno_id = ?"""

        resultset = None
        try:
            resultset =  cursor.execute(sql,(matri,)).fetchall()
        except Error as e:
            print(f"O erro '{e}' ocorreu.")

        cursor.close()
        conexao.close()
        return resultset

    def consultar_ultimo_id(self):
        conn = Conexao()
        conexao = conn.conectar()
        cursor = conexao.cursor()

        try:
            resultset = cursor.execute('SELECT MAX(id) FROM nota').fetchone()
        except Error as e:
            print(f"O erro '{e}' ocorreu.")

        
        cursor.close()
        conexao.close()
        return resultset[0]