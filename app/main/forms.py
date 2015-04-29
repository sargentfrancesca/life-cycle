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
    jobtitle = StringField('Your Job Title', validators=[Length(0, 200)])
    location = StringField('Location', validators=[Length(0, 64)])
    about_me = PageDownField('Your Bio', default='Write your bio here, you can use your Exeter profile bio if you wish.')
    quals = PageDownField('Your Qualifications')
    pub_email = StringField('Public Email', validators=[Length(0, 64)])
    website = StringField('Website', validators=[Length(0, 100)])
    twitter = StringField('Twitter Handle (including @) - if none, use @spand_ex', default="@spand_ex", validators=[Length(0, 64), Regexp('(?<=^|(?<=[^a-zA-Z0-9-_\.]))@([A-Za-z]+[A-Za-z0-9]+)', 0, 'Twitter handle must be valid, and include leading @')])
    linkedin = StringField('LinkedIn Profile Full URL', validators=[Length(0, 64)])
    google = StringField('Google Profile Full URL', validators=[Length(0, 200)])
    submit = SubmitField('Submit')


class EditProfileAdminForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64),
                                             Email()])
    username = StringField('Username', validators=[
        Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                          'Usernames must have only letters, '
                                          'numbers, dots or underscores')])
    confirmed = BooleanField('Confirmed')
    role = SelectField('Role', coerce=int)
    name = StringField('Full name', validators=[Length(0, 64)])
    jobtitle = StringField('Your Job Title', validators=[Length(0, 64)])
    location = StringField('Location', validators=[Length(0, 64)])
    about_me = PageDownField('Your Bio')
    quals = PageDownField('Your Qualifications')
    pub_email = StringField('Public Email', validators=[Length(0, 64)])
    website = StringField('Website', validators=[Length(0, 100)])
    twitter = StringField('Twitter Handle (including @) - if none, use @spand_ex', default='@', validators=[Length(0, 64), Regexp('(?<=^|(?<=[^a-zA-Z0-9-_\.]))@([A-Za-z]+[A-Za-z0-9]+)', 0, 'Twitter handle must be valid, and include leading @')])
    linkedin = StringField('LinkedIn Profile Full URL', validators=[Length(0, 64)])
    google = StringField('Google Profile Full URL', validators=[Length(0, 64)])
    tw_widget_id = StringField('Twitter Widget Data ID', validators=[Length(0,64)])
    tw_confirmed = BooleanField('Twitter Widget Generated')
    submit = SubmitField('Submit')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name)
                             for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and \
                User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if field.data != self.user.username and \
                User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')


class ProjectPostForm(Form):
    title = StringField('Project Title', default="Brief one-word title for display purposes, for example Demography or Lobsters, max 20 letters", validators=[Required(), Length(0,20)])
    urlname = StringField('Web Address Name', default="One word, lowercase descriptor for the project address, for example demography or lobsters", validators=[Required(), Length(0,15), Regexp('^[a-z]+$', 0,
                                          'Lowercase letters only')])
    full_title = StringField('Project Full Title', validators=[Length(0,300)])
    brief_synopsis = TextAreaField('Brief Synopsis', default="Quick synopsis of project, summed up in around 100 words for quick reference")
    synopsis = PageDownField("Full Synopsis of project")
    website = StringField('Project Website', validators=[Length(0,64)])
    twitter = StringField('Project Twitter Handle (including @) - if none, use @spand_ex', default="@spand_ex", validators=[Length(0,64), Regexp('(?<=^|(?<=[^a-zA-Z0-9-_\.]))@([A-Za-z]+[A-Za-z0-9]+)', 0, 'Twitter handle must be valid, and include leading @')])
    facebook = StringField('Project Facebook', validators=[Length(0,64)])
    submit = SubmitField('Submit')


