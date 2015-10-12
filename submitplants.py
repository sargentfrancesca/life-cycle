import datetime, logging
from sqlalchemy import create_engine, exc
import sqlalchemy.exc
from sqlalchemy.orm import sessionmaker
from flask import current_app
from app.demography import models
import unicodecsv
import sys
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')

engine = create_engine('mysql://root:jeh5t@localhost/lifecycle', echo=False)

logging.basicConfig(level=logging.DEBUG, filename='dberrors.log')
 
# create a Session
Session = sessionmaker(bind=engine)
session = Session()
session._model_changes = {}

error = sqlalchemy.exc.ProgrammingError


def importCSV():
	import csv

	def unicode_csv_reader(utf8_data, dialect=csv.excel, **kwargs):
		csv_reader = csv.reader(utf8_data, dialect=dialect, **kwargs)
		for row in csv_reader:
			yield [unicode(cell, 'utf-8') for cell in row]
			print 'Unpacked CSV'

	

	with open('compadreFlat.csv', 'rU') as csvfile:
		fileread = unicodecsv.reader(csvfile, delimiter=',', quotechar='"', encoding='utf-8')
		allMatrices = []

		print 'Opened CSV for reading'

		for i, row in enumerate(fileread):
			if i != 0:
				print i
# 			if i != 0:
# 				allMatrices.append({
# 					'name' : row[21],
# 					'matrixnumber' : row[51], 
# 					'matrix' : row[55],
# 					'dimension' : row[53],
# 					'matrixclassnumber' : row[52],
# 					'matrixclassorganised' : row[50],
# 					'matrixsplit' : row[48],
# 					'classnames' : row[56],
# 					'observation' : row[49],
# 					'matrixcomposite' : row[27],
# 					'matrixtreatment' : row[28],
# 					'matrixcaptivity' : row[29],
# 					'matrixstartyear' : row[30],
# 					'matrixstartseason' : row[31],
# 					'matrixstartmonth' : row[32],
# 					'matrixendyear' : row[33],
# 					'matrixendseason' : row[34],
# 					'matrixendmonth' : row[35],
# 					'studiedsex' : row[26],
# 					'population' : row[36],
# 					'latdeg' : row[37],
# 					'latmin' : row[38],
# 					'latsec' : row[39],
# 					'londeg' : row[40],
# 					'lonmin' : row[41],
# 					'lonsec' : row[42],
# 					'latitudedec' : row[43],
# 					'longitudedec' : row[44],
# 					'altitude' : row[45],
# 					'country' : row[46],
# 					'continent' : row[47],
# 					'criteriasize' : row[10],
# 					'criteriaontogeny' : row[11],
# 					'authors' : row[0],
# 					'journal' : row[1],
# 					'yearpublication' : row[2],
# 					'doiisbn' : row[3],
# 					'additionalsource' : row[4],
# 					'enteredby' : row[22],
# 					'entereddate' : row[23],
# 					'source' : row[24],
# 					'statusstudy' : row[57],
# 					'statusstudyref' : row[58],
# 					'statuselsewhere' : row[59],
# 					'statuselsewhereref' : row[60]
# 					})

# 		for matrix in allMatrices:
				
# 			plantname = matrix['name']
# 			speciesname = session.query(Species).filter_by(name=plantname).first()

# 			if speciesname is None:
# 				pass

# 			else:

# 				mn = matrix['matrixnumber']
# 				cn = session.query(Plant).filter_by(matrixnumber=mn).first()
				
# 				if cn is None :
# 					newplant = [Plant(
# 						matrix['name'],
# 						matrix['matrixnumber'],
# 						matrix['matrix'],
# 						matrix['dimension'],
# 						matrix['matrixclassnumber'],
# 						matrix['matrixclassorganised'],
# 						matrix['matrixsplit'],
# 						matrix['classnames'],
# 						matrix['observation'],
# 						matrix['matrixcomposite'],
# 						matrix['matrixtreatment'],
# 						matrix['matrixcaptivity'],
# 						matrix['matrixstartyear'],
# 						matrix['matrixstartseason'],
# 						matrix['matrixstartmonth'],
# 						matrix['matrixendyear'],
# 						matrix['matrixendseason'],
# 						matrix['matrixendmonth'],
# 						matrix['studiedsex'],
# 						matrix['population'],
# 						matrix['latdeg'],
# 						matrix['latmin'],
# 						matrix['latsec'],
# 						matrix['londeg'],
# 						matrix['lonmin'],
# 						matrix['lonsec'],
# 						matrix['latitudedec'],
# 						matrix['longitudedec'],
# 						matrix['altitude'],
# 						matrix['country'],
# 						matrix['continent'],
# 						matrix['criteriasize'],
# 						matrix['criteriaontogeny'],
# 						matrix['authors'],
# 						matrix['journal'],
# 						matrix['yearpublication'],
# 						matrix['doiisbn'],
# 						matrix['additionalsource'],
# 						matrix['enteredby'],
# 						matrix['entereddate'],
# 						matrix['source'],
# 						matrix['statusstudy'],
# 						matrix['statusstudyref'],
# 						matrix['statuselsewhere'],
# 						matrix['statuselsewhereref'],
# 						)]
					
# 					print "Adding", matrix['matrixnumber'], matrix['matrixnumber'], "to Session"
# 					speciesname.plants.extend(newplant)
# 					session.add(speciesname)


# 				try:
# 					"Committing to database"
# 					session.commit()
# 					session.flush()
				
# 				except sqlalchemy.exc.ProgrammingError, exc:
# 					session.rollback()
# 					logging.exception("Fail: ")
# 					pass

importCSV()