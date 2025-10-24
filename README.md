# AI Project Manager v10

A professional dashboard-style web application for managing AI-generated software projects. This application allows users to create, edit, and manage software projects using AI assistance, with automatic GitHub repository creation and code generation.

## Features

- Create new projects with AI-generated code
- Edit existing projects with AI assistance
- Automatic GitHub repository creation and management
- Professional dashboard interface
- Real-time project status updates
- Full project history tracking

## Technology Stack

- Backend: Python with Flask
- Frontend: HTML, CSS, and JavaScript
- Database: SQLite
- Version Control: GitHub API integration

## Setup Instructions

1. Clone the repository:
bash
git clone <repository-url>
cd ai-project-manager


2. Create and activate a virtual environment:
bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate


3. Install dependencies:
bash
pip install -r requirements.txt


4. Set up environment variables:
Create a `.env` file with the following variables:

GITHUB_TOKEN=your_github_token
OPENROUTER_API_KEY=your_openrouter_api_key


5. Initialize the database:
bash
python main.py


6. Run the application:
bash
flask run


## Usage

1. Open your web browser and navigate to `http://localhost:5000`
2. Click "Create New Project" to start a new project
3. Fill in the project details and submit
4. Use the dashboard to manage your projects

## Security Notes

- Never commit your API keys or tokens
- Use environment variables for sensitive information
- Keep your dependencies updated

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License
