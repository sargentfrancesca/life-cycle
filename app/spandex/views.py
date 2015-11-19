from flask import render_template, redirect, url_for, abort, flash, request,\
    current_app, jsonify
from flask.ext.login import login_required, current_user
from . import spandex
from .forms import EditProfileForm, EditProfileAdminForm, ProjectPostForm, ProjectEditForm, BookingForm, BookingFormAdmin, PublicationPostForm, PublicationEditForm
from .. import db
from .models import Permission, Role, User, Project, Publication, Booking, coauthors
from ..decorators import admin_required
import re
from jinja2 import evalcontextfilter, Markup, escape
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
import csv
import twitter



def anon_view(model):
    # For anon users, show only active objects
    if current_user.is_authenticated():
        if model == Publication:
            objects = model.query.order_by(model.title.asc(), model.year_published.desc(), model.active.desc()).all()
        else:
            objects = model.query.order_by(model.active.desc()).all()
    else:
        if model == Publication:
            objects = model.query.order_by(model.title.asc(), model.year_published.desc()).filter_by(active=True).all()
        else:
            objects = model.query.filter_by(active=True).all()



    return objects

def nav_init():
    # List all navigation items
    nav = { 'researchers' : '', 'projects' : '', 'publications' : ''}
    nav['researchers'] = User.query.order_by(User.name.asc()).all()
    nav['projects'] = anon_view(Project)
    nav['publications'] = anon_view(Publication)

    return nav

@spandex.route('/')
def index():
    api = twitter.Api(consumer_key='4G7C729hkGfcpHDI8zCTFZkBA',
                      consumer_secret='hA67P0DOFE8jISpIMgqp25rAxh2WpEhtrlyEQw6diluaJwdGkm',
                      access_token_key='23463646-j5rbrfFGlMPmQMK7dsL1IC6f5g8K5GuccwKykU8PK',
                      access_token_secret='VOsJmHgp7o8gkMxlB5ffMRjeTTD3wIAx2MO2CYLA37O2r')

    twitter_user = "DaveHodgson00"
    statuses = api.GetUserTimeline(screen_name=twitter_user)

    twitter_statuses = []

    for s in statuses:
        status = {}
        status["text"] = s.text
        status["status_id"] = s.id

        if s.media != []:
            status["media"] = []
            for media in s.media:
                media_item = {}
                media_item["display_url"] = media["display_url"]
                media_item["media_url"] = media["media_url"]
                media_item["type"] = media["type"]
                status["media"].append(media_item)


        status["created_date"] = s.created_at
        
        usr = s.user
        status["user_id"] = usr.id
        status["user_name"] = usr.name 
        status["profile_background_color"] = usr.profile_background_color
        status["profile_background_image_url"] = usr.profile_background_image_url
        status["profile_image_url"] = usr.profile_image_url
        status["profile_link_color"] = usr.profile_link_color
        status["user_url"] = usr.url
        status["profile_sidebar_fill_color"] = usr.profile_sidebar_fill_color
        status["user_screen_name"] = usr.screen_name

        twitter_statuses.append(status)

    return render_template('home.html', nav=nav_init(), tweets=twitter_statuses)

def unicode_csv_reader(utf8_data, **kwargs):
    csv_reader = csv.reader(utf8_data, **kwargs)
    for row in csv_reader:
        yield [unicode(cell, 'utf-8') for cell in row]

@spandex.route('/dave-cite')
def dave():
    
    filename = 'citations.csv'
    reader = unicode_csv_reader(open(filename))
    allCitations = []
    
    for i, row in enumerate(reader):
        if i != 0:
            allCitations.append({"authors": row[0], "title": row[1], "publication": row[2], "volume" : row[3], "number" : row[4], "pages" : row[5], "year": row[6], "publisher": row[7]})

    for citation in allCitations:
        string = citation["authors"][:-2] + ".(" + citation["year"] + "). " + citation["title"] + ". " + citation["publication"]
        if citation["volume"] != '':
            string += ", " + citation["volume"]
        if citation["number"] != '':
            string += "(" + citation["number"] + ") "
        if citation["pages"] != '':
            string += ", " + citation["pages"]

        string += '.'

        
        
        publication = Publication()
        publication.other_researchers= citation["authors"].encode('ascii', 'ignore')
        publication.full_title = citation["title"].encode('ascii', 'ignore')
        publication.citation= string.encode('ascii', 'ignore')
        publication.researchers = [User.query.get(6)]

        db.session.add(publication)


    db.session.commit()

    return "Hi"

