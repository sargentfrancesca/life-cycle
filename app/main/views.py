from flask import render_template, redirect, url_for, abort, flash, request,\
    current_app, jsonify
from flask.ext.login import login_required, current_user
from . import main
# from .forms import EditProfileForm, EditProfileAdminForm, ProjectPostForm, ProjectEditForm, BookingForm, BookingFormAdmin, PublicationPostForm, PublicationEditForm
# from .. import db
from ..spandex.models import Permission, Role, User, Project, Publication, Booking, coauthors
# from ..decorators import admin_required
# import re
# from jinja2 import evalcontextfilter, Markup, escape
# from sqlalchemy import *
# from sqlalchemy.ext.declarative import declarative_base
# import csv

@main.route('/')
def index():
    users = User.query.all()
    projects = Project.query.all()
    publications = Publication.query.all()
    return render_template('index.html', researchers=users, projects=projects, publications=publications)

# def unicode_csv_reader(utf8_data, **kwargs):
#     csv_reader = csv.reader(utf8_data, **kwargs)
#     for row in csv_reader:
#         yield [unicode(cell, 'utf-8') for cell in row]

# @main.route('/dave-cite')
# def dave():
    
#     filename = 'citations.csv'
#     reader = unicode_csv_reader(open(filename))
#     allCitations = []
    
#     for i, row in enumerate(reader):
#         if i != 0:
#             print row[0]
#             allCitations.append({"authors": row[0], "title": row[1], "publication": row[2], "volume" : row[3], "number" : row[4], "pages" : row[5], "year": row[6], "publisher": row[7]})

#     for citation in allCitations:
#         string = citation["authors"][:-2] + ".(" + citation["year"] + "). " + citation["title"] + ". " + citation["publication"]
#         if citation["volume"] != '':
#             string += ", " + citation["volume"]
#         if citation["number"] != '':
#             string += "(" + citation["number"] + ") "
#         if citation["pages"] != '':
#             string += ", " + citation["pages"]

#         string += '.'

        
        
#         publication = Publication()
#         publication.other_researchers= citation["authors"].encode('ascii', 'ignore')
#         publication.full_title = citation["title"].encode('ascii', 'ignore')
#         publication.citation= string.encode('ascii', 'ignore')
#         publication.researchers = [User.query.get(6)]

#         db.session.add(publication)


#     db.session.commit()

#     return "Hi"
# # Researchers
# @main.route('/researchers/')
# @login_required
# def researcherpage():
#     page = request.args.get('page', 1, type=int)
#     pagination = User.query.order_by(User.name.desc()).paginate(
#         page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
#         error_out=False)
#     posts = pagination.items
#     users = User.query.all()
#     projects = Project.query.all()
#     publications = Publication.query.all()
#     return render_template('researchers.html', posts=posts,
#                            pagination=pagination, projects=projects, researchers=users, publications=publications)

# @main.route('/researchers/<username>')
# @login_required
# def user(username):
#     user = User.query.filter_by(username=username).first_or_404()

#     posts = user.projects.order_by(Project.timestamp.desc())


#     users = User.query.all()
#     projects = Project.query.all()

#     if user.publications:
#         publications = user.publications.order_by(Publication.timestamp.desc())


#     print posts
#     print publications 

#     return render_template('user.html', user=user, researchers=users, posts=posts, publications=publications)

# @main.route('/researchers/<user>/projects')
# @login_required
# def user_projects(user):
#     user = User.query.filter_by(username=user).first() 
#     if user is None:
#         abort(404)

#     page = request.args.get('page', 1, type=int)
#     posts = user.posts.order_by(Project.timestamp.desc()).all

#     pagination = Project.query.order_by(Project.timestamp.desc()).paginate(
#         page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
#         error_out=False)
#     posts = pagination.items

#     users = User.query.all()
#     projects = Project.query.all()
#     publications = Publication.query.all()
#     ptype = "Project"
#     return render_template('projects.html', user=user, researchers=users, posts=posts, projects=projects, ptype=ptype, publications=publications)


# # Profile Editing
# @main.route('/edit-profile', methods=['GET', 'POST'])
# @login_required
# def edit_profile():
#     form = EditProfileForm()
#     if form.validate_on_submit():
#         tweet = re.sub('[@]', '', form.twitter.data)

