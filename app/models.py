from datetime import datetime
import hashlib
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app, request
from flask.ext.login import UserMixin, AnonymousUserMixin
from . import db, login_manager
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
    db.Column('user_name', db.String(64), db.ForeignKey('users.name')),
    db.Column('project_id', db.Integer, db.ForeignKey('projects.id'))
)

copubauthors = db.Table('copubauthors',
    db.Column('user_name', db.String(64), db.ForeignKey('users.name')),
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
    jobtitle = db.Column(db.String(64))
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)
    avatar_hash = db.Column(db.String(32))
    pub_email = db.Column(db.String(64))
    website = db.Column(db.String(100))
    twitter = db.Column(db.String(64))
    twitter_name = db.Column(db.String(64))
    linkedin = db.Column(db.String(64))
    google = db.Column(db.String(64))
    tw_confirmed = db.Column(db.Boolean(), default=False)
    tw_widget_id = db.Column(db.String(64))

    posts = db.relationship('Project', backref='researcher', lazy='dynamic')
    pages = db.relationship('Page', backref='researcher', lazy='dynamic')
    uploads = db.relationship('Upload', backref='researcher', lazy='dynamic')


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
        return '<User %r>' % self.username


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
    brief_synopsis = db.Column(db.Text)
    synopsis = db.Column(db.Text)
    synopsis_html = db.Column(db.Text)
    website = db.Column(db.String(64))
    twitter = db.Column(db.String(64))
    twitter_name = db.Column(db.String(64))
    facebook = db.Column(db.String(64))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    researcher_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    researchers = db.relationship('User', secondary=coauthors, backref=db.backref('projects', lazy='dynamic'))
    other_researchers = db.Column(db.String(100))
    publications = db.relationship('Publication', backref='projects', lazy='dynamic')
    pages = db.relationship('Page', backref='projects', lazy='dynamic')
    tw_confirmed = db.Column(db.Boolean(), default=False)
    tw_widget_id = db.Column(db.String(64))
    status = db.Column(db.Boolean(), default=False)




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
    brief_synopsis = db.Column(db.Text)
    synopsis = db.Column(db.Text)
    synopsis_html = db.Column(db.Text)
    website = db.Column(db.String(64))
    twitter = db.Column(db.String(64))
    facebook = db.Column(db.String(64))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    researcher_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    researchers = db.relationship('User', secondary=copubauthors, backref=db.backref('publications', lazy='dynamic')) 
    other_researchers = db.Column(db.String(100))
    project_id = db.Column(db.String(100), db.ForeignKey('roles.name'))
    project_name = db.Column(db.String(100), db.ForeignKey('projects.urlname'))
    citation = db.Column(db.Text)
    status = db.Column(db.Boolean(), default=False)

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                        'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                        'h1', 'h2', 'h3', 'p', 'mark']
        target.synopsis_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True))

db.event.listen(Publication.synopsis, 'set', Publication.on_changed_body)

