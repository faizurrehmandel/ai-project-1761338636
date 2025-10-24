// DOM Elements
const projectsList = document.getElementById('projectsList');
const createProjectBtn = document.getElementById('createProjectBtn');
const createModal = document.getElementById('createModal');
const editModal = document.getElementById('editModal');
const createProjectForm = document.getElementById('createProjectForm');
const editProjectForm = document.getElementById('editProjectForm');

// Event Listeners
document.addEventListener('DOMContentLoaded', loadProjects);
createProjectBtn.addEventListener('click', () => openModal('createModal'));
createProjectForm.addEventListener('submit', handleCreateProject);
editProjectForm.addEventListener('submit', handleEditProject);

// Functions
async function loadProjects() {
    try {
        const response = await fetch('/projects');
        const projects = await response.json();
        
        projectsList.innerHTML = projects.map(project => `
            <tr>
                <td>${project.name}</td>
                <td><span class="status-${project.status.toLowerCase()}">${project.status}</span></td>
                <td>${new Date(project.created_at).toLocaleString()}</td>
                <td>
                    <a href="${project.github_url}" target="_blank" class="btn-secondary">View on GitHub</a>
                    <button onclick="openEditModal(${project.id})" class="btn-primary">Edit</button>
                    <button onclick="deleteProject(${project.id})" class="btn-danger">Delete</button>
                </td>
            </tr>
        `).join('');
    } catch (error) {
        console.error('Error loading projects:', error);
    }
}

async function handleCreateProject(e) {
    e.preventDefault();
    
    const name = document.getElementById('projectName').value;
    const command = document.getElementById('projectCommand').value;
    
    try {
        const response = await fetch('/create', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ name, command })
        });
        
        if (response.ok) {
            closeModal('createModal');
            createProjectForm.reset();
            loadProjects();
        } else {
            const error = await response.json();
            alert('Error creating project: ' + error.error);
        }
    } catch (error) {
        console.error('Error creating project:', error);
        alert('Failed to create project');
    }
}

function openEditModal(projectId) {
    document.getElementById('editProjectId').value = projectId;
    openModal('editModal');
}

async function handleEditProject(e) {
    e.preventDefault();
    
    const projectId = document.getElementById('editProjectId').value;
    const command = document.getElementById('editCommand').value;
    
    try {
        const response = await fetch(`/edit/${projectId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ command })
        });
        
        if (response.ok) {
            closeModal('editModal');
            editProjectForm.reset();
            loadProjects();
        } else {
            const error = await response.json();
            alert('Error updating project: ' + error.error);
        }
    } catch (error) {
        console.error('Error updating project:', error);
        alert('Failed to update project');
    }
}

async function deleteProject(projectId) {
    if (!confirm('Are you sure you want to delete this project?')) return;
    
    try {
        const response = await fetch(`/delete/${projectId}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            loadProjects();
        } else {
            const error = await response.json();
            alert('Error deleting project: ' + error.error);
        }
    } catch (error) {
        console.error('Error deleting project:', error);
        alert('Failed to delete project');
    }
}

function openModal(modalId) {
    document.getElementById(modalId).style.display = 'block';
}

function closeModal(modalId) {
    document.getElementById(modalId).style.display = 'none';
}