# Researchers
@spandex.route('/researchers/')
def researcherpage():
    page = request.args.get('page', 1, type=int)
    pagination = User.query.order_by(User.name.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    users = User.query.order_by(User.name.asc()).all()
    return render_template('researchers.html', nav=nav_init(), researchers=users)

@spandex.route('/researchers/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()

    posts = user.projects.order_by(Project.timestamp.desc())

    if user.publications:
        publications = user.publications.filter_by(active=True).order_by(Publication.year_published.desc())[:5]


    return render_template('user.html', nav=nav_init(), user=user, posts=posts, publications=publications)

@spandex.route('/researchers/<user>/projects')
def user_projects(user):
    user = User.query.filter_by(username=user).first() 
    if user is None:
        abort(404)

    page = request.args.get('page', 1, type=int)

    pagination = Project.query.filter(Project.researchers.any(id=user.id)).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items

    ptype = "Project"

    return render_template('projects.html', user=user, posts=posts, ptype=ptype, nav=nav_init())


# Profile Editing
@spandex.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        tweet = re.sub('[@]', '', form.twitter.data)

        current_user.name = form.name.data
        current_user.jobtitle = form.jobtitle.data 
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        current_user.quals = form.quals.data
        current_user.pub_email = form.pub_email.data
        current_user.website = form.website.data
        current_user.twitter = form.twitter.data
        current_user.twitter_name = tweet
        current_user.linkedin = form.linkedin.data
        current_user.google = form.google.data
        current_user.google_scholar = form.google_scholar.data
        current_user.research_gate = form.research_gate.data
        db.session.add(current_user)
        flash('Your profile has been updated.')
        return redirect(url_for('.user', username=current_user.username))
    form.name.data = current_user.name
    form.jobtitle.data = current_user.jobtitle
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    form.quals.data = current_user.quals
    form.pub_email.data = current_user.pub_email
    form.website.data = current_user.website
    form.twitter.data = current_user.twitter
    form.linkedin.data = current_user.linkedin
    form.google.data = current_user.google
    form.google_scholar.data = current_user.google_scholar
    form.research_gate.data = current_user.research_gate

    ptype = "Profile"
    user = current_user.name
    return render_template('edit_something.html', user=user, form=form, ptype=ptype, nav=nav_init())


@spandex.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        tweet = re.sub('[@]', '', form.twitter.data)

        user.email = form.email.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.name = form.name.data
        user.jobtitle = form.jobtitle.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        user.quals = form.quals.data
        user.pub_email = form.pub_email.data
        user.website = form.website.data
        user.twitter = form.twitter.data
        user.twitter_name = tweet
        user.linkedin = form.linkedin.data
        user.google = form.google.data
        user.google_scholar = form.google_scholar.data
        user.research_gate = form.research_gate.data
        user.tw_confirmed = form.tw_confirmed.data
        user.tw_widget_id = form.tw_widget_id.data
        db.session.add(user)
        flash('The profile has been updated.')
        return redirect(url_for('.user', username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.name.data = user.name
    form.jobtitle.data = user.jobtitle
    form.location.data = user.location
    form.about_me.data = user.about_me
    form.quals.data = user.quals
    form.pub_email.data = user.pub_email
    form.website.data = user.website
    form.twitter.data = user.twitter
    form.linkedin.data = user.linkedin
    form.google.data = user.google
    form.google_scholar.data = user.google_scholar
    form.research_gate.data = user.research_gate
    form.tw_confirmed.data = user.tw_confirmed
    form.tw_widget_id.data = user.tw_widget_id

    ptype = "Profile"
    return render_template('edit_something.html', form=form, user=user, ptype=ptype, nav=nav_init())

# Projects
@spandex.route('/projects/')
def projectpage():
    page = request.args.get('page', 1, type=int)
    pagination = Project.query.filter_by(active=True).order_by(Project.active.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
   
    projects = Project.query.filter_by(active=True).order_by(Project.title.desc()).all()

    return render_template('projects.html', posts=posts,
                           pagination=pagination, projects=projects, nav=nav_init())

@spandex.route('/projects/user/<int:id>')
def userprojectpage(id):
    page = request.args.get('page', 1, type=int)
    pagination = Project.query.filter_by(active=True).order_by(Project.active.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
   
    projects = Project.query.filter(Project.researchers.any(id=id)).all()


    return render_template('projects.html', posts=posts,
                           pagination=pagination, projects=projects, nav=nav_init())

@spandex.route('/projects/<int:id>')
def projnamepage(id):
    kwargs = {
    'id' : id
    }


    post = Project.query.filter_by(**kwargs).first_or_404()

    if post.active == True:
        return render_template('project.html', post=post, id=id, nav=nav_init())
       
    else:
        if current_user.is_authenticated():
            return render_template('project.html', post=post, id=id, nav=nav_init())
        else:
            return redirect(url_for('.index'))



@spandex.route('/projects/post', methods=['GET', 'POST'])
@login_required
def postproject():
    form = ProjectPostForm()
    if current_user.can(Permission.WRITE_ARTICLES) and \
            form.validate_on_submit():
        tweet = re.sub('[@]', '', form.twitter.data)
        post = Project(title=form.title.data,
                        full_title=form.full_title.data,
                        synopsis=form.synopsis.data,
                        website=form.website.data,
                        twitter=form.twitter.data,
                        twitter_name = tweet,
                        facebook=form.facebook.data,
                        active = form.active.data,
                        researchers = [current_user._get_current_object()])
        db.session.add(post)
        return redirect(url_for('spandex.projectpage'))
    page = request.args.get('page', 1, type=int)
    pagination = Project.query.order_by(Project.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    ptype = "Project"
    return render_template('post_something.html', form=form, posts=posts,
                           pagination=pagination, ptype=ptype, nav=nav_init())


@spandex.route('/projects/edit/<int:id>', methods=['GET', 'POST']) 
@login_required
def edit_project(id):
    
    kwargs = {
    'id' : id
    }

    post = Project.query.filter_by(**kwargs).first()

    if current_user != post.researchers and \
        not current_user.can(Permission.WRITE_ARTICLES): abort(403)
    form = ProjectEditForm()
    if form.validate_on_submit():
        tweet = re.sub('[@]', '', form.twitter.data)
        post.title = form.title.data
        post.full_title = form.full_title.data
        post.synopsis = form.synopsis.data 
        post.website = form.website.data
        post.twitter = form.twitter.data
        post.twitter_name = tweet
        post.facebook = form.facebook.data
        post.active = form.active.data
        db.session.add(post)
        flash('The post has been updated.')
        return redirect(url_for('spandex.projectpage', id=post.id))


    form.title.data = post.title
    form.full_title.data = post.full_title
    form.synopsis.data = post.synopsis
    form.website.data = post.website
    form.twitter.data = post.twitter
    form.facebook.data = post.facebook
    form.active.data = post.active

    ptype = "Project"
    return render_template('edit_something.html', id=id, post=post, form=form, ptype=ptype, user=user, nav=nav_init())


@spandex.route('/delete/', methods=['POST'])
@login_required
def delete_user():

    id = request.form['id']
    name = request.form['name']

    stuff = {
        'id' : id
    }

    kwargs = {
        'name' : name,
    }

    project = Project.query.filter_by(**stuff).first()
    oldpost = User.query.filter_by(**kwargs).first()
    project.researchers.remove(oldpost)
    db.session.commit()

    return render_template('index.html')

@spandex.route('/delete/publication', methods=['POST'])
@login_required
def delete_user_pub():

    id = request.form['id']
    name = request.form['name']

    stuff = {
        'id' : id
    }

    kwargs = {
        'name' : name,
    }

    publication = Publication.query.filter_by(**stuff).first()
    oldpost = User.query.filter_by(**kwargs).first()
    publication.researchers.remove(oldpost)

    db.session.commit()

    return render_template('index.html')


@spandex.route('/add/', methods=['POST'])
@login_required
def add_remove_coauthor():

    id = request.form['id']
    name = request.form['name']
    
    stuff = {
        'id' : id
    }

    kwargs = {
        'name' : name,
    }


    project = Project.query.filter_by(**stuff).first()
    newpost = [User.query.filter_by(**kwargs).first()]
    project.researchers.extend(newpost)
    db.session.commit()


    return render_template('index.html')


@spandex.route('/add/publication', methods=['POST'])
@login_required
def add_remove_coauthor_pub():

    id = request.form['id']
    name = request.form['name']
    
    stuff = {
        'id' : id
    }

    kwargs = {
        'name' : name,
    }


    publication = Publication.query.filter_by(**stuff).first()
    newpost = [User.query.filter_by(**kwargs).first()]
    publication.researchers.extend(newpost)
    db.session.commit()

    return render_template('index.html')


@spandex.route('/landing')
@login_required

def landing():  
    page = request.args.get('page', 1, type=int)
    pagination = Project.query.order_by(Project.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    bookings = Booking.query.all()
    return render_template('landing.html', posts=posts,
                           pagination=pagination, nav=nav_init(), bookings=bookings)

@spandex.route('/booking/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_booking(id):
    kwargs = {
    'id' : id
    }

    post = Booking.query.filter_by(**kwargs).first_or_404()

    form = BookingForm(user=user)
    
    if form.validate_on_submit():
        post.researcher = current_user._get_current_object()
        post.description = form.description.data 
        post.available = 0
    
        db.session.add(post)
        flash('The booking has been updated.')
        return redirect(url_for('.landing'))

    ptype = "Booking"

    return render_template('edit_something.html', id=id, post=post, form=form, ptype=ptype, user=user, nav=nav_init())

@spandex.route('/booking/add', methods=['GET', 'POST'])
@login_required
def add_booking():
    form = BookingFormAdmin(user=user)
    if current_user.can(Permission.WRITE_ARTICLES) and \
            form.validate_on_submit():
        
        booking = Booking()
        booking.day = form.week.data
        booking.researcher = User.query.get_or_404(form.researcher.data)
        booking.description = form.description.data

        db.session.add(booking)
        return redirect(url_for('spandex.landing'))

    return render_template('post_something.html', form=form, nav=nav_init())

@spandex.route('/booking/edit/admin/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_booking_admin(id):
    kwargs = {
    'id' : id
    }

    post = Booking.query.filter_by(**kwargs).first_or_404()

    form = BookingFormAdmin(user=user)
    
    if form.validate_on_submit():
        post.researcher = User.query.filter_by(id=form.researcher.data).first()
        post.description = form.description.data 
        post.available = form.available.data
    
        db.session.add(post)
        flash('The booking has been updated.')
        return redirect(url_for('.landing'))

    form.week.data = post.day

    if post.available == False:
        
        form.researcher.data = post.researcher.id
        form.description.data = post.description

    ptype = "Booking Admin"

    return render_template('edit_something.html', id=id, post=post, form=form, ptype=ptype, user=user, nav=nav_init())


# Publications   
@spandex.route('/publications/')
def publicationpage():
    page = request.args.get('page', 1, type=int)
    pagination = Publication.query.order_by(Publication.year_published.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    publications = Publication.query.order_by(Publication.year_published.desc(), Publication.active.desc()).all()

    title = "All Publications"

    return render_template('publications.html', posts=posts,
                           pagination=pagination, publications=publications, title=title, nav=nav_init())

@spandex.route('/publications/project/<int:id>/')
def projectpublications(id):
    page = request.args.get('page', 1, type=int)
    posts = Publication.query.filter_by(project_id=id)
    publications = Publication.query.filter_by(project_id=id).all()
    project = Project.query.filter_by(id=id).first()
    return render_template('project_publication.html', posts=posts, publications=publications, project=project, nav=nav_init())

@spandex.route('/publications/user/<int:id>/')
def userpublications(id):
    user = User.query.filter_by(id=id).first_or_404()
    page = request.args.get('page', 1, type=int)
    pagination = Publication.query.filter_by(researcher_id=id).order_by(Publication.year_published.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items

    publications = Publication.query.filter(Publication.researchers.any(id=id)).order_by(Publication.year_published.desc(), Publication.active.desc()).all()
    
    title = "All Publications by "+ user.name

    print title
    return render_template('publications.html', posts=posts,
                           pagination=pagination, publications=publications, title=title, nav=nav_init())

@spandex.route('/publications/post', methods=['GET', 'POST'])
@login_required
def postpublication():
    form = PublicationPostForm(user=user)
    if current_user.can(Permission.WRITE_ARTICLES) and \
            form.validate_on_submit():

        

        post = Publication() 

        post.full_title=form.full_title.data
        post.synopsis=form.synopsis.data
        post.website=form.website.data
        post.citation=form.citation.data
        
        if form.project.data != 1000001:
            post.project_id = form.project.data
        post.active = form.active.data
        post.researchers = [current_user._get_current_object()]

        db.session.add(post)
        return redirect(url_for('.publicationpage'))
    page = request.args.get('page', 1, type=int)
    pagination = Publication.query.order_by(Publication.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    ptype = "Publication"
    return render_template('post_something.html', form=form, #posts=posts, pagination=pagination, 
                                ptype=ptype, nav=nav_init())


@spandex.route('/publications/<int:id>') 
def pubnamepage(id):
    kwargs = {
    'id' : id
    }
    post = Publication.query.filter_by(**kwargs).first_or_404()

    if post.active == True:
        return render_template('publication.html', post=post, id=id, nav=nav_init())
       
    else:
        if current_user.is_authenticated():
            return render_template('publication.html', post=post, id=id, nav=nav_init())
        else:
            return redirect(url_for('.index'))

@spandex.route('/publications/edit/<int:id>', methods=['GET', 'POST']) 
@login_required
def edit_publication(id):
    kwargs = {
    'id' : id
    }
    post = Publication.query.filter_by(**kwargs).first_or_404()
    if current_user != post.researchers and \
        not current_user.can(Permission.WRITE_ARTICLES): abort(403)
    form = PublicationEditForm(user=user)
    if form.validate_on_submit():

        post.full_title = form.full_title.data
        post.synopsis = form.synopsis.data 
        post.website = form.website.data
        post.citation = form.citation.data
        if form.project.data != 1000001:
            post.project_id = form.project.data
        post.active = form.active.data
        db.session.add(post)
        flash('The post has been updated.')
        return redirect(url_for('.pubnamepage', id=post.id))
    form.full_title.data = post.full_title
    form.synopsis.data = post.synopsis
    form.website.data = post.website
    form.citation.data = post.citation
    form.project.data = post.project_id
    form.active.data = post.active


    ptype = "Publication"

    return render_template('edit_something.html', id=id, post=post, form=form, ptype=ptype, user=user, nav=nav_init())



# JSON fun
@spandex.route('/researchersjson')
def researchersjson():
    researchers = [(u.name) for u in User.query.all()]
    return jsonify(json_list=researchers) 

@spandex.route('/json/<int:id>')
def json(id):
    kwargs = {
        'id' : id
    }

    projects = Project.query.filter_by(**kwargs).first()
    people = Project.query.filter_by(**kwargs).first()
    alls = User.query.all()

    inproject = []

    rs = people.researchers

    for research in rs:
        inproject.append(research.name) 


    researchers = {
    'in' : [],
    'out' : []
    }

    allresearchers = []

    for researcher in alls:
        allresearchers.append(researcher.name)



    for researcher in alls:
        if researcher.name in inproject:
            ins = {
            'name' : researcher.name
            }

            researchers["in"].append(ins)
        if researcher.name not in inproject:
            out = {
            'name' : researcher.name
            }

            researchers["out"].append(out)


    return jsonify(researchers=researchers) 

@spandex.route('/jsonpub/<int:id>')
def jsonpub(id):
    kwargs = {
        'id' : id
    }

    publications = Publication.query.filter_by(**kwargs).first()
    people = Publication.query.filter_by(**kwargs).first()
    alls = User.query.all()

    inproject = []

    rs = people.researchers

    for research in rs:
        inproject.append(research.name) 


    researchers = {
    'in' : [],
    'out' : []
    }

    allresearchers = []

    for researcher in alls:
        allresearchers.append(researcher.name)


    for researcher in alls:
        if researcher.name in inproject:
            ins = {
            'name' : researcher.name
            }

            researchers["in"].append(ins)
        if researcher.name not in inproject:
            out = {
            'name' : researcher.name
            }

            researchers["out"].append(out)


    return jsonify(researchers=researchers) 

@spandex.route('/projectsjson')
def projectsjson():
    projects = [(p.urlname) for p in Project.query.all()]
    return jsonify(json_list=projects) 

@spandex.route('/migrateyears')
def migrate_year():
    publications = Publication.query.all()
    for p in publications:
        group = re.findall(r"\D(\d{4})\D", p.citation)
        try:
            year = int(group[0])
        except:
            year = 0001
        finally:
            if year > 1900:
                p.year_published = year
                db.session.add(p)
                db.session.commit()
    return "Done"
            
     
@spandex.route('/delete_user/<usr>')
def delete_researcher(usr):
    user = User.query.filter_by(name=usr).first()
    db.session.delete(user)
    return jsonify({ 'hello' : 'there '}) 