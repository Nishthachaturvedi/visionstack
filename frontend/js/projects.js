/**
 * Projects Module - Project submission and management
 */

class ProjectsModule {
    constructor() {
        this.currentUser = JSON.parse(localStorage.getItem('currentUser') || '{}');
        this.projects = [];
    }

    /**
     * Initialize project module
     */
    async init() {
        this.setupEventListeners();
        await this.loadUserProjects();
    }

    /**
     * Setup event listeners
     */
    setupEventListeners() {
        const submitBtn = document.getElementById('submitProjectBtn');
        if (submitBtn) {
            submitBtn.addEventListener('click', () => this.openProjectModal());
        }

        const submitForm = document.getElementById('projectSubmitForm');
        if (submitForm) {
            submitForm.addEventListener('submit', (e) => this.handleProjectSubmit(e));
        }

        // Tech stack input
        const techStackInput = document.getElementById('projectTechStack');
        if (techStackInput) {
            techStackInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    e.preventDefault();
                    this.addTechStackTag();
                }
            });
        }
    }

    /**
     * Open project submission modal
     */
    openProjectModal() {
        if (!this.currentUser.email) {
            alert('Please login to submit a project');
            window.location.href = '/login.html';
            return;
        }

        const modal = document.getElementById('projectModal');
        if (modal) {
            modal.style.display = 'flex';
        }
    }

    /**
     * Close project modal
     */
    closeProjectModal() {
        const modal = document.getElementById('projectModal');
        if (modal) {
            modal.style.display = 'none';
        }
    }

    /**
     * Handle project form submission
     */
    async handleProjectSubmit(e) {
        e.preventDefault();

        const form = e.target;
        const formData = new FormData(form);

        // Add user info
        formData.append('user_email', this.currentUser.email);
        formData.append('user_id', this.currentUser.id);

        try {
            const response = await api.submitProject(formData);
            
            // Show success message
            alert('Project submitted successfully! We will review and respond within 24-48 hours.');
            
            // Reset form and close modal
            form.reset();
            this.closeProjectModal();
            
            // Reload projects
            await this.loadUserProjects();
        } catch (error) {
            alert(`Error submitting project: ${error.message}`);
        }
    }

    /**
     * Load user's projects
     */
    async loadUserProjects() {
        if (!this.currentUser.email) return;

        try {
            this.projects = await api.getUserProjects(this.currentUser.email);
            this.displayProjects();
        } catch (error) {
            console.error('Error loading projects:', error);
        }
    }

    /**
     * Display projects in UI
     */
    displayProjects() {
        const container = document.getElementById('projectsContainer');
        if (!container) return;

        if (this.projects.length === 0) {
            container.innerHTML = '<p style="text-align: center; color: #999;">No projects submitted yet</p>';
            return;
        }

        container.innerHTML = this.projects.map(project => `
            <div class="project-card">
                <div class="project-header">
                    <h3>${project.title}</h3>
                    <span class="status-badge status-${project.status}">${project.status}</span>
                </div>
                <p class="project-description">${project.description.substring(0, 150)}...</p>
                <div class="project-meta">
                    <span><strong>Budget:</strong> $${project.budget}</span>
                    <span><strong>Priority:</strong> ${project.priority}</span>
                    <span><strong>Category:</strong> ${project.category}</span>
                </div>
                <div class="project-tech">
                    ${project.tech_stack.map(tech => `<span class="tech-tag">${tech}</span>`).join('')}
                </div>
                ${project.admin_notes ? `<p class="admin-notes"><strong>Admin Notes:</strong> ${project.admin_notes}</p>` : ''}
                <button class="btn-secondary" onclick="projectsModule.viewProject('${project.id}')">View Details</button>
            </div>
        `).join('');
    }

    /**
     * View project details
     */
    viewProject(projectId) {
        const project = this.projects.find(p => p.id === projectId);
        if (!project) return;

        const details = `
        Project Details:
        Title: ${project.title}
        Description: ${project.description}
        Budget: $${project.budget}
        Deadline: ${new Date(project.deadline).toLocaleDateString()}
        Status: ${project.status}
        ${project.admin_notes ? `Admin Notes: ${project.admin_notes}` : ''}
        `;

        alert(details);
    }

    /**
     * Add tech stack tag
     */
    addTechStackTag() {
        const input = document.getElementById('projectTechStack');
        const tagsContainer = document.getElementById('techStackTags');
        
        if (!input || !tagsContainer || !input.value.trim()) return;

        const tag = input.value.trim();
        const tagEl = document.createElement('span');
        tagEl.className = 'tech-tag';
        tagEl.innerHTML = `
            ${tag}
            <button type="button" onclick="this.parentElement.remove()">×</button>
        `;

        tagsContainer.appendChild(tagEl);
        input.value = '';
    }

    /**
     * Get projects stats
     */
    async getStats() {
        try {
            return await api.getProjectStats();
        } catch (error) {
            console.error('Error getting project stats:', error);
            return null;
        }
    }
}

// Create global instance
const projectsModule = new ProjectsModule();

// Auto-init when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    projectsModule.init();
});
