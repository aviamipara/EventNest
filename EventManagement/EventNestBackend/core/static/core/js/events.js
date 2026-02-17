document.addEventListener('DOMContentLoaded', () => {
    const tabsContainer = document.getElementById('category-tabs');
    const eventsContainer = document.getElementById('events-container');
    const searchInput = document.getElementById('eventSearch');
    const sortSelect = document.getElementById('sortEvents');

    // Handle Sort Change
    if (sortSelect) {
        sortSelect.addEventListener('change', (e) => {
            const currentUrl = new URL(window.location.href);
            currentUrl.searchParams.set('sort', e.target.value);
            // Reset to page 1 on new sort
            currentUrl.searchParams.delete('page');
            window.location.href = currentUrl.toString();
        });
    }

    // Handle Category Click (server-side navigation for robustness)
    const buttons = document.querySelectorAll('.category-tab');
    buttons.forEach(btn => {
        btn.addEventListener('click', () => {
            const category = btn.getAttribute('data-category');
            const currentUrl = new URL(window.location.href);

            if (category === 'All') {
                currentUrl.searchParams.delete('category');
            } else {
                currentUrl.searchParams.set('category', category);
            }

            // Reset to page 1 on category change
            currentUrl.searchParams.delete('page');
            window.location.href = currentUrl.toString();
        });
    });

    // Client-side Search (Keep existing client-side text filter for speed on current page)
    if (searchInput) {
        const clearBtn = document.getElementById('clearSearch');

        searchInput.addEventListener('input', (e) => {
            const query = e.target.value.toLowerCase();
            const allCards = document.querySelectorAll('.event-card');
            let visibleCount = 0;

            // Show/Hide Clear Button
            if (clearBtn) {
                if (query.length > 0) {
                    clearBtn.classList.remove('d-none');
                } else {
                    clearBtn.classList.add('d-none');
                }
            }

            allCards.forEach(card => {
                const cardName = card.getAttribute('data-name');
                if (cardName.includes(query)) {
                    card.style.display = '';
                    visibleCount++;
                } else {
                    card.style.display = 'none';
                }
            });

            // Toggle No Results
            let noResultsMsg = document.getElementById('no-results-msg');
            if (visibleCount === 0) {
                if (!noResultsMsg) {
                    noResultsMsg = document.createElement('div');
                    noResultsMsg.id = 'no-results-msg';
                    noResultsMsg.className = 'col-12 text-center py-5';
                    noResultsMsg.innerHTML = '<p class="text-muted fs-5">No events matching your search.</p>';
                    eventsContainer.appendChild(noResultsMsg);
                }
                noResultsMsg.style.display = 'block';
            } else {
                if (noResultsMsg) noResultsMsg.style.display = 'none';
            }
        });

        if (clearBtn) {
            clearBtn.addEventListener('click', () => {
                searchInput.value = '';

                // If we are on the main events page (server-side search), we should reload to clear the URL query
                const urlParams = new URLSearchParams(window.location.search);
                if (urlParams.has('q')) {
                    urlParams.delete('q');
                    window.location.search = urlParams.toString();
                } else {
                    // Otherwise just trigger the input event for client-side filtering (Student Zone)
                    searchInput.dispatchEvent(new Event('input'));
                    searchInput.focus();
                }
            });
        }
    }

    // Server-side filtering is now primary.
    // Client-side search (above) is kept for instant feedback on the current page.
});

// Helper for the "Book Now" buttons to pre-fill the modal
function openBookingModal(eventName) {
    const modalEl = document.getElementById('bookingModal');
    if (modalEl) {
        const modal = new bootstrap.Modal(modalEl);
        const visionInput = document.getElementById('vision');
        if (visionInput) visionInput.value = `Inquiry for: ${eventName}`;
        modal.show();
    }
}

// EventNest UI Logic: Open Detail Modal on Card Click
function openEventModal(card) {
    const modalEl = document.getElementById('eventDetailsModal');
    if (!modalEl) return;

    // 1. Populate Data
    document.getElementById('modalTitle').textContent = card.getAttribute('data-title');
    document.getElementById('modalCategory').textContent = card.getAttribute('data-category');
    document.getElementById('modalDate').textContent = card.getAttribute('data-date');
    document.getElementById('modalLocation').textContent = card.getAttribute('data-location');
    // Price Parsing Logic
    let rawPrice = card.getAttribute('data-price') || '0';
    let cleanPrice = rawPrice.toLowerCase();
    let displayPrice = rawPrice;

    let firstDigitIdx = cleanPrice.search(/\d/);
    if (firstDigitIdx !== -1) {
        let numericPart = cleanPrice.substring(firstDigitIdx).replace(/[^\d.]/g, '');
        let priceValue = parseFloat(numericPart) || 0;

        // Handle 'k' multiplier
        if (cleanPrice.includes('k') && priceValue < 100) {
            priceValue *= 1000;
        }

        displayPrice = '₹' + Math.round(priceValue).toLocaleString('en-IN');
    }

    document.getElementById('modalPrice').textContent = displayPrice;
    document.getElementById('modalDescription').textContent = card.getAttribute('data-description');

    // Image
    const imgUrl = card.getAttribute('data-image');
    document.getElementById('modalImage').src = imgUrl;

    // Update Book Link
    const bookBtn = document.getElementById('modalBookBtn') || document.getElementById('modalBookLink');
    if (bookBtn) {
        bookBtn.href = `/booking/?event=${encodeURIComponent(card.getAttribute('data-title'))}`;
    }

    // 2. Show Modal
    const modal = new bootstrap.Modal(modalEl);
    modal.show();
}

function toggleLike(btn, eventId) {
    // 1. Get the heart icon
    const icon = btn.querySelector('i');
    const isLiked = btn.classList.contains('liked');

    // 2. Optimistic UI update
    if (isLiked) {
        btn.classList.remove('liked');
        icon.classList.remove('fas'); // Solid
        icon.classList.add('far');    // Outline
    } else {
        btn.classList.add('liked');
        icon.classList.remove('far');
        icon.classList.add('fas');
    }

    // 3. API Call
    fetch(`/api/toggle-like/${eventId}/`)
        .then(response => {
            if (response.status === 401) {
                // Not logged in -> revert and redirect
                window.location.href = "/login/";
                return null;
            }
            return response.json();
        })
        .then(data => {
            if (!data) return;
            if (data.status !== 'success') {
                // Revert UI on error
                if (isLiked) {
                    btn.classList.add('liked');
                    icon.classList.add('fas');
                    icon.classList.remove('far');
                } else {
                    btn.classList.remove('liked');
                    icon.classList.add('far');
                    icon.classList.remove('fas');
                }
                console.error('Like toggle failed:', data.message);
            }
        })
        .catch(err => {
            console.error('Like toggle error:', err);
        });

    // 4. Prevent bubbling if needed
    if (window.event) {
        window.event.stopPropagation();
    }
}
