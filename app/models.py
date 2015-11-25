from datetime import datetime
import hashlib
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app, request
from flask.ext.login import UserMixin, AnonymousUserMixin
from . import db, login_manager
from markdown import markdown
import bleach

class Plant(db.Model):
    __tablename__ = 'plant'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    matrixnumber = db.Column(db.Integer, unique=True, index=True)
    matrix_a = db.Column(db.Text)
    matrix_u = db.Column(db.Text)
    matrix_f = db.Column(db.Text)
    matrix_c = db.Column(db.Text)
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
    matrixstartmonth = db.Column(db.String(64))
    matrixendyear = db.Column(db.String(64))
    matrixendseason = db.Column(db.String(64))
    matrixendmonth = db.Column(db.String(16))
    matrixfec = db.Column(db.String(64))
    studiedsex = db.Column(db.String(4))
    population = db.Column(db.String(64))
    ecoregion = db.Column(db.String(64))
    latdeg = db.Column(db.Integer)
    latmin = db.Column(db.Integer)
    latsec = db.Column(db.Integer)
    latns = db.Column(db.String(64))
    londeg = db.Column(db.Integer)
    lonmin = db.Column(db.Integer)
    lonsec = db.Column(db.Integer)
    lonwe = db.Column(db.String(64))
    latitudedec = db.Column(db.Integer)
    longitudedec = db.Column(db.Integer)
    annualperiodicity = db.Column(db.String(64))
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


    def __repr__(self):
        return '<Plant %r>' % self.id
    

class Species(db.Model):
    __tablename__ = 'species'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    speciesauthor = db.Column(db.String(64))
    authority = db.Column(db.Text())
    taxonomy = db.Column(db.String(64))
    tplversion = db.Column(db.String(64))
    intraspecificaccepted = db.Column(db.String(64))
    speciesepithetaccepted = db.Column(db.String(64))
    genusaccepted = db.Column(db.String(64))
    kingdom = db.Column(db.String(64))
    phylum = db.Column(db.String(64))
    angiogymno = db.Column(db.String(64))
    dicotmonoc = db.Column(db.String(64))
    _class = db.Column(db.String(64))
    _order = db.Column(db.String(64))
    family = db.Column(db.String(64))
    genus = db.Column(db.String(64))
    growthtype = db.Column(db.String(64))    
    planttype = db.Column(db.String(64))
    commonname = db.Column(db.String(64))
    originalimageurl = db.Column(db.String(64))
    localimageurl = db.Column(db.String(64))
    originalpageurl = db.Column(db.String(200))

    plants = db.relationship("Plant", backref="species")

    def __repr__(self):
        return '<Species %r>' % self.name

class OldPlant(db.Model):
    __tablename__ = 'oldplant'
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

    species_id = db.Column(db.Integer, db.ForeignKey("oldspecies.id"))

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
        return '<OldPlant %r>' % self.matrixnumber
    

class OldSpecies(db.Model):
    __tablename__ = 'oldspecies'
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

    plants = db.relationship("OldPlant", backref="species")

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
        return '<OldSpecies %r>' % self.name

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



# Begin new Database trial 

class TheSpecies (db.Model):
    __tablename__ = 'thespecies'
    id = db.Column(db.Integer, primary_key=True)
    species = db.Column(db.String(64), index=True)
    subspecies = db.Column(db.String(64))
    family = db.Column(db.String(64))
    tax_order = db.Column(db.String(64))
    iucn_status = db.Column(db.Enum('EX', 'EW', 'CR', 'EN', 'VU', 'NT', 'LC', 'DD', 'NE', 'LR/cd', 'LR/nt', 'LR/lc', name='categories'))
    esa_status = db.Column(db.Enum('EN', 'TH', 'NL', name='categories'))
    invasive_status = db.Column(db.Boolean())
    user_created = db.Column(db.Integer, db.ForeignKey('users.id'))
    user_modified = db.Column(db.Integer, db.ForeignKey('users.id'))
    timestamp_created = db.Column(db.DateTime, default=datetime.utcnow)
    timestamp_modified = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<Species %r>' % self.id



















