from api.api import Aluno
from flask import Flask, render_template, request, redirect, url_for

def Main():

    app = Flask(__name__)

    @app.route("/", methods=["GET", "POST"])
    def login():

        mensagem = ""

        if request.method == "POST":

            usuario = request.form["username"]
            senha = request.form["password"]

            a = Aluno.login(usuario, senha)

            if a is False:
                mensagem = "Login ou senha incorreto"

            elif a is True:
                return redirect(url_for("BemVindo'"))

        return render_template(
            "login.html",
            mensagem=mensagem
        )

    @app.route("/remember", methods=["GET", "POST"])
    def remember():

        mensagem = ""

        if request.method == "POST":

            usuario = request.form["usuario"]

            if Aluno.enviarEmail(usuario):

                return redirect(
                    url_for(
                        "verificar_codigo",
                        login=usuario
                    )
                )
            else:
              mensagem = "Usuário não encontrado"

        return render_template(
            "remember.html",
            mensagem=mensagem
        )

    @app.route(
        "/verificar_codigo/<login>",
        methods=["GET", "POST"]
    )
    def verificar_codigo(login):

        mensagem = ""

        if request.method == "POST":

            codigo = request.form["codigo"]

            if Aluno.verificarCodigo(login, codigo):

                return redirect(
                    url_for(
                        "nova_senha",
                        login=login
                    )
                )

            mensagem = "Código inválido"

        return render_template(
            "verificar_codigo.html",
            login=login,
            mensagem=mensagem
        )

    @app.route(
        "/nova_senha/<login>",
        methods=["GET", "POST"]
    )
    def nova_senha(login):
        print("Método:", request.method)

        mensagem = ""
        if request.method == "POST":
            
            senha = request.form["senha"]
            confirm_senha = request.form["confirm_senha"]

            if senha == confirm_senha:
              Aluno.recuperarSenha(
                  login,
                  senha
              )

              return redirect(url_for("login"))
            else:
                mensagem = "As senhas devem ser iguais"
        print(f"Mensagem: '{mensagem}'")

        return render_template(
            "nova_senha.html",
            mensagem=mensagem
        )
    
    @app.route("/register", methods=["GET", "POST"])
    def register():
        
        mensagem = ""
        if request.method == "POST":
            name = request.form["name"]
            username = request.form["username"]
            email = request.form["email"]
            phone = request.form["phone"]
            birthday = str(request.form["birthday"])
            password = request.form["password"]
            confirmPassword = request.form["confirmpassword"]

            if password != confirmPassword:
                mensagem = "As senhas devem ser iguais"
            else:
                Aluno.add(username, name, email, phone, birthday, "0", password)
                return redirect(url_for("login"))

        return render_template("register.html", mensagem=mensagem)

    @app.route("/BemVindo")
    def BemVindo():
        return render_template("index.html")

    app.run(host="0.0.0.0", port=5000, debug=True)

if __name__ == "__main__":
    Main()