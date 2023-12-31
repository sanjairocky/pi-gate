from flask import Blueprint, request, redirect, url_for, render_template
from models import Project, App, Cluster, Quota, Region, Stage, Secret, AppSecret, Pipeline
from kubernetes import config, client
from utils.kube_templates import get_kube_template, sanitize_for_kube

from .workflows import conford_api

from typing import List

ci_api = Blueprint('ci', __name__,  url_prefix='ci')

ci_api.register_blueprint(conford_api)


@ci_api.get('/')
def index():
    features = [{'name': 'Projects',
                 'description': 'Manage RnCp projects',
                 'link': '/ci/projects'},
                {'name': 'Clusters',
                 'description': "Manage connected clusters",
                 'link': '/ci/clusters'}, {'name': 'Regions',
                'description': "Manage cluster regions",
                                           'link': '/ci/regions'},
                {'name': 'Confords',
                'description': "Manage App Confords",
                 'link': '/ci/confords'}
                ]
    return render_template('ci.html', features=features)


# Get all projects

@ci_api.route('/projects')
def projects():
    return render_template('projects.html', projects=Project.all())


@ci_api.route('/clusters')
def clusters():
    return render_template('clusters.html', clusters=Cluster.all())


@ci_api.route('/regions')
def regions():
    return render_template('regions.html', regions=Region.all())


build_types = ['docker', 'node']

# Route for individual project pages


@ci_api.route('/projects/<int:project_id>', methods=['GET', 'POST'])
def project_detail(project_id):
    # Retrieve the specific project based on project_id
    project: Project = Project.query.filter_by(id=project_id).first()
    if project:
        if request.method == 'POST':
            kubectl = client.CoreV1Api(
                api_client=config.new_client_from_config())
            if 'delete' in request.form and request.form['delete']:
                try:
                    kubectl.delete_namespace(project.name)
                except:
                    pass
                for quota in project.quotas:
                    quota.delete()
                project.delete()
                return redirect("/ci/projects", code=302)
            elif 'active' in request.form and request.form['active']:
                delete = eval(request.form['active'])
                if project.active and delete:
                    kubectl.delete_namespace(project.name)
                elif not project.active and not delete:
                    kubectl.create_namespace(get_kube_template(
                        'create_ns.kube', project=project))
                    for quota in project.quotas:
                        quota.active = not delete
                        kubectl.create_namespaced_resource_quota(namespace=project.name, body=get_kube_template(
                            'create_quota.kube', project=project, quota=quota))
                project.active = not delete
                project.save()
        return render_template('project_detail.html', project=project)
    return redirect("/ci/projects", code=302)


@ci_api.route('/quotas/<int:quota_id>', methods=['POST'])
def quota_detail(quota_id):

    quota: Quota = Quota.query.get(quota_id)

    if not quota:
        return "Quota not found", 400

    if request.method == 'POST':
        kubectl = client.CoreV1Api(
            api_client=config.new_client_from_config())
        if request.form['delete']:
            delete = eval(request.form['delete'])
            if quota.active and delete:
                kubectl.delete_namespaced_resource_quota(
                    name=quota.name, namespace=quota.project.name)
            elif not quota.active and not delete:
                kubectl.create_namespaced_resource_quota(namespace=quota.project.name, body=get_kube_template(
                    'create_quota.kube', project=quota.project, quota=quota))
            quota.active = not delete
        quota.save()

    return redirect(f"/ci/projects/{quota.project_id}", code=302)

# Route for creating a new project


@ci_api.route('/projects/create_project', methods=['GET', 'POST'])
def create_project():
    error = None
    if request.method == 'POST':
        if Project.query.filter_by(
                name=request.form['name']).first():
            error = "Project already exists"
        if len(sanitize_for_kube(request.form['name'])) != len(request.form['name']):
            error = "name is not alpha numeric"
        if not error:
            new_project = Project()
            new_project.active = False
            new_project.name = request.form['name']
            new_project.description = request.form['description']
            new_project.save()
            return redirect(url_for('root.ci.projects'))
    return render_template('create_project.html', error=error)


@ci_api.route('/regions/create_region', methods=['GET', 'POST'])
def create_region():
    if request.method == 'POST':
        region = Region()
        region.name = request.form['name']
        region.description = request.form['description']
        region.country = request.form['country']
        region.save()
        return redirect(url_for('root.ci.regions'))
    return render_template('create_region.html', regions=Region.all())


@ci_api.route('/regions/<int:region_id>', methods=['GET', 'POST'])
def region_detail(region_id):
    # Retrieve the specific project based on region_id
    region: Region = Region.query.filter_by(id=region_id).first()
    if region:
        return render_template('region_detail.html', region=region)
    return redirect("/ci/regions", code=302)


@ci_api.route('/clusters/create_cluster', methods=['GET', 'POST'])
def create_cluster():
    error = None
    if request.method == 'POST':
        if Cluster.query.filter_by(
                name=request.form['name']).first():
            error = "Cluster already exists"
        if not error:
            cluster = Cluster()
            cluster.name = request.form['name']
            cluster.description = request.form['description']
            cluster.region_id = request.form['region_id']
            cluster.save()
            return redirect(url_for('root.ci.clusters'))
    return render_template('create_cluster.html', regions=Region.all(), error=error)


@ci_api.route('/clusters/<int:cluster_id>', methods=['GET', 'POST'])
def cluster_detail(cluster_id):
    # Retrieve the specific project based on cluster_id
    cluster: Cluster = Cluster.query.filter_by(id=cluster_id).first()
    if cluster:
        return render_template('cluster_detail.html', cluster=cluster)
    return redirect("/ci/clusters", code=302)


