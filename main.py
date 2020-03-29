from flask import Flask, redirect, url_for, request, render_template
import urlshort

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form["linkentry"]
        customurl = request.form["custom"]
        if customurl == "":
            nurl = urlshort.shorten(url)
        else:
            nurl = urlshort.customlink(customurl, url)
        if nurl == "long":
            return render_template("index.html", newlink="Link provided was too long.")
        if nurl == "taken":
            return render_template("index.html", newlink="The custom link was already taken.")
        if nurl == "illegal":
            return render_template("index.html", newlink="The custom link contains illegal characters (alphanumeric characters only).")
        return render_template("index.html", newlink=nurl)
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