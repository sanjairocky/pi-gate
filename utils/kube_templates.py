from flask import render_template
import yaml
import json
import re
from utils.env import get_env_variable


def get_kube_template(template: str, **kwargs):
    return json.loads(json.dumps(yaml.safe_load(render_template(template, **kwargs))))


def sanitize_for_kube(name):

    # Replace spaces with a single hyphen and remove consecutive hyphens
    name = re.sub(r'[-\s]+', '-', name)
    # Remove any characters that are not lowercase letters, numbers, hyphens, or periods
    name = re.sub(r'[^a-z0-9\-.]', '', name)

    return name
