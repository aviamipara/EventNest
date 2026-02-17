const galleryData = [
    // Wedding (Local Images + Placeholders)
    { id: 1, category: "wedding", image: "../images/cat_wedding.png", title: "Royal Wedding Ceremony" },
    { id: 2, category: "wedding", image: "https://images.unsplash.com/photo-1519741497674-611481863552?auto=format&fit=crop&w=800&q=80", title: "Grand Reception" },
    { id: 3, category: "wedding", image: "https://images.unsplash.com/photo-1511285560982-1356c11d4606?auto=format&fit=crop&w=800&q=80", title: "Floral Decor" },
    { id: 4, category: "wedding", image: "https://images.unsplash.com/photo-1520342868574-5fa3804e551c?auto=format&fit=crop&w=800&q=80", title: "Bride Entry" },
    { id: 5, category: "wedding", image: "https://images.unsplash.com/photo-1522673607200-1645062cd958?auto=format&fit=crop&w=800&q=80", title: "Groom Preparation" },
    { id: 6, category: "wedding", image: "https://images.unsplash.com/photo-1507915977619-6ccfe8003ae6?auto=format&fit=crop&w=800&q=80", title: "Mandap Setup" },
    { id: 7, category: "wedding", image: "https://images.unsplash.com/photo-1525268771113-32d9e9021a97?auto=format&fit=crop&w=800&q=80", title: "Sangeet Night" },
    { id: 8, category: "wedding", image: "https://images.unsplash.com/photo-1606800052052-a08af7148866?auto=format&fit=crop&w=800&q=80", title: "Haldi Ceremony" },
    { id: 9, category: "wedding", image: "https://images.unsplash.com/photo-1515934751635-c81c6bc9a2d8?auto=format&fit=crop&w=800&q=80", title: "Wedding Vows" },
    { id: 10, category: "wedding", image: "https://images.unsplash.com/photo-1465495976277-4387d4b0b4c6?auto=format&fit=crop&w=800&q=80", title: "Couple Shoot" },
    { id: 11, category: "wedding", image: "https://images.unsplash.com/photo-1519225469958-19e5db4109f2?auto=format&fit=crop&w=800&q=80", title: "Wedding Dinner" },

    // Corporate (Local + Placeholders)
    { id: 12, category: "corporate", image: "../images/cat_corporate.png", title: "Business Conference" },
    { id: 13, category: "corporate", image: "https://images.unsplash.com/photo-1515187029135-18ee286d815b?auto=format&fit=crop&w=800&q=80", title: "Tech Summit" },
    { id: 14, category: "corporate", image: "https://images.unsplash.com/photo-1556761175-5973dc0f32e7?auto=format&fit=crop&w=800&q=80", title: "Networking Event" },
    { id: 15, category: "corporate", image: "https://images.unsplash.com/photo-1542744173-8e7e53415bb0?auto=format&fit=crop&w=800&q=80", title: "Product Launch" },
    { id: 16, category: "corporate", image: "https://images.unsplash.com/photo-1505373877841-8d43f703fb8f?auto=format&fit=crop&w=800&q=80", title: "Team Building" },
    { id: 17, category: "corporate", image: "https://images.unsplash.com/photo-1511632765486-a01980e01a18?auto=format&fit=crop&w=800&q=80", title: "Annual Meeting" },
    { id: 18, category: "corporate", image: "https://images.unsplash.com/photo-1524178232363-1fb2b075b655?auto=format&fit=crop&w=800&q=80", title: "Award Night" },
    { id: 19, category: "corporate", image: "https://images.unsplash.com/photo-1591115765373-5207764f72e7?auto=format&fit=crop&w=800&q=80", title: "Workshop Session" },
    { id: 20, category: "corporate", image: "https://images.unsplash.com/photo-1475721027767-pnsj1423?auto=format&fit=crop&w=800&q=80", title: "Seminar Hall" },

    // Birthday
    { id: 21, category: "birthday", image: "../images/cat_birthday.png", title: "Kids Birthday Info" },
    { id: 22, category: "birthday", image: "https://images.unsplash.com/photo-1530103862676-de3c9a59af57?auto=format&fit=crop&w=800&q=80", title: "Surprise Party" },
    { id: 23, category: "birthday", image: "https://images.unsplash.com/photo-1464349153912-bc6163bd89a7?auto=format&fit=crop&w=800&q=80", title: "Cake Cutting" },
    { id: 24, category: "birthday", image: "https://images.unsplash.com/photo-1563720760-4963574d7547?auto=format&fit=crop&w=800&q=80", title: "Decoration Setup" },
    { id: 25, category: "birthday", image: "https://images.unsplash.com/photo-1558223694-84d5df2ae047?auto=format&fit=crop&w=800&q=80", title: "Live Magic Show" },
    { id: 26, category: "birthday", image: "https://images.unsplash.com/photo-1574041113546-d250320ba17d?auto=format&fit=crop&w=800&q=80", title: "1st Birthday" },
    { id: 27, category: "birthday", image: "https://images.unsplash.com/photo-1621539257602-0c9f1fe746a5?auto=format&fit=crop&w=800&q=80", title: "Sweet 16" },

    // Concerts
    { id: 31, category: "concert", image: "../images/cat_music.png", title: "Live Band" },
    { id: 32, category: "concert", image: "https://images.unsplash.com/photo-1501281668745-f7f57925c3b4?auto=format&fit=crop&w=800&q=80", title: "Rock Concert" },
    { id: 33, category: "concert", image: "https://images.unsplash.com/photo-1514525253440-b393452e3383?auto=format&fit=crop&w=800&q=80", title: "DJ Night" },
    { id: 34, category: "concert", image: "https://images.unsplash.com/photo-1493225255756-d9584f8606e9?auto=format&fit=crop&w=800&q=80", title: "Jazz Festival" },
    { id: 35, category: "concert", image: "https://images.unsplash.com/photo-1533174072545-e8d4aa97edf9?auto=format&fit=crop&w=800&q=80", title: "Music Crowd" }
];

