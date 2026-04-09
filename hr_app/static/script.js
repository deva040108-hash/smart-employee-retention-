document.addEventListener('DOMContentLoaded', () => {
    // Cache DOM Elements
    const form = document.getElementById('prediction-form');
    const resultsSection = document.getElementById('results-section');
    const submitBtn = document.getElementById('analyze-btn');
    const spinner = document.getElementById('loading-spinner');
    const btnText = submitBtn.querySelector('span');
    
    form.addEventListener('submit', async (e) => {
        // Prevent default form submission via browser
        e.preventDefault();
        
        // --- 1. Set Loading UI State ---
        btnText.classList.add('hidden');
        spinner.classList.remove('hidden');
        resultsSection.classList.add('hidden');
        submitBtn.disabled = true;

        // --- 2. Extract Data from Form ---
        const formData = new FormData(form);
        const requestData = Object.fromEntries(formData.entries());
        
        try {
            // --- 3. Make Fetch API Call to Flask Backend ---
            const response = await fetch('/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(requestData)
            });

            // Check if backend returned an error
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            // Parse JSON response
            const result = await response.json();
            
            // --- 4. Update UI with Predictions ---
            updateResultsUI(result);
            
            // Reveal the results block smoothly
            resultsSection.classList.remove('hidden');
            
            // Scroll user down to see the results
            setTimeout(() => {
                resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }, 100);

        } catch (error) {
            console.error('Error fetching prediction:', error);
            alert("Connection error! Make sure the Flask backend is running on port 5000.");
        } finally {
            // --- 5. Restore Button State ---
            btnText.classList.remove('hidden');
            spinner.classList.add('hidden');
            submitBtn.disabled = false;
        }
    });

    /**
     * Helper function to dynamically update the UI elements based on API response
     */
    function updateResultsUI(data) {
        // DOM Elements for Results
        const predText = document.getElementById('turnover-prediction');
        const riskLevel = document.getElementById('risk-level');
        const probText = document.getElementById('probability-score');
        const strategiesList = document.getElementById('strategies-list');
        const summaryCard = document.getElementById('summary-card');

        // Apply raw text values
        predText.textContent = data.prediction;
        riskLevel.textContent = data.risk_level;
        probText.textContent = `${data.probability}%`;

        // Strip previous risk classes from summary card and badge
        summaryCard.className = 'card result-card';
        riskLevel.className = 'risk-badge';

        // Apply dynamic conditional styling based on 'Risk Level'
        if (data.risk_level === 'High') {
            summaryCard.classList.add('risk-high');
            riskLevel.classList.add('badge-high');
        } else if (data.risk_level === 'Medium') {
            summaryCard.classList.add('risk-medium');
            riskLevel.classList.add('badge-medium');
        } else {
            summaryCard.classList.add('risk-low');
            riskLevel.classList.add('badge-low');
        }

        // Clear previous strategies
        strategiesList.innerHTML = '';
        
        // Loop over the list of strategies returned and append cleanly to list
        data.strategies.forEach(strategy => {
            const li = document.createElement('li');
            li.textContent = strategy;
            strategiesList.appendChild(li);
        });
    }
});
