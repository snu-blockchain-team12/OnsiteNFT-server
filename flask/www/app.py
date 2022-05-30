from flask import Flask, render_template, request, redirect, url_for, make_response, jsonify, abort
from flask_cors import CORS

import sys

app = Flask(__name__)
CORS(app, resources={r"*": {"origins": "*"}}, supports_credentials=True)

product_key = ['title','content', 'price', 'link']
product = [\
        ["Test Title1", "Test Content1", "0.01", "1.avi"],\
        ["Test Title2", "Test Content2", "0.02", "2.avi"],\
        ["Test Title3", "Test Content3", "0.02", "3.avi"],\
        ["Test Title4", "Test Content4", "0.02", "4.png"],\
        ["Test Title5", "Test Content5", "0.02", "5.avi"],\
        ["Test Title6", "Test Content3", "0.02", "6.avi"],\
        ["Test Title7", "Test Content4", "0.02", "7.png"],\
        ["Test Title8", "Test Content5", "0.02", "8.png"],\
        ["Test Title9", "no image content", "0.00", "8"],\
        ["Test Title8", "Test Content5", "0.02", "8.png"],\
        ["Test Title8", "Test Content5", "0.02", "8.png"],\
        ["Test Title8", "Test Content5", "0.02", "8.png"],\
        ["Test Title8", "Test Content5", "0.02", "8.png"],\
        ["Test Title8", "Test Content5", "0.02", "8.png"],\
        ["Test Title8", "Test Content5", "0.02", "8.png"],\
        ]

def CORS_response(response):
    new_response = response
    new_response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
    new_response.headers.add('Access-Control-Allow-Credentials', 'true')
    return new_response

@app.route("/register_post", methods=['POST'])
def register_post():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form['content']
        f = request.files['file']
        print(type(f.filename))
        filename = str(len(product)+1) + "." + f.filename.split(".")[-1]
        f.save("./media/"+ filename)
        print(title, content, filename)
        product.append([title, content, "0.01", filename])
        return redirect(url_for("index"))

@app.route("/register")
def register():
    user = request.cookies.get('user')
    if user != "admin":
        return redirect(url_for("index"))
    return render_template("register.html")

@app.route("/login_post", methods=["POST"])
def login_post():
    if request.method == "POST":
        try:
            user = request.json["name"]
            password = request.json["pass"]
        except Exception as e:
            user = request.form["name"]
            password = request.form["pass"]

        is_admin = user == "admin" and password == "admin"
        is_user = user == "user" and password == "user"

        if request.headers['Accept'] == 'application/json':
            resp = jsonify(
                {
                    'success':(is_user or is_admin),
                    'user':(user or ""),
                    'is_user':is_user,
                    'is_admin':is_admin
                }
            )
        else:
            if is_user or is_admin:
                # if login succeed, redirect to /index
                resp = make_response(redirect('/index'))
            else:
                return "<p>Login Error</p>"

        resp.set_cookie("user", user)

        return resp


@app.route("/login")
def login(name=None):
    return render_template('login.html', name=name)

@app.route("/index")
def index():
    user = request.cookies.get('user')
    if user == None:
        return redirect(url_for("login"))
    return render_template("index.html", user=user, product=product)    

@app.route("/products")
def products():
    user = request.cookies.get('user')
    print(request.cookies)

    # client에서 cookie 전송이 안되어 임시로 모든 접근 허용
    # if user == None:
    #     return abort(403)
    resp_json = { "products" : []}
    for raw_product in product:
        p = {
            product_key[0] : raw_product[0],
            product_key[1] : raw_product[1],
            product_key[2] : raw_product[2],
            product_key[3] : raw_product[3],
        }
        resp_json["products"].append(p)
    resp = resp_json
    
    return resp

@app.route("/")
def main():
    user = request.cookies.get('user')
    if user == None:
        return CORS_response(redirect(url_for("login")))
    return CORS_response(redirect(url_for("index")))
