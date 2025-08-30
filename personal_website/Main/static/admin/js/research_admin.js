document.addEventListener('DOMContentLoaded', function() {
    const statusField = document.querySelector('#id_status');
    const abstractField = document.querySelector('#id_abstract');
    const publishedDateField = document.querySelector('#id_published_date');
    
    function toggleFields() {
        const isOngoing = statusField.value === 'ongoing';
        
        // Get the field containers (usually the parent div)
        const abstractContainer = abstractField.closest('.field-abstract');
        const publishedDateContainer = publishedDateField.closest('.field-published_date');
        
        // Toggle required attribute and visual indicators
        if (isOngoing) {
            // Make fields optional for ongoing research
            abstractField.removeAttribute('required');
            publishedDateField.removeAttribute('required');
            
            // Add visual indication that these fields are optional
            if (abstractContainer) {
                const abstractLabel = abstractContainer.querySelector('label');
                if (abstractLabel && !abstractLabel.textContent.includes('(optional)')) {
                    abstractLabel.textContent = abstractLabel.textContent.replace('*', '') + ' (optional for ongoing research)';
                    abstractLabel.style.fontWeight = 'normal';
                }
            }
            
            if (publishedDateContainer) {
                const publishedDateLabel = publishedDateContainer.querySelector('label');
                if (publishedDateLabel && !publishedDateLabel.textContent.includes('(optional)')) {
                    publishedDateLabel.textContent = publishedDateLabel.textContent.replace('*', '') + ' (optional for ongoing research)';
                    publishedDateLabel.style.fontWeight = 'normal';
                }
            }
        } else {
            // Make fields required for completed research
            abstractField.setAttribute('required', 'required');
            publishedDateField.setAttribute('required', 'required');
            
            // Remove optional indicators
            if (abstractContainer) {
                const abstractLabel = abstractContainer.querySelector('label');
                if (abstractLabel) {
                    abstractLabel.textContent = abstractLabel.textContent.replace(' (optional for ongoing research)', '');
                    if (!abstractLabel.textContent.includes('*')) {
                        abstractLabel.textContent = abstractLabel.textContent + ' *';
                    }
                    abstractLabel.style.fontWeight = 'bold';
                }
            }
            
            if (publishedDateContainer) {
                const publishedDateLabel = publishedDateContainer.querySelector('label');
                if (publishedDateLabel) {
                    publishedDateLabel.textContent = publishedDateLabel.textContent.replace(' (optional for ongoing research)', '');
                    if (!publishedDateLabel.textContent.includes('*')) {
                        publishedDateLabel.textContent = publishedDateLabel.textContent + ' *';
                    }
                    publishedDateLabel.style.fontWeight = 'bold';
                }
            }
        }
    }
    
    // Initial setup
    if (statusField) {
        toggleFields();
        
        // Listen for changes
        statusField.addEventListener('change', toggleFields);
    }
});
