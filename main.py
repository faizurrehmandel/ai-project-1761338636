import os
from flask import Flask, render_template, request, jsonify
from database import Database
from datetime import datetime
import requests
import base64

app = Flask(__name__)
db = Database()

# Initialize database
db.setup()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/projects', methods=['GET'])
def get_projects():
    projects = db.get_all_projects()
    return jsonify(projects)

@app.route('/create', methods=['POST'])
def create_project():
    try:
        data = request.json
        project_name = data.get('name')
        command = data.get('command')
        
        # GitHub API setup
        github_token = os.getenv('GITHUB_TOKEN')
        headers = {
            'Authorization': f'token {github_token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        
        # Create GitHub repository
        repo_data = {
            'name': project_name,
            'private': False,
            'auto_init': True
        }
        repo_response = requests.post(
            'https://api.github.com/user/repos',
            headers=headers,
            json=repo_data
        )
        
        if repo_response.status_code != 201:
            return jsonify({'error': 'Failed to create GitHub repository'}), 500
            
        github_url = repo_response.json()['html_url']
        
        # Generate code using AI
        openrouter_key = os.getenv('OPENROUTER_API_KEY')
        ai_response = requests.post(
            'https://openrouter.ai/api/v1/chat/completions',
            headers={
                'Authorization': f'Bearer {openrouter_key}',
                'Content-Type': 'application/json'
            },
            json={
                'model': 'anthropic/claude-2',
                'messages': [{'role': 'user', 'content': command}]
            }
        )
        
        generated_code = ai_response.json()['choices'][0]['message']['content']
        
        # Commit code to GitHub
        content = base64.b64encode(generated_code.encode()).decode()
        commit_data = {
            'message': 'Initial commit',
            'content': content
        }
        
        commit_response = requests.put(
            f'https://api.github.com/repos/user/{project_name}/contents/main.py',
            headers=headers,
            json=commit_data
        )
        
        # Save to database
        db.create_project(project_name, command, 'Completed', github_url)
        
        return jsonify({'success': True, 'github_url': github_url})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/edit/<int:project_id>', methods=['POST'])
def edit_project(project_id):
    try:
        data = request.json
        edit_command = data.get('command')
        
        # Get project details
        project = db.get_project(project_id)
        if not project:
            return jsonify({'error': 'Project not found'}), 404
            
        # GitHub operations here (similar to create but with updates)
        # Update database
        db.update_project(project_id, edit_command)
        
        return jsonify({'success': True})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/delete/<int:project_id>', methods=['DELETE'])
def delete_project(project_id):
    try:
        db.delete_project(project_id)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
