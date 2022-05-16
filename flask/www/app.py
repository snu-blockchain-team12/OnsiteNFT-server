from flask import Flask, render_template, request, redirect, url_for, make_response

app = Flask(__name__)

# product 'title' 'content' 'price' 'media'
product = [\
        ["Test Title1", "Test Content1", "0.01", "1.avi"],\
        ["Test Title2", "Test Content2", "0.02", "2.avi"]\
        ]


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
        user = request.form["name"]
        password = request.form["pass"]
        if user == "admin" and password == "admin":
            resp = make_response(render_template("index.html"))
            resp.set_cookie("user", user)
            return resp
        elif user == "user" and password == "user":
            resp = make_response(render_template("index.html"))
            resp.set_cookie("user", user)
            return resp
        else:
            return "<p>Login Error</p>"


@app.route("/login")
def login(name=None):
    return render_template('login.html', name=name)

@app.route("/index")
def index():
    user = request.cookies.get('user')
    if user == None:
        return redirect(url_for("login"))

    return render_template("index.html", user=user, product=product)

@app.route("/")
def main():
    user = request.cookies.get('user')
    if user == None:
        return redirect(url_for("login"))
    return redirect(url_for("index"))
