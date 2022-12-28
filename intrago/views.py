from flask import (
    Blueprint,
    render_template,
    redirect,
)
from database import db
from intrago.models import Site

intrago = Blueprint("intrago", __name__, template_folder="templates")


@intrago.route("/")
def index():
    sites = db.session.query(Site).order_by(Site.created.desc()).all()
    return render_template("pages/index.html", sites=sites)


@intrago.route("/go/<path:name>")
def go(name: str):
    # Find regular site
    site = db.session.query(Site).filter(Site.name == name).first()

    if site is None:
        # Check for a prefixed site
        terms = name.split(" ")
        if len(terms) > 1:
            site = db.session.query(Site).filter(Site.name == terms[0]).first()
            if site is None:
                return render_template("pages/notfound.html", name=name)
        else:
            return render_template("pages/notfound.html", name=name)

    url: str = site.url

    if site.prefixed:
        terms = name.split(" ")[1:]

        # Get number of placeholder terms in URL
        placeholder_count = 0
        while True:
            if "{" + str(placeholder_count) + "}" not in url:
                break
            placeholder_count += 1

        # Replace the term placeholders
        for i in range(placeholder_count):
            if i < len(terms):
                if i == placeholder_count - 1:
                    # Last placeholder, combine rest of terms
                    url = url.replace("{" + str(i) + "}", " ".join(terms[i:]))
                else:
                    # Not last placeholder, replace with one term
                    url = url.replace("{" + str(i) + "}", terms[i])
            else:
                # There are no terms left, replace placeholder with empty string
                url = url.replace("{" + str(i) + "}", "")

    site.accesses += 1
    db.session.commit()
    return redirect(url)