@ci_api.route('/projects/<int:project_id>/create_app', methods=['GET', 'POST'])
def create_app(project_id):
    project = Project.query.get(project_id)

    if not project:
        return "Project not found", 400

    if request.method == 'POST':
        new_app = App()
        new_app.name = request.form['name']
        new_app.description = request.form['description']
        new_app.repository_url = request.form['repository_url']
        new_app.project = project
        new_app.save()
        return redirect(url_for('root.ci.project_detail', project_id=project_id))

    return render_template('create_app.html', project=project, build_types=build_types)


@ci_api.route('/projects/<int:project_id>/create_quota', methods=['GET', 'POST'])
def create_quota(project_id):
    project = Project.query.get(project_id)
    error = None

    if not project:
        return "Project not found", 400

    if request.method == 'POST':
        if Quota.query.filter_by(
                project_id=project_id, cluster_id=request.form['cluster']).first():
            error = "Quota already exists"
        if len(sanitize_for_kube(request.form['name'])) != len(request.form['name']):
            error = "name is not alpha numeric"
        if not error:
            quota = Quota()
            quota.project_id = project_id
            quota.name = request.form['name']
            quota.cpu = int(request.form['cpu'])
            quota.memory = int(request.form['memory'])
            quota.cluster_id = request.form['cluster']
            quota.save()
            return redirect(url_for('root.ci.project_detail', project_id=project_id))

    return render_template('create_quota.html', project=project, clusters=Cluster.all(), error=error)


@ci_api.route('/project/<int:project_id>/app/<int:app_id>')
def app_detail(project_id, app_id):
    project = Project.query.get(project_id)
    if not project:
        return "Project not found", 400
    app = App.query.get(app_id)
    if not app:
        return "App not found", 400

    return render_template('app_detail.html', project=project, app=app)


@ci_api.route('/project/<int:project_id>/app/<int:app_id>/stages', methods=['GET', 'POST'])
def create_stage(project_id, app_id):
    project = Project.query.get(project_id)
    error = None
    if not project:
        return "Project not found", 400
    app = App.query.get(app_id)
    if not app:
        return "App not found", 400
    if request.method == 'POST':
        if Stage.query.filter_by(
                app_id=app_id, quota_id=request.form['quota_id']).first():
            error = "Stage already exists"
        if not error:
            stage = Stage()
            stage.name = request.form['name']
            stage.description = request.form['description']
            stage.c_names = request.form['c_names']
            stage.app_id = app_id
            stage.quota_id = request.form['quota_id']
            stage.refs = request.form['refs']
            stage.save()
            return redirect(url_for('root.ci.app_detail', project_id=project_id, app_id=app_id))
    return render_template('create_stage.html', app=app, project=project, error=error)


@ci_api.route('/project/<int:project_id>/app/<int:app_id>/stages/<int:quota_id>', methods=['DELETE'])
def delete_stage(project_id, app_id, quota_id):
    project: Project = Project.query.get(project_id)
    if not project:
        return "Project not found", 400
    app: App = App.query.get(app_id)
    if not app:
        return "App not found", 400

    stage: Stage = Stage.query.filter_by(
        app_id=app_id, quota_id=quota_id).first()

    if not stage:
        return "stage not found", 404

    stage.delete()

    return "deleted", 200


@ci_api.route('/project/<int:project_id>/app/<int:app_id>/secrets', methods=['GET', 'POST'])
def create_secret(project_id, app_id):
    project = Project.query.get(project_id)
    error = None
    if not project:
        return "Project not found", 400
    app = App.query.get(app_id)
    if not app:
        return "App not found", 400
    if request.method == 'POST':
        secret = Secret()
        secret.name = request.form['name']
        secret.value = request.form['value']
        secret.save()
        app_secret = AppSecret()
        app_secret.app_id = app_id
        app_secret.secret = secret
        app_secret.mount_path = request.form['mount_path']
        app_secret.base_path = request.form['base_path']
        app_secret.target_name = request.form['target_name']
        if request.form['env'] == 'True':
            app_secret.env = True
        else:
            app_secret.env = False
        app_secret.save()
        return redirect(url_for('root.ci.app_detail', project_id=project_id, app_id=app_id))
    return render_template('create_secret.html', app=app, project=project, error=error)


@ci_api.route('/project/<int:project_id>/app/<int:app_id>/secrets/<int:secret_id>', methods=['DELETE'])
def delete_secret(project_id, app_id, secret_id):
    project: Project = Project.query.get(project_id)
    if not project:
        return "Project not found", 400
    app: App = App.query.get(app_id)
    if not app:
        return "App not found", 400

    secret: List(AppSecret) = list(filter(
        lambda s: s.secret_id == secret_id, app.secrets))

    if len(secret) > 0:
        for s in secret:
            s.secret.delete()
            s.delete()

    return "deleted", 200


@ci_api.route('/project/<int:project_id>/app/<int:app_id>/deploy_app', methods=['GET'])
def deploy_app(project_id, app_id):
    project = Project.query.get(project_id)
    if not project:
        return "Project not found", 400
    app = App.query.get(app_id)
    if not app:
        return "App not found", 400

    for p in Pipeline.query.filter_by(app_id=app_id, version='latest', active=True):
        p.active = False
        p.save()

    pipeline = Pipeline()
    pipeline.app_id = app_id
    pipeline.artifactory_id = 1
    pipeline.build_skip = False
    pipeline.deploy_skip = True
    pipeline.active = True
    pipeline.version = 'latest'
    pipeline.artifact = f"{project.name}-{app.name}"
    pipeline.log = ""
    pipeline.save()
    return redirect(url_for('root.ci.app_detail', project_id=project_id, app_id=app_id))
