/* Custom Event Wizard Logic */

document.addEventListener('DOMContentLoaded', () => {
    let currentStep = 1;
    const totalSteps = 6; // 1:Basics, 2:Theme, 3:Food, 4:Media, 5:Review, 6:Payment

    // DOM Elements
    const steps = document.querySelectorAll('.wizard-step');
    const progressBar = document.querySelector('.wizard-progress-bar');
    const btnNext = document.getElementById('btnNext');
    const btnPrev = document.getElementById('btnPrev');
    const btnSubmit = document.getElementById('btnSubmit');

    // State to store event data
    const eventData = {
        baseCost: 0,
        totalCost: 0
    };

    /* --- Final Submission Logic --- */
    btnSubmit.addEventListener('click', () => {
        // Data is already in eventData...
        const payload = {
            eventName: eventData.eventName,
            eventType: eventData.eventType,
            eventDate: eventData.eventDate,
            guests: eventData.guests,
            location: eventData.eventLocation,
            theme: eventData.theme,
            decor: {
                stage: eventData.stageDecor,
                flowers: eventData.flowerDecor,
                lighting: eventData.lightingStyle
            },
            catering: {
                type: eventData.foodType,
                cost: document.getElementById('plateCost').value || 0
            },
            entertainment: eventData.music,
            media: {
                photo: eventData.photography,
                video: eventData.videography,
                drone: eventData.droneShoot
            },
            setup: {
                seating: document.getElementById('seating').value,
                security: eventData.security
            },
            notes: document.getElementById('specialReq').value,
            payment: eventData.payment,
            totalCost: document.getElementById('totalCostDisplay').innerText
        };

        // Send to Django Backend
        fetch('/api/custom-event', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken') // Function to get cookie needs to be defined or we use csrf_exempt
            },
            body: JSON.stringify(payload)
        })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    alert('Success! Your custom event has been saved.');
                    window.location.href = '/';
                } else {
                    alert('Error: ' + data.message);
                }
            })
            .catch((error) => {
                console.error('Error:', error);
                alert('Failed to connect to backend.');
            });
    });

    // Helper to get CSRF token (Django specific)
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    /* --- Navigation Functions --- */

    function updateWizard() {
        // Show/Hide Steps
        steps.forEach((step, index) => {
            if (index + 1 === currentStep) {
                step.classList.add('active');
            } else {
                step.classList.remove('active');
            }
        });

        // Update Progress Bar
        const progress = ((currentStep - 1) / (totalSteps - 1)) * 100;
        progressBar.style.width = `${progress}%`;

        // Button States
        if (currentStep === 1) {
            btnPrev.disabled = true;
        } else {
            btnPrev.disabled = false;
        }

        if (currentStep === totalSteps) { // Payment Step
            btnNext.classList.add('d-none');
            btnSubmit.classList.remove('d-none');
        } else {
            btnNext.classList.remove('d-none');
            btnSubmit.classList.add('d-none');
        }

        // Scroll to top
        document.querySelector('.wizard-container').scrollIntoView({ behavior: 'smooth' });
    }

    function validateStep(step) {
        // Simple validation: check if required inputs in current step are filled
        const currentStepEl = document.querySelector(`.wizard-step[data-step="${step}"]`);
        const requiredInputs = currentStepEl.querySelectorAll('input[required], select[required]');

        let isValid = true;
        requiredInputs.forEach(input => {
            if (!input.value) {
                isValid = false;
                input.classList.add('is-invalid');
            } else {
                input.classList.remove('is-invalid');
            }
        });

        return isValid;
    }

    /* --- Event Listeners --- */

    btnNext.addEventListener('click', () => {
        if (validateStep(currentStep)) {
            if (currentStep < totalSteps) {
                // Collect Data before moving
                collectData();
                calculateCost();
                if (currentStep === 4) generateReview(); // Generate review before step 5

                currentStep++;
                updateWizard();
            }
        } else {
            alert('Please fill in all required fields.');
        }
    });

    btnPrev.addEventListener('click', () => {
        if (currentStep > 1) {
            currentStep--;
            updateWizard();
        }
    });

    // Selection Card Click Logic
    document.querySelectorAll('.selection-card').forEach(card => {
        card.addEventListener('click', function () {
            // Find inputs within the same group
            const input = this.querySelector('input');
            const name = input.name;

            // Unselect others in group
            document.querySelectorAll(`input[name="${name}"]`).forEach(inp => {
                inp.closest('.selection-card').classList.remove('selected');
                inp.checked = false;
            });

            // Select this one
            this.classList.add('selected');
            input.checked = true;

            // Trigger calculation
            calculateCost();
        });
    });

    /* --- Logic Functions --- */

    function collectData() {
        // Gather inputs into eventData object
        const inputs = document.querySelectorAll('input, select, textarea');
        inputs.forEach(input => {
            if (input.type === 'radio') {
                if (input.checked) eventData[input.name] = input.value;
            } else if (input.type === 'checkbox') {
                eventData[input.id] = input.checked;
            } else {
                eventData[input.id] = input.value;
            }
        });
        console.log('Current Data:', eventData); // Debugging
    }

    function calculateCost() {
        let total = 0;
        const guests = parseInt(document.getElementById('guests').value) || 0;

        // 1. Basic Cost based on Type (Mock)
        if (eventData.eventType === 'wedding') total += 5000;
        else if (eventData.eventType === 'corporate') total += 3000;
        else total += 2000;

        // 2. Decor Cost
        if (eventData.theme) total += 1000;
        if (eventData.stageDecor) total += 500;

        // 3. Food Cost (Per Plate)
        const plateCost = parseInt(document.getElementById('plateCost').value) || 0;
        total += (plateCost * guests);

        // 4. Media
        if (eventData.photography === 'yes') total += 500;
        if (eventData.videography === '4k') total += 800;

        eventData.totalCost = total;

        // Update UI
        const costDisplay = document.getElementById('totalCostDisplay');
        if (costDisplay) costDisplay.innerText = `₹${total.toLocaleString()}`;

        const reviewTotal = document.getElementById('reviewTotal');
        if (reviewTotal) reviewTotal.innerText = `₹${total.toLocaleString()}`;
    }

    function generateReview() {
        const reviewList = document.getElementById('reviewList');
        reviewList.innerHTML = ''; // Clear previous

        const fieldsToReview = [
            { label: 'Event Name', key: 'eventName' },
            { label: 'Type', key: 'eventType' },
            { label: 'Date', key: 'eventDate' },
            { label: 'Guests', key: 'guests' },
            { label: 'Theme', key: 'theme' },
            { label: 'Catering', key: 'foodType' },
            { label: 'Total Estimated Cost', value: `₹${eventData.totalCost.toLocaleString()}` }
        ];

        fieldsToReview.forEach(field => {
            let val = field.value || eventData[field.key] || 'Not Selected';
            if (val === true) val = 'Yes';
            if (val === false) val = 'No';

            const item = document.createElement('div');
            item.className = 'review-item d-flex justify-content-between';
            item.innerHTML = `
                <span class="review-label">${field.label}</span>
                <span class="review-value text-capitalize">${val}</span>
            `;
            reviewList.appendChild(item);
        });
    }

    // Initial Setup
    updateWizard();
});
