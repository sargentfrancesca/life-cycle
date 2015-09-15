from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, BooleanField, SelectField,\
    SubmitField, IntegerField
from flask.ext.wtf.file import FileField, FileRequired, FileAllowed
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import Required, Length, Email, Regexp
from flask.ext.pagedown.fields import PageDownField
from wtforms import ValidationError
from ..models import Page
from markdown import markdown
import bleach

class PageForm(Form):
    title = StringField('Page Title', validators=[Length(0, 64)])
    content = PageDownField('Page Content')
    publish = BooleanField('Publish Immediately?')
    submit = SubmitField('Submit')
