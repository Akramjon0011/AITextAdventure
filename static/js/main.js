// Main JavaScript file for UzbekNews AI
document.addEventListener('DOMContentLoaded', function() {
    
    // Initialize all components
    initializeClock();
    initializeSearchFunctionality();
    initializeImageLazyLoading();
    initializeTooltips();
    initializeSmoothScrolling();
    
});

/**
 * Initialize and update Tashkent time
 */
function initializeClock() {
    const timeElement = document.getElementById('tashkent-time');
    if (!timeElement) return;
    
    function updateTime() {
        try {
            // Create date object for Tashkent timezone (UTC+5)
            const now = new Date();
            const utc = now.getTime() + (now.getTimezoneOffset() * 60000);
            const tashkentTime = new Date(utc + (5 * 3600000));
            
            const options = {
                hour: '2-digit',
                minute: '2-digit',
                second: '2-digit',
                hour12: false
            };
            
            const timeString = tashkentTime.toLocaleTimeString('uz-UZ', options);
            const dateString = tashkentTime.toLocaleDateString('uz-UZ', {
                weekday: 'short',
                day: 'numeric',
                month: 'short'
            });
            
            timeElement.textContent = `${dateString}, ${timeString}`;
        } catch (error) {
            console.error('Error updating time:', error);
            timeElement.textContent = new Date().toLocaleTimeString();
        }
    }
    
    // Update immediately and then every second
    updateTime();
    setInterval(updateTime, 1000);
}

/**
 * Enhanced search functionality
 */
function initializeSearchFunctionality() {
    const searchForm = document.querySelector('form[action*="search"]');
    const searchInput = document.querySelector('input[name="q"]');
    
    if (!searchForm || !searchInput) return;
    
    // Add search suggestions (basic implementation)
    let searchTimeout;
    
    searchInput.addEventListener('input', function() {
        clearTimeout(searchTimeout);
        const query = this.value.trim();
        
        if (query.length < 2) {
            hideSuggestions();
            return;
        }
        
        searchTimeout = setTimeout(() => {
            fetchSearchSuggestions(query);
        }, 300);
    });
    
    // Hide suggestions when clicking outside
    document.addEventListener('click', function(e) {
        if (!e.target.closest('.search-container')) {
            hideSuggestions();
        }
    });
}

/**
 * Fetch search suggestions (placeholder for future implementation)
 */
function fetchSearchSuggestions(query) {
    // This would connect to a search API endpoint
    // For now, just a placeholder
    console.log('Search suggestions for:', query);
}

/**
 * Hide search suggestions
 */
function hideSuggestions() {
    const suggestionsEl = document.querySelector('.search-suggestions');
    if (suggestionsEl) {
        suggestionsEl.style.display = 'none';
    }
}

/**
 * Lazy loading for images
 */
function initializeImageLazyLoading() {
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('lazy');
                    imageObserver.unobserve(img);
                }
            });
        });
        
        document.querySelectorAll('img[data-src]').forEach(img => {
            imageObserver.observe(img);
        });
    }
}

/**
 * Initialize Bootstrap tooltips
 */
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

/**
 * Smooth scrolling for anchor links
 */
function initializeSmoothScrolling() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            if (href === '#' || href === null) return; // Skip empty anchors
            
            const target = document.querySelector(href);
            if (target) {
                e.preventDefault();
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

/**
 * Copy text to clipboard
 */
function copyToClipboard(text) {
    if (navigator.clipboard) {
        navigator.clipboard.writeText(text).then(() => {
            showNotification('Matn nusxa olindi!', 'success');
        }).catch(err => {
            console.error('Failed to copy text: ', err);
            fallbackCopyTextToClipboard(text);
        });
    } else {
        fallbackCopyTextToClipboard(text);
    }
}

/**
 * Fallback for older browsers
 */
function fallbackCopyTextToClipboard(text) {
    const textArea = document.createElement('textarea');
    textArea.value = text;
    textArea.style.top = '0';
    textArea.style.left = '0';
    textArea.style.position = 'fixed';
    
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();
    
    try {
        const successful = document.execCommand('copy');
        if (successful) {
            showNotification('Matn nusxa olindi!', 'success');
        } else {
            showNotification('Nusxa olishda xatolik!', 'error');
        }
    } catch (err) {
        console.error('Fallback: Oops, unable to copy', err);
        showNotification('Nusxa olishda xatolik!', 'error');
    }
    
    document.body.removeChild(textArea);
}

/**
 * Show notification message
 */
function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `alert alert-${type === 'error' ? 'danger' : type} alert-dismissible fade show position-fixed`;
    notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 250px;';
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(notification);
    
    // Auto remove after 3 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, 3000);
}

/**
 * Format numbers in Uzbek style
 */
function formatNumber(num) {
    return new Intl.NumberFormat('uz-UZ').format(num);
}

