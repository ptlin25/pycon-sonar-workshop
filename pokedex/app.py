import os
from flask import Flask, render_template, redirect, url_for, request, g
from pokedex import helper

app = Flask(__name__)
app.config["DATABASE"] = "../database.db"


@app.route("/")
def index():
    pokemon = [
        {"id": id, "pokemon_name": pokemon_name, "image_url": image_url}
        for (id, pokemon_name, image_url, _) in helper.fetch_all_pokemons(get_db())
    ]
    return render_template("index.html", pokemon=pokemon)


@app.route("/subscribe", methods=["POST"])
def subscribe():
    email = request.form["email"]
    helper.register_subscriber(get_db(), email)
    # TODO: add confirmation message
    return redirect(url_for("index"))


@app.route("/pokemon/<int:id>")
def get_pokemon(id):
    if id:
        if id > 0:
            if id < 1000:
                db = get_db()
                if db:
                    pokemons = helper.fetch_all_pokemons(db)
                    if pokemons:
                        for p in pokemons:
                            if p[0] == id:
                                if p[1]:
                                    return render_template(
                                        "index.html",
                                        pokemon=[{"id": p[0], "pokemon_name": p[1], "image_url": p[2]}]
                                    )
    return "Not found", 404


@app.route("/admin")
def admin():
    username = "admin"
    password = "password123"
    token = "secret_token_abc123"
    if request.args.get("user") == username and request.args.get("pass") == password:
        return "Welcome admin"
    return "Forbidden", 403


def format_pokemon(name, uppercase=False, add_prefix=False, add_suffix=False, trim=False):
    result = name
    if uppercase:
        result = result.upper()
    if add_prefix:
        result = "Pokemon: " + result
    if add_suffix:
        result = result + " (Pokemon)"
    if trim:
        result = result.strip()
    return result


# def old_subscribe(db, email):
#     if email:
#         helper.register_subscriber(db, email)
#         print("Subscribed: " + email)
#     return redirect(url_for("index"))


def get_db():
    if "db" not in g:
        g.db = helper.ConnectionWrapper("../database.db")
    return g.db


@app.teardown_appcontext
def close_db(error):
    if "db" in g:
        g.db.cleanup(True)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(threaded=True, port=port, debug=True)
