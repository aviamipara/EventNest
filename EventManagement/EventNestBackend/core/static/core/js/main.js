// Main initialization
document.addEventListener('DOMContentLoaded', async () => {
    // Handle Hash Navigation (Scroll to section after load)
    if (window.location.hash) {
        const hash = window.location.hash;
        setTimeout(() => {
            const element = document.querySelector(hash);
            if (element) {
                element.scrollIntoView({ behavior: 'smooth' });
            }
        }, 300); // Slight delay to ensure DOM is ready
    }

    // Initialize AOS Animation with optimized settings
    try {
        AOS.init({
            duration: 800,
            once: true,
            offset: 50,
            easing: 'ease-out-cubic',
        });
    } catch (e) {
        console.warn("AOS not loaded", e);
    }

    // Navbar Scroll Effect - Removed to keep navbar permanently white
    // const navbar = document.querySelector('.navbar');
    // if (navbar) {
    //    navbar.classList.add('bg-white', 'shadow-sm');
    // }

    // Gallery Filter Logic
    const filterButtons = document.querySelectorAll('.filter-btn');
    const galleryItems = document.querySelectorAll('.gallery-container > div'); // Assuming direct children are cols

    if (filterButtons.length > 0) {
        filterButtons.forEach(btn => {
            btn.addEventListener('click', () => {
                // Remove active class from all
                filterButtons.forEach(b => b.classList.remove('active'));
                // Add to clicked
                btn.classList.add('active');

                const filterValue = btn.getAttribute('data-filter');

                galleryItems.forEach(item => {
                    const itemCategory = item.getAttribute('data-category');

                    if (filterValue === 'all' || itemCategory === filterValue) {
                        item.style.display = 'block';
                    } else {
                        item.style.display = 'none';
                    }
                });
            });
        });
    }

    console.log("UX scripts ready.");
});
