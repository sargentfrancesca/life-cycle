from datetime import datetime
import hashlib
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app, request
from flask.ext.login import UserMixin, AnonymousUserMixin
from . import db, login_manager
from markdown import markdown
import bleach


''' TODO: Stuff with arbitrary data - use methods to enter data (such as ecoregions), run these when deploying or setting up system '''
''' We will add a method to the matrix model to generate the unique ID, as designed by Danny, once we have decided the best protocol '''
''' Talk about enum (meta data within columns) vs meta tables '''

''' Meta tables '''
''' Meta Tables for Species '''
class IUCNStatus(db.Model):
	__tablename__ = 'iucn_status'
	id = db.Column(db.Integer, primary_key=True)
	status_code = db.Column(db.String(64), index=True)
	status_name = db.Column(db.String(64))
	status_description = db.Column(db.Text())

	species = db.relationship("Species", backref="iucn_status")

	def __repr__(self):
        return '<IUCN Status %r>' % self.status_code

class ESAStatus(db.Model):
	__tablename__ = 'esa_status'
	id = db.Column(db.Integer, primary_key=True)
	status_code = db.Column(db.String(64), index=True)
	status_name = db.Column(db.String(64))
	status_description = db.Column(db.Text())

	species = db.relationship("Species", backref="esa_status")

	def __repr__(self):
        return '<ESA Status %r>' % self.status_code
''' End Meta Tables for Species '''

''' Meta Tables for Plant Traits '''
class GrowthType(db.Model):
	__tablename__ = 'growth_types'
	id = db.Column(db.Integer, primary_key=True)
	type_name = db.Column(db.String(64), index=True)

	plant_traits = db.relationship("PlantTrait", backref="growth_type")

	def __repr__(self):
        return '<Growth Type %r>' % self.type_name

class GrowthFormRaunkiaer(db.Model):
	__tablename__ = 'growth_forms_raunkiaer'
	id = db.Column(db.Integer, primary_key=True)
	form_name = db.Column(db.Text(), index=True)

	plant_traits = db.relationship("PlantTrait", backref="growth_form_raunkiaer")

	def __repr__(self):
        return '<Growth Form Raunkiaer %r>' % self.form_name

class ReproductiveRepetition(db.Model):
	__tablename__ = 'reproductive_repetition'
	id = db.Column(db.Integer, primary_key=True)
	repetition_name = db.Column(db.Text(), index=True)

	plant_traits = db.relationship("PlantTrait", backref="reproductive_repetition")

	def __repr__(self):
        return '<Growth Form Raunkiaer %r>' % self.repetiton_name

class DicotMonoc(db.Model):
	__tablename__ = 'reproductive_repetition'
	id = db.Column(db.Integer, primary_key=True)
	dicot_monoc_name = db.Column(db.String(64), index=True)

	plant_traits = db.relationship("PlantTrait", backref="dicot_monoc")

	def __repr__(self):
        return '<Dicot Monoc %r>' % self.dicot_monoc_name

class AngioGymno(db.Model):
	__tablename__ = 'angio_gymno'
	id = db.Column(db.Integer, primary_key=True)
	angio_gymno_name = db.Column(db.String(64), index=True)

	plant_traits = db.relationship("PlantTrait", backref="angio_gymno")

	def __repr__(self):
        return '<Angio Gymno %r>' % self.angio_gymno
''' End Meta Tables for Plant Traits '''

''' Meta Tables for Publication/Additional Source '''
class SourceType(db.Model):
	__tablename__ = 'source_types'
	id = db.Column(db.Integer, primary_key=True)
	source_name = db.Column(db.String(64), index=True)
	source_description = db.Column(db.Text())

	publications = db.relationship("Publication", backref="source_type")
	additional_sources = db.relationship("AdditionalSource", backref="source_type")

	def __repr__(self):
		return '<Source Type %r>' % self.source_name

