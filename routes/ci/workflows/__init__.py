from flask import Blueprint, request, redirect, url_for, render_template


conford_api = Blueprint('confords', __name__,  url_prefix='confords')


@conford_api.get('/')
def workflows():
    wf = {
        'jobs': {
            'total': 10,
            'running': 4
        },
        'tasks': {
            'total': 20,
            'running': 2
        }
    }
    return render_template('confords.html', wf=wf)