class Plant(db.Model):
    __tablename__ = 'plant'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    matrixnumber = db.Column(db.Integer, unique=True, index=True)
    matrix = db.Column(db.Text)
    dimension = db.Column(db.Integer)
    matrixclassnumber = db.Column(db.Integer)
    matrixclassorganised = db.Column(db.String(64))
    matrixsplit = db.Column(db.String(64))
    classnames = db.Column(db.Text)
    observation = db.Column(db.String(250))
    matrixcomposite = db.Column(db.String(64))
    matrixtreatment = db.Column(db.String(84))
    matrixcaptivity = db.Column(db.String(10))
    matrixstartyear = db.Column(db.Integer)
    matrixstartseason = db.Column(db.String(10))
    matrixstartmonth = db.Column(db.Integer)
    matrixendyear = db.Column(db.Integer)
    matrixendseason = db.Column(db.Integer)
    matrixendmonth = db.Column(db.String(16))
    studiedsex = db.Column(db.String(4))
    population = db.Column(db.String(64))
    latdeg = db.Column(db.Integer)
    latmin = db.Column(db.Integer)
    latsec = db.Column(db.Integer)
    londeg = db.Column(db.Integer)
    lonmin = db.Column(db.Integer)
    lonsec = db.Column(db.Integer)
    latitudedec = db.Column(db.Integer)
    longitudedec = db.Column(db.Integer)
    altitude = db.Column(db.Integer)
    country = db.Column(db.String(64))
    continent = db.Column(db.String(64))
    criteriasize = db.Column(db.String(64))
    criteriaontogeny = db.Column(db.String(64))
    authors = db.Column(db.String(64))
    journal = db.Column(db.String(64))
    yearpublication = db.Column(db.Integer)
    doiisbn = db.Column(db.String(64))
    additionalsource = db.Column(db.String(200))
    enteredby = db.Column(db.String(64))
    entereddate = db.Column(db.String(64))
    source = db.Column(db.String(100))
    statusstudy = db.Column(db.String(64))
    statusstudyref = db.Column(db.String(64))
    statuselsewhere = db.Column(db.String(64))
    statuselsewhereref = db.Column(db.String(64))

    species_id = db.Column(db.Integer, db.ForeignKey("species.id"))

    def __init__(self, name, matrixnumber, matrix, dimension, matrixclassnumber, matrixclassorganised, matrixsplit, classnames, observation, matrixcomposite, matrixtreatment, matrixcaptivity, matrixstartyear, matrixstartseason, matrixstartmonth, matrixendyear, matrixendseason, matrixendmonth, studiedsex, population, latdeg, latmin, latsec, londeg, lonmin, lonsec, latitudedec, longitudedec, altitude, country, continent, criteriasize, criteriaontogeny, authors, journal, yearpublication, doiisbn, additionalsource, enteredby, entereddate, source, statusstudy, statusstudyref, statuselsewhere, statuselsewhereref):
        """"""
        self.name = name
        self.matrixnumber = matrixnumber
        self.matrix = matrix
        self.dimension = dimension
        self.matrixclassnumber = matrixclassnumber
        self.matrixclassorganised = matrixclassorganised
        self.matrixsplit = matrixsplit
        self.classnames = classnames
        self.observation = observation
        self.matrixcomposite = matrixcomposite
        self.matrixtreatment = matrixtreatment
        self.matrixcaptivity = matrixcaptivity
        self.matrixstartyear = matrixstartyear
        self.matrixstartseason = matrixstartseason
        self.matrixstartmonth = matrixstartmonth
        self.matrixendyear = matrixendyear
        self.matrixendseason = matrixendseason
        self.matrixendmonth = matrixendmonth
        self.studiedsex = studiedsex
        self.population = population
        self.latdeg = latdeg
        self.latmin = latmin
        self.latsec = latsec
        self.londeg = londeg
        self.lonmin = lonmin
        self.lonsec = lonsec
        self.latitudedec = latitudedec
        self.longitudedec = longitudedec
        self.altitude = altitude
        self.country = country
        self.continent = continent
        self.criteriasize = criteriasize
        self.criteriaontogeny = criteriaontogeny
        self.authors = authors
        self.journal = journal
        self.yearpublication = yearpublication
        self.doiisbn = doiisbn
        additionalsource = additionalsource
        self.enteredby = enteredby
        self.entereddate = entereddate
        self.source = source
        self.statusstudy = statusstudy
        self.statusstudyref = statusstudyref
        self.statuselsewhere = statuselsewhere
        self.statuselsewhereref = statuselsewhereref


    def __repr__(self):
        return '<Plant %r>' % self.matrixnumber
    

class Species(db.Model):
    __tablename__ = 'species'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    speciesauthor = db.Column(db.String(64))
    kingdom = db.Column(db.String(64))
    phylum = db.Column(db.String(64))
    angiogymno = db.Column(db.String(64))
    dicotmonoc = db.Column(db.String(64))
    _class = db.Column(db.String(64))
    _order = db.Column(db.String(64))
    family = db.Column(db.String(64))
    genus = db.Column(db.String(64))
    ecoregion = db.Column(db.String(64))
    growthtype = db.Column(db.String(64))
    growthformraunkiaer = db.Column(db.String(64))
    annualperiodicity = db.Column(db.String(64))
    planttype = db.Column(db.String(64))
    commonname = db.Column(db.String(64))
    originalimageurl = db.Column(db.String(64))
    localimageurl = db.Column(db.String(64))
    originalpageurl = db.Column(db.String(200))

    plants = db.relationship("Plant", backref="species")

    def __init__(self, name, speciesauthor, kingdom, phylum, angiogymno, dicotmonoc, _class, _order, family, genus, ecoregion, growthtype, growthformraunkiaer, annualperiodicity, planttype, commonname, originalimageurl):
        """"""
        self.name = name
        self.speciesauthor = speciesauthor
        self.kingdom = kingdom
        self.phylum = phylum
        self.angiogymno = angiogymno
        self.dicotmonoc = dicotmonoc
        self._class = _class
        self._order = _order
        self.family = family
        self.genus = genus
        self.ecoregion = ecoregion
        self.growthtype = growthtype
        self.growthformraunkiaer = growthformraunkiaer
        self.annualperiodicity = annualperiodicity
        self.planttype = planttype
        self.commonname = commonname
        self.originalimageurl = originalimageurl
        self.localimageurl = localimageurl
        self.originalpageurl = originalpageurl

    def __repr__(self):
        return '<Species %r>' % self.name

class Page(db.Model):
    __tablename__ = 'page'
    id = db.Column(db.Integer, primary_key=True, index=True)
    pagetype = db.Column(db.String(64))
    title = db.Column(db.String(64))
    publish = db.Column(db.Boolean)
    content = db.Column(db.Text())
    content_html = db.Column(db.Text())
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    project_name = db.Column(db.String(100), db.ForeignKey('projects.urlname'))
    image_url = db.Column(db.String(100), db.ForeignKey('uploads.filename'))

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                        'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                        'h1', 'h2', 'h3', 'p', 'mark', 'strong']
        target.content_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True))


db.event.listen(Page.content, 'set', Page.on_changed_body)

class Upload(db.Model):
    __tablename__ = 'uploads'
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(64))
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    page = db.relationship('Page', backref='uploads', lazy='dynamic')



