class Purpose(db.Model):
	__tablename__ = 'purposes'
	id = db.Column(db.Integer, primary_key=True)
	purpose_name = db.Column(db.String(64), index=True)
	purpose_description = db.Column(db.Text())

	publications = db.relationship("Publication", backref="source_type")

	def __repr__(self):
		return '<Purpose %r>' % self.purpose_name

class MissingData(db.Model):
	__tablename__ = 'missing_data'
	id = db.Column(db.Integer, primary_key=True)
	missing_code = db.Column(db.String(5), index=True)
	missing_description = db.Column(db.Text())

	publications = db.relationship("Publication", backref="missing_data")

	def __repr__(self):
		return '<Missing Data %r>' % self.missing_code
''' End Meta Tables for Publication/Additional Source '''

''' Meta Tables for Author Contact '''
class ContentEmail(db.Model):
	__tablename__ = 'content_email'
	id = db.Column(db.Integer, primary_key=True)
	content_code = db.Column(db.String(5), index=True)
	content_description = db.Column(db.Text())

	author_contacts = db.relationship("AuthorContact", backref="content_email")

	def __repr__(self):
		return '<Missing Data %r>' % self.content_code
''' End Meta Tables for Author Contact '''

''' Meta Tables for Population '''
class Ecoregion(db.Model):
	__tablename__ = 'ecoregions'
	id = db.Column(db.Integer, primary_key=True)
	ecoregion_code = db.Column(db.String(5), index=True)
	ecoregion_description = db.Column(db.Text())

	populations = db.relationship("Population", backref="ecoregion")

	def __repr__(self):
		return '<Ecoregion %r>' % self.ecoregion_code

class Continent(db.Model):
	__tablename__ = 'continents'
	id = db.Column(db.Integer, primary_key=True)
	continent_name = db.Column(db.String(64), index=True)	
	
	populations = db.relationship("Population", backref="continent")

	def __repr__(self):
		return '<Continent %r>' % self.continent_name
''' End Meta Tables for Population '''

''' Meta Tables for Stage Type '''
class StageTypeClass(db.Model):
	__tablename__ = 'stage_type_classes'
	id = db.Column(db.Integer, primary_key=True)
	type_class = db.Column(db.String(64), index=True)

	stage_types = db.relationship("StageType", backref="stage_type_class")

	def __repr__(self):
		return '<Stage Type Class %r>' % self.id
''' End Meta Tables for Stage Type '''

''' Meta Tables for MatrixValue '''
class TransitionType(db.Model):
	__tablename__ = 'transition_types'
	id = db.Column(db.Integer, primary_key=True)
	trans_code = db.Column(db.String(64), index=True)
	trans_description = db.Column(db.Text())

	matrix_values = db.relationship("MatrixValue", backref="transition_type")

	def __repr__(self):
		return '<Transition Type %r>' % self.id
''' End Meta Tables for MatrixValue '''

''' Meta Tables for Matrix '''
class MatrixComposition(db.Model):
	__tablename__ = 'matrix_compositions'
	id = db.Column(db.Integer, primary_key=True)
	comp_name = db.Column(db.String())

	matrices = db.relationship("Matrix", backref="matrix_composition")

	def __repr__(self):
		return '<Matrix Composition %r>' % self.id

class Periodicity(db.Model):
	__tablename__ = 'periodicities'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), index=True)

	matrices = db.relationship("Matrix", backref="periodicity")

	def __repr__(self):
		return '<Periodicity %r>' % self.id

class StudiedSex(db.Model):
	__tablename__ = 'studied_sex'
	id = db.Column(db.Integer, primary_key=True)
	sex_code = db.Column(db.String(5), index=True)
	sex_description = db.Column(db.Text())

	matrices = db.relationship("Matrix", backref="studied_sex")

	def __repr__(self):
		return '<Studied Sex %r>' % self.id

class Captivity(db.Model):
	__tablename__ = 'captivities'
	id = db.Column(db.Integer, primary_key=True)
	cap_code = db.Column(db.String(5), index=True)
	cap_description = db.Column(db.Text())

	matrices = db.relationship("Matrix", backref="captivities")

	def __repr__(self):
		return '<Captivity %r>' % self.id
