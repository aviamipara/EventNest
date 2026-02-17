/* Main JavaScript for EventNest */

// Event Data
const eventsData = [
    {
        id: 1,
        title: "Electronic Dreams",
        date: "Oct 12, 2024",
        price: "₹12,000",
        category: "Music",
        image: "assets/images/event_concert_1767965755734.png",
        description: "A night of immersive electronic beats and outstanding visuals."
    },
    {
        id: 2,
        title: "Global Startup Meet",
        date: "Nov 05, 2024",
        price: "₹25,000",
        category: "Business",
        image: "assets/images/event_business_1767965776179.png",
        description: "Connect with investors and founders from around the globe."
    },
    {
        id: 3,
        title: "Creative Art Workshop",
        date: "Oct 20, 2024",
        price: "₹3,500",
        category: "Workshops",
        image: "assets/images/event_workshop_1767965814183.png",
        description: "Unleash your creativity with hands-on painting and sculpting."
    },
    {
        id: 4,
        title: "Community Meetup",
        date: "Every Friday",
        price: "Free",
        category: "Private",
        image: "assets/images/event_networking_1767965836836.png",
        description: "Weekly gathering for local tech enthusiasts."
    },
    {
        id: 5,
        title: "Jazz Evening",
        date: "Nov 12, 2024",
        price: "₹6,500",
        category: "Music",
        image: "assets/images/event_concert_1767965755734.png",
        description: "Smooth jazz performances under the stars."
    },
    {
        id: 6,
        title: "Future AI Conference",
        date: "Dec 01, 2024",
        price: "₹40,000",
        category: "Business",
        image: "assets/images/event_business_1767965776179.png",
        description: "Deep dive into the future of Artificial Intelligence."
    },
    {
        id: 7,
        title: "Tech Innovation Summit",
        date: "Jan 15, 2025",
        price: "₹15,000",
        category: "Business",
        image: "assets/images/event_tech_summit_1767975078707.png",
        description: "Explore the latest trends in technology and innovation."
    },
    {
        id: 8,
        title: "Indie Music Fest",
        date: "Feb 20, 2025",
        price: "₹5,000",
        category: "Music",
        image: "assets/images/event_indie_fest_1767975098730.png",
        description: "A vibrant festival featuring the best indie bands."
    },
    {
        id: 9,
        title: "Photography Masterclass",
        date: "Mar 10, 2025",
        price: "₹8,000",
        category: "Workshops",
        image: "assets/images/event_photo_masterclass_1767975119057.png",
        description: "Learn professional photography techniques from experts."
    },
    {
        id: 10,
        title: "Neon Cyber Party",
        date: "Apr 05, 2025",
        price: "₹10,000",
        category: "Music",
        image: "assets/images/event_neon_party.png",
        description: "Step into the future with a neon-themed dance night."
    },
    {
        id: 11,
        title: "Corporate Leadership Seminar",
        date: "Apr 15, 2025",
        price: "₹30,000",
        category: "Business",
        image: "assets/images/event_leadership.png",
        description: "Enhance your leadership skills with top industry mentors."
    },
    {
        id: 12,
        title: "Pottery Basics",
        date: "Apr 20, 2025",
        price: "₹2,500",
        category: "Workshops",
        image: "assets/images/event_pottery.png",
        description: "Get your hands dirty and make something beautiful."
    },
    {
        id: 13,
        title: "Private Yacht Party",
        date: "May 01, 2025",
        price: "₹1,50,000",
        category: "Private",
        image: "assets/images/event_yacht.png",
        description: "Exclusive party on a luxury yacht for select guests."
    },
    {
        id: 14,
        title: "Classical Symphony",
        date: "May 10, 2025",
        price: "₹7,000",
        category: "Music",
        image: "assets/images/event_symphony.png",
        description: "A mesmerizing evening of Mozart and Beethoven."
    },
    {
        id: 15,
        title: "Digital Marketing Bootcamp",
        date: "Jun 01, 2025",
        price: "₹12,000",
        category: "Workshops",
        image: "assets/images/event_marketing.png",
        description: "Master the art of online marketing in 3 days."
    },
    {
        id: 16,
        title: "Wedding Expo 2025",
        date: "Jun 15, 2025",
        price: "₹1,000",
        category: "Business",
        image: "assets/images/event_wedding_expo.png",
        description: "Meet the best wedding planners and vendors in the city."
    },
    {
        id: 17,
        title: "Summer Pool Bash",
        date: "Jul 04, 2025",
        price: "₹4,000",
        category: "Private",
        image: "assets/images/event_pool_party.png",
        description: "Beat the heat with the coolest pool party in town."
    },
    {
        id: 18,
        title: "Cooking with Stars",
        date: "Jul 20, 2025",
        price: "₹9,000",
        category: "Workshops",
        image: "assets/images/event_cooking.png",
        description: "Cook alongside celebrity chefs."
    },
    {
        id: 19,
        title: "Rock N Roll Night",
        date: "Aug 12, 2025",
        price: "₹5,500",
        category: "Music",
        image: "assets/images/event_rock.png",
        description: "High energy rock performances all night long."
    },
    {
        id: 20,
        title: "Blockchain Summit",
        date: "Sep 05, 2025",
        price: "₹35,000",
        category: "Business",
        image: "assets/images/event_blockchain.png",
        description: "Understand the future of decentralized finance."
    }
];

