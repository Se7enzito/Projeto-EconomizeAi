import sqlite3 as sql
import os

class GerenciamentoUsers():
    def __init__(self) -> None:
        self.database = "backend/libs/db/database.db"
        self.connection = None
        self.cursor = None

    def conectar(self) -> None:
        self.connection = sql.connect(self.database)
        self.cursor = self.connection.cursor()

    def desconectar(self) -> None:
        self.connection.close()

    def tabelaExiste(self, nome_tabela: str) -> bool:
        self.conectar()
        consulta = self.cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{nome_tabela}'").fetchone()
        self.desconectar()
        
        return consulta is not None
    
    def criarTabela(self) -> None:
        if self.tabelaExiste('users'):
            return
        
        self.conectar()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                user TEXT NOT NULL UNIQUE,
                                senha TEXT NOT NULL,
                                perm INTEGER NOT NULL
                            )''')
        self.cursor.execute('''INSERT INTO users (user, senha, perm) VALUES ('admin', 'admin', 3)''')
        self.connection.commit()
        self.desconectar()
    
    def criarUser(self, user: str, senha: str, perm: int) -> list:
        if (user == "" or senha == "" or perm == None):
            return []
        
        self.conectar()
        self.cursor.execute("INSERT INTO users (user, senha, perm) VALUES (?,?,?)", (user, senha, perm))
        
        nomeTabela = user.replace(' ', '_')
        
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS ? (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            data TEXT NOT NULL,
            valor INTEGER NOT NULL,
            tipo INTEGER NOT NULL
            )''', (nomeTabela,))
        self.connection.commit()
        self.desconectar()
        
        return [user, senha, perm]
    
    def getIdDados(self, user: str, nome: str):
        self.conectar()
        id = self.cursor.execute("SELECT id FROM? WHERE nome =?", (user.replace(' ', '_'), nome)).fetchone()
        self.desconectar()
        
        return id[0] if id else None
    
    def atualizarDados(self, user: str, nome: str, data: str, valor: int, tipo: int):
        self.conectar()
        
        id = self.getIdDados(user, nome)
        
        self.cursor.execute("UPDATE ? SET nome =?, data =?, valor =?, tipo =? WHERE id =?", (user.replace(' ', '_'), nome, data, valor, tipo, id))
        self.connection.commit()
        self.desconectar()
    
    def removerDados(self, user: str, nome: str):
        self.conectar()
        self.cursor.execute("DELETE FROM ? WHERE nome =?", (user.replace(' ', '_'), nome))
        self.connection.commit()
        self.desconectar()
    
    def adicionarDados(self, user: str, nome: str, data: str, valor: int, tipo: int):
        self.conectar()
        self.cursor.execute("INSERT INTO ? (nome, data, valor, tipo) VALUES (?,?,?,?)", (user.replace(' ', '_'), nome, data, valor, tipo))
        self.connection.commit()
        self.desconectar()
        
    def listarDados(self, user: str):
        self.conectar()
        dados = self.cursor.execute(f"SELECT * FROM ?", (user.replace(' ', '_')))
        self.desconectar()
        
        return dados.fetchall()

    def buscarDadosData(self, user: str, data: str):
        self.conectar()
        dados = self.cursor.execute(f"SELECT * FROM ? WHERE data = ?", (user.replace(' ', '_'), data))
        self.desconectar()
        
        return dados.fetchall()
    
    def buscarDadosTipo(self, user: str, tipo: int):
        self.conectar()
        dados = self.cursor.execute(f"SELECT * FROM ? WHERE tipo = ?", (user.replace(' ', '_'), tipo))
        self.desconectar()
        
        return dados.fetchall()    

    def buscarDadosNome(self, user: str, nome: str):
        self.conectar()
        dados = self.cursor.execute(f"SELECT * FROM ? WHERE nome LIKE ?", (user.replace(' ', '_'), nome))
        self.desconectar()
        
        return dados.fetchone()

    def atualizarUserAdmin(self, user: str, senha: str, perm: int) -> list:
        if (user == ""):
            return []
        
        if (senha == ""):
            senha = self.getSenha(user)
        
        if (perm == 0 or perm == "" or perm is None):
            perm = self.getPerm(user)

        self.conectar()
        self.cursor.execute("UPDATE users SET senha =?, perm =? WHERE user =?", (senha, perm, user))
        self.connection.commit()
        self.desconectar()
        
        return [user, senha, perm]
    
    def atualizarUser(self, user: str, senha: str) -> bool:
        if (senha == "" or senha == self.getSenha(user)):
            return [user, senha]
        
        self.conectar()
        self.cursor.execute("UPDATE users SET senha =? WHERE user =?", (senha, user))
        self.connection.commit()
        self.desconectar()
        
        return [user, senha]
    
    def deletarUser(self, user: str) -> bool:
        self.conectar()
        self.cursor.execute("DELETE FROM users WHERE user =?", (user,))
        self.connection.commit()
        self.desconectar()
        
        return True
    
    def getAllUsers(self) -> list:
        self.conectar()
        consulta = self.cursor.execute("SELECT * FROM users").fetchall()
        self.desconectar()
        
        return consulta
    
    def getSenha(self, user: str) -> str:
        self.conectar()
        consulta = self.cursor.execute("SELECT senha FROM users WHERE user =?", (user,)).fetchone()
        self.desconectar()
        
        if consulta:
            return consulta[0]
        else:
            return None
        
    def getPerm(self, user: str) -> int:
        self.conectar()
        consulta = self.cursor.execute("SELECT perm FROM users WHERE user =?", (user,)).fetchone()
        self.desconectar()
        
        if consulta:
            return consulta[0]
        else:
            return None 
    
    def containsUser(self, user: str) -> bool:
        self.conectar()
        consulta = self.cursor.execute("SELECT user FROM users").fetchall()
        self.desconectar()
        
        for row in consulta:
            if row[0] == user:
                return True
        
        return False

    def senhaCorreta(self, user: str, senha: str) -> bool:
        self.conectar()
        consulta = self.cursor.execute("SELECT senha FROM users WHERE user = ?", (user,)).fetchall()
        self.desconectar()
        
        if consulta and consulta[0][0] == senha:
            return True
        else:
            return False

if __name__ == "__main__":
    pass