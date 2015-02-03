from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, BooleanField, SelectField,\
    SubmitField, IntegerField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import Required, Length, Email, Regexp
from flask.ext.pagedown.fields import PageDownField
from wtforms import ValidationError
from ..models import Role, User, Publication, Project
from markdown import markdown
import bleach

class EditProfileForm(Form):
    name = StringField('Full name', validators=[Length(0, 64)])
    jobtitle = StringField('Your Job Title', validators=[Length(0, 64)])
    location = StringField('Location', validators=[Length(0, 64)])
    about_me = PageDownField('Your Bio', default='Write your bio here, you can use your Exeter profile bio if you wish.')
    quals = PageDownField('Your Qualifications')
    pub_email = StringField('Public Email', validators=[Length(0, 64)])
    website = StringField('Website', validators=[Length(0, 100)])
    twitter = StringField('Twitter Handle (including @) - if none, use @spand_ex', default="@spand_ex", validators=[Length(0, 64), Regexp('(?<=^|(?<=[^a-zA-Z0-9-_\.]))@([A-Za-z]+[A-Za-z0-9]+)', 0, 'Twitter handle must be valid, and include leading @')])
    linkedin = StringField('LinkedIn Profile Full URL', validators=[Length(0, 64)])
    google = StringField('Google Profile Full URL', validators=[Length(0, 64)])
    submit = SubmitField('Submit')
