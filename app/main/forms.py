from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, BooleanField, SelectField,\
    SubmitField, IntegerField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import Required, Length, Email, Regexp
from wtforms import ValidationError
from ..models import Role, User, Publication, Project

class EditProfileForm(Form):
    name = StringField('Full name', validators=[Length(0, 64)])
    jobtitle = StringField('Your Job Title', validators=[Length(0, 64)])
    location = StringField('Location', validators=[Length(0, 64)])
    about_me = TextAreaField('Your Bio', default='Write your bio here, you can use your Exeter profile bio if you wish.')
    quals = TextAreaField('Your Qualifications')
    pub_email = StringField('Public Email', validators=[Length(0, 64)])
    website = StringField('Website', validators=[Length(0, 50)])
    twitter = StringField('Twitter Handle', default="@", validators=[Length(0, 64), Regexp('(?<=^|(?<=[^a-zA-Z0-9-_\.]))@([A-Za-z]+[A-Za-z0-9]+)', 0, 'Twitter handle must be valid, and include leading @')])
    linkedin = StringField('LinkedIn Profile', validators=[Length(0, 64)])
    google = StringField('Google Profile', validators=[Length(0, 64)])
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
    about_me = TextAreaField('About me')
    quals = TextAreaField('Your Qualifications')
    pub_email = StringField('Public Email', validators=[Length(0, 64)])
    website = StringField('Website', validators=[Length(0, 50)])
    twitter = StringField('Twitter Handle (including @)', default='@', validators=[Length(0, 64), Regexp('(?<=^|(?<=[^a-zA-Z0-9-_\.]))@([A-Za-z]+[A-Za-z0-9]+)', 0, 'Twitter handle must be valid, and include leading @')])
    linkedin = StringField('LinkedIn Profile', validators=[Length(0, 64)])
    google = StringField('Google Profile', validators=[Length(0, 64)])
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
    title = StringField('Project Title', default="Brief title for display purposes, for example Demography or Lobsters, max 20 letters", validators=[Required(), Length(0,20)])
    urlname = StringField('Url Name', default="One word, lowercase descriptor for the project URL", validators=[Required(), Length(0,15), Regexp('^[a-z]+$', 0,
                                          'Lowercase letters only')])
    full_title = StringField('Project Full Title', validators=[Length(0,300)])
    brief_synopsis = TextAreaField('Brief Synopsis', default="Quick synopsis of project, summed up in around 100 words for quick reference", validators=[Required()])
    synopsis = TextAreaField("Full Synopsis of project")
    website = StringField('Project Website', validators=[Length(0,64)])
    twitter = StringField('Project Twitter Handle', default="@", validators=[Length(0,64), Regexp('(?<=^|(?<=[^a-zA-Z0-9-_\.]))@([A-Za-z]+[A-Za-z0-9]+)', 0, 'Twitter handle must be valid, and include leading @')])
    facebook = StringField('Project Facebook', validators=[Length(0,64)])
    submit = SubmitField('Submit')


class ProjectEditForm(Form):
    title = StringField('Project Title', default="Brief title for display purposes, for example Demography or Lobsters, max 20 letters", validators=[Required(), Length(0,20)])
    urlname = StringField('Url Name', default="One word descriptor for the project URL", validators=[Required(), Length(0,100), Regexp('^[a-z]+$', 0,
                                          'Lowercase letters only')])
    full_title = StringField('Project Full Title', validators=[Length(0,300)])
    brief_synopsis = TextAreaField('Brief Synopsis', default="Quick synopsis of project, summed up in around 100 words for quick reference", validators=[Required()])
    synopsis = TextAreaField("Full Synopsis of project")
    website = StringField('Project Website', validators=[Length(0,64)])
    twitter = StringField('Project Twitter Handle', validators=[Length(0,64), Regexp('(?<=^|(?<=[^a-zA-Z0-9-_\.]))@([A-Za-z]+[A-Za-z0-9]+)', 0, 'Twitter handle must be valid, and include leading @')])
    facebook = StringField('Project Facebook', validators=[Length(0,64)])
    submit = SubmitField('Submit')


class PublicationPostForm(Form):
    title = StringField('Publication Title', default="Brief title for display purposes, for example Demography or Lobsters, max 20 letters", validators=[Required(), Length(0,20)])
    urlname = StringField('Url Name', default="One word descriptor for the project URL", validators=[Required(), Length(0,15), Regexp('^[a-z]+$', 0,
                                          'Lowercase letters only')])
    full_title = StringField('Publication Full Title', validators=[Length(0,300)])
    brief_synopsis = TextAreaField('Brief Synopsis', default="Quick synopsis of project, summed up in around 100 words for quick reference", validators=[Required()])
    synopsis = TextAreaField("Full Synopsis of publication")
    website = StringField('Publication Website', validators=[Length(0,64)])
    citation = StringField('Citation')
    project_name = StringField('Project Associated')
    submit = SubmitField('Submit')

class PublicationEditForm(Form):
    title = StringField('Publication Title', default="Brief title for display purposes, for example Demography or Lobsters, max 20 letters", validators=[Required(), Length(0,20)])
    urlname = StringField('Url Name', default="One word descriptor for the project URL", validators=[Required(), Length(0,15), Regexp('^[a-z]+$', 0,
                                          'Lowercase letters only')])
    full_title = StringField('Publication Full Title', validators=[Length(0,300)])
    brief_synopsis = TextAreaField('Brief Synopsis', default="Quick synopsis of project, summed up in around 100 words for quick reference", validators=[Required()])
    synopsis = TextAreaField("Full Synopsis of publication")
    website = StringField('Publication Website', validators=[Length(0,64)])
    citation = StringField('Citation')
    project_name = StringField('Project Associated')
    submit = SubmitField('Submit')
