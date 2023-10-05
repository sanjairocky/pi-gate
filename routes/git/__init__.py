from flask import Blueprint, request, jsonify

git_api =  Blueprint('git',__name__,  url_prefix='git')


@git_api.get('/')
def hello_git():
    return 'hello from git path', 200

@git_api.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    try:
        # Check if the webhook event is a push to the repository
        repository_name = data['repository']['full_name']
        if 'commits' in data:
            commits = data['commits']
            
            print(f"Received a push event :  {repository_name} with {len(commits)} commits:")
            for commit in commits:
                print(f"Commit by {commit['author']['name']}: {commit['message']}")
        else:
            print(f"Received a push event to {repository_name}")
    except:
        pass
    return jsonify({'message': 'Webhook received successfully'}), 200
