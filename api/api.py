import json
import sqlite3
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
    name TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    phone TEXT NOT NULL UNIQUE,
    birthday TEXT NOT NULL,
    is_student INTEGER NOT NULL
);
""")
  
  @staticmethod
  def add(name, email, phone, birthday, is_student):  # ---> Make a function for add a new Person
    try:


      user_data = (name, email, phone, birthday, is_student)
      Aluno.cursor.execute("INSERT INTO users (name, email, phone, birthday, is_student) VALUES (?, ?, ?, ?, ?)", user_data)
      Aluno.conn.commit()
    except Exception as e:
      print(f"Erro ao criar novo usuario {e}")
  
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
      idade = Aluno.calcular_idade(row[4])
      print(f"ID: {row[0]}, Name: {row[1]}, Email: {row[2]}, Phone: {row[3]}, BirthDay: {row[4]}, Age: {idade}")