// AJAX Comment System
document.addEventListener('DOMContentLoaded', function() {
    const commentForms = document.querySelectorAll('form[action*="post_comment"]');
    
    commentForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const submitButton = form.querySelector('button[type="submit"]');
            const originalButtonText = submitButton.innerHTML;
            const formData = new FormData(form);
            
            // Show loading state
            submitButton.disabled = true;
            submitButton.innerHTML = '<i class="ri-loader-4-line ri-spin"></i> <span>Submitting...</span>';
            
            // Clear any previous messages
            clearMessages();
            
            // Submit via AJAX
            fetch(form.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': formData.get('csrfmiddlewaretoken')
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Show success message
                    showMessage(data.message, 'success');
                    
                    // Clear the form
                    form.reset();
                    
                    // Add the new comment to the DOM
                    addCommentToDOM(data.comment);
                    
                    // Scroll to the new comment or show success area
                    scrollToComments();
                } else {
                    // Show error message
                    showMessage(data.message, 'error');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showMessage('An error occurred while submitting your comment. Please try again.', 'error');
            })
            .finally(() => {
                // Restore button
                submitButton.disabled = false;
                submitButton.innerHTML = originalButtonText;
            });
        });
    });
    
    function showMessage(message, type) {
        // Remove existing messages
        clearMessages();
        
        // Create message element
        const messageDiv = document.createElement('div');
        messageDiv.className = `notion-callout notion-callout-${type} ajax-message`;
        messageDiv.innerHTML = `
            <div class="notion-callout-content">
                <p>${message}</p>
            </div>
        `;
        
        // Add close button
        const closeBtn = document.createElement('button');
        closeBtn.innerHTML = '×';
        closeBtn.className = 'message-close-btn';
        closeBtn.style.cssText = `
            position: absolute;
            top: 10px;
            right: 15px;
            background: none;
            border: none;
            font-size: 20px;
            cursor: pointer;
            color: inherit;
        `;
        closeBtn.onclick = () => messageDiv.remove();
        messageDiv.appendChild(closeBtn);
        
        // Style the message
        messageDiv.style.position = 'relative';
        messageDiv.style.marginBottom = '20px';
        messageDiv.style.animation = 'fadeIn 0.3s ease-in';
        
        // Insert message before the comment form
        const commentForm = document.querySelector('.notion-comment-form');
        if (commentForm) {
            commentForm.parentNode.insertBefore(messageDiv, commentForm);
        }
        
        // Auto-remove success messages after 5 seconds
        if (type === 'success') {
            setTimeout(() => {
                if (messageDiv.parentNode) {
                    messageDiv.style.animation = 'fadeOut 0.3s ease-out';
                    setTimeout(() => messageDiv.remove(), 300);
                }
            }, 5000);
        }
    }
    
    function clearMessages() {
        const existingMessages = document.querySelectorAll('.ajax-message');
        existingMessages.forEach(msg => msg.remove());
    }
    
    function addCommentToDOM(comment) {
        const commentsContainer = document.querySelector('.notion-comments');
        if (!commentsContainer) return;
        
        // Check if "no comments" message exists and remove it
        const noCommentsMsg = commentsContainer.parentNode.querySelector('.notion-callout:has(p)');
        if (noCommentsMsg && (noCommentsMsg.textContent.includes('Be the first to comment') || 
                              noCommentsMsg.textContent.includes('No comments yet'))) {
            noCommentsMsg.remove();
        }
        
        // Create new comment element
        const commentHTML = `
            <div class="notion-comment new-comment">
                <div class="notion-comment-header">
                    <div class="notion-comment-author">
                        ${comment.name}
                        ${comment.website ? `<a href="${comment.website}" target="_blank" rel="noopener noreferrer"><i class="ri-link"></i></a>` : ''}
                    </div>
                    <div class="notion-comment-date">${comment.created_at}</div>
                </div>
                <div class="notion-comment-content">
                    ${comment.content.replace(/\n/g, '<br>')}
                </div>
            </div>
        `;
        
        // Add to top of comments (since we order by -created_at)
        commentsContainer.insertAdjacentHTML('afterbegin', commentHTML);
        
        // Highlight new comment briefly
        const newComment = commentsContainer.querySelector('.new-comment');
        if (newComment) {
            newComment.style.animation = 'newCommentHighlight 2s ease-out';
            setTimeout(() => {
                newComment.classList.remove('new-comment');
                newComment.style.animation = '';
            }, 2000);
        }
    }
    
    function scrollToComments() {
        const commentsSection = document.querySelector('.notion-comments');
        if (commentsSection) {
            commentsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    }
});

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes fadeOut {
        from { opacity: 1; transform: translateY(0); }
        to { opacity: 0; transform: translateY(-10px); }
    }
    
    @keyframes newCommentHighlight {
        0% { background-color: rgba(0, 123, 255, 0.1); transform: scale(1.02); }
        50% { background-color: rgba(0, 123, 255, 0.05); }
        100% { background-color: transparent; transform: scale(1); }
    }
    
    .notion-callout-success {
        background-color: rgba(40, 167, 69, 0.1);
        border-left: 4px solid #28a745;
        color: #155724;
    }
    
    .notion-callout-error {
        background-color: rgba(220, 53, 69, 0.1);
        border-left: 4px solid #dc3545;
        color: #721c24;
    }
    
    .ri-spin {
        animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    
    .message-close-btn:hover {
        opacity: 0.7;
    }
`;
document.head.appendChild(style);