/**
 * Format currency in UZS
 */
function formatCurrency(amount) {
    return new Intl.NumberFormat('uz-UZ', {
        style: 'currency',
        currency: 'UZS',
        minimumFractionDigits: 0
    }).format(amount);
}

/**
 * Format date in Uzbek locale
 */
function formatUzbekDate(date) {
    const options = {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    };
    return new Date(date).toLocaleDateString('uz-UZ', options);
}

/**
 * Debounce function for performance optimization
 */
function debounce(func, wait, immediate) {
    let timeout;
    return function executedFunction() {
        const context = this;
        const args = arguments;
        const later = function() {
            timeout = null;
            if (!immediate) func.apply(context, args);
        };
        const callNow = immediate && !timeout;
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
        if (callNow) func.apply(context, args);
    };
}

/**
 * Handle form submissions with loading states
 */
function handleFormSubmission(formSelector) {
    const form = document.querySelector(formSelector);
    if (!form) return;
    
    form.addEventListener('submit', function(e) {
        const submitBtn = form.querySelector('button[type="submit"], input[type="submit"]');
        if (submitBtn) {
            const originalText = submitBtn.textContent || submitBtn.value;
            submitBtn.disabled = true;
            
            if (submitBtn.tagName === 'BUTTON') {
                submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Yuklanmoqda...';
            } else {
                submitBtn.value = 'Yuklanmoqda...';
            }
            
            // Re-enable after 5 seconds as fallback
            setTimeout(() => {
                submitBtn.disabled = false;
                if (submitBtn.tagName === 'BUTTON') {
                    submitBtn.innerHTML = originalText;
                } else {
                    submitBtn.value = originalText;
                }
            }, 5000);
        }
    });
}

/**
 * Initialize reading progress bar
 */
function initializeReadingProgress() {
    const progressBar = document.createElement('div');
    progressBar.id = 'reading-progress';
    progressBar.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 0%;
        height: 3px;
        background: linear-gradient(to right, #0066cc, #00cc66);
        z-index: 9999;
        transition: width 0.3s ease;
    `;
    document.body.appendChild(progressBar);
    
    window.addEventListener('scroll', debounce(() => {
        const winScroll = document.body.scrollTop || document.documentElement.scrollTop;
        const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
        const scrolled = (winScroll / height) * 100;
        progressBar.style.width = scrolled + '%';
    }, 10));
}

/**
 * Social sharing functionality
 */
function shareToSocial(platform, url, title) {
    const encodedUrl = encodeURIComponent(url || window.location.href);
    const encodedTitle = encodeURIComponent(title || document.title);
    
    let shareUrl = '';
    
    switch (platform) {
        case 'telegram':
            shareUrl = `https://t.me/share/url?url=${encodedUrl}&text=${encodedTitle}`;
            break;
        case 'facebook':
            shareUrl = `https://www.facebook.com/sharer/sharer.php?u=${encodedUrl}`;
            break;
        case 'twitter':
            shareUrl = `https://twitter.com/intent/tweet?url=${encodedUrl}&text=${encodedTitle}`;
            break;
        case 'whatsapp':
            shareUrl = `https://wa.me/?text=${encodedTitle} ${encodedUrl}`;
            break;
        default:
            console.error('Unsupported platform:', platform);
            return;
    }
    
    window.open(shareUrl, '_blank', 'width=600,height=400');
}

/**
 * Initialize page based on current location
 */
function initializePage() {
    const path = window.location.pathname;
    
    if (path.includes('/admin')) {
        initializeAdminFeatures();
    }
    
    if (path.includes('/yangilik/')) {
        initializeArticlePage();
    }
    
    if (path === '/' || path === '/index') {
        initializeHomePage();
    }
}

/**
 * Initialize admin-specific features
 */
function initializeAdminFeatures() {
    // Handle form submissions
    handleFormSubmission('.admin-form');
    
    // Initialize admin tooltips and modals
    initializeTooltips();
    
    console.log('Admin features initialized');
}

/**
 * Initialize article page features
 */
function initializeArticlePage() {
    // Initialize reading progress
    initializeReadingProgress();
    
    // Add social share event listeners
    document.querySelectorAll('[data-share]').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const platform = this.dataset.share;
            const url = this.dataset.url || window.location.href;
            const title = this.dataset.title || document.title;
            shareToSocial(platform, url, title);
        });
    });
    
    console.log('Article page features initialized');
}

/**
 * Initialize home page features
 */
function initializeHomePage() {
    // Any home page specific functionality
    console.log('Home page features initialized');
}

// Initialize page-specific features
initializePage();

// Export functions for global use
window.UzbekNews = {
    copyToClipboard,
    showNotification,
    formatNumber,
    formatCurrency,
    formatUzbekDate,
    shareToSocial
};
