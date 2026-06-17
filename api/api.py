import time
import json
import sqlite3
import bcrypt
import random
import smtplib
from datetime import datetime, date
from email.message import EmailMessage

class Aluno():
  try:
    with open("data/data.json", "r") as arquivo:
      resultadoJson = json.load(arquivo)
  except (FileNotFoundError, json.JSONDecodeError):
    raise Exception("Arquivo data.json não encontrado ou inválido")
  
  db = resultadoJson["database"]
  dirdb = resultadoJson["dirDatabasse"]
  conn = sqlite3.connect(f"{dirdb}/{db}", check_same_thread=False)

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
    password TEXT NOT NULL,
    reset_code TEXT,
    reset_expires INTEGER
);
""")

  @staticmethod
  def enviarEmail(user):
    codigo = str(random.randint(100000, 999999))
    expira_em = int(time.time()) + 300
    Aluno.cursor.execute("SELECT email FROM users WHERE login = ?", (user,))
    row = Aluno.cursor.fetchone()
    if not row:
      return False
    email_usuario = row[0]

    try:
      msg = EmailMessage()

      msg["Subject"] = "No Reply"
      msg["From"] = "paulolux814@gmail.com"
      msg["To"] = email_usuario

      msg.set_content(
        f"""  Olá,

  Recebemos uma solicitação para redefinir a senha da sua conta.

  Utilize o código abaixo para continuar o processo de recuperação:

  Código de recuperação: {codigo}

  Por motivos de segurança, este código é válido por 5 minutos e deve ser utilizado apenas por você.

  Se você não solicitou a recuperação de senha, ignore este e-mail. Nenhuma alteração será realizada em sua conta.

  Atenciosamente,

  Equipe de Suporte"""
      )

      with smtplib.SMTP_SSL(
        "smtp.gmail.com",
        465
      ) as smtp:
        smtp.login(
          "samuelbonfimaraujo@gmail.com",
          "ieqp nccw rukn wtps"
        )

        smtp.send_message(msg)
    
      Aluno.cursor.execute(
    """
    UPDATE users
    SET reset_code = ?, reset_expires = ?
    WHERE login = ?
    """,
    (codigo, expira_em, user)
)
      Aluno.conn.commit()
      return True
    except Exception as e:
      print(f"ERRO: {e}")
      return False

  @staticmethod
  def verificarCodigo(login, codigo_digitado):

      Aluno.cursor.execute(
          """
          SELECT reset_code,
                reset_expires
          FROM users
          WHERE login = ?
          """,
          (login,)
      )

      row = Aluno.cursor.fetchone()

      if row:

          codigo_salvo = row[0]
          expiracao = row[1]

          if (
              codigo_digitado == codigo_salvo
              and time.time() < expiracao
          ):
              return True

      return False

  @staticmethod
  def encrypt(senha):
    hash_senha = bcrypt.hashpw(senha.encode(), bcrypt.gensalt()).decode()
    return hash_senha

  @staticmethod
  def add(login, name, email, phone, birthday, is_student, passwd):  # ---> Make a function for add a new Person
    nascimento = datetime.strptime(birthday, "%Y-%m-%d").date()
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
        return True
      else:
        return False
  
  @staticmethod
  def calcular_idade(data_str):
    nascimento = datetime.strptime(data_str, "%Y-%m-%d").date()
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