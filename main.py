import time
from api.api import Aluno
from flask import Flask, render_template, request, redirect, url_for

def Main():
  # Aluno.show()
  # Aluno.add("SamuelDF", "Samuel Bonfim Araujo", "samuelbonfimaraujo@gmail.com", "61996445622", "09/02/2010", "1", "1234")
  app = Flask(__name__)

  @app.route("/", methods=["GET", "POST"])
  def login():
      mensagem = ""
      if request.method == "POST":
          usuario = request.form["username"]
          senha = request.form["password"]

          a = Aluno.login(usuario, senha)
          if a == False:
             mensagem = "Login ou senha incorreto"
             print("bruh")
          elif a == True:
             return redirect(url_for("remember"))
      return render_template("login.html", mensagem=mensagem)
      

  @app.route("/remember", methods=["GET", "POST"])
  def remember():
      if request.method == "POST":
          usuario = request.form["usuario"]
          a = Aluno.enviarEmail(usuario)
          if a == True:
             url_for("verificar_codigo", login=usuario)
      return render_template("remember.html")

  app.run(debug=True)

if __name__ == "__main__":
  Main()