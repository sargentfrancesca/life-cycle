# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
from scrapy.http import Request
from scrapy.contrib.pipeline.images import ImagesPipeline

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

from PIL import Image

import sys

sys.path.append('/Users/francesca/sites/env/life-cycle/')

from app.models import Plant, Species

class EolPipeline(object):
	def process_item(self, item, spider):

		try:
			engine = create_engine('mysql://root:jeh5t@localhost/lifecycle', echo=False)	 
			Session = sessionmaker(bind=engine)
			session = Session()

			species = session.query(Species).filter_by(name=item['name']).first()
			species.commonname = item['common_name']
			species.originalimageurl = item['image_urls']
			species.localimageurl = item["local_image_url"]
			species.originalpageurl = item["main_url"]
			session._model_changes = {}

			session.add(species)

		except:
			text_file = open("error.txt", "a")
			text_file.write("Did not work: " + item['name'] + "\n")
			text_file.close()

		else:
			print species.name
			session.commit()

		return item

class MyImagesPipeline(ImagesPipeline):

    #Name download version
    def file_path(self, request, response=None, info=None):		
		image_guid = request.url.split('/')[-1]

		return 'full/%s' % (image_guid)

    #Name thumbnail version
    def thumb_path(self, request, thumb_id, response=None, info=None):
        image_guid = thumb_id + response.url.split('/')[-1]
        return 'thumbs/%s/%s.jpg' % (thumb_id, image_guid)

    def get_media_requests(self, item, info):
        #yield Request(item['images']) # Adding meta. Dunno how to put it in one line :-)
        for image in item['image_urls']:
            yield Request(image)