''' End Meta Tables for Matrix '''
''' End Meta Tables '''

class Species(db.Model):
    __tablename__ = 'species'
    id = db.Column(db.Integer, primary_key=True)
    species = db.Column(db.String(64), index=True)
    subspecies = db.Column(db.String(64))
    family = db.Column(db.String(64))
    tax_order = db.Column(db.String(64))
    iucn_status = db.Column(db.Integer, db.ForeignKey('iucn_status.id'))
    esa_status = db.Column(db.Integer, db.ForeignKey('esa_status.id'))
    invasive_status = db.Column(db.Boolean())
    # user keys might be a problem.. or might not.. will implement and find out
    user_created = db.Column(db.Integer, db.ForeignKey('users.id'))
    user_modified = db.Column(db.Integer, db.ForeignKey('users.id'))
    timestamp_created = db.Column(db.DateTime, default=datetime.utcnow)
    timestamp_modified = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    plant_traits = db.relationship("PlantTrait", backref="species")
    populations = db.relationship("Population", backref="species")
    stages = db.relationship("Stage", backref="species")

    def __repr__(self):
        return '<Species %r>' % self.id


class PlantTrait(db.Model):
	 __tablename__ = 'plant_traits'
	id = db.Column(db.Integer, primary_key=True)
	species_id = db.Column(db.Integer, db.ForeignKey('species.id'))
	max_height = db.Column(db.Float()) #This should be a double, eventually
	growth_type = db.Column(db.Integer, db.ForeignKey('growth_types.id'))
	growth_form_raunkiaer = db.Column(db.Integer, db.ForeignKey('growth_forms_raunkiaer.id'))
	reproductive_repetition = db.Column(db.Integer, db.ForeignKey('reproductive_repetition.id'))
	dicot_monoc = db.Column(db.Integer, db.ForeignKey('dicot_monoc.id'))
	angio_gymno = db.Column(db.Integer, db.ForeignKey('angio_gymno.id'))

	def __repr__(self):
        return '<Plant Trait %r>' % self.id

class Publication(db.Model):
	__tablename__ = 'publications'
	id = db.Column(db.Integer, primary_key=True)
	source_type = db.Column(db.Integer, db.ForeignKey('source_types.id'))
	# These appear as vectors in Judy's schema, trying to think of the best way to implement this within MySQL and Django/Flask
	authors = db.Column(db.Text())
	editors = db.Column(db.Text())
	pub_title = db.Column(db.Text())
	journal_book_conf = db.Column(db.Text())
	year = db.Column(db.SmallInteger(), length=4) #proto
	volume = db.Column(db.Text())
	pages = db.Column(db.Text())
	publisher = db.Column(db.Text())
	city = db.Column(db.Text())
	country = db.Column(db.Text())
	institution = db.Column(db.Text())
	DOI_ISBN = db.Column(db.Text())
	name = db.Column(db.Text()) #r-generated, needs more info, probably generated in method of this model
	corresponding_author = db.Column(db.Text())
	email = db.Column(db.Text())
	purposes = db.Column(db.Integer, db.ForeignKey('purposes.id'))
	date_digitised = db.Column(db.Date(), default=datetime.utcnow)
	embargo = db.Column(db.Date()) #nullable
	missing_data = db.Column(db.Integer, db.ForeignKey('missing_data.id'))

	# Again, these might be problematic
	user_created = db.Column(db.Integer, db.ForeignKey('users.id'))
    user_modified = db.Column(db.Integer, db.ForeignKey('users.id'))
    timestamp_created = db.Column(db.DateTime, default=datetime.utcnow)
    timestamp_modified = db.Column(db.DateTime, default=datetime.utcnow)

    # Establishing one to many relationships between tables
    author_contacts = db.relationship("AuthorContact", backref="publication")
    additional_sources = db.relationship("AdditionalSource", backref="publication")
    populations = db.relationship("Population", backref="publication")
    stages = db.relationship("Stage", backref="publication")
    treatments = db.relationship("Treatment", backref="publication")

   	def __repr__(self):
        return '<Publication %r>' % self.id