#         current_user.name = form.name.data
#         current_user.jobtitle = form.jobtitle.data 
#         current_user.location = form.location.data
#         current_user.about_me = form.about_me.data
#         current_user.quals = form.quals.data
#         current_user.pub_email = form.pub_email.data
#         current_user.website = form.website.data
#         current_user.twitter = form.twitter.data
#         current_user.twitter_name = tweet
#         current_user.linkedin = form.linkedin.data
#         current_user.google = form.google.data
#         current_user.google_scholar = form.google_scholar.data
#         current_user.research_gate = form.research_gate.data
#         db.session.add(current_user)
#         flash('Your profile has been updated.')
#         return redirect(url_for('.user', username=current_user.username))
#     form.name.data = current_user.name
#     form.jobtitle.data = current_user.jobtitle
#     form.location.data = current_user.location
#     form.about_me.data = current_user.about_me
#     form.quals.data = current_user.quals
#     form.pub_email.data = current_user.pub_email
#     form.website.data = current_user.website
#     form.twitter.data = current_user.twitter
#     form.linkedin.data = current_user.linkedin
#     form.google.data = current_user.google
#     form.google_scholar.data = current_user.google_scholar
#     form.research_gate.data = current_user.research_gate

#     ptype = "Profile"
#     user = current_user.name
#     users = User.query.all()
#     projects = Project.query.all()
#     publications = Publication.query.all()
#     return render_template('edit_something.html', researchers=users, user=user, form=form, ptype=ptype, projects=projects, publications=publications)


# @main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
# @login_required
# @admin_required
# def edit_profile_admin(id):
#     user = User.query.get_or_404(id)
#     form = EditProfileAdminForm(user=user)
#     if form.validate_on_submit():
#         tweet = re.sub('[@]', '', form.twitter.data)

#         user.email = form.email.data
#         user.username = form.username.data
#         user.confirmed = form.confirmed.data
#         user.role = Role.query.get(form.role.data)
#         user.name = form.name.data
#         user.jobtitle = form.jobtitle.data
#         user.location = form.location.data
#         user.about_me = form.about_me.data
#         user.quals = form.quals.data
#         user.pub_email = form.pub_email.data
#         user.website = form.website.data
#         user.twitter = form.twitter.data
#         user.twitter_name = tweet
#         user.linkedin = form.linkedin.data
#         user.google = form.google.data
#         user.google_scholar = form.google_scholar.data
#         user.research_gate = form.research_gate.data
#         user.tw_confirmed = form.tw_confirmed.data
#         user.tw_widget_id = form.tw_widget_id.data
#         db.session.add(user)
#         flash('The profile has been updated.')
#         return redirect(url_for('.user', username=user.username))
#     form.email.data = user.email
#     form.username.data = user.username
#     form.confirmed.data = user.confirmed
#     form.role.data = user.role_id
#     form.name.data = user.name
#     form.jobtitle.data = user.jobtitle
#     form.location.data = user.location
#     form.about_me.data = user.about_me
#     form.quals.data = user.quals
#     form.pub_email.data = user.pub_email
#     form.website.data = user.website
#     form.twitter.data = user.twitter
#     form.linkedin.data = user.linkedin
#     form.google.data = user.google
#     form.google_scholar.data = user.google_scholar
#     form.research_gate.data = user.research_gate
#     form.tw_confirmed.data = user.tw_confirmed
#     form.tw_widget_id.data = user.tw_widget_id

#     ptype = "Profile"
#     users = User.query.all()
#     projects = Project.query.all()
#     publications = Publication.query.all()
#     return render_template('edit_something.html', researchers=users, form=form, user=user, ptype=ptype, projects=projects, publications=publications)

# # Projects
# @main.route('/projects/')
# @login_required
# def projectpage():
#     page = request.args.get('page', 1, type=int)
#     pagination = Project.query.order_by(Project.timestamp.desc()).paginate(
#         page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
#         error_out=False)
#     posts = pagination.items
#     users = User.query.all()
#     projects = Project.query.all()
#     publications = Publication.query.all()
#     return render_template('projects.html', posts=posts,
#                            pagination=pagination, projects=projects, researchers=users, publications=publications)

# @main.route('/projects/<int:id>')
# @login_required 
# def projnamepage(id):
#     kwargs = {
#     'id' : id
#     }

#     post = Project.query.filter_by(**kwargs).first_or_404()

