from BookStoreManager import app, db
from BookStoreManager.models import Category, Product, User
from functools import wraps
import json
import os
import hashlib


def read_products(keyword=None, from_price=None, to_price=None, is_latest=False):
    products = Product.query

    if keyword:
        products = products.filter(Product.name.contains(keyword))

    if from_price and to_price:
        products = products.filter(Product.price.__gt__(from_price), Product.price__lt__(to_price))

    if is_latest:
        products = products.order_by(-Product.id)
        return products.all()[:3]

    return products.all()


def read_product_by_id(product_id):
    products = read_products()
    for p in products:
        if p["id"] == product_id:
            return p

    return None


def del_product(product_id):
    products = read_products()

    for idx, p in enumerate(products):
        if p["id"] == product_id:
            del products[idx]
            break

    return update_product_json(products)





def delete_product(product_id):
    products = read_products()
    for idx, p in enumerate(products):
        if p["id"] == int(product_id):
            del products[idx]
            break

    return update_product_json(products)


def update_product(product_id, name, description, price, images, category_id):
    products = read_products()
    for idx, p in enumerate(products):
        if p["id"] == int(product_id):
            products[idx]["name"] = name
            products[idx]["description"] = description
            products[idx]["price"] = float(price)
            products[idx]["images"] = images
            products[idx]["category_id"] = int(category_id)

            break

    return update_json(products)

def read_categories():
    return Category.query.all()


def read_products_by_cate_id(cate_id):
    return Category.query.get(cate_id).products


def load_users():
    with open(os.path.join(app.root_path, "data/users.json"), encoding="utf-8") as f:
        return json.load(f)


def add_user(name, loginname, password):
    user = User(name=name,
                loginname=loginname,
                password=str(hashlib.md5(password.strip().encode("utf-8")).hexdigest()))
    db.session.add(user)
    db.session.commit()

    return user

def check_login(username, password):
    password = str(hashlib.md5(password.strip().encode("utf-8")).hexdigest())
    return User.query.filter(User.username == username,
                             User.password == password).first()


def add_receipt(cart_products=[]):
    try:
        r = Receipt()
        db.session.add(r)
        db.session.commit()

        for p in cart_products:
            d = ReceiptDetail(product_id=p["id"], receipt_id=r.id, unit_price=p["price"], quantity=p["quantity"])
            db.session.add(d)

        db.session.commit()
        return True
    except Exception as ex:
        print(ex)
        return False


def get_user_by_id(user_id):
    return User.query.get(user_id)



def add_product(name,price,category_id,publisher,publishing_year,description,amount):
    pro =  Product(name=name,price=price,category_id= category_id,publisher=publisher,publishing_year=publishing_year,description=description,amount=amount)
    db.session.add(pro)
    db.session.commit()
    return pro


if __name__ == "__main__":
    print(read_products())


