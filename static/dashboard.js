// Clean Dashboard JavaScript
document.addEventListener('DOMContentLoaded', function() {
    
    // Update time display
    updateTime();
    setInterval(updateTime, 60000);
    
    // Initialize copy buttons
    initializeCopyButtons();
    
    /**
     * Update current time display
     */
    function updateTime() {
        const now = new Date();
        const timeString = now.toLocaleString('en-US', {
            weekday: 'short',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
        
        const timeElement = document.getElementById('current-time');
        if (timeElement) {
            timeElement.textContent = timeString;
        }
    }
    
    /**
     * Initialize copy to clipboard functionality
     */
    function initializeCopyButtons() {
        document.querySelectorAll('.copy-btn').forEach(button => {
            button.addEventListener('click', function() {
                const endpoint = this.getAttribute('data-endpoint');
                const fullUrl = window.location.origin + endpoint;
                
                // Copy to clipboard
                if (navigator.clipboard) {
                    navigator.clipboard.writeText(fullUrl).then(() => {
                        showCopySuccess(this);
                    });
                } else {
                    // Fallback for older browsers
                    const textArea = document.createElement('textarea');
                    textArea.value = fullUrl;
                    document.body.appendChild(textArea);
                    textArea.select();
                    document.execCommand('copy');
                    document.body.removeChild(textArea);
                    showCopySuccess(this);
                }
            });
        });
    }
    
    /**
     * Show copy success feedback
     */
    function showCopySuccess(button) {
        const originalIcon = button.innerHTML;
        button.innerHTML = '<i class="bi bi-check-lg"></i>';
        button.style.background = '#10B981';
        button.style.color = 'white';
        
        setTimeout(() => {
            button.innerHTML = originalIcon;
            button.style.background = '';
            button.style.color = '';
        }, 2000);
    }
});