#     users = User.query.all()
#     projects = Project.query.all()
#     publications = Publication.query.all()
#     return render_template('project.html', researchers=users, projects=projects, post=post, id=id, publications=publications)



# @main.route('/projects/post', methods=['GET', 'POST'])
# @login_required
# def postproject():
#     form = ProjectPostForm()
#     if current_user.can(Permission.WRITE_ARTICLES) and \
#             form.validate_on_submit():
#         tweet = re.sub('[@]', '', form.twitter.data)
#         post = Project(title=form.title.data,
#                         full_title=form.full_title.data,
#                         synopsis=form.synopsis.data,
#                         website=form.website.data,
#                         twitter=form.twitter.data,
#                         twitter_name = tweet,
#                         facebook=form.facebook.data,
#                         researchers = [current_user._get_current_object()])
#         db.session.add(post)
#         return redirect(url_for('.projnamepage', id=post.id))
#     page = request.args.get('page', 1, type=int)
#     pagination = Project.query.order_by(Project.timestamp.desc()).paginate(
#         page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
#         error_out=False)
#     posts = pagination.items
#     ptype = "Project"
#     users = User.query.all()
#     projects = Project.query.all()
#     publications = Publication.query.all()
#     return render_template('post_something.html', form=form, researchers=users, posts=posts,
#                            pagination=pagination, ptype=ptype, projects=projects, publications=publications)


# @main.route('/projects/edit/<int:id>', methods=['GET', 'POST']) 
# @login_required
# def edit_project(id):
    
#     kwargs = {
#     'id' : id
#     }

#     post = Project.query.filter_by(**kwargs).first()

#     if current_user != post.researchers and \
#         not current_user.can(Permission.WRITE_ARTICLES): abort(403)
#     form = ProjectEditForm()
#     if form.validate_on_submit():
#         tweet = re.sub('[@]', '', form.twitter.data)
#         post.title = form.title.data
#         post.full_title = form.full_title.data
#         post.synopsis = form.synopsis.data 
#         post.website = form.website.data
#         post.twitter = form.twitter.data
#         post.twitter_name = tweet
#         post.facebook = form.facebook.data
#         db.session.add(post)
#         flash('The post has been updated.')
#         return redirect(url_for('.projnamepage', id=post.id))


#     form.title.data = post.title
#     form.full_title.data = post.full_title
#     form.synopsis.data = post.synopsis
#     form.website.data = post.website
#     form.twitter.data = post.twitter
#     form.facebook.data = post.facebook

#     ptype = "Project"
#     users = User.query.all()
#     projects = Project.query.all()
#     publications = Publication.query.all()
#     return render_template('edit_something.html', id=id, post=post, researchers=users, projects=projects, form=form, ptype=ptype, user=user, publications=publications)


# @main.route('/delete/', methods=['POST'])
# @login_required
# def delete_user():

#     id = request.form['id']
#     name = request.form['name']

#     stuff = {
#         'id' : id
#     }

#     kwargs = {
#         'name' : name,
#     }

#     project = Project.query.filter_by(**stuff).first()
#     oldpost = User.query.filter_by(**kwargs).first()
#     project.researchers.remove(oldpost)
#     db.session.commit()

#     return render_template('index.html')

# @main.route('/delete/publication', methods=['POST'])
# @login_required
# def delete_user_pub():

#     id = request.form['id']
#     name = request.form['name']

#     stuff = {
#         'id' : id
#     }

#     kwargs = {
#         'name' : name,
#     }

#     publication = Publication.query.filter_by(**stuff).first()
#     oldpost = User.query.filter_by(**kwargs).first()
#     publication.researchers.remove(oldpost)

#     db.session.commit()

#     return render_template('index.html')


# @main.route('/add/', methods=['POST'])
# @login_required
# def add_remove_coauthor():

#     id = request.form['id']
#     name = request.form['name']
    
#     stuff = {
#         'id' : id
#     }

#     kwargs = {
#         'name' : name,
#     }

#     print name

#     project = Project.query.filter_by(**stuff).first()
#     newpost = [User.query.filter_by(**kwargs).first()]
#     project.researchers.extend(newpost)
#     db.session.commit()


#     return render_template('index.html')


# @main.route('/add/publication', methods=['POST'])
# @login_required
# def add_remove_coauthor_pub():

#     id = request.form['id']
#     name = request.form['name']
    
#     stuff = {
#         'id' : id
#     }