class ProjectEditForm(Form):
    title = StringField('Page Title', default="Brief one-word title for display purposes, for example Demography or Lobsters, max 20 letters", validators=[Required(), Length(0,20)])
    urlname = StringField('Web Address Name', default="One word descriptor for the project address, for example demography or lobsters", validators=[Required(), Length(0,100), Regexp('^[a-z]+$', 0,
                                          'Lowercase letters only')])
    full_title = StringField('Project Full Title', validators=[Length(0,300)])
    brief_synopsis = TextAreaField('Brief Synopsis', default="Quick synopsis of project, summed up in around 100 words for quick reference")
    synopsis = PageDownField("Full Synopsis of project")
    website = StringField('Project Website', validators=[Length(0,64)])
    twitter = StringField('Project Twitter Handle (including @) - if none, use @spand_ex', validators=[Length(0,64), Regexp('(?<=^|(?<=[^a-zA-Z0-9-_\.]))@([A-Za-z]+[A-Za-z0-9]+)', 0, 'Twitter handle must be valid, and include leading @')])
    facebook = StringField('Project Facebook', validators=[Length(0,64)])
    other_researchers = StringField('Other Researchers involved (not part of SPANDEX/yet)', validators=[Length(0,100)])
    submit = SubmitField('Submit')

class ProjectEditFormAdmin(Form):
    title = StringField('Page Title', default="Brief one-word title for display purposes, for example Demography or Lobsters, max 20 letters", validators=[Required(), Length(0,20)])
    urlname = StringField('Web Address Name', default="One word descriptor for the project address, for example demography or lobsters", validators=[Required(), Length(0,100), Regexp('^[a-z]+$', 0,
                                          'Lowercase letters only')])
    full_title = StringField('Project Full Title', validators=[Length(0,300)])
    brief_synopsis = TextAreaField('Brief Synopsis', default="Quick synopsis of project, summed up in around 100 words for quick reference")
    synopsis = PageDownField("Full Synopsis of project")
    website = StringField('Project Website', validators=[Length(0,64)])
    twitter = StringField('Project Twitter Handle (including @) - if none, use @spand_ex', validators=[Length(0,64), Regexp('(?<=^|(?<=[^a-zA-Z0-9-_\.]))@([A-Za-z]+[A-Za-z0-9]+)', 0, 'Twitter handle must be valid, and include leading @')])
    facebook = StringField('Project Facebook', validators=[Length(0,64)])
    other_researchers = StringField('Other Researchers involved (not part of SPANDEX/yet)', validators=[Length(0,100)])
    submit = SubmitField('Submit')


class PublicationPostForm(Form):
    title = StringField('Page Title', default="Brief one-word title for display purposes, for example Demography or Lobsters, max 20 letters", validators=[Required(), Length(0,20)])
    urlname = StringField('Web Address Name', default="One word descriptor for the project address, for example demography or lobsters", validators=[Required(), Length(0,15), Regexp('^[a-z]+$', 0,
                                          'Lowercase letters only')])
    full_title = StringField('Publication Full Title', validators=[Length(0,300)])
    brief_synopsis = TextAreaField('Brief Synopsis', default="Quick synopsis of project, summed up in around 100 words for quick reference")
    synopsis = PageDownField("Full Synopsis of publication")
    website = StringField('Publication Website', validators=[Length(0,200)])
    citation = StringField('Citation')
    submit = SubmitField('Submit')

class PublicationEditForm(Form):
    title = StringField('Page Title', default="Brief one-word title for display purposes, for example Demography or Lobsters, max 20 letters", validators=[Required(), Length(0,20)])
    urlname = StringField('Web Address Name', default="One word descriptor for the project address, for example demography or lobsters", validators=[Required(), Length(0,15), Regexp('^[a-z]+$', 0,
                                          'Lowercase letters only')])
    full_title = StringField('Publication Full Title', validators=[Length(0,300)])
    brief_synopsis = TextAreaField('Brief Synopsis', default="Quick synopsis of project, summed up in around 100 words for quick reference")
    synopsis = PageDownField("Full Synopsis of publication")
    website = StringField('Publication Website', validators=[Length(0,200)])
    citation = StringField('Citation')
    other_researchers = StringField('Other Researchers involved (not part of SPANDEX/yet)', validators=[Length(0,100)])
    submit = SubmitField('Submit')
