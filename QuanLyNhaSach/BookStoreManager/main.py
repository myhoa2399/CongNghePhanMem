# from itertools import product

from flask import render_template, request, redirect, url_for, jsonify, send_file, session
from werkzeug.wrappers import json

from BookStoreManager.models import *
from BookStoreManager.decorator import login_required
from flask_login import login_user
from BookStoreManager import app, login, dao, utils
import hashlib
# from saleapp import decorator
# import json
import flask_admin


@app.route("/")
def index():
    return render_template("admin/index.html")


@app.route("/home")
def index1():
    return render_template("index.html")


@app.route("/login-admin", methods=['GET', 'POST'])
def login_admin():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password", "")
        password = str(hashlib.md5(password.strip().encode("utf-8")).hexdigest())
        user = User.query.filter(User.loginname == username.strip(),
                                 User.password == password.strip()).first()
        if user:
            login_user(user=user)
    return redirect("/admin")


@app.route("/signup", methods=["get", "post"])
def register():
    if session.get("user"):
        return redirect(request.url)

    err_msg = ""
    if request.method == "POST":
        name = request.form.get("name")
        loginname = request.form.get("loginname")
        password = request.form.get("password")
        confirm = request.form.get("confirm")
        if password.strip() != confirm.strip():
            err_msg = "Mat khau khong khop"
        else:
            if dao.add_user(name=name, loginname=loginname, password=password):
                return redirect(url_for("login_admin"))
            else:
                err_msg = "Something Wrong!!!"

    return render_template("signin.html", err_msg=err_msg)


@app.route("/products")
def product_list():
    keyword = request.args["keyword"] if request.args.get("keyword") else None

    return render_template("product-list.html", products=dao.read_products(keyword=keyword))


@app.route("/products/detail/<int:product_id>")
def product_detail(product_id):
    return render_template("product-detail.html")


@app.route("/products/<int:category_id>")
def product_list_by_cate(category_id):
    return render_template("product-list.html", products=dao.read_products_by_cate_id(cate_id=category_id))


@app.route("/api/products/<int:product_id>", methods=["delete"])
def delete_product(product_id):
    if dao.delete_product(product_id=product_id):
        return jsonify({"status": 200, "product_id": product_id})

    return jsonify({"status": 500, "error_message": "Something Wrong!!!"})


@app.route("/cart", methods=['get', 'post'])
@login_required
def cart():
    err_msg = ""
    if request.method == 'POST':
        if 'cart' in session and session['cart']:
            if dao.add_receipt(cart_products=session["cart"].values()):
                session['cart'] = None
                return redirect(url_for('cart'))
            else:
                err_msg = "Add receipt failed"
        else:
            err_msg = "No products in cart"

    return render_template("payment.html", err_msg=err_msg)


@app.route("/products/add", methods=["get", "post"])
@login_required
def add_product():
    """
    add: /products/add
    update: /products/add?product_id
    :return: template

    """
    if session.get("product"):
        return redirect(request.url)

    err_msg = ""
    if request.method == "POST":
        name = request.form.get("name")
        price = request.form.get("price")
        category_id = request.form.get("category_id", 1)
        publisher = request.form.get("publisher")
        publishing_year = request.form.get("publishing_year")
        description = request.form.get("description")
        amount = (int)(request.form.get("amount"))
        if amount < 150:
            err_msg = "Amount must be bigger than 150!"
        else:
            if dao.add_product(name=name, price=price, category_id=category_id, publisher=publisher,
                               publishing_year=publishing_year, description=description, amount=amount):
                return redirect(url_for("product-list.html"))
            else:
                err_msg = "ERROR"
    categories = dao.read_categories()
    product = None
    if request.args.get("product_id"):
        product = dao.read_product_by_id(product_id=int(request.args["product_id"]))

    return render_template("product-add.html", categories=categories, product=product, err_msg=err_msg)


@app.route("/products/export")
def export_product():
    p = utils.export()

    return send_file(filename_or_fp=p)


@app.route("/api/cart", methods=["post"])
def add_to_cart():
    data = request.data
    product_id = data.get("id")
    name = data.get("name")
    price = data.get("price")
    if "cart" not in session or session['cart'] == None:
        session["cart"] = {}

    cart = session["cart"]

    product_key = str(product_id)
    if product_key in cart:  # đa từng bỏ sản phẩm product_id vào giỏ
        cart[product_key]["quantity"] = cart[product_key]["quantity"] + 1
    else:  # bỏ sản phẩm mới vào giỏ
        cart[product_key] = {
            "id": product_id,
            "name": name,
            "price": price,
            "quantity": 1
        }

    session["cart"] = cart
    q = 0
    s = 0
    for c in list(session["cart"].values()):
        q = q + c['quantity']
        s = s + c['quantity'] * c['price']

    return jsonify({"success": 1, "quantity": q, 'sum': s})


@app.context_processor
def append_cate():
    common = {
        "categories": dao.read_categories()
    }

    if 'cart' in session and session['cart']:
        q = 0
        s = 0
        for c in list(session["cart"].values()):
            q = q + c['quantity']
            s = s + c['quantity'] * c['price']

        common['cart_quantity'] = q
        common['cart_price'] = s

    return common


@app.route("/logout")
def logout():
    logout_user()

    return redirect(url_for("login_admin"))


@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
