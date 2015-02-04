# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
from scrapy.http import Request

from flask import render_template, redirect, url_for, abort, flash, request,\
    current_app, jsonify
from flask.ext.login import login_required, current_user
import re
from jinja2 import evalcontextfilter, Markup, escape
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
import datetime, logging
from sqlalchemy import create_engine, exc
import sqlalchemy.exc
from sqlalchemy.orm import sessionmaker

import sys

sys.path.append('/home/francesca/Sites/life-cycle/')

from app.models import Plant, Species

class EolPipeline(object):
	def process_item(self, item, spider):

		try:
			engine = create_engine('mysql://root:jeh5t@localhost/lifecycle', echo=False)	 
			Session = sessionmaker(bind=engine)
			session = Session()

			species = session.query(Species).filter_by(name=item['name']).first()
			species.commonname = item['common_name']
			species.originalimageurl = item['image_url']

			session.add(species)

		except:
			text_file = open("error.txt", "w")
			text_file.write("Did not work: " + item['name'])
			text_file.close()

		else:
			print species.name
			session.commit()

		return item
