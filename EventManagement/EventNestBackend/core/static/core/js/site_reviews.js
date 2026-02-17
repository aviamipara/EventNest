// Helper to get cookie
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

document.addEventListener('DOMContentLoaded', function () {
    console.log("Site Reviews JS v1.2 Loaded");
    const siteReviewForm = document.getElementById('siteReviewForm');
    const submitBtn = document.getElementById('submitSiteReviewBtn');
    const ratingError = document.getElementById('siteRatingError');

    if (siteReviewForm) {
        siteReviewForm.addEventListener('submit', function (e) {
            e.preventDefault();

            // Validation
            const rating = siteReviewForm.querySelector('input[name="rating"]:checked');
            if (!rating) {
                ratingError.classList.remove('d-none');
                return;
            }
            ratingError.classList.add('d-none');

            // Disable button & show loading
            const originalBtnText = submitBtn.innerHTML;
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span> Submitting...';

            const formData = new FormData(siteReviewForm);
            const data = {
                client_name: formData.get('client_name'),
                client_role: formData.get('client_role'),
                rating: parseInt(formData.get('rating')),
                quote: formData.get('quote')
            };

            const csrftoken = formData.get('csrfmiddlewaretoken') || getCookie('csrftoken');

            fetch('/api/reviews/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken
                },
                body: JSON.stringify(data)
            })
                .then(async response => {
                    const contentType = response.headers.get("content-type");
                    if (response.ok) {
                        return response.json();
                    } else {
                        // Handle non-JSON errors (like 500 HTML page)
                        if (contentType && contentType.indexOf("application/json") !== -1) {
                            return response.json().then(err => { throw err; });
                        } else {
                            const text = await response.text();
                            console.error("Server API Error (Non-JSON):", text);
                            throw new Error(`Server Error: ${response.status} ${response.statusText}`);
                        }
                    }
                })
                .then(result => {
                    // Success!
                    const modal = bootstrap.Modal.getInstance(document.getElementById('siteReviewModal'));
                    modal.hide();

                    // Show success modal
                    const successModal = new bootstrap.Modal(document.getElementById('reviewSuccessModal'));
                    successModal.show();

                    // Reset form
                    siteReviewForm.reset();
                    submitBtn.disabled = false;
                    submitBtn.innerHTML = originalBtnText;
                })
                .catch(error => {
                    console.error('Error:', error);
                    let msg = 'An error occurred. Please try again.';

                    if (error.detail) {
                        msg = error.detail;
                    } else if (error.message) {
                        msg = error.message;
                    } else if (typeof error === 'object') {
                        // Handle DRF validation errors (e.g. {"field": ["Error message"]})
                        let errors = [];
                        for (const [key, value] of Object.entries(error)) {
                            const errorText = Array.isArray(value) ? value.join(', ') : value;
                            errors.push(`${key}: ${errorText}`);
                        }
                        if (errors.length > 0) {
                            msg = errors.join('\n');
                        }
                    }

                    alert(msg);
                    submitBtn.disabled = false;
                    submitBtn.innerHTML = originalBtnText;
                });
        });
    }
});