document.addEventListener('DOMContentLoaded', () => {
    // 1. Navbar scroll effect
    const header = document.querySelector('header');

    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
    });

    // 2. Dynamic Event Rendering (for events.html)
    const eventsContainer = document.getElementById('events-grid');
    if (eventsContainer) {
        renderEvents(eventsData);

        // Filter Logic
        const filterBtns = document.querySelectorAll('.filter-btn');
        filterBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                // Remove active class from all
                filterBtns.forEach(b => b.classList.remove('active'));
                // Add active to click
                btn.classList.add('active');

                const category = btn.textContent;
                if (category === 'All') {
                    renderEvents(eventsData);
                } else {
                    const filtered = eventsData.filter(event => event.category === category);
                    renderEvents(filtered);
                }
            });
        });

        // Search Logic
        const searchInput = document.getElementById('event-search');
        if (searchInput) {
            searchInput.addEventListener('input', (e) => {
                const searchTerm = e.target.value.toLowerCase();
                const activeBtn = document.querySelector('.filter-btn.active');
                const category = activeBtn ? activeBtn.textContent : 'All';

                let filtered = eventsData;

                // 1. Filter by Category first
                if (category !== 'All') {
                    filtered = filtered.filter(event => event.category === category);
                }

                // 2. Filter by Search term
                filtered = filtered.filter(event =>
                    event.title.toLowerCase().includes(searchTerm) ||
                    event.description.toLowerCase().includes(searchTerm)
                );

                renderEvents(filtered);
            });
        }
    }

    // 3. Contact Form Validation (Simple)
    const contactForm = document.querySelector('form');
    if (contactForm && !contactForm.id) { // Avoid conflicting with booking form
        contactForm.addEventListener('submit', (e) => {
            e.preventDefault();
            // Simple validation check
            const inputs = contactForm.querySelectorAll('input, textarea');
            let isValid = true;
            inputs.forEach(input => {
                if (!input.value.trim()) isValid = false;
            });

            if (isValid) {
                alert('Thank you! Your message has been sent successfully.');
                contactForm.reset();
            } else {
                alert('Please fill in all fields.');
            }
        });
    }

    // 4. Mobile Menu Toggle
    const mobileToggle = document.querySelector('.mobile-toggle');
    const navLinks = document.querySelector('.nav-links');

    if (mobileToggle) {
        mobileToggle.addEventListener('click', () => {
            navLinks.classList.toggle('active');

            // Toggle icon shape
            const icon = mobileToggle.querySelector('i');
            if (navLinks.classList.contains('active')) {
                icon.classList.remove('fa-bars');
                icon.classList.add('fa-xmark');
            } else {
                icon.classList.remove('fa-xmark');
                icon.classList.add('fa-bars');
            }
        });

        // Close menu when clicking a link
        navLinks.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                navLinks.classList.remove('active');
                mobileToggle.querySelector('i').classList.remove('fa-xmark');
                mobileToggle.querySelector('i').classList.add('fa-bars');
            });
        });
    }
    // 5. FAQ Accordion
    const faqItems = document.querySelectorAll('.faq-item');
    if (faqItems) {
        faqItems.forEach(item => {
            const question = item.querySelector('.faq-question');
            question.addEventListener('click', () => {
                // Close others
                faqItems.forEach(otherItem => {
                    if (otherItem !== item) otherItem.classList.remove('active');
                });
                // Toggle current
                item.classList.toggle('active');
            });
        });
    }

    // 6. Stats Counter Animation
    const stats = document.querySelectorAll('.stat-item h3');
    if (stats.length > 0) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const target = entry.target;
                    const value = parseInt(target.innerText.replace(/\D/g, ''));
                    const suffix = target.innerText.replace(/[0-9]/g, '');

                    let count = 0;
                    const duration = 2000; // 2 seconds
                    const increment = value / (duration / 16); // 60fps

                    const updateCount = () => {
                        count += increment;
                        if (count < value) {
                            target.innerText = Math.ceil(count) + suffix;
                            requestAnimationFrame(updateCount);
                        } else {
                            target.innerText = value + suffix;
                        }
                    };
                    updateCount();
                    observer.unobserve(target);
                }
            });
        }, { threshold: 0.5 });

        stats.forEach(stat => observer.observe(stat));
    }
});

function renderEvents(events) {
    const container = document.getElementById('events-grid');
    container.innerHTML = ''; // Clear existing

    events.forEach(event => {
        const card = document.createElement('div');
        card.classList.add('card');
        card.innerHTML = `
            <div class="price-tag">${event.price}</div>
            <div class="event-img-container">
                <img src="${event.image}" alt="${event.title}">
            </div>
            <h3>${event.title}</h3>
            <p style="margin-bottom: 10px; color: var(--accent);"><i class="fa-regular fa-calendar"></i> ${event.date}</p>
            <p style="margin-bottom: 20px;">${event.description}</p>
            <a href="booking.html?event=${encodeURIComponent(event.title)}" class="btn btn-outline" style="width: 100%; text-align: center;">Book Ticket</a>
        `;
        // Animation delay for nice functionality
        card.style.animation = 'fadeIn 0.5s ease-in-out';
        container.appendChild(card);
    });
}
