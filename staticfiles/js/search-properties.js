// Search Properties AJAX functionality
class SearchPropertiesManager {
    constructor() {
        this.isLoading = false;
        this.debounceTimer = null;
        this.init();
    }

    init() {
        this.bindEvents();
        this.applyLayoutFixes();
        this.handleUrlParameters();
    }

    bindEvents() {
        // Mobile filter toggle
        const filterToggle = document.getElementById('filterToggle');
        const filterPanel = document.getElementById('filterPanel');
        
        if (filterToggle && filterPanel) {
            filterToggle.addEventListener('click', () => {
                const isHidden = filterPanel.classList.contains('hidden');
                if (isHidden) {
                    filterPanel.classList.remove('hidden');
                    filterToggle.querySelector('svg:last-child').classList.add('rotate-180');
                } else {
                    filterPanel.classList.add('hidden');
                    filterToggle.querySelector('svg:last-child').classList.remove('rotate-180');
                }
            });
        }

        // Form change handlers with debouncing
        const form = document.getElementById('advanced-search-form');
        if (form) {
            // Handle all form changes
            form.addEventListener('change', (e) => {
                this.debounceFormSubmit();
            });

            // Handle text input with debouncing
            const textInputs = form.querySelectorAll('input[type="text"], input[type="search"]');
            textInputs.forEach(input => {
                input.addEventListener('input', () => {
                    this.debounceFormSubmit(500); // Longer delay for text inputs
                });
            });
        }

        // Quick search form
        const quickSearchForm = document.querySelector('form[action*="search_properties"]');
        if (quickSearchForm && quickSearchForm.id !== 'advanced-search-form') {
            quickSearchForm.addEventListener('submit', (e) => {
                e.preventDefault();
                this.submitQuickSearch(quickSearchForm);
            });
        }

        // Handle browser back/forward buttons
        window.addEventListener('popstate', (event) => {
            if (!this.isLoading) {
                this.loadFromUrl(window.location.href, false);
            }
        });

        // Auto-fix layout on visibility change
        document.addEventListener('visibilitychange', () => {
            if (!document.hidden) {
                setTimeout(() => this.applyLayoutFixes(), 100);
            }
        });

        // Fix layout on window focus
        window.addEventListener('focus', () => {
            setTimeout(() => this.applyLayoutFixes(), 100);
        });
    }

    debounceFormSubmit(delay = 300) {
        clearTimeout(this.debounceTimer);
        this.debounceTimer = setTimeout(() => {
            this.submitAdvancedForm();
        }, delay);
    }

    submitQuickSearch(form) {
        const formData = new FormData(form);
        const params = new URLSearchParams(formData);
        const url = form.action + '?' + params.toString();
        this.makeAjaxRequest(url);
    }

    submitAdvancedForm() {
        const form = document.getElementById('advanced-search-form');
        if (!form) return;

        const formData = new FormData(form);
        const params = new URLSearchParams(window.location.search);
        
        // Preserve search query from quick search
        const quickSearch = document.querySelector('input[name="q"]');
        if (quickSearch && quickSearch.value) {
            params.set('q', quickSearch.value);
        }

        // Add form data to URL params
        for (const [key, value] of formData.entries()) {
            if (value) {
                params.set(key, value);
            } else {
                params.delete(key);
            }
        }

        // Remove page parameter when filtering
        params.delete('page');

        const url = window.location.pathname + '?' + params.toString();
        this.makeAjaxRequest(url);
    }

    showLoading() {
        if (this.isLoading) return;
        this.isLoading = true;

        // Show loading overlay on results section
        const resultsSection = document.querySelector('.flex-1');
        if (resultsSection) {
            const loadingOverlay = document.createElement('div');
            loadingOverlay.id = 'loadingOverlay';
            loadingOverlay.className = 'absolute inset-0 bg-white/80 backdrop-blur-sm flex items-center justify-center z-50 rounded-xl';
            loadingOverlay.innerHTML = `
                <div class="flex flex-col items-center space-y-4">
                    <div class="relative">
                        <div class="w-12 h-12 border-4 border-red-200 border-t-red-600 rounded-full animate-spin"></div>
                    </div>
                    <div class="text-center">
                        <p class="text-sm font-semibold text-gray-900">Loading Properties</p>
                        <p class="text-xs text-gray-600">Please wait...</p>
                    </div>
                </div>
            `;
            resultsSection.style.position = 'relative';
            resultsSection.appendChild(loadingOverlay);
        }

        // Disable interactive elements
        this.disableInteractiveElements(true);
    }

