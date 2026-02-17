
function toggleLike(btn, eventId) {
    const icon = btn.querySelector('i');

    // Optimistic UI update
    const isLiked = btn.classList.contains('liked');

    if (isLiked) {
        btn.classList.remove('liked');
        icon.classList.remove('fas'); // Solid
        icon.classList.add('far');    // Outline
    } else {
        btn.classList.add('liked');
        icon.classList.remove('far');
        icon.classList.add('fas');
    }

    const url = `/api/toggle-like/${eventId}/`;

    fetch(url)
        .then(response => {
            if (response.status === 401) {
                // If not logged in, revert UI and redirect
                if (isLiked) {
                    btn.classList.add('liked');
                    icon.classList.add('fas');
                    icon.classList.remove('far');
                } else {
                    btn.classList.remove('liked');
                    icon.classList.add('far');
                    icon.classList.remove('fas');
                }
                window.location.href = "/login/";
                return null;
            }
            return response.json();
        })
        .then(data => {
            if (data && data.status === 'error') {
                console.error('Error toggling like:', data.message);
                // Revert on error
                if (isLiked) {
                    btn.classList.add('liked');
                    icon.classList.add('fas');
                    icon.classList.remove('far');
                } else {
                    btn.classList.remove('liked');
                    icon.classList.add('far');
                    icon.classList.remove('fas');
                }
            }
        })
        .catch(err => {
            console.error('Fetch error:', err);
            // Revert on error
            if (isLiked) {
                btn.classList.add('liked');
                icon.classList.add('fas');
                icon.classList.remove('far');
            } else {
                btn.classList.remove('liked');
                icon.classList.add('far');
                icon.classList.remove('fas');
            }
        });

    // Prevent card click
    event.stopPropagation();
}
