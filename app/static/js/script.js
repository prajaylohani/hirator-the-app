let currentFileName = '';

window.addEventListener('load', function() {
    const form = document.getElementById('theForm');
    if (form) {
        // clear all fields to their default values on refresh
        form.reset();
    }
});

document.addEventListener('DOMContentLoaded', function() {
    const fileInput = document.getElementById('fileInput');
    const preview = document.getElementById('preview');

    if (!fileInput || !preview) {
        console.error('Required elements not found');
        return;
    }

    fileInput.addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (!file) {
            resetPreview();
            return;
        }

        // Store filename & extension
        currentFileName = file.name;

        // Validate extension
        const ext = file.name.split('.').pop().toLowerCase();
        if (!['yaml', 'yml', 'tex'].includes(ext)) {
            alert('Please select YAML (.yaml, .yml) or TeX (.tex) file');
            resetPreview();
            fileInput.value = '';
            return;
        }

        // Load preview
        const reader = new FileReader();
        reader.onload = function(e) {
            preview.value = e.target.result;
        };
        reader.readAsText(file);
    });
});

function loadSample(sampleURL) {
    fetch(sampleURL)
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to load sample');
            }
            return response.text();
        })
        .then(text => {
            document.getElementById('preview').value = text;
            currentFileName = 'sample.yaml';
            document.getElementById('fileInput').value = '';
        })
        .catch(error => {
            console.error('Error loading sample:', error);
            alert('Failed to load sample YAML');
        });
}

function resetPreview() {
    currentFileName = '';
    document.getElementById('preview').value = '';
}
