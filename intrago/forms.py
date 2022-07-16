from wtforms import Form, StringField, IntegerField, validators


class AddSiteForm(Form):
    name = StringField("Name", [validators.Length(min=1, max=256)])
    url = StringField("URL", [validators.Length(min=1, max=32779)])


class DeleteSiteForm(Form):
    id = IntegerField("ID")
