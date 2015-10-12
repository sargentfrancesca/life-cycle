import datetime, logging
from sqlalchemy import create_engine, exc
import sqlalchemy.exc
from sqlalchemy.orm import sessionmaker
from flask import current_app
from app.models import Plant, Species
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
logf = open("error.log", "w")

def degtodec(deg, mins, sec):
	if deg == 'NA' or mins == 'NA' or sec == 'NA':
		return
	else:
		dec = (float(deg) + (float(mins) * 1/60) + (float(sec) * 1/60 * 1/60))
		return dec

def submitSpecies(species):
				
	speciesname = species['speciesaccepted']
	print speciesname


	if session.query(Species).filter_by(name=speciesname).first() is None:
		
		print "Entering new data", speciesname

		n_species = Species()
		n_species.name = species['speciesaccepted']
		n_species.speciesauthor = species['speciesauthor']
		n_species.authority = str(species['authority'])
		n_species.taxonomy = species['taxonomy']
		n_species.tplversion = species['tplversion']
		n_species.intraspecificaccepted = species['intraspecificaccepted']
		n_species.speciesepithetaccepted = species['speciesepithetaccepted']
		n_species.genusaccepted = species['genusaccepted']
		n_species.kingdom = species['kingdom']
		n_species.phylum = species['phylum']
		n_species.angiogymno = species['angiogymno']
		n_species.dicotmonoc = species['dicotmonoc']
		n_species._class = species['t_class']
		n_species._order = species['order']
		n_species.family = species['family']
		n_species.genus = species['genus']

		try:
			session.add(n_species)
			session.commit()
		except:
			logf.write("Failed to download {0}\n".format(n_species.name))
			pass

	
	else:
		print "Data already exists"

def submitPlant(plant):
	plantname = plant['speciesaccepted']
	speciesname = session.query(Species).filter_by(name=plantname).first()

	print plantname

	if speciesname is None:
		print "No Species"
		pass

	else:

		mat = plant['matrix_a']
		comp = plant['matrixcomposite']

		cn = session.query(Plant).filter_by(matrixcomposite=comp, matrix_a=mat).first()
		
		if cn is None :
			newplant = [Plant()]

			newplant[0].name = plant['speciesaccepted']
			newplant[0].matrix_a = plant['matrix_a']
			newplant[0].matrix_u = plant['matrix_u']
			newplant[0].matrix_f = plant['matrix_f']
			newplant[0].matrix_c = plant['matrix_c']
			newplant[0].dimension = plant['matrixdimension']
			newplant[0].matrixsplit = plant['matrixsplit']
			newplant[0].classnames = str(plant['classnames'])
			newplant[0].observation = str(plant['observation'])
			newplant[0].matrixcomposite = plant['matrixcomposite']
			newplant[0].matrixtreatment = str(plant['matrixtreatment'])
			newplant[0].matrixcaptivity = plant['matrixcaptivity']
			newplant[0].matrixstartyear = plant['matrixstartyear']
			newplant[0].matrixstartseason = plant['matrixstartseason']
			newplant[0].matrixstartmonth = plant['matrixstartmonth']
			newplant[0].matrixendyear = plant['matrixendyear']
			newplant[0].matrixendseason = plant['matrixendseason']
			newplant[0].matrixendmonth = plant['matrixendmonth']
			newplant[0].matrixfec = plant['matrixfec']
			newplant[0].studiedsex = plant['studiedsex']
			newplant[0].population = str(plant['matrixpopulation'])
			newplant[0].latdeg = plant['latdeg']
			newplant[0].latmin = plant['latmin']
			newplant[0].latsec = plant['latsec']
			newplant[0].latns = plant['latns']
			newplant[0].londeg = plant['londeg']
			newplant[0].lonmin = plant['lonmin']
			newplant[0].lonsec = plant['lonsec']
			newplant[0].lonwe = plant['lonwe']
			newplant[0].latitudedec = degtodec(plant['latdeg'], plant['latmin'], plant['latsec'])
			newplant[0].longitudedec = degtodec(plant['londeg'], plant['lonmin'], plant['lonsec'])
			newplant[0].annualperiodicity = plant['annualperiodicity']
			newplant[0].altitude = plant['altitude']
			newplant[0].country = plant['country']
			newplant[0].continent = plant['continent']
			newplant[0].criteriasize = plant['criteriasize']
			newplant[0].criteriaontogeny = plant['criteriaontogeny']
			newplant[0].authors = str(plant['authors'])
			newplant[0].journal = plant['journal']
			newplant[0].yearpublication = plant['yearpublished']
			newplant[0].doiisbn = plant['doiisbn']
			newplant[0].additionalsource = str(plant['additionalsource'])
		    # newplant.enteredby = db.Column(db.String(64))
		    # newplant.entereddate = db.Column(db.String(64))
		    # newplant.source = db.Column(db.String(100))
		    # newplant.statusstudy = db.Column(db.String(64))
		    # newplant.statusstudyref = db.Column(db.String(64))
		    # newplant.statuselsewhere = db.Column(db.String(64))
		    # newplant.statuselsewhereref = db.Column(db.String(64))

			print vars(newplant[0])

			
			print "Adding", plant['speciesaccepted'], "to Session"
			if len(speciesname.plants) is 0:
				speciesname.plants.append(newplant[0])
			else:
				speciesname.plants.extend(newplant)
			session.add(speciesname)


		try:
			"Committing to database"
			session.commit()
			session.flush()
		
		except sqlalchemy.exc.ProgrammingError, exc:
			session.rollback()
			logging.exception("Fail: ")
			pass