    hideLoading() {
        this.isLoading = false;

        // Remove loading overlay
        const loadingOverlay = document.getElementById('loadingOverlay');
        if (loadingOverlay) {
            loadingOverlay.remove();
        }

        // Re-enable interactive elements
        this.disableInteractiveElements(false);
    }

    disableInteractiveElements(disable) {
        // Disable/enable sort buttons
        document.querySelectorAll('[onclick^="submitSort"], .sort-btn').forEach(btn => {
            btn.disabled = disable;
            if (disable) {
                btn.classList.add('opacity-50', 'cursor-not-allowed');
            } else {
                btn.classList.remove('opacity-50', 'cursor-not-allowed');
            }
        });

        // Disable/enable form elements
        const form = document.getElementById('advanced-search-form');
        if (form) {
            const inputs = form.querySelectorAll('input, select, button');
            inputs.forEach(input => {
                input.disabled = disable;
            });
        }
    }

    updateResults(data) {
        const resultsContainer = document.querySelector('.flex-1');
        if (resultsContainer) {
            // Create a temporary container to parse the new content
            const tempDiv = document.createElement('div');
            tempDiv.innerHTML = data;
            
            // Extract only the results content (skip the filter sidebar)
            const newResultsContent = tempDiv.querySelector('.flex-1');
            if (newResultsContent) {
                // Smooth transition
                resultsContainer.style.opacity = '0';
                resultsContainer.style.transform = 'translateY(10px)';
                
                setTimeout(() => {
                    resultsContainer.innerHTML = newResultsContent.innerHTML;
                    
                    // Trigger reflow
                    resultsContainer.offsetHeight;
                    
                    // Animate back
                    resultsContainer.style.transition = 'all 0.3s ease-out';
                    resultsContainer.style.opacity = '1';
                    resultsContainer.style.transform = 'translateY(0)';
                    
                    // Re-initialize dynamic elements
                    this.initializeDynamicElements();
                    this.applyLayoutFixes();
                    
                    // Remove transition after animation
                    setTimeout(() => {
                        resultsContainer.style.transition = '';
                    }, 300);
                }, 50);
            }
        }

        // Smooth scroll to results
        setTimeout(() => {
            const resultsHeader = document.querySelector('.flex-1 .bg-white');
            if (resultsHeader) {
                resultsHeader.scrollIntoView({ 
                    behavior: 'smooth', 
                    block: 'start',
                    inline: 'nearest'
                });
            }
        }, 100);
    }

