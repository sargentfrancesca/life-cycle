from flask import render_template, redirect, url_for, abort, flash, request,\
    current_app, jsonify
from flask.ext.login import login_required, current_user
from . import main
from .forms import EditProfileForm, EditProfileAdminForm, ProjectPostForm, ProjectEditForm
from .. import db
from ..models import Permission, Role, User, Project
from ..decorators import admin_required
import re
from jinja2 import evalcontextfilter, Markup, escape

@main.route('/')
def index():
    users = User.query.all()
    projects = Project.query.all()
    return render_template('index.html', researchers=users, projects=projects)


@main.route('/projects/')
def projectpage():
    page = request.args.get('page', 1, type=int)
    pagination = Project.query.order_by(Project.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    users = User.query.all()
    projects = Project.query.all()
    return render_template('projects.html', posts=posts,
                           pagination=pagination, projects=projects, researchers=users)

@main.route('/researchers/')
def researcherpage():
    page = request.args.get('page', 1, type=int)
    pagination = User.query.order_by(User.name.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    users = User.query.all()
    projects = Project.query.all()
    return render_template('researchers.html', posts=posts,
                           pagination=pagination, projects=projects, researchers=users)

@main.route('/researchers/<user>/projects')
def user_projects(user):
    user = User.query.filter_by(username=user).first() 
    if user is None:
        abort(404)

    page = request.args.get('page', 1, type=int)
    posts = user.posts.order_by(Project.timestamp.desc()).all

    pagination = Project.query.order_by(Project.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items

    users = User.query.all()
    projects = Project.query.all()
    ptype = "Project"
    return render_template('projects.html', user=user, researchers=users, posts=posts, projects=projects, ptype=ptype)


@main.route('/projects/edit/<int:id>', methods=['GET', 'POST']) 
@login_required
def edit_project(id):
    post = Project.query.get_or_404(id)
    if current_user != post.researcher and \
        not current_user.can(Permission.ADMINISTER): abort(403)
    form = ProjectEditForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.urlname = form.urlname.data
        post.full_title = form.full_title.data
        post.brief_synopsis = ''
        post.synopsis = form.synopsis.data 
        post.website = form.website.data
        post.twitter = form.twitter.data
        post.facebook = form.facebook.data

        researchers = [x.strip() for x in form.researchers.data.split(',')]
        for researcher in researchers:
            extend_researchers = [User.query.filter(User.name == researcher).first()]
            post.researchers.extend(extend_researchers)

        # extend_researchers = [User.query.filter(User.name == form.researchers.data).first()]
        
        db.session.add(post)
        flash('The post has been updated.')
        return redirect(url_for('.index', id=post.id))
    form.title.data = post.title
    form.urlname.data = post.urlname
    form.full_title.data = post.full_title
    form.brief_synopsis.data = post.brief_synopsis
    form.synopsis.data = post.synopsis
    form.website.data = post.website
    form.twitter.data = post.twitter
    form.facebook.data = post.facebook
    form.researchers.data = ''

    ptype = "Project"
    users = User.query.all()
    projects = Project.query.all()
    return render_template('edit_something.html', id=id, post=post, researchers=users, projects=projects, form=form, ptype=ptype, user=user)


@main.route('/projects/<int:id>') 
@login_required
def projpage(id):
    post = Project.query.get_or_404(id)
    users = User.query.all()
    projects = Project.query.all()
    return render_template('project.html', researchers=users, projects=projects, post=post, id=id)



@main.route('/landing')
@login_required
def landing():  
    page = request.args.get('page', 1, type=int)
    pagination = Project.query.order_by(Project.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    users = User.query.all()
    projects = Project.query.all()
    return render_template('landing.html', posts=posts,
                           pagination=pagination, researchers=users, projects=projects)


@main.route('/projects/post', methods=['GET', 'POST'])
@login_required
def postproject():
    form = ProjectPostForm()
    if current_user.can(Permission.WRITE_ARTICLES) and \
            form.validate_on_submit():
            
        post = Project(title=form.title.data,
                        urlname=form.urlname.data,
                        full_title=form.full_title.data,
                        brief_synopsis=form.brief_synopsis.data,
                        synopsis=form.synopsis.data,
                        website=form.website.data,
                        twitter=form.twitter.data,
                        facebook=form.facebook.data,
                        researchers = [current_user._get_current_object()])
        db.session.add(post)
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = Project.query.order_by(Project.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    ptype = "Project"
    users = User.query.all()
    projects = Project.query.all()
    return render_template('post_something.html', form=form, researchers=users, posts=posts,
                           pagination=pagination, ptype=ptype, projects=projects)


@main.route('/researchers/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    pagination = user.posts.order_by(Project.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    users = User.query.all()
    projects = Project.query.all()
    return render_template('user.html', user=user, researchers=users, posts=posts,
                           pagination=pagination, projects=projects)


@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.jobtitle = form.jobtitle.data 
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        current_user.quals = form.quals.data
        current_user.pub_email = form.pub_email.data
        current_user.website = form.website.data
        current_user.twitter = form.twitter.data
        current_user.linkedin = form.linkedin.data
        current_user.google = form.google.data
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

    ptype = "Profile"
    user = current_user.name
    users = User.query.all()
    projects = Project.query.all()
    return render_template('edit_something.html', researchers=users, user=user, form=form, ptype=ptype, projects=projects)


@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
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
        user.linkedin = form.linkedin.data
        user.google = form.google.data
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

    ptype = "Profile"
    users = User.query.all()
    projects = Project.query.all()
    return render_template('edit_something.html', researchers=users, form=form, user=user, ptype=ptype, projects=projects)


@main.route('/researchersjson')
def researchersjson():
    researchers = [(u.name) for u in User.query.all()]
    return jsonify(json_list=researchers) 