let currentFilter = "all";
let currentPaginationPage = 1;
const galleryItemsPerPage = 9;
let filteredGalleryData = [];

document.addEventListener('DOMContentLoaded', () => {
    const galleryGrid = document.getElementById('gallery-grid');
    const filterContainer = document.getElementById('gallery-filters');
    const pagContainers = document.getElementById('gallery-pagination');
    const searchInput = document.getElementById('gallerySearch'); // From Hero

    if (!galleryGrid || !filterContainer) return;

    // Filters
    renderFilters();

    // Initial Load
    filterAndRenderGallery();

    // Search Listener
    if (searchInput) {
        searchInput.addEventListener('input', (e) => {
            currentPaginationPage = 1;
            filterAndRenderGallery(e.target.value);
        });
    }

    // --- Helpers ---

    function renderFilters() {
        // Unique categories from data
        const categories = ["all", "wedding", "corporate", "birthday", "concert"];

        filterContainer.innerHTML = '';
        categories.forEach(cat => {
            const btn = document.createElement('button');
            btn.className = `btn btn-outline-navy filter-btn rounded-pill px-4 ${cat === currentFilter ? 'active' : ''}`;
            btn.textContent = cat === "all" ? "All Moments" : cat.charAt(0).toUpperCase() + cat.slice(1);
            btn.addEventListener('click', () => {
                currentFilter = cat;
                currentPaginationPage = 1;
                searchInput.value = ''; // Reset search
                updateActiveFilterBtn();
                filterAndRenderGallery();
            });
            filterContainer.appendChild(btn);
        });
    }

    function updateActiveFilterBtn() {
        const btns = filterContainer.querySelectorAll('.filter-btn');
        btns.forEach(btn => {
            if (btn.textContent.toLowerCase().includes(currentFilter === 'all' ? 'all' : currentFilter)) {
                btn.classList.add('active');
                btn.classList.remove('btn-outline-navy');
                btn.classList.add('btn-navy'); // Assume fill class exists or use style
                btn.style.backgroundColor = 'var(--accent-color)';
                btn.style.color = '#fff';
            } else {
                btn.classList.remove('active');
                btn.classList.add('btn-outline-navy');
                btn.classList.remove('btn-navy');
                btn.style.backgroundColor = 'transparent';
                btn.style.color = 'var(--accent-color)';
            }
        });
    }

    function filterAndRenderGallery(searchTerm = '') {
        const query = searchTerm.toLowerCase();

        // Filter by Category
        let candidates = galleryData;
        if (currentFilter !== "all") {
            candidates = galleryData.filter(item => item.category === currentFilter);
        }

        // Filter by Search
        if (query) {
            candidates = candidates.filter(item =>
                item.title.toLowerCase().includes(query) ||
                item.category.toLowerCase().includes(query)
            );
        }

        filteredGalleryData = candidates;
        renderGrid();
        renderPaginationUI();
    }

    function renderGrid() {
        galleryGrid.innerHTML = '';

        const start = (currentPaginationPage - 1) * galleryItemsPerPage;
        const end = start + galleryItemsPerPage;
        const pageItems = filteredGalleryData.slice(start, end);

        if (pageItems.length === 0) {
            galleryGrid.innerHTML = '<div class="col-12 text-center text-muted">No images found.</div>';
            return;
        }

        pageItems.forEach((item, index) => {
            // Slight delay for stagger effect (optional, handled by AOS usually)
            const delay = (index % 3) * 100;

            const col = document.createElement('div');
            col.className = 'col-md-4 col-sm-6';
            col.setAttribute('data-aos', 'fade-up');
            col.setAttribute('data-aos-delay', delay);

            col.innerHTML = `
                <div class="gallery-item-card">
                    <img src="${item.image}" alt="${item.title}" class="img-fluid rounded shadow hover-scale w-100 img-cover-300">
                    <div class="gallery-overlay">
                        <h5>${item.title}</h5>
                    </div>
                </div>
            `;
            galleryGrid.appendChild(col);
        });
    }

    function renderPaginationUI() {
        if (!pagContainers) return;
        pagContainers.innerHTML = '';

        const totalPages = Math.ceil(filteredGalleryData.length / galleryItemsPerPage);

        if (totalPages <= 1) return;

        // Container for buttons
        const nav = document.createElement('nav');
        const ul = document.createElement('ul');
        ul.className = 'pagination justify-content-center';

        // Prev
        const prevLi = document.createElement('li');
        prevLi.className = `page-item ${currentPaginationPage === 1 ? 'disabled' : ''}`;
        prevLi.innerHTML = `<a class="page-link" href="#">Previous</a>`;
        prevLi.onclick = (e) => { e.preventDefault(); if (currentPaginationPage > 1) { currentPaginationPage--; renderGrid(); renderPaginationUI(); } };
        ul.appendChild(prevLi);

        // Numbers
        for (let i = 1; i <= totalPages; i++) {
            const li = document.createElement('li');
            li.className = `page-item ${i === currentPaginationPage ? 'active' : ''}`;
            li.innerHTML = `<a class="page-link" href="#">${i}</a>`;
            li.onclick = (e) => { e.preventDefault(); currentPaginationPage = i; renderGrid(); renderPaginationUI(); };
            ul.appendChild(li);
        }

        // Next
        const nextLi = document.createElement('li');
        nextLi.className = `page-item ${currentPaginationPage === totalPages ? 'disabled' : ''}`;
        nextLi.innerHTML = `<a class="page-link" href="#">Next</a>`;
        nextLi.onclick = (e) => { e.preventDefault(); if (currentPaginationPage < totalPages) { currentPaginationPage++; renderGrid(); renderPaginationUI(); } };
        ul.appendChild(nextLi);

        nav.appendChild(ul);
        pagContainers.appendChild(nav);
    }
});
