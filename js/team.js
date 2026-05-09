/**
 * Team Module - Team members display and management
 */

class TeamModule {
    constructor() {
        this.teamMembers = [];
    }

    /**
     * Initialize team module
     */
    async init() {
        this.setupEventListeners();
        await this.loadTeamMembers();
    }

    /**
     * Setup event listeners
     */
    setupEventListeners() {
        const addMemberBtn = document.getElementById('addTeamMemberBtn');
        if (addMemberBtn) {
            addMemberBtn.addEventListener('click', () => this.openTeamModal());
        }

        const addForm = document.getElementById('addTeamMemberForm');
        if (addForm) {
            addForm.addEventListener('submit', (e) => this.handleAddTeamMember(e));
        }
    }

    /**
     * Open add team member modal
     */
    openTeamModal() {
        const modal = document.getElementById('teamModal');
        if (modal) {
            modal.style.display = 'flex';
        }
    }

    /**
     * Close team modal
     */
    closeTeamModal() {
        const modal = document.getElementById('teamModal');
        if (modal) {
            modal.style.display = 'none';
        }
    }

    /**
     * Handle add team member form submission
     */
    async handleAddTeamMember(e) {
        e.preventDefault();

        const form = e.target;
        const formData = new FormData(form);

        try {
            const response = await api.addTeamMember(formData);
            
            alert('Team member added successfully!');
            form.reset();
            this.closeTeamModal();
            
            // Reload team members
            await this.loadTeamMembers();
        } catch (error) {
            alert(`Error adding team member: ${error.message}`);
        }
    }

    /**
     * Load team members from API
     */
    async loadTeamMembers() {
        try {
            this.teamMembers = await api.getTeamMembers();
            this.displayTeamMembers();
        } catch (error) {
            console.error('Error loading team members:', error);
        }
    }

    /**
     * Display team members in grid
     */
    displayTeamMembers() {
        const container = document.getElementById('teamGrid');
        if (!container) return;

        if (this.teamMembers.length === 0) {
            container.innerHTML = '<p style="text-align: center; grid-column: 1/-1;">No team members yet</p>';
            return;
        }

        container.innerHTML = this.teamMembers.map(member => `
            <div class="team-card">
                ${member.photo_url ? `<img src="${member.photo_url}" alt="${member.name}" class="team-photo">` : '<div class="team-photo-placeholder">👤</div>'}
                <h3>${member.name}</h3>
                <p class="team-role">${member.role}</p>
                <p class="team-bio">${member.bio}</p>
                
                ${member.skills && member.skills.length > 0 ? `
                    <div class="team-skills">
                        ${member.skills.map(skill => `<span class="skill-tag">${skill}</span>`).join('')}
                    </div>
                ` : ''}
                
                <div class="team-contact">
                    <small>📧 ${member.email}</small><br>
                    <small>📱 ${member.phone}</small>
                </div>
                
                ${member.social_links && Object.keys(member.social_links).length > 0 ? `
                    <div class="team-social">
                        ${Object.entries(member.social_links).map(([platform, url]) => `
                            <a href="${url}" target="_blank" title="${platform}">
                                ${this.getSocialIcon(platform)}
                            </a>
                        `).join('')}
                    </div>
                ` : ''}
            </div>
        `).join('');
    }

    /**
     * Get social media icon
     */
    getSocialIcon(platform) {
        const icons = {
            'twitter': '𝕏',
            'linkedin': 'in',
            'github': '⚙️',
            'instagram': '📷',
            'facebook': 'f',
            'website': '🌐'
        };
        return icons[platform.toLowerCase()] || '🔗';
    }

    /**
     * Delete team member (admin only)
     */
    async deleteTeamMember(memberId) {
        if (!confirm('Are you sure you want to delete this team member?')) return;

        try {
            await api.deleteTeamMember(memberId);
            alert('Team member deleted');
            await this.loadTeamMembers();
        } catch (error) {
            alert(`Error deleting team member: ${error.message}`);
        }
    }

    /**
     * Get team stats
     */
    async getStats() {
        try {
            return await api.getTeamStats();
        } catch (error) {
            console.error('Error getting team stats:', error);
            return null;
        }
    }
}

// Create global instance
const teamModule = new TeamModule();

// Auto-init when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    teamModule.init();
});
