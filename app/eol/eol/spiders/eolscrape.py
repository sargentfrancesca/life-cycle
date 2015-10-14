from scrapy.spider 	import Spider
from scrapy.selector 	import HtmlXPathSelector
from eol.items import EolItem
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

sys.path.append('/Users/francesca/sites/env/life-cycle/')

print sys.path

from app.models import Plant, Species



def getNames():
	engine = create_engine('mysql://root:jeh5t@localhost/lifecycle', echo=False)
	 
	# create a Session
	Session = sessionmaker(bind=engine)
	session = Session()

	all_species = session.query(Species).all()

	start_urls = []

	for species in all_species:
		name = species.name
		url_name = name.replace(" ", "+")
		start_urls.append("http://eol.org/search?q="+url_name+"&show_all=true")

	return start_urls

getNames()

class EolPage(Spider):
	name = "eolscrape"
	allowed_domains = ["eol.org"]

	start_urls = getNames()

	def parse(self, response):
		hxs = HtmlXPathSelector(response)
		urls = hxs.select('//*[@id="main"]/div/ul/li[1]/h4/a/@href').extract()

		try:
			res1 = Request('http://eol.org' + urls[0], callback=self.parse_two)
			
		except:
			print "Passing"
			return urls
			pass

		else:
			print res1
			return res1

			

			
	def parse_two(self, response1):
		item = EolItem()
		referring_url = response1.url
		hxs2 = HtmlXPathSelector(response1)
		name = hxs2.select('//*[@id="page_heading"]/div/div[1]/h1/i/text()').extract()
		common_name = hxs2.select('//*[@id="page_heading"]/div/div[1]/h2/text()').extract()
		image_urls = hxs2.select('//*[@id="media_summary"]/div/div[1]/a/img/@src').extract()
		

		try:
			item["main_url"] = referring_url
			item["name"] = str(name[0])
			item["common_name"] = str(common_name[0].replace('\n', ''))
			item["image_urls"] = str(image_urls[0])
			local_image_url = item["image_urls"].split('/')[-1]
			item["local_image_url"] = local_image_url

		except IndexError:
			print "Passing"
			pass
		
		else:

			yield item






