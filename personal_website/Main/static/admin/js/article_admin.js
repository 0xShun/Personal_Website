document.addEventListener('DOMContentLoaded', function() {
    // Add current datetime button for created_at and updated_at fields
    const createdAtField = document.querySelector('#id_created_at');
    const updatedAtField = document.querySelector('#id_updated_at');
    
    function addCurrentTimeButton(field, fieldName) {
        if (!field) return;
        
        const fieldWrapper = field.closest('.field-' + fieldName);
        if (!fieldWrapper) return;
        
        // Create button
        const button = document.createElement('button');
        button.type = 'button';
        button.textContent = 'Use Current Time';
        button.className = 'button small-button';
        button.style.marginLeft = '10px';
        
        // Add click handler
        button.addEventListener('click', function() {
            const now = new Date();
            // Format as YYYY-MM-DDTHH:MM for datetime-local input
            const formattedDate = now.getFullYear() + '-' +
                String(now.getMonth() + 1).padStart(2, '0') + '-' +
                String(now.getDate()).padStart(2, '0') + 'T' +
                String(now.getHours()).padStart(2, '0') + ':' +
                String(now.getMinutes()).padStart(2, '0');
            
            field.value = formattedDate;
        });
        
        // Insert button after the input field
        field.parentNode.insertBefore(button, field.nextSibling);
    }
    
    // Add buttons for both fields
    addCurrentTimeButton(createdAtField, 'created_at');
    addCurrentTimeButton(updatedAtField, 'updated_at');
    
    // Add helpful placeholder text
    if (createdAtField) {
        createdAtField.placeholder = 'YYYY-MM-DD HH:MM';
    }
    if (updatedAtField) {
        updatedAtField.placeholder = 'YYYY-MM-DD HH:MM';
    }
});
