from datetime import datetime
import hashlib
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app, request
from flask.ext.login import UserMixin, AnonymousUserMixin
from .. import db, login_manager
from markdown import markdown
import bleach


class Permission:
    FOLLOW = 0x01
    COMMENT = 0x02
    WRITE_ARTICLES = 0x04
    MODERATE_COMMENTS = 0x08
    ADMINISTER = 0x80


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    @staticmethod
    def insert_roles():
        roles = {
            'User': (Permission.FOLLOW |
                     Permission.COMMENT |
                     Permission.WRITE_ARTICLES, False),
            'Moderator': (Permission.FOLLOW |
                          Permission.COMMENT |
                          Permission.WRITE_ARTICLES |
                          Permission.MODERATE_COMMENTS, False),
            'Administrator': (0xff, True)
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()

    def __repr__(self):
        return '<Role %r>' % self.name

coauthors = db.Table('coauthors',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), index=True),
    db.Column('project_id', db.Integer, db.ForeignKey('projects.id'))
)

copubauthors = db.Table('copubauthors',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), index=True),
    db.Column('publication_id', db.Integer, db.ForeignKey('publications.id'))
)

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)
    name = db.Column(db.String(64), unique=True)
    location = db.Column(db.String(64))
    about_me = db.Column(db.Text())
    about_me_html = db.Column(db.Text())
    quals = db.Column(db.Text())
    quals_html = db.Column(db.Text())
    jobtitle = db.Column(db.String(200))
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)
    avatar_hash = db.Column(db.String(32))
    pub_email = db.Column(db.String(64))
    website = db.Column(db.String(100))
    twitter = db.Column(db.String(64))
    twitter_name = db.Column(db.String(64))
    linkedin = db.Column(db.String(100))
    google = db.Column(db.String(200))
    google_scholar = db.Column(db.String(200))
    research_gate = db.Column(db.String(200))
    tw_confirmed = db.Column(db.Boolean(), default=False)
    tw_widget_id = db.Column(db.String(64))

    posts = db.relationship('Project', backref='researcher', lazy='dynamic')
    bookings = db.relationship('Booking', backref='researcher', lazy='dynamic')
    pages = db.relationship('Page', backref='researcher', lazy='dynamic')
    uploads = db.relationship('Upload', backref='researcher', lazy='dynamic')
    
    # Begin new Database


    @staticmethod
    def generate_fake(count=100):
        from sqlalchemy.exc import IntegrityError
        from random import seed
        import forgery_py

        seed()
        for i in range(count):
            u = User(email=forgery_py.internet.email_address(),
                     username=forgery_py.internet.user_name(True),
                     password=forgery_py.lorem_ipsum.word(),
                     confirmed=True,
                     name=forgery_py.name.full_name(),
                     location=forgery_py.address.city(),
                     about_me=forgery_py.lorem_ipsum.sentence(),
                     member_since=forgery_py.date.date(True))
            db.session.add(u)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['FLASKY_ADMIN']:
                self.role = Role.query.filter_by(permissions=0xff).first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()
        if self.email is not None and self.avatar_hash is None:
            self.avatar_hash = hashlib.md5(
                self.email.encode('utf-8')).hexdigest()

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def generate_reset_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id})

    def reset_password(self, token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('reset') != self.id:
            return False
        self.password = new_password
        db.session.add(self)
        return True

    def generate_email_change_token(self, new_email, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'change_email': self.id, 'new_email': new_email})

    def change_email(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('change_email') != self.id:
            return False
        new_email = data.get('new_email')
        if new_email is None:
            return False
        if self.query.filter_by(email=new_email).first() is not None:
            return False
        self.email = new_email
        self.avatar_hash = hashlib.md5(
            self.email.encode('utf-8')).hexdigest()
        db.session.add(self)
        return True

    def can(self, permissions):
        return self.role is not None and \
            (self.role.permissions & permissions) == permissions

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)

    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)

    def gravatar(self, size=100, default='identicon', rating='g'):
        if request.is_secure:
            url = 'https://secure.gravatar.com/avatar'
        else:
            url = 'http://www.gravatar.com/avatar'
        hash = self.avatar_hash or hashlib.md5(
            self.email.encode('utf-8')).hexdigest()
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
            url=url, hash=hash, size=size, default=default, rating=rating)

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                        'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                        'h3', 'p', 'mark']
        target.about_me_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True))
        target.quals_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True))

    def __repr__(self):
        return self.id


class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False

login_manager.anonymous_user = AnonymousUser
db.event.listen(User.about_me, 'set', User.on_changed_body)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



class Project(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    urlname = db.Column(db.String(15), unique=True)
    full_title = db.Column(db.String(300))
    synopsis = db.Column(db.Text)
    synopsis_html = db.Column(db.Text)
    website = db.Column(db.String(64))
    twitter = db.Column(db.String(64))
    twitter_name = db.Column(db.String(64))
    facebook = db.Column(db.String(64))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    researcher_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    researchers = db.relationship('User', secondary=coauthors, backref=db.backref('projects', lazy='dynamic'))
    other_researchers = db.Column(db.String(200))
    publications = db.relationship('Publication', backref='projects', lazy='dynamic')
    pages = db.relationship('Page', backref='projects', lazy='dynamic')
    tw_confirmed = db.Column(db.Boolean(), default=False)
    tw_widget_id = db.Column(db.String(64))
    active = db.Column(db.Boolean(), default=False)
    image = db.Column(db.String(100))




    @staticmethod
    def generate_fake(count=100):
        from random import seed, randint
        import forgery_py

        seed()
        user_count = User.query.count()
        for i in range(count):
            u = User.query.offset(randint(0, user_count - 1)).first()
            p = Post(body=forgery_py.lorem_ipsum.sentences(randint(1, 5)),
                     timestamp=forgery_py.date.date(True),
                     author=u)
            db.session.add(p)
            db.session.commit()

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                        'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                        'h1', 'h2', 'h3', 'p', 'mark']
        target.synopsis_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True))


db.event.listen(Project.synopsis, 'set', Project.on_changed_body)

class Publication(db.Model):
    __tablename__ = 'publications'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    urlname = db.Column(db.String(15))
    full_title = db.Column(db.String(300))
    synopsis = db.Column(db.Text)
    synopsis_html = db.Column(db.Text)
    website = db.Column(db.String(200))
    twitter = db.Column(db.String(64))
    facebook = db.Column(db.String(64))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    researcher_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    researchers = db.relationship('User', secondary=copubauthors, backref=db.backref('publications', lazy='dynamic')) 
    other_researchers = db.Column(db.String(100))
    project_id = db.Column(db.String(100), db.ForeignKey('projects.id'))
    citation = db.Column(db.Text)
    year_published = db.Column(db.Integer())
    active = db.Column(db.Boolean(), default=False)

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                        'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                        'h1', 'h2', 'h3', 'p', 'mark']
        target.synopsis_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True))

db.event.listen(Publication.synopsis, 'set', Publication.on_changed_body)

class Booking(db.Model):
    __tablename__ = 'bookings'
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.DateTime(), unique=True)
    available = db.Column(db.Boolean)
    researcher_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    description = db.Column(db.Text)



















