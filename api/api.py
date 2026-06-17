import json
import sqlite3
import bcrypt
from datetime import datetime, date

class Aluno():
  try:
    with open("data/data.json", "r") as arquivo:
      resultadoJson = json.load(arquivo)
  except (FileNotFoundError, json.JSONDecodeError):
    raise Exception("Arquivo data.json não encontrado ou inválido")
  
  db = resultadoJson["database"]
  dirdb = resultadoJson["dirDatabasse"]
  conn = sqlite3.connect(f"{dirdb}/{db}")

  cursor = conn.cursor()

  cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    login TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    phone TEXT NOT NULL,
    birthday TEXT NOT NULL,
    is_student INTEGER NOT NULL,
    password TEXT NOT NULL
);
""")
  
  @staticmethod
  def encrypt(senha):
    hash_senha = bcrypt.hashpw(senha.encode(), bcrypt.gensalt()).decode()
    return hash_senha

  @staticmethod
  def add(login, name, email, phone, birthday, is_student, passwd):  # ---> Make a function for add a new Person
    nascimento = datetime.strptime(birthday, "%d/%m/%Y").date()
    if (nascimento.year > date.today().year) or (nascimento.year < (date.today().year - 130)):
      print("Data de aniversario invalida")
    elif (is_student != "1") and (is_student != "0"):
      print("Valor invalido do campo: is_student")
    else:
      try:
        user_data = (login, name, email, phone, birthday, is_student, Aluno.encrypt(passwd))
        Aluno.cursor.execute("INSERT INTO users (login, name, email, phone, birthday, is_student, password) VALUES (?, ?, ?, ?, ?, ?, ?)", user_data)
        Aluno.conn.commit()
      except Exception as e:
        if str(e) == "UNIQUE constraint failed: users.email":
          print("Email existente")
        elif str(e) == "UNIQUE constraint failed: users.login":
          print("Login existente")
        else:
          print(f"ERRO: {e}")

  @staticmethod
  def login(login, passwd):
    Aluno.cursor.execute("SELECT * FROM users WHERE login = ?", (login,))
    row = Aluno.cursor.fetchone()
    if row:
      hash_salvo = row[7]
      if bcrypt.checkpw(passwd.encode(), hash_salvo.encode()):
        print("OK")
      else:
        print("Senha ou login incorreto")
  
  @staticmethod
  def calcular_idade(data_str):
    nascimento = datetime.strptime(data_str, "%d/%m/%Y").date()
    hoje = date.today()

    idade = hoje.year - nascimento.year

    if (hoje.month, hoje.day) < (nascimento.month, nascimento.day):
        idade -= 1

    return idade

  @staticmethod
  def show():
    Aluno.cursor.execute("SELECT * FROM users")
    rows = Aluno.cursor.fetchall()

    for row in rows:
      idade = Aluno.calcular_idade(row[5])
      print(f"ID: {row[0]}, Login: {row[1]}, Name: {row[2]}, Email: {row[3]}, Phone: {row[4]}, BirthDay: {row[5]}, Age: {idade}")
  
  @staticmethod
  def delete(id):
    try:
      Aluno.cursor.execute("DELETE FROM users WHERE id = ?", (id,))
      Aluno.conn.commit()
    except Exception as e:
      print(f"Erro: {e}")
  
  @staticmethod
  def recuperarSenha(login, passwd):
    try:
      Aluno.cursor.execute("UPDATE users SET password = ? WHERE login = ?", (Aluno.encrypt(passwd), login,))
      Aluno.conn.commit()
    except Exception as e:
      print(f"ERRO: {e}")