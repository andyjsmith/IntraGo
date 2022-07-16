from flask import Blueprint, render_template, request, redirect, url_for, flash
from sqlalchemy.exc import IntegrityError

from database import db
from intrago.forms import AddSiteForm, DeleteSiteForm
from intrago.models import Site

api = Blueprint("api", __name__)


@api.route("/site/add", methods=["POST"])
def add_site():
    """Add a new site"""
    form = AddSiteForm(request.form)
    if not form.validate():
        flash("Invalid form data", "danger")
        return redirect(url_for("intrago.index"))

    site = Site(form.name.data, form.url.data)

    db.session.add(site)
    try:
        db.session.commit()
    except IntegrityError:
        # Site with that name already exists
        db.session.rollback()
        flash(f"Site '{form.name.data}' already exists, try another name", "danger")
        return redirect(url_for("intrago.index"))

    flash(f"Added site '{form.name.data}' successfully", "success")
    return redirect(url_for("intrago.index"))


@api.route("/site/delete", methods=["POST"])
def delete_site():
    """Delete a site"""
    form = DeleteSiteForm(request.form)
    if not form.validate():
        flash("Invalid form data", "danger")
        return redirect(url_for("intrago.index"))

    site = db.session.query(Site).filter(Site.id == form.id.data).first()
    if site is None:
        flash("Site not found. It may already be deleted.", "danger")
        return redirect(url_for("intrago.index"))

    db.session.delete(site)
    try:
        db.session.commit()
    except:
        # Site with that name already exists
        db.session.rollback()
        flash(f"Error deleting", "danger")
        return redirect(url_for("intrago.index"))

    flash(f"Deleted site '{site.name}' successfully", "success")
    return redirect(url_for("intrago.index"))