def importCSV():
	import csv

	def unicode_csv_reader(utf8_data, dialect=csv.excel, **kwargs):
		csv_reader = csv.reader(utf8_data, dialect=dialect, **kwargs)
		for row in csv_reader:
			yield [unicode(cell, 'utf-8') for cell in row]
			print 'Unpacked CSV'
	

	with open('compadreFlat3.csv', 'rU') as csvfile:
		fileread = unicodecsv.reader(csvfile, delimiter=',', quotechar='"', encoding='utf-8')
		allMatrices = []

		allSpecies = []
		allPlants = []

		for i, row in enumerate(fileread):
			if i > 0:
				allSpecies.append ({
					'speciesauthor' : row[0],
					'speciesaccepted': row[1],
					'authority' : row[2],
					'taxonomy' : row[3],
					'tplversion' : row[4],
					'intraspecificaccepted' : row[5],
					'speciesepithetaccepted' : row[6],
					'genusaccepted' : row[7],
					'genus' : row[8],
					'family' : row[9],
					'order' : row[10],
					't_class' : row[11],
					'dicotmonoc' : row[12],
					'angiogymno' : row[13], 
					'phylum' : row[14],
					'kingdom' : row[15],
					'growthtype' : row[16]
					})

				allPlants.append({
					'speciesaccepted' : row[1],
					'authors' : row[17],
					'journal' : row[18],
					'yearpublished' : row[19],
					'doiisbn' : row[20],
					'additionalsource' : row[21],
					'studyduration' : row[22],
					'studystart' : row[23],
					'studyend' : row[24],
					'annualperiodicity' : row[25],
					'numberpopulations' : row[26],
					'criteriasize' : row[27],
					'criteriaontogeny' : row[28],
					'criteriaage' : row[29],
					'matrixpopulation' : row[30],
					'latdeg' : row[31],
					'latmin' : row[32],
					'latsec' : row[33],
					'latns' : row[34],
					'londeg' : row[35],
					'lonmin' : row[36],
					'lonsec' : row[37],
					'lonwe' : row[38],
					'altitude' : row[39],
					'country' : row[40],
					'continent' : row[41],
					'ecoregion' : row[42],
					'studiedsex' : row[43],
					'matrixcomposite' : row[44],
					'matrixtreatment' : row[45],
					'matrixcaptivity' : row[46],
					'matrixstartyear' : row[47],
					'matrixstartseason' : row[48],
					'matrixstartmonth' : row[49],
					'matrixendyear' : row[50],
					'matrixendseason' : row[51],
					'matrixendmonth' : row[52],
					'matrixsplit' : row[53],
					'matrixfec' : row[54],
					'observation' : row[55],
					'matrixdimension' : row[56],
					'survivalissue' : row[57],
					'classnames' : row[58],
					'matrix_a' : row[59],
					'matrix_u' : row[60],
					'matrix_f' : row[61],
					'matrix_c' : row[62]
				})
				
		for species in allSpecies:
			submitSpecies(species)

		for plant in allPlants:
			submitPlant(plant)


importCSV()

