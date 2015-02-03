from flask import render_template, redirect, url_for, abort, flash, request,\
    current_app, jsonify
from flask.ext.login import login_required, current_user
from . import demography
# from .forms import EditProfileForm, EditProfileAdminForm, ProjectPostForm, ProjectEditForm, PublicationPostForm, PublicationEditForm
from .. import db
from ..models import Permission, Role, User, Project, Publication, Species, Plant
from ..decorators import admin_required
import re
from jinja2 import evalcontextfilter, Markup, escape
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base

@demography.route('/')
@login_required
def map():
	species = Species.query.all()
	plants = Plant.query.all()
	return render_template('map.html', plants=plants, species=species)

@demography.route('/geojson/all')
def geojson():

	geojson = {
	'type' : 'FeatureCollection',
	'features' : []
	}

	plants = Plant.query.all()

	for plant in plants:
		longi = plant.longitudedec
		lati = plant.latitudedec

		if longi == 'NA':
			pass

		elif lati == 'NA':
			pass

		else:

			fe = {
					'type' : 'Feature',
					'geometry' : {
						'type' : 'Point',
						'coordinates' : [plant.longitudedec, plant.latitudedec]
					},
					'properties' : {
						'title' : '<em>'+plant.name+'</em>',
						'name' : plant.name,
						'matrixnumber' : plant.matrixnumber,
						'matrix' : plant.matrix,
						'dimension' : plant.dimension,
						'matrixclassnumber' : plant.matrixclassnumber,
						'matrixclassorganised' : plant.matrixclassorganised,
						'matrixsplit' : plant.matrixsplit,
						'classnames' : plant.classnames,
						'observation' : plant.observation,
						'matrixcomposite' : plant.matrixcomposite,
						'matrixtreatment' : plant.matrixtreatment,
						'matrixcaptivity' : plant.matrixcaptivity,
						'matrixstartyear' : plant.matrixstartyear,
						'matrixstartseason' : plant.matrixstartseason,
						'matrixstartmonth' : plant.matrixstartmonth,
						'matrixendyear' : plant.matrixendyear,
						'matrixendseason' : plant.matrixendseason,
						'matrixendmonth' : plant.matrixendmonth,
						'studiedsex' : plant.studiedsex,
						'population' : plant.population,
						'latdeg' : plant.latdeg,
						'latmin' : plant.latmin,
						'latsec' : plant.latsec,
						'londeg' : plant.londeg,
						'lonmin' : plant.lonmin,
						'lonsec' : plant.lonsec,
						'altitude' : plant.altitude,
						'country' : plant.country,
						'continent' : plant.continent,
						'criteriasize' : plant.criteriasize,
						'criteriaontogeny' : plant.criteriaontogeny,
						'authors' : plant.authors,
						'journal': plant.journal,
						'yearpublication' : plant.yearpublication,
						'doiisbn' : plant.doiisbn,
						'enteredby' : plant.enteredby,
						'entereddate' : plant.entereddate,
						'source' : plant.source,
						'statusstudy' : plant.statusstudy,
						'statusstudyref' : plant.statusstudyref,
						'statuselsewhere' : plant.statuselsewhere,
						'statuselsewhereref' : plant.statuselsewhereref,
						'marker-color' : '#e74c3c',
						'marker-size' : 'small',
						}
					
				}


			geojson["features"].append(fe)


	return jsonify(geojson)

@demography.route('/geojson/<param>/<filters>')
def geojsonfilter(param, filters):

	kwargs = {
		param : filters
	}

	geojson = {
	'type' : 'FeatureCollection',
	'features' : []
	}


	plants = Plant.query.filter_by(**kwargs)

	for plant in plants:
		longi = plant.longitudedec
		lati = plant.latitudedec

		if longi == 'NA':
			pass

		elif lati == 'NA':
			pass

		else:
			fe = {
					'type' : 'Feature',
					'geometry' : {
						'type' : 'Point',
						'coordinates' : [plant.longitudedec, plant.latitudedec]
					},
					'properties' : {
						'title' : '<em>'+plant.name+'</em>',
						'name' : plant.name,
						'matrixnumber' : plant.matrixnumber,
						'matrix' : plant.matrix,
						'dimension' : plant.dimension,
						'matrixclassnumber' : plant.matrixclassnumber,
						'matrixclassorganised' : plant.matrixclassorganised,
						'matrixsplit' : plant.matrixsplit,
						'classnames' : plant.classnames,
						'observation' : plant.observation,
						'matrixcomposite' : plant.matrixcomposite,
						'matrixtreatment' : plant.matrixtreatment,
						'matrixcaptivity' : plant.matrixcaptivity,
						'matrixstartyear' : plant.matrixstartyear,
						'matrixstartseason' : plant.matrixstartseason,
						'matrixstartmonth' : plant.matrixstartmonth,
						'matrixendyear' : plant.matrixendyear,
						'matrixendseason' : plant.matrixendseason,
						'matrixendmonth' : plant.matrixendmonth,
						'studiedsex' : plant.studiedsex,
						'population' : plant.population,
						'latdeg' : plant.latdeg,
						'latmin' : plant.latmin,
						'latsec' : plant.latsec,
						'londeg' : plant.londeg,
						'lonmin' : plant.lonmin,
						'lonsec' : plant.lonsec,
						'altitude' : plant.altitude,
						'country' : plant.country,
						'continent' : plant.continent,
						'criteriasize' : plant.criteriasize,
						'criteriaontogeny' : plant.criteriaontogeny,
						'authors' : plant.authors,
						'journal': plant.journal,
						'yearpublication' : plant.yearpublication,
						'doiisbn' : plant.doiisbn,
						'enteredby' : plant.enteredby,
						'entereddate' : plant.entereddate,
						'source' : plant.source,
						'statusstudy' : plant.statusstudy,
						'statusstudyref' : plant.statusstudyref,
						'statuselsewhere' : plant.statuselsewhere,
						'statuselsewhereref' : plant.statuselsewhereref,
						'marker-color' : '#e74c3c',
						'marker-size' : 'small',
						}
					
				}


			geojson["features"].append(fe)

	return jsonify(geojson)

@demography.route('/speciesjson/<name>')
def speciesjson(name):


	geojson = {
	'type' : 'FeatureCollection',
	'features' : []
	}

	kwargs = {
	'name' : name
	}

	species = Species.query.filter_by(**kwargs)

	for sp in species:

		if sp.name == 'NA':
			fe = {
			'name' : 'Not Enough Data'
			}
			

		else:
			fe = {
					'name' : sp.name,
					'speciesauthor' : sp.speciesauthor,
					'kingdom' : sp.kingdom,
					'phylum' : sp.phylum,
					'angiogymno' : sp.angiogymno,
					'dicotmonoc' : sp.dicotmonoc,
					'class' : sp._class,
					'order' : sp._order,
					'family': sp.family,
					'genus' : sp.genus,
					'ecoregion' : sp.ecoregion,
					'growthtype' : sp.growthtype,
					'growthformraunkiaer' : sp.growthformraunkiaer,
					'annualperiodicity' : sp.annualperiodicity,
					'planttype' : sp.planttype,
					'commonname' : sp.commonname,
					'originalimageurl' : sp.originalimageurl
						}
					
				


			geojson['features'].append(fe)

	return jsonify(geojson)