#     kwargs = {
#         'name' : name,
#     }

#     print name

#     publication = Publication.query.filter_by(**stuff).first()
#     newpost = [User.query.filter_by(**kwargs).first()]
#     publication.researchers.extend(newpost)
#     db.session.commit()

#     return render_template('index.html')


# @main.route('/landing')
# @login_required

# def landing():  
#     page = request.args.get('page', 1, type=int)
#     pagination = Project.query.order_by(Project.timestamp.desc()).paginate(
#         page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
#         error_out=False)
#     posts = pagination.items
#     bookings = Booking.query.all()
#     print bookings
#     users = User.query.all()
#     projects = Project.query.all()
#     publications = Publication.query.all()
#     return render_template('landing.html', posts=posts,
#                            pagination=pagination, researchers=users, projects=projects, publications=publications, bookings=bookings)

# @main.route('/booking/edit/<int:id>', methods=['GET', 'POST'])
# @login_required
# def edit_booking(id):
#     kwargs = {
#     'id' : id
#     }

#     post = Booking.query.filter_by(**kwargs).first_or_404()

#     form = BookingForm(user=user)
    
#     if form.validate_on_submit():
#         post.researcher = current_user._get_current_object()
#         post.description = form.description.data 
#         post.available = 0
    
#         db.session.add(post)
#         print post
#         flash('The booking has been updated.')
#         return redirect(url_for('.landing'))

#     ptype = "Booking"
#     users = User.query.all()
#     projects = Project.query.all()
#     publications = Publication.query.all()

#     return render_template('edit_something.html', id=id, post=post, researchers=users, projects=projects, form=form, ptype=ptype, user=user, publications=publications)

# @main.route('/booking/edit/admin/<int:id>', methods=['GET', 'POST'])
# @login_required
# @admin_required
# def edit_booking_admin(id):
#     kwargs = {
#     'id' : id
#     }

#     post = Booking.query.filter_by(**kwargs).first_or_404()

#     form = BookingFormAdmin(user=user)
    
#     if form.validate_on_submit():
#         post.researcher = User.query.filter_by(id=form.researcher.data).first()
#         post.description = form.description.data 
#         post.available = form.available.data
    
#         db.session.add(post)
#         print post
#         flash('The booking has been updated.')
#         return redirect(url_for('.landing'))

#     form.week.data = post.day

#     if post.available == False:
        
#         form.researcher.data = post.researcher.id
#         form.description.data = post.description

#     ptype = "Booking Admin"
#     users = User.query.all()
#     projects = Project.query.all()
#     publications = Publication.query.all()

#     return render_template('edit_something.html', id=id, post=post, researchers=users, projects=projects, form=form, ptype=ptype, user=user, publications=publications)


# # Publications   
# @main.route('/publications/')
# @login_required
# def publicationpage():
#     page = request.args.get('page', 1, type=int)
#     pagination = Publication.query.order_by(Publication.timestamp.desc()).paginate(
#         page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
#         error_out=False)
#     posts = pagination.items
#     users = User.query.all()
#     projects = Project.query.all()
#     publications = Publication.query.all()
#     return render_template('publications.html', posts=posts,
#                            pagination=pagination, projects=projects, researchers=users, publications=publications)

# @main.route('/publications/project/<int:id>/')
# @login_required
# def projectpublications(id):
#     page = request.args.get('page', 1, type=int)
#     posts = Publication.query.filter_by(project_id=id)
#     users = User.query.all()
#     projects = Project.query.all()
#     publications = Publication.query.filter_by(project_id=id).all()
#     project = Project.query.filter_by(id=id).first()
#     return render_template('project_publication.html', posts=posts, projects=projects, researchers=users, publications=publications, project=project)

# @main.route('/publications/post', methods=['GET', 'POST'])
# @login_required
# def postpublication():
#     form = PublicationPostForm(user=user)
#     if current_user.can(Permission.WRITE_ARTICLES) and \
#             form.validate_on_submit():

#         post = Publication(full_title=form.full_title.data,
#                         synopsis=form.synopsis.data,
#                         website=form.website.data,
#                         citation=form.citation.data,
#                         project_id = form.project.data,
#                         researchers = [current_user._get_current_object()])
#         db.session.add(post)
#         return redirect(url_for('.publicationpage'))
#     page = request.args.get('page', 1, type=int)
#     pagination = Publication.query.order_by(Publication.timestamp.desc()).paginate(
#         page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
#         error_out=False)
#     posts = pagination.items
#     ptype = "Publication"
#     users = User.query.all()
#     projects = Project.query.all()
#     publications = Publication.query.all()
#     return render_template('post_something.html', form=form, researchers=users, posts=posts,
#                            pagination=pagination, ptype=ptype, projects=projects, publications=publications)


