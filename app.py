from flask import *
from flask_cors import CORS
import random
import sqlite3


app = Flask(__name__)
app.secret_key = "nobodyisguessingthisonelmao"

CORS(app)

db = sqlite3.connect("file:database.db?mode=ro", uri=True, check_same_thread=False)
db.row_factory = sqlite3.Row
auth = sqlite3.connect("file:auth.db?mode=ro", uri=True, check_same_thread=False)
auth.row_factory = sqlite3.Row


def template(name, **args):
    return render_template(
        name,
        **args,
        cart=session.get("cart", []),
        weather=random.randint(50, 90),
        fmt_money = lambda cents: f"{'-' if cents < 0 else ''}${abs(cents) / 100:.2f}",
    )


@app.route("/")
def index():
    return template("index.html")


@app.route("/search")
def search():
    query = request.args.get("query")

    cur = db.execute(f"SELECT * FROM books WHERE title LIKE '%{query}%' AND hidden = 0")
    books = cur.fetchall()
    books = list(enumerate(books))

    return template("search.html", results=books, query=query)


@app.route("/book", methods=["POST"])
def book():
    cart = session.get("cart", [])

    req = int(request.form["book"])
    if req in cart:
        cart.remove(req)
    else:
        cart.append(req)

    session["cart"] = cart

    if request.form.get("from") == "cart":
        return redirect("/cart")

    return redirect("/search?query=" + request.form["query"])


def calculate_cart():
    cart = session.get("cart", [])
    cur = db.execute(
        "SELECT * FROM books WHERE id IN ({})".format(", ".join("?" * len(cart))),
        cart,
    )
    books = cur.fetchall()

    prices = {}
    prices["books"] = sum(book["price"] for book in books)
    prices["handling"] = 1000
    prices["shipping"] = 1500
    prices["total"] = sum(prices.values())

    coupon = session.get("coupon")
    if coupon:
        prices["discount"] = -int(prices["total"] * coupon[1] / 100)
        prices["total"] += prices["discount"]

    return books, prices


@app.route("/cart")
def cart():
    books, prices = calculate_cart()
    coupon = session.get("coupon")

    return template("cart.html", results=books, prices=prices, coupon=coupon)


@app.route("/coupon", methods=["POST"])
def coupon():
    coupon = request.form["coupon"]

    cur = db.execute(f"SELECT * FROM coupons WHERE code='{coupon}'")
    coupon = cur.fetchone()

    if coupon:
        session["coupon"] = (coupon["code"], coupon["discount"])
    else:
        flash("The coupon code entered is not valid.", "error")

    return redirect("/cart")


@app.route("/order/justify")
def justify():
    books, prices = calculate_cart()

    if len(books) == 0:
        return redirect("/cart")

    if prices["total"] > 0:
        return redirect("/cart")

    return template("justify.html", results=books, prices=prices)


@app.route("/order/confirm", methods=["GET", "POST"])
def confirm():
    cart = session.get("cart", [])

    if set(session.get("confirmed", [])) == set(cart):
        return template("confirm.html")

    error = 0
    for book_id in cart:
        justification = request.form.get(str(book_id), "")
        if justification == "":
            error = "You must provide a justification for all entries in your order."
            break

        cur = db.execute("SELECT * FROM books WHERE id = (?)", str(book_id))
        book = cur.fetchone()

        if book["justification"] != justification:
            error += 1

    if error == 0:
        session["confirmed"] = list(cart)
        return redirect("/order/confirm")

    if isinstance(error, int):
        flash(f"You have provided incorrect justification for {error} entr{'y' if error == 1 else 'ies'} in your order.")
    else:
        flash(error)

    return redirect("/order/justify")


@app.route("/login", methods=["GET", "POST"])
def admin():
    cart = session.get("cart", [])

    if set(session.get("confirmed", [])) != set(cart):
        return redirect("/")

    if 0 not in cart:
        return redirect("/")

    if request.method == "GET":
        return template("login.html")

    username = request.form["username"]
    password = request.form["password"]

    cur = auth.execute(f"SELECT * FROM users WHERE username = '{username}'")
    res = cur.fetchone()

    if res is None:
        flash("User not found")
        return redirect("/login")

    cur2 = auth.execute("SELECT * FROM users WHERE username = 'admin'")
    res2 = cur2.fetchone()

    if username != res2["username"] or password != res2["password"]:
        flash("Invalid username or password")
        return redirect("/login")

    session["youdidit"] = True
    return redirect("/yay")


@app.route("/yay")
def yay():
    if not session.get("youdidit", False):
        return redirect("/")

    return template("yay.html")


@app.route("/reset")
def reset():
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    app.run("0.0.0.0", threaded=False, debug=False)