    initializeDynamicElements() {
        // Re-attach sort button events
        document.querySelectorAll('[onclick^="submitSort"]').forEach(button => {
            const onclickAttr = button.getAttribute('onclick');
            const sortValue = onclickAttr.match(/submitSort\('([^']+)'\)/);
            if (sortValue) {
                button.removeAttribute('onclick');
                button.addEventListener('click', (e) => {
                    e.preventDefault();
                    this.submitSort(sortValue[1]);
                });
            }
        });

        // Re-attach pagination events
        document.querySelectorAll('a[href*="page="]').forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                this.makeAjaxRequest(link.href);
            });
        });

        // Force layout recalculation for grid
        const grid = document.querySelector('.property-grid');
        if (grid) {
            grid.style.display = 'none';
            grid.offsetHeight; // Trigger reflow
            grid.style.display = 'grid';
        }
    }

    applyLayoutFixes() {
        const grid = document.querySelector('.property-grid');
        if (grid) {
            // Apply grid fixes
            grid.style.gridAutoRows = 'min-content';
            grid.style.contain = 'layout';
            
            // Fix individual grid items
            const gridItems = grid.querySelectorAll('> div');
            gridItems.forEach(item => {
                item.style.alignSelf = 'start';
                item.style.contain = 'layout';
            });
        }

        // Force repaint
        document.body.offsetHeight;
    }

    makeAjaxRequest(url, updateHistory = true) {
        if (this.isLoading) return;

        this.showLoading();

        fetch(url, {
            method: 'GET',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'Content-Type': 'application/x-www-form-urlencoded',
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.text();
        })
        .then(data => {
            this.updateResults(data);
            
            // Update URL without page refresh
            if (updateHistory) {
                window.history.pushState({ ajaxLoad: true }, '', url);
            }
        })
        .catch(error => {
            console.error('AJAX Error:', error);
            
            // Show user-friendly error message
            this.showErrorMessage('Failed to load properties. Please try again.');
            
            // Fallback to regular page load after short delay
            setTimeout(() => {
                window.location.href = url;
            }, 2000);
        })
        .finally(() => {
            this.hideLoading();
        });
    }

    loadFromUrl(url, updateHistory = true) {
        this.makeAjaxRequest(url, updateHistory);
    }

    showErrorMessage(message) {
        const resultsContainer = document.querySelector('.flex-1');
        if (resultsContainer) {
            const errorDiv = document.createElement('div');
            errorDiv.className = 'bg-red-50 border border-red-200 rounded-xl p-6 text-center';
            errorDiv.innerHTML = `
                <div class="flex flex-col items-center space-y-3">
                    <svg class="w-12 h-12 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z"/>
                    </svg>
                    <div>
                        <h3 class="text-lg font-semibold text-red-800 mb-1">Oops! Something went wrong</h3>
                        <p class="text-sm text-red-600">${message}</p>
                    </div>
                </div>
            `;
            
            // Insert error message
            const firstChild = resultsContainer.firstElementChild;
            if (firstChild) {
                resultsContainer.insertBefore(errorDiv, firstChild);
                
                // Remove error message after 5 seconds
                setTimeout(() => {
                    errorDiv.remove();
                }, 5000);
            }
        }
    }

    handleUrlParameters() {
        // Parse URL parameters and update form fields
        const urlParams = new URLSearchParams(window.location.search);
        const form = document.getElementById('advanced-search-form');
        
        if (form) {
            urlParams.forEach((value, key) => {
                const field = form.querySelector(`[name="${key}"]`);
                if (field) {
                    if (field.type === 'radio') {
                        const radioButton = form.querySelector(`[name="${key}"][value="${value}"]`);
                        if (radioButton) {
                            radioButton.checked = true;
                        }
                    } else {
                        field.value = value;
                    }
                }
            });
        }
    }

    // Public methods for global access
    submitSort(sortValue) {
        const params = new URLSearchParams(window.location.search);
        params.set('sort', sortValue);
        params.delete('page'); // Reset to first page when sorting
        
        const url = window.location.pathname + '?' + params.toString();
        this.makeAjaxRequest(url);
    }

    loadPage(pageNumber) {
        const params = new URLSearchParams(window.location.search);
        params.set('page', pageNumber);
        
        const url = window.location.pathname + '?' + params.toString();
        this.makeAjaxRequest(url);
    }

    clearFilters() {
        // Reset form
        const form = document.getElementById('advanced-search-form');
        if (form) {
            form.reset();
        }
        
        // Clear quick search
        const quickSearch = document.querySelector('input[name="q"]');
        if (quickSearch) {
            quickSearch.value = '';
        }
        
        // Load clean search page
        this.makeAjaxRequest(window.location.pathname);
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    window.searchManager = new SearchPropertiesManager();
});

// Global functions for compatibility
function submitSort(sortValue) {
    if (window.searchManager) {
        window.searchManager.submitSort(sortValue);
    }
}

function loadPage(pageNumber) {
    if (window.searchManager) {
        window.searchManager.loadPage(pageNumber);
    }
}

function clearFilters() {
    if (window.searchManager) {
        window.searchManager.clearFilters();
    }
}
