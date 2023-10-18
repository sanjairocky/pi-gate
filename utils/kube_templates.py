from flask import render_template
import yaml
import json


def get_kube_template(template: str, **kwargs):
    return json.loads(json.dumps(yaml.safe_load(render_template(template, **kwargs))))
