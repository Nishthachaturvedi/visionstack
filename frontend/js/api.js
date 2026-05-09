/**
 * API Helper - Centralized API communication with authentication
 */

class APIClient {
    constructor() {
        this.baseURL = '/api';
        this.token = localStorage.getItem('token');
        this.headers = {
            'Content-Type': 'application/json',
        };
        if (this.token) {
            this.headers['Authorization'] = `Bearer ${this.token}`;
        }
    }

    /**
     * Set authorization token
     */
    setToken(token) {
        this.token = token;
        localStorage.setItem('token', token);
        this.headers['Authorization'] = `Bearer ${token}`;
    }

    /**
     * Clear authorization token
     */
    clearToken() {
        this.token = null;
        localStorage.removeItem('token');
        delete this.headers['Authorization'];
    }

    /**
     * Generic fetch wrapper
     */
    async fetch(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        const config = {
            headers: { ...this.headers },
            ...options
        };

        try {
            const response = await fetch(url, config);
            
            // Handle unauthorized
            if (response.status === 401) {
                this.clearToken();
                window.location.href = '/login.html';
                throw new Error('Session expired. Please login again.');
            }

            if (!response.ok) {
                const error = await response.json().catch(() => ({ detail: response.statusText }));
                throw new Error(error.detail || response.statusText);
            }

            return await response.json();
        } catch (error) {
            console.error(`API Error (${endpoint}):`, error);
            throw error;
        }
    }

    /**
     * GET request
     */
    get(endpoint) {
        return this.fetch(endpoint, { method: 'GET' });
    }

    /**
     * POST request
     */
    post(endpoint, data) {
        return this.fetch(endpoint, {
            method: 'POST',
            body: JSON.stringify(data)
        });
    }

    /**
     * POST with FormData (for file uploads)
     */
    postFormData(endpoint, formData) {
        const headers = { ...this.headers };
        delete headers['Content-Type']; // Let browser set it
        
        return this.fetch(endpoint, {
            method: 'POST',
            headers,
            body: formData
        });
    }

    /**
     * PUT request
     */
    put(endpoint, data) {
        return this.fetch(endpoint, {
            method: 'PUT',
            body: JSON.stringify(data)
        });
    }

    /**
     * DELETE request
     */
    delete(endpoint) {
        return this.fetch(endpoint, { method: 'DELETE' });
    }

    // ========================
    // AUTH ENDPOINTS
    // ========================

    async register(firstName, lastName, email, password) {
        return this.post('/auth/register', {
            first_name: firstName,
            last_name: lastName,
            email,
            password
        });
    }

    async login(email, password) {
        return this.post('/auth/login', { email, password });
    }

    async adminLogin(email, password) {
        return this.post('/auth/admin/login', { email, password });
    }

    // ========================
    // PROJECT ENDPOINTS
    // ========================

    async submitProject(formData) {
        return this.postFormData('/projects/submit', formData);
    }

    async getUserProjects(userEmail) {
        return this.get(`/projects/user/${userEmail}`);
    }

    async getAllProjects() {
        return this.get('/projects/all');
    }

    async getProject(projectId) {
        return this.get(`/projects/${projectId}`);
    }

    async updateProjectStatus(projectId, status, adminNotes) {
        return this.put(`/projects/${projectId}/status`, {
            status,
            admin_notes: adminNotes
        });
    }

    async deleteProject(projectId) {
        return this.delete(`/projects/${projectId}`);
    }

    async getProjectStats() {
        return this.get('/projects/stats/overview');
    }

    // ========================
    // TEAM ENDPOINTS
    // ========================

    async getTeamMembers() {
        return this.get('/team/members');
    }

    async getTeamMember(memberId) {
        return this.get(`/team/members/${memberId}`);
    }

    async addTeamMember(formData) {
        return this.postFormData('/team/members/add', formData);
    }

    async updateTeamMember(memberId, formData) {
        return this.postFormData(`/team/members/${memberId}`, formData);
    }

    async deleteTeamMember(memberId) {
        return this.delete(`/team/members/${memberId}`);
    }

    async getTeamStats() {
        return this.get('/team/stats/count');
    }

    // ========================
    // REVIEWS ENDPOINTS
    // ========================

    async submitReview(formData) {
        return this.postFormData('/reviews/submit', formData);
    }

    async getApprovedReviews() {
        return this.get('/reviews/approved');
    }

    async getReview(reviewId) {
        return this.get(`/reviews/${reviewId}`);
    }

    async approveReview(reviewId) {
        return this.put(`/reviews/${reviewId}/approve`, {});
    }

    async rejectReview(reviewId) {
        return this.put(`/reviews/${reviewId}/reject`, {});
    }

    async deleteReview(reviewId) {
        return this.delete(`/reviews/${reviewId}`);
    }

    async getReviewsStats() {
        return this.get('/reviews/stats/overview');
    }

    // ========================
    // ADMIN ENDPOINTS
    // ========================

    async getDashboardStats() {
        return this.get('/admin/dashboard/stats');
    }

    async getAllUsers() {
        return this.get('/admin/users');
    }

    async getUser(userId) {
        return this.get(`/admin/users/${userId}`);
    }

    async deleteUser(userId) {
        return this.delete(`/admin/users/${userId}`);
    }

    async getPendingProjects() {
        return this.get('/admin/projects/pending');
    }

    async getAllAdminProjects() {
        return this.get('/admin/projects');
    }

    async getPendingReviews() {
        return this.get('/admin/reviews/pending');
    }

    async adminApproveReview(reviewId) {
        return this.put(`/admin/reviews/${reviewId}/approve`, {});
    }

    async adminDeleteReview(reviewId) {
        return this.delete(`/admin/reviews/${reviewId}`);
    }

    async getAllContacts() {
        return this.get('/admin/contacts');
    }

    async markContactRead(messageId) {
        return this.put(`/admin/contacts/${messageId}/mark-read`, {});
    }

    async deleteContact(messageId) {
        return this.delete(`/admin/contacts/${messageId}`);
    }

    async getNewsletterSubscribers() {
        return this.get('/admin/newsletter/subscribers');
    }

    async removeSubscriber(subscriberId) {
        return this.delete(`/admin/newsletter/subscribers/${subscriberId}`);
    }

    // ========================
    // FILE ENDPOINTS
    // ========================

    async uploadFile(file) {
        const formData = new FormData();
        formData.append('file', file);
        return this.postFormData('/files/upload', formData);
    }

    async getMyFiles() {
        return this.get('/files/my');
    }

    // ========================
    // CONTACT ENDPOINTS
    // ========================

    async submitContact(name, email, subject, message) {
        return this.post('/contact', { name, email, subject, message });
    }

    // ========================
    // NEWSLETTER ENDPOINTS
    // ========================

    async subscribeNewsletter(email) {
        return this.post('/newsletter/subscribe', { email });
    }
}

// Create global instance
const api = new APIClient();