# @main.route('/publications/<int:id>') 
# @login_required
# def pubnamepage(id):
#     kwargs = {
#     'id' : id
#     }
#     post = Publication.query.filter_by(**kwargs).first_or_404()
#     users = User.query.all()
#     projects = Project.query.all()
#     publications = Publication.query.all()
#     return render_template('publication.html', researchers=users, projects=projects, post=post, id=id, publications=publications)

# @main.route('/publications/edit/<int:id>', methods=['GET', 'POST']) 
# @login_required
# def edit_publication(id):
#     kwargs = {
#     'id' : id
#     }
#     post = Publication.query.filter_by(**kwargs).first_or_404()
#     if current_user != post.researchers and \
#         not current_user.can(Permission.WRITE_ARTICLES): abort(403)
#     form = PublicationEditForm(user=user)
#     if form.validate_on_submit():

#         post.full_title = form.full_title.data
#         post.synopsis = form.synopsis.data 
#         post.website = form.website.data
#         post.citation = form.citation.data
#         post.project_id = form.project.data
#         db.session.add(post)
#         print post
#         flash('The post has been updated.')
#         return redirect(url_for('.pubnamepage', id=post.id))
#     form.full_title.data = post.full_title
#     form.synopsis.data = post.synopsis
#     form.website.data = post.website
#     form.citation.data = post.citation
#     form.project.data = post.project_id


#     ptype = "Publication"
#     users = User.query.all()
#     projects = Project.query.all()
#     publications = Publication.query.all()

#     return render_template('edit_something.html', id=id, post=post, researchers=users, projects=projects, form=form, ptype=ptype, user=user, publications=publications)



# # JSON fun
# @main.route('/researchersjson')
# @login_required
# def researchersjson():
#     researchers = [(u.name) for u in User.query.all()]
#     return jsonify(json_list=researchers) 

# @main.route('/json/<int:id>')
# @login_required
# def json(id):
#     kwargs = {
#         'id' : id
#     }

#     projects = Project.query.filter_by(**kwargs).first()
#     people = Project.query.filter_by(**kwargs).first()
#     alls = User.query.all()

#     inproject = []

#     rs = people.researchers

#     for research in rs:
#         inproject.append(research.name) 

#     print inproject

#     researchers = {
#     'in' : [],
#     'out' : []
#     }

#     allresearchers = []

#     for researcher in alls:
#         allresearchers.append(researcher.name)


#     print allresearchers

#     for researcher in alls:
#         print researcher.name
#         if researcher.name in inproject:
#             ins = {
#             'name' : researcher.name
#             }

#             researchers["in"].append(ins)
#         if researcher.name not in inproject:
#             out = {
#             'name' : researcher.name
#             }

#             print out
#             researchers["out"].append(out)


#     return jsonify(researchers=researchers) 

# @main.route('/jsonpub/<int:id>')
# @login_required
# def jsonpub(id):
#     kwargs = {
#         'id' : id
#     }

#     publications = Publication.query.filter_by(**kwargs).first()
#     people = Publication.query.filter_by(**kwargs).first()
#     alls = User.query.all()

#     inproject = []

#     rs = people.researchers

#     for research in rs:
#         inproject.append(research.name) 

#     print inproject

#     researchers = {
#     'in' : [],
#     'out' : []
#     }

#     allresearchers = []

#     for researcher in alls:
#         allresearchers.append(researcher.name)


#     print allresearchers

#     for researcher in alls:
#         print researcher.name
#         if researcher.name in inproject:
#             ins = {
#             'name' : researcher.name
#             }

#             researchers["in"].append(ins)
#         if researcher.name not in inproject:
#             out = {
#             'name' : researcher.name
#             }

#             print out
#             researchers["out"].append(out)


#     return jsonify(researchers=researchers) 

# @main.route('/projectsjson')
# @login_required
# def projectsjson():
#     projects = [(p.urlname) for p in Project.query.all()]
#     return jsonify(json_list=projects) 