class AuthorContact(db.Model):
	__tablename__ = 'author_contacts'
	id = db.Column(db.Integer, primary_key=True)
	publication_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	date_contacted = db.Column(db.Date(), index=True)
	contacting_user = db.Column(db.Integer, db.ForeignKey('users.id'))
	content_email = db.Column(db.Integer, db.ForeignKey('content_email.id')) #possibly many to many, probably a good idea if vector
	author_reply = db.Column(db.Text())

	def __repr__(self):
        return '<Author Contact %r>' % self.id

class AdditionalSource(db.Model):
	__tablename__ = 'additional_sources'
	id = db.Column(db.Integer, primary_key=True)
	publication_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	source_type = db.Column(db.Integer, db.ForeignKey('source_types.id'))
	authors = db.Column(db.Text())
	editors = db.Column(db.Text())
	pub_title = db.Column(db.Text())
	journal_book_conf = db.Column(db.Text())
	year = db.Column(db.SmallInteger(), length=4) #proto
	volume = db.Column(db.Text())
	pages = db.Column(db.Text())
	publisher = db.Column(db.Text())
	city = db.Column(db.Text())
	country = db.Column(db.Text())
	institution = db.Column(db.Text())
	DOI_ISBN = db.Column(db.Text())
	name = db.Column(db.Text()) #r-generated, needs more info, probably to be generated in method of this model, first author in author list?
	description = db.Column(db.Text())

	def __repr__(self):
        return '<Additional Source %r>' % self.id

class Population(db.Model):
	__tablename__ = 'populations'
	id = db.Column(db.Integer, primary_key=True)
	species_id = db.Column(db.Integer, db.ForeignKey('species.id'))
	publication_id = db.Column(db.Integer, db.ForeignKey('publications.id'))
	species_author = db.Column(db.String(64))
	name = db.Column(db.Text(), index=True)
	ecoregion = db.Column(db.Integer, db.ForeignKey('ecoregions.id'))
	#Django plugin for country, and generic python package too - we'll be just fine. Unfortunately, unless we download a CSV of this and enter into sep table, will probably be more efficient to do this outside of the database. Further thought reqd!
	country = db.Column(db.Text())
	continent = db.Column(db.Integer, db.ForeignKey('continents.id'))
	geometries = db.Column(db.Text()) #This needs work once i've decided wether to use Flask or Django - such good cases for both. Databases support point geometry, including altitude.

	matrices = db.relationship("Matrix", backref="population")

	def __repr__(self):
        return '<Population %r>' % self.id

class Stage(db.Model):
	__tablename__ = 'stages'
	id = db.Column(db.Integer, primary_key=True)
	species_id = db.Column(db.Integer, db.ForeignKey('species.id'))
	publication_id = db.Column(db.Integer, db.ForeignKey('publications.id'))
	stage_type_id = db.Column(db.Integer, db.ForeignKey('stage_types.id')) 
	name = db.Column(db.Text(), index=True) #Schema says 'author's', need clarification - author's name possibly, according to protocol?

	matrix_stages = db.relationship("Stage", backref="stage")

	def __repr__(self):
        return '<Stage %r>' % self.id

class StageType(db.Model):
	__tablename__ = 'stage_types'
	id = db.Column(db.Integer, primary_key=True)
	type_name = db.Column(db.Text(), index=True)
	type_class_id = db.Column(db.Integer, db.ForeignKey('stage_type_classes.id'))

	stages = db.relationship("Stage", backref="stage_types")

	def __repr__(self):
        return '<Stage Type %r>' % self.id


