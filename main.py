from flask import Flask, redirect, url_for, request, render_template
import urlshort

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form["linkentry"]
        nurl = urlshort.shorten(url)
        if nurl == "long":
            return render_template("index.html", newlink="Link provided was too long.")
        return render_template("index.html", newlink=f"http://localhost:8496/{nurl}")
    return render_template("index.html", newlink="")

@app.route("/<id>")
def shortlink(id):
    newurl = urlshort.checkid(id)
    if newurl == False:
        return "Not found"
    return redirect(newurl)

if __name__ == "__main__":
    urlshort.createdb()
    app.run(port=8496)