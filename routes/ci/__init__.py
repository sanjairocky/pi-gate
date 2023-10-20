from flask import Blueprint, request, redirect, url_for, render_template
from models import Project, App, Cluster, Quota, Region
from kubernetes import config, client
from utils.kube_templates import get_kube_template

ci_api = Blueprint('ci', __name__,  url_prefix='ci')


@ci_api.get('/')
def index():
    features = [{'name': 'Projects',
                 'description': 'Manage RnCp projects',
                 'link': '/ci/projects'},
                {'name': 'Clusters',
                 'description': "Manage connected clusters",
                 'link': '/ci/clusters'}
                ]
    return render_template('ci.html', features=features)


# Get all projects

@ci_api.route('/projects')
def projects():
    return render_template('projects.html', projects=Project.all())


@ci_api.route('/clusters')
def clusters():
    return render_template('clusters.html', clusters=Cluster.all())


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
            if request.form['delete']:
                delete = eval(request.form['delete'])
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
    if request.method == 'POST':
        new_project = Project()
        new_project.active = False
        new_project.name = request.form['name']
        new_project.description = request.form['description']
        new_project.save()
        return redirect(url_for('root.ci.projects'))
    return render_template('create_project.html')


@ci_api.route('/clusters/create_cluster', methods=['GET', 'POST'])
def create_cluster():
    if request.method == 'POST':
        cluster = Cluster()
        cluster.name = request.form['name']
        cluster.description = request.form['description']
        cluster.region_id = request.form['region_id']
        cluster.save()
        return redirect(url_for('root.ci.clusters'))
    return render_template('create_cluster.html', regions=Region.all())


@ci_api.route('/clusters/<int:cluster_id>', methods=['GET', 'POST'])
def cluster_detail(cluster_id):
    # Retrieve the specific project based on project_id
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
        new_app.build_type = request.form['build_type']
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
