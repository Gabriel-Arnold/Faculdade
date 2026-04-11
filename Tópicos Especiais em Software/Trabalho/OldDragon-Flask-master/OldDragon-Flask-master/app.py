from flask import Flask, render_template, request, redirect, url_for
from model.personagem import Personagem
from model.regras import gerar_atributos

app = Flask(__name__)
app.config["SECRET_KEY"] = "chave-secreta"

@app.route("/")
def index():
    return redirect(url_for("criar_personagem"))

@app.route("/criar", methods=["GET", "POST"])
def criar_personagem():
    if request.method == "POST":
        nome = request.form.get("nome", "Sem Nome")
        atributos = gerar_atributos()
        personagem = Personagem(nome=nome, atributos=atributos)
        return render_template("criar_personagem.html", personagem=personagem, criado=True)

    return render_template("criar_personagem.html", personagem=None, criado=False)

if __name__ == "__main__":
    app.run(debug=False)
