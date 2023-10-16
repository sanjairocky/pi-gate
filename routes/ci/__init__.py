from flask import Blueprint, request, redirect, url_for, render_template
from models import Project, App

ci_api = Blueprint('ci', __name__,  url_prefix='ci')


@ci_api.get('/')
def hello_git():
    return 'hello from ci path', 200


# Get all projects

@ci_api.route('/projects')
def index():
    return render_template('projects.html', projects=Project.all())


build_types = ['docker', 'node']

# Route for individual project pages


@ci_api.route('/projects/<int:project_id>')
def project_detail(project_id):
    # Retrieve the specific project based on project_id
    project = Project.query.filter_by(id=project_id).first()
    if project:
        return render_template('project_detail.html', project=project)
    else:
        return "Project not found", 404

# Route for creating a new project


@ci_api.route('/projects/create_project', methods=['GET', 'POST'])
def create_project():
    if request.method == 'POST':
        new_project = Project()
        new_project.name = request.form['name']
        new_project.description = request.form['description']
        new_project.save()
        return redirect(url_for('root.ci.index'))

    return render_template('create_project.html')


@ci_api.route('/projects/<int:project_id>/create_app', methods=['GET', 'POST'])
def create_app(project_id):
    project = Project.query.get(project_id)

    if not project:
        return "Project not found", 404

    if request.method == 'POST':
        new_app = App()
        new_app.name = request.form['name']
        new_app.description = request.form['description']
        new_app.repository_url = request.form['repository_url']
        new_app.build_type = request.form['build_type']
        new_app.project = project
        new_app.save()
        return redirect(url_for('root.ci.project_detail', project_id=project_id))

    return render_template('create_app.html', project=project, build_types=build_types)


@ci_api.route('/project/<int:project_id>/app/<int:app_id>')
def app_detail(project_id, app_id):
    project = Project.query.get(project_id)
    if not project:
        return "Project not found", 404
    app = App.query.get(app_id)
    if not app:
        return "App not found", 404

    return render_template('app_detail.html', project=project, app=app)
