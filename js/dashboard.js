/**
 * Dashboard Module - User dashboard functionality
 */

class DashboardModule {
    constructor() {
        this.currentUser = JSON.parse(localStorage.getItem('currentUser') || '{}');
        this.userFiles = [];
    }

    /**
     * Initialize dashboard module
     */
    async init() {
        if (!this.currentUser.email) {
            window.location.href = '/login.html';
            return;
        }

        this.setupEventListeners();
        await this.loadUserData();
    }

    /**
     * Setup event listeners
     */
    setupEventListeners() {
        const uploadBtn = document.getElementById('uploadFileBtn');
        if (uploadBtn) {
            uploadBtn.addEventListener('click', () => this.openUploadModal());
        }

        const uploadForm = document.getElementById('uploadForm');
        if (uploadForm) {
            uploadForm.addEventListener('submit', (e) => this.handleFileUpload(e));
        }

        const logoutBtn = document.getElementById('logoutBtn');
        if (logoutBtn) {
            logoutBtn.addEventListener('click', () => this.logout());
        }
    }

    /**
     * Load user data
     */
    async loadUserData() {
        try {
            // Display user info
            const userInfo = document.getElementById('userInfo');
            if (userInfo) {
                userInfo.innerHTML = `
                    <h2>Welcome, ${this.currentUser.name || this.currentUser.email}!</h2>
                    <p>Email: ${this.currentUser.email}</p>
                `;
            }

            // Load user files
            await this.loadUserFiles();
            
            // Load user projects
            await this.loadUserProjects();
        } catch (error) {
            console.error('Error loading user data:', error);
        }
    }

    /**
     * Load user files
     */
    async loadUserFiles() {
        try {
            this.userFiles = await api.getMyFiles();
            this.displayUserFiles();
        } catch (error) {
            console.error('Error loading files:', error);
        }
    }

    /**
     * Display user files
     */
    displayUserFiles() {
        const container = document.getElementById('userFiles');
        if (!container) return;

        if (this.userFiles.length === 0) {
            container.innerHTML = '<p>No files uploaded yet</p>';
            return;
        }

        container.innerHTML = `
            <table class="files-table">
                <thead>
                    <tr>
                        <th>File Name</th>
                        <th>Type</th>
                        <th>Size</th>
                        <th>Uploaded</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    ${this.userFiles.map(file => `
                        <tr>
                            <td>${file.original_name}</td>
                            <td>${file.content_type}</td>
                            <td>${this.formatFileSize(file.size)}</td>
                            <td>${new Date(file.uploaded_at).toLocaleDateString()}</td>
                            <td>
                                <a href="${file.url}" target="_blank" class="btn-mini">Download</a>
                                <button onclick="dashboardModule.deleteFile('${file.id}')" class="btn-mini btn-danger">Delete</button>
                            </td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        `;
    }

    /**
     * Load user projects
     */
    async loadUserProjects() {
        try {
            if (typeof projectsModule !== 'undefined') {
                await projectsModule.loadUserProjects();
            }
        } catch (error) {
            console.error('Error loading projects:', error);
        }
    }

    /**
     * Open file upload modal
     */
    openUploadModal() {
        const modal = document.getElementById('uploadModal');
        if (modal) {
            modal.style.display = 'flex';
        }
    }

    /**
     * Close upload modal
     */
    closeUploadModal() {
        const modal = document.getElementById('uploadModal');
        if (modal) {
            modal.style.display = 'none';
        }
    }

    /**
     * Handle file upload
     */
    async handleFileUpload(e) {
        e.preventDefault();

        const fileInput = document.getElementById('fileInput');
        if (!fileInput.files.length) {
            alert('Please select a file');
            return;
        }

        const file = fileInput.files[0];
        
        // Validate file size (50MB max)
        if (file.size > 50 * 1024 * 1024) {
            alert('File too large (max 50MB)');
            return;
        }

        try {
            const response = await api.uploadFile(file);
            alert('File uploaded successfully!');
            
            fileInput.value = '';
            this.closeUploadModal();
            
            await this.loadUserFiles();
        } catch (error) {
            alert(`Error uploading file: ${error.message}`);
        }
    }

    /**
     * Delete file
     */
    async deleteFile(fileId) {
        if (!confirm('Are you sure you want to delete this file?')) return;

        try {
            await api.delete(`/files/${fileId}`);
            alert('File deleted');
            await this.loadUserFiles();
        } catch (error) {
            alert(`Error deleting file: ${error.message}`);
        }
    }

    /**
     * Format file size
     */
    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        
        return Math.round((bytes / Math.pow(k, i)) * 100) / 100 + ' ' + sizes[i];
    }

    /**
     * Logout user
     */
    logout() {
        if (confirm('Are you sure you want to logout?')) {
            api.clearToken();
            localStorage.removeItem('currentUser');
            window.location.href = '/';
        }
    }

    /**
     * Update profile
     */
    async updateProfile(data) {
        try {
            await api.put('/user/profile', data);
            alert('Profile updated successfully!');
            await this.loadUserData();
        } catch (error) {
            alert(`Error updating profile: ${error.message}`);
        }
    }
}

// Create global instance
const dashboardModule = new DashboardModule();

// Auto-init when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    dashboardModule.init();
});
