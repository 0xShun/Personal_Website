document.addEventListener('DOMContentLoaded', function() {
    function toggleFields() {
        var pdfField = document.querySelector('.form-row.field-pdf_file, .form-group.field-pdf_file');
        var linkField = document.querySelector('.form-row.field-link, .form-group.field-link');
        var fileTypeRadios = document.getElementsByName('file_type');
        var selected = Array.from(fileTypeRadios).find(r => r.checked)?.value;
        if (selected === 'pdf') {
            if (pdfField) pdfField.style.display = '';
            if (linkField) linkField.style.display = 'none';
        } else if (selected === 'link') {
            if (pdfField) pdfField.style.display = 'none';
            if (linkField) linkField.style.display = '';
        }
    }
    var fileTypeRadios = document.getElementsByName('file_type');
    fileTypeRadios.forEach(function(radio) {
        radio.addEventListener('change', toggleFields);
    });
    toggleFields();
}); 