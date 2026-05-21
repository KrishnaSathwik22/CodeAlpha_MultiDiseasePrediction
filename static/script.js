document.addEventListener('DOMContentLoaded', () => {
    // Navigation Logic
    const navItems = document.querySelectorAll('.nav-item');
    const formSections = document.querySelectorAll('.form-section');
    const resultPanel = document.getElementById('result-panel');

    navItems.forEach(item => {
        item.addEventListener('click', () => {
            // Remove active class from all
            navItems.forEach(nav => nav.classList.remove('active'));
            formSections.forEach(section => section.classList.remove('active-section'));
            
            // Hide result panel when switching tabs
            resultPanel.classList.add('hidden');

            // Add active class to clicked
            item.classList.add('active');
            const targetId = item.getAttribute('data-target');
            document.getElementById(targetId).classList.add('active-section');
            
            // Update Body Theme
            const newTheme = item.getAttribute('data-theme');
            document.body.className = ''; // reset classes
            if (newTheme) {
                document.body.classList.add(newTheme);
            }
        });
    });

    // Form Submission Logic
    const forms = document.querySelectorAll('.prediction-form');
    
    forms.forEach(form => {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const disease = form.getAttribute('data-disease');
            const formData = new FormData(form);
            const data = {};
            
            formData.forEach((value, key) => {
                data[key] = parseFloat(value);
            });

            // Show loading state
            resultPanel.classList.remove('hidden');
            resultPanel.className = 'result-panel'; // reset themes
            
            const resultIconFa = document.getElementById('result-icon-fa');
            const resultTitle = document.getElementById('result-title');
            const resultProb = document.getElementById('result-probability');
            
            resultIconFa.className = 'fa-solid fa-circle-notch fa-spin';
            resultTitle.textContent = 'Processing...';
            resultProb.textContent = 'Analyzing biomarkers...';

            try {
                const response = await fetch(`/predict/${disease}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(data)
                });

                const result = await response.json();

                if (response.ok) {
                    // Update UI with results
                    resultTitle.textContent = result.result_text;
                    const probPercent = (result.probability * 100).toFixed(1);
                    resultProb.textContent = `Confidence: ${probPercent}%`;
                    
                    // The backend might return different logic for positive/negative. 
                    // Let's assume prediction == 1 means High Risk / Positive for all.
                    if (result.prediction === 1) {
                        resultPanel.classList.add('theme-danger');
                        resultIconFa.className = 'fa-solid fa-triangle-exclamation';
                    } else {
                        resultPanel.classList.add('theme-success');
                        resultIconFa.className = 'fa-solid fa-check-circle';
                    }
                } else {
                    resultTitle.textContent = 'Error';
                    resultProb.textContent = result.error || 'An unexpected error occurred.';
                    resultIconFa.className = 'fa-solid fa-circle-xmark';
                }
            } catch (error) {
                resultTitle.textContent = 'Network Error';
                resultProb.textContent = 'Failed to connect to the server.';
                resultIconFa.className = 'fa-solid fa-circle-xmark';
            }
        });
    });
});
