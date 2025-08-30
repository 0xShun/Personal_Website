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
        button.style.fontSize = '12px';
        button.style.padding = '5px 10px';
        
        // Add click handler
        button.addEventListener('click', function() {
            const now = new Date();
            // Format as YYYY-MM-DDTHH:MM for datetime-local input
            const year = now.getFullYear();
            const month = String(now.getMonth() + 1).padStart(2, '0');
            const day = String(now.getDate()).padStart(2, '0');
            const hours = String(now.getHours()).padStart(2, '0');
            const minutes = String(now.getMinutes()).padStart(2, '0');
            
            const formattedDate = `${year}-${month}-${day}T${hours}:${minutes}`;
            
            field.value = formattedDate;
            
            // Trigger change event
            field.dispatchEvent(new Event('change'));
        });
        
        // Insert button after the input field
        field.parentNode.appendChild(button);
    }
    
    // Add buttons for both fields
    addCurrentTimeButton(createdAtField, 'created_at');
    addCurrentTimeButton(updatedAtField, 'updated_at');
    
    // Format existing datetime values for display
    function formatDateTimeForInput(field) {
        if (!field || !field.value) return;
        
        // If value doesn't match datetime-local format, try to convert it
        const value = field.value;
        if (value && !value.includes('T') && value.includes(' ')) {
            // Convert from "YYYY-MM-DD HH:MM:SS" to "YYYY-MM-DDTHH:MM"
            const parts = value.split(' ');
            if (parts.length >= 2) {
                const datePart = parts[0];
                const timePart = parts[1].substring(0, 5); // Get HH:MM
                field.value = `${datePart}T${timePart}`;
            }
        }
    }
    
    // Format existing values
    formatDateTimeForInput(createdAtField);
    formatDateTimeForInput(updatedAtField);
});