class Treatment(db.Model):
	__tablename__ = 'treatments'
	id = db.Column(db.Integer, primary_key=True)
	publication_id = db.Column
	treatment_type_id = db.Column(db.Integer, db.ForeignKey('treatment_types.id'))
	name = db.Column(db.Text(), index=True) #Schema says 'author's', need clarification - author's name possibly, according to protocol?
	description = db.Column(db.Text())

	matrices = db.relationship("Matrix", backref="treatment")

	def __repr__(self):
        return '<Treatment %r>' % self.id

class TreatmentType(db.Model):
	__tablename__ = 'treatment_types'
	id = db.Column(db.Integer, primary_key=True)
	type_name = db.Column(db.Text(), index=True)
	

	treatments = db.relationship("Treatment", backref="treatment_types")

	def __repr__(self):
		return '<Treatment Type %r>' % self.id

class MatrixStage(db.Model):
	__tablename__ = 'matrix_stages'
	id = db.Column(db.Integer, primary_key=True)
	stage_order = db.Column(db.SmallInteger())
	stage_id = db.Column(db.Integer, db.ForeignKey('stages.id'))

	matrix_id = db.Column(db.Integer, db.ForeignKey('matrices.id'))

	def __repr__(self):
		return '<Matrix Stage %r>' % self.id

class MatrixValue(db.Model):
	__tablename__ = 'matrix_values'
	id = db.Column(db.Integer, primary_key=True)
	column_number = db.Column(db.SmallInteger())
	row_number = db.Column(db.SmallInteger())
	transition_type = db.Column(db.Integer, db.ForeignKey('transition_types.id'))
	value = db.Column(db.Float())

	matrix_id = db.Column(db.Integer, db.ForeignKey('matrices.id'))

	def __repr__(self):
		return '<Matrix Value %r>' % self.id

class Matrix(db.Model):
	__tablename__ = 'matrices'
	id = db.Column(db.Integer, primary_key=True)
	population_id = db.Column(db.Integer, db.ForeignKey('populations.id'))
	treatment_id = db.Column(db.Integer, db.ForeignKey('treatments.id'))
	matrix_split = db.Column(db.Boolean())
	matrix_composition = db.Column(db.Integer, db.ForeignKey('matrix_compositions.id'))
	n_intervals = db.Column(db.SmallInteger()) # Danny/Jenni/Dave, what are these? Schema says, "Number of transition intervals represented in the matrix - should only be >1 for mean matrices", so 0 or 1 or more? Can it be a float, ie 0.8?
	periodicity = db.Column(db.Integer, db.ForeignKey('periodicities.id'))
	relative = db.Column(db.Boolean())
	matrix_start = db.Column(db.Date()) # These will include month, day, etc. Create method to return these - matrix_start.day() matrix_start.year() etc
	matrix_end = db.Column(db.Date()) # These will include month, day, etc. Create method to return these - matrix_start.day() matrix_start.year() etc
	# Season?
	n_plots = db.Column(db.SmallInteger()) # Danny/Jenni/Dave, will need your help with plots too.
	plot_size = db.Column(db.Float()) # Schema states, 'R convert to m^2'
	n_individuals = db.Column(db.Integer()) # Schema states, 'total number of individuals observed'
	studied_sex = db.Column(db.Integer, db.ForeignKey('periodicities.id'))
	captivity = db.Column(db.Integer, db.ForeignKey('captivities.id'))
	matrix_stages = db.relationship("MatrixStage", backref="matrix")
	matrix_values = db.relationship("MatrixValue", backref="matrix")
	observations = db.Column(db.Text())

	intervals = db.relationship("Interval", backref="matrix")

	def __repr__(self):
		return '<Matrix %r>' % self.id

''' This table only applies to mean matrices, to identify the intervals that the mean values are derived from '''
class Interval(db.Model):
	__tablename__ = 'intervals'
	id = db.Column(db.Integer, primary_key=True)
	matrix_id = db.Column(db.Integer, db.ForeignKey('matrices.id'))
	interval_order = db.Column(db.Integer())
	interval_start = db.Column(db.Date())
	interval_end = db.Column(db.Date())

	def __repr__(self):
		return '<Interval %r>' % self.id






