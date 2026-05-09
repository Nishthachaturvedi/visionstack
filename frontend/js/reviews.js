/**
 * Reviews Module - Review submission and management
 */

class ReviewsModule {
    constructor() {
        this.reviews = [];
        this.currentIndex = 0;
    }

    /**
     * Initialize reviews module
     */
    async init() {
        this.setupEventListeners();
        await this.loadApprovedReviews();
    }

    /**
     * Setup event listeners
     */
    setupEventListeners() {
        const submitBtn = document.getElementById('submitReviewBtn');
        if (submitBtn) {
            submitBtn.addEventListener('click', () => this.openReviewModal());
        }

        const submitForm = document.getElementById('reviewSubmitForm');
        if (submitForm) {
            submitForm.addEventListener('submit', (e) => this.handleReviewSubmit(e));
        }

        // Carousel controls
        const prevBtn = document.getElementById('reviewPrev');
        const nextBtn = document.getElementById('reviewNext');
        
        if (prevBtn) prevBtn.addEventListener('click', () => this.previousReview());
        if (nextBtn) nextBtn.addEventListener('click', () => this.nextReview());
    }

    /**
     * Open review submission modal
     */
    openReviewModal() {
        const modal = document.getElementById('reviewModal');
        if (modal) {
            modal.style.display = 'flex';
        }
    }

    /**
     * Close review modal
     */
    closeReviewModal() {
        const modal = document.getElementById('reviewModal');
        if (modal) {
            modal.style.display = 'none';
        }
    }

    /**
     * Handle review form submission
     */
    async handleReviewSubmit(e) {
        e.preventDefault();

        const form = e.target;
        const formData = new FormData(form);

        try {
            const response = await api.submitReview(formData);
            
            // Show success message
            alert('Review submitted successfully! Our team will review and approve it soon.');
            
            // Reset form and close modal
            form.reset();
            this.closeReviewModal();
            
            // Reload reviews
            await this.loadApprovedReviews();
        } catch (error) {
            alert(`Error submitting review: ${error.message}`);
        }
    }

    /**
     * Load approved reviews
     */
    async loadApprovedReviews() {
        try {
            this.reviews = await api.getApprovedReviews();
            this.currentIndex = 0;
            this.displayCurrentReview();
        } catch (error) {
            console.error('Error loading reviews:', error);
        }
    }

    /**
     * Display current review in carousel
     */
    displayCurrentReview() {
        const container = document.getElementById('reviewCarousel');
        if (!container || this.reviews.length === 0) {
            if (container) {
                container.innerHTML = '<p style="text-align: center;">No reviews yet</p>';
            }
            return;
        }

        const review = this.reviews[this.currentIndex];
        
        container.innerHTML = `
            <div class="review-card">
                <div class="review-header">
                    <h4>${review.author_name}</h4>
                    <div class="stars">${this.generateStars(review.rating)}</div>
                </div>
                <p class="review-text">${review.text}</p>
                
                ${review.image_urls && review.image_urls.length > 0 ? `
                    <div class="review-images">
                        ${review.image_urls.map(img => `<img src="${img}" alt="Review image" style="max-width: 200px; margin: 10px 5px;">`).join('')}
                    </div>
                ` : ''}
                
                ${review.video_urls && review.video_urls.length > 0 ? `
                    <div class="review-videos">
                        ${review.video_urls.map(vid => `<video width="200" style="margin: 10px 5px;" controls><source src="${vid}" type="video/mp4"></video>`).join('')}
                    </div>
                ` : ''}
                
                <p class="review-footer">
                    ${this.currentIndex + 1} / ${this.reviews.length}
                </p>
            </div>
        `;
    }

    /**
     * Generate star rating HTML
     */
    generateStars(rating) {
        let stars = '';
        for (let i = 0; i < 5; i++) {
            stars += i < rating ? '⭐' : '☆';
        }
        return stars;
    }

    /**
     * Next review
     */
    nextReview() {
        if (this.reviews.length === 0) return;
        this.currentIndex = (this.currentIndex + 1) % this.reviews.length;
        this.displayCurrentReview();
    }

    /**
     * Previous review
     */
    previousReview() {
        if (this.reviews.length === 0) return;
        this.currentIndex = (this.currentIndex - 1 + this.reviews.length) % this.reviews.length;
        this.displayCurrentReview();
    }

    /**
     * Get reviews stats
     */
    async getStats() {
        try {
            return await api.getReviewsStats();
        } catch (error) {
            console.error('Error getting reviews stats:', error);
            return null;
        }
    }

    /**
     * Display all reviews in list format
     */
    displayAllReviews() {
        const container = document.getElementById('reviewsList');
        if (!container) return;

        if (this.reviews.length === 0) {
            container.innerHTML = '<p>No reviews available</p>';
            return;
        }

        container.innerHTML = this.reviews.map(review => `
            <div class="review-item">
                <div class="review-header">
                    <h4>${review.author_name}</h4>
                    <span class="rating">${this.generateStars(review.rating)}</span>
                </div>
                <p>${review.text}</p>
                <small>${new Date(review.created_at).toLocaleDateString()}</small>
            </div>
        `).join('');
    }
}

// Create global instance
const reviewsModule = new ReviewsModule();

// Auto-init when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    reviewsModule.init();
});
