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


@intrago.route("/go/<name>")
def go(name: str):
    site = db.session.query(Site).filter(Site.name == name).first()
    if site is None:
        return render_template("pages/notfound.html", name=name)

    site.accesses += 1
    db.session.commit()
    return redirect(site.url)
