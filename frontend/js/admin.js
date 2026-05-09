/**
 * Admin Dashboard Module - Admin functions and statistics
 */

class AdminModule {
    constructor() {
        this.stats = null;
        this.currentUser = JSON.parse(localStorage.getItem('currentUser') || '{}');
    }

    /**
     * Initialize admin module
     */
    async init() {
        // Verify admin access
        if (this.currentUser.role !== 'admin') {
            window.location.href = '/';
            return;
        }

        this.setupEventListeners();
        await this.loadDashboard();
    }

    /**
     * Setup event listeners
     */
    setupEventListeners() {
        const tabs = document.querySelectorAll('.admin-tab-btn');
        tabs.forEach(tab => {
            tab.addEventListener('click', (e) => this.switchTab(e.target.dataset.tab));
        });
    }

    /**
     * Load dashboard data
     */
    async loadDashboard() {
        try {
            this.stats = await api.getDashboardStats();
            this.displayStats();
            await this.loadPendingProjects();
            await this.loadPendingReviews();
        } catch (error) {
            console.error('Error loading dashboard:', error);
            alert('Error loading dashboard data');
        }
    }

    /**
     * Display statistics
     */
    displayStats() {
        if (!this.stats) return;

        const statsContainer = document.getElementById('adminStats');
        if (!statsContainer) return;

        statsContainer.innerHTML = `
            <div class="stat-card">
                <h3>${this.stats.users?.total || 0}</h3>
                <p>Total Users</p>
            </div>
            <div class="stat-card">
                <h3>${this.stats.projects?.total || 0}</h3>
                <p>Total Projects</p>
            </div>
            <div class="stat-card">
                <h3>${this.stats.projects?.pending || 0}</h3>
                <p>Pending Projects</p>
            </div>
            <div class="stat-card">
                <h3>${this.stats.projects?.completed || 0}</h3>
                <p>Completed Projects</p>
            </div>
            <div class="stat-card">
                <h3>${this.stats.reviews?.total || 0}</h3>
                <p>Total Reviews</p>
            </div>
            <div class="stat-card">
                <h3>${this.stats.reviews?.pending || 0}</h3>
                <p>Pending Reviews</p>
            </div>
            <div class="stat-card">
                <h3>${this.stats.team?.total || 0}</h3>
                <p>Team Members</p>
            </div>
            <div class="stat-card">
                <h3>${this.stats.newsletter?.subscribers || 0}</h3>
                <p>Newsletter Subscribers</p>
            </div>
        `;
    }

    /**
     * Load pending projects
     */
    async loadPendingProjects() {
        try {
            const projects = await api.getPendingProjects();
            const container = document.getElementById('pendingProjects');
            
            if (!container) return;

            if (projects.length === 0) {
                container.innerHTML = '<p>No pending projects</p>';
                return;
            }

            container.innerHTML = projects.map(project => `
                <div class="admin-item">
                    <h4>${project.title}</h4>
                    <p>${project.description.substring(0, 100)}...</p>
                    <div class="item-actions">
                        <button onclick="adminModule.approveProject('${project.id}')">Approve</button>
                        <button onclick="adminModule.rejectProject('${project.id}')">Reject</button>
                        <button onclick="adminModule.viewProject('${project.id}')">View</button>
                    </div>
                </div>
            `).join('');
        } catch (error) {
            console.error('Error loading pending projects:', error);
        }
    }

    /**
     * Load pending reviews
     */
    async loadPendingReviews() {
        try {
            const reviews = await api.getPendingReviews();
            const container = document.getElementById('pendingReviews');
            
            if (!container) return;

            if (reviews.length === 0) {
                container.innerHTML = '<p>No pending reviews</p>';
                return;
            }

            container.innerHTML = reviews.map(review => `
                <div class="admin-item">
                    <h4>${review.author_name}</h4>
                    <p>${review.text.substring(0, 100)}...</p>
                    <div class="rating">Rating: ${this.generateStars(review.rating)}</div>
                    <div class="item-actions">
                        <button onclick="adminModule.approveReview('${review.id}')">Approve</button>
                        <button onclick="adminModule.rejectReview('${review.id}')">Reject</button>
                    </div>
                </div>
            `).join('');
        } catch (error) {
            console.error('Error loading pending reviews:', error);
        }
    }

    /**
     * Generate star rating
     */
    generateStars(rating) {
        let stars = '';
        for (let i = 0; i < 5; i++) {
            stars += i < rating ? '⭐' : '☆';
        }
        return stars;
    }

    /**
     * Approve project
     */
    async approveProject(projectId) {
        const notes = prompt('Add approval notes (optional):');
        
        try {
            await api.updateProjectStatus(projectId, 'approved', notes || '');
            alert('Project approved!');
            await this.loadPendingProjects();
        } catch (error) {
            alert(`Error approving project: ${error.message}`);
        }
    }

    /**
     * Reject project
     */
    async rejectProject(projectId) {
        const notes = prompt('Add rejection notes:');
        if (!notes) return;
        
        try {
            await api.updateProjectStatus(projectId, 'rejected', notes);
            alert('Project rejected!');
            await this.loadPendingProjects();
        } catch (error) {
            alert(`Error rejecting project: ${error.message}`);
        }
    }

    /**
     * View project details
     */
    async viewProject(projectId) {
        try {
            const project = await api.getProject(projectId);
            
            const details = `
Project: ${project.title}
Description: ${project.description}
Budget: $${project.budget}
Deadline: ${new Date(project.deadline).toLocaleDateString()}
Tech Stack: ${project.tech_stack.join(', ')}
Category: ${project.category}
Priority: ${project.priority}
Status: ${project.status}
            `;
            
            alert(details);
        } catch (error) {
            alert(`Error loading project: ${error.message}`);
        }
    }

    /**
     * Approve review
     */
    async approveReview(reviewId) {
        try {
            await api.adminApproveReview(reviewId);
            alert('Review approved!');
            await this.loadPendingReviews();
        } catch (error) {
            alert(`Error approving review: ${error.message}`);
        }
    }

    /**
     * Reject review
     */
    async rejectReview(reviewId) {
        if (!confirm('Delete this review?')) return;
        
        try {
            await api.adminDeleteReview(reviewId);
            alert('Review rejected and deleted!');
            await this.loadPendingReviews();
        } catch (error) {
            alert(`Error rejecting review: ${error.message}`);
        }
    }

    /**
     * Switch admin tabs
     */
    switchTab(tabName) {
        // Hide all tabs
        const tabs = document.querySelectorAll('.admin-tab-content');
        tabs.forEach(tab => tab.style.display = 'none');

        // Remove active class from buttons
        const buttons = document.querySelectorAll('.admin-tab-btn');
        buttons.forEach(btn => btn.classList.remove('active'));

        // Show selected tab
        const selectedTab = document.getElementById(`tab-${tabName}`);
        if (selectedTab) {
            selectedTab.style.display = 'block';
            event.target.classList.add('active');
        }
    }

    /**
     * Logout admin
     */
    logout() {
        if (confirm('Are you sure you want to logout?')) {
            api.clearToken();
            localStorage.removeItem('currentUser');
            window.location.href = '/';
        }
    }
}

// Create global instance
const adminModule = new AdminModule();

// Auto-init when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    adminModule.init();
});
