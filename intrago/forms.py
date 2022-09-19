from email.policy import default
from wtforms import Form, StringField, IntegerField, BooleanField, validators


class AddSiteForm(Form):
    name = StringField("Name", [validators.Length(min=1, max=256)])
    url = StringField("URL", [validators.Length(min=1, max=32779)])
    prefixed = BooleanField("Prefixed", default=False)


class DeleteSiteForm(Form):
    id = IntegerField("ID")
