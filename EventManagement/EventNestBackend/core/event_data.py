from datetime import date, timedelta

# Static data to replace Database for Events
EVENTS_DATA = [
    {
        'id': 1,
        'title': 'Royal Palace Wedding',
        'description': 'Experience the grandeur of a royal wedding at our exclusive heritage palace venues. Includes traditional decor, royal procession, and a feast fit for kings.',
        'category': 'Wedding',
        'image_url': '/static/core/images/defaults/wedding_event.png',
        'price': '₹25,00,000',
        'location': 'Jaipur, Rajasthan',
        'date': (date.today() + timedelta(days=45)).strftime('%Y-%m-%d'),
        'total_tickets': 150,
        'available_tickets': 150
    },
    {
        'id': 2,
        'title': 'Destination Beach Wedding',
        'description': 'Say "I do" with the ocean as your backdrop. A serene and romantic setting with floral arches, sunset views, and beachside dining.',
        'category': 'Wedding',
        'image_url': 'https://images.unsplash.com/photo-1544550581-5f7ceaf7f992?auto=format&fit=crop&w=800&q=80',
        'price': '₹15,00,000',
        'location': 'Goa, India',
        'date': (date.today() + timedelta(days=60)).strftime('%Y-%m-%d'),
        'total_tickets': 100,
        'available_tickets': 100
    },
    {
        'id': 3,
        'title': 'Tech Innovators Summit',
        'description': 'A premier conference for tech leaders and startups. Features keynote sessions, networking zones, and product showcases with state-of-the-art AV setup.',
        'category': 'Corporate',
        'image_url': '/static/core/images/defaults/corporate_event.png',
        'price': '₹50,000 / ticket',
        'location': 'Bangalore International Convention Centre',
        'date': (date.today() + timedelta(days=20)).strftime('%Y-%m-%d'),
        'total_tickets': 500,
        'available_tickets': 500
    },
    {
        'id': 4,
        'title': 'Annual Business Gala',
        'description': 'Celebrate your company achievements in style. Black tie event with gourmet dinner, awards ceremony, and live jazz band.',
        'category': 'Corporate',
        'image_url': 'https://images.unsplash.com/photo-1511578314322-379afb476865?auto=format&fit=crop&w=800&q=80',
        'price': '₹10,000 / ticket',
        'location': 'Mumbai, Hyatt Regency',
        'date': (date.today() + timedelta(days=30)).strftime('%Y-%m-%d'),
        'total_tickets': 200,
        'available_tickets': 200
    },
    {
        'id': 5,
        'title': 'Neon Night Birthday Bash',
        'description': 'An electrifying birthday party experience with neon themes, glow-in-the-dark face painting, and a top DJ spinning the latest hits.',
        'category': 'Party',
        'image_url': '/static/core/images/defaults/social_party.png',
        'price': '₹1,50,000',
        'location': 'Cyber Hub, Gurgaon',
        'date': (date.today() + timedelta(days=10)).strftime('%Y-%m-%d'),
        'total_tickets': 50,
        'available_tickets': 50
    },
    {
        'id': 6,
        'title': 'Silver Jubilee Anniversary',
        'description': 'Marking 25 years of togetherness with elegance. Intimate gathering with sophisticated silver decor, classical music, and fine dining.',
        'category': 'Party',
        'image_url': 'https://images.unsplash.com/photo-1530103862676-de3c9a59af57?auto=format&fit=crop&w=800&q=80',
        'price': '₹5,00,000',
        'location': 'New Delhi, The Lodhi',
        'date': (date.today() + timedelta(days=15)).strftime('%Y-%m-%d'),
        'total_tickets': 80,
        'available_tickets': 80
    },
    {
        'id': 7,
        'title': 'Summer Rock Fest',
        'description': 'Get ready to headbang! A massive open-air concert featuring top rock bands, food trucks, and a high-energy crowd.',
        'category': 'Concert',
        'image_url': '/static/core/images/defaults/concert_event.png',
        'price': '₹2,500 / ticket',
        'location': 'JLN Stadium, Delhi',
        'date': (date.today() + timedelta(days=90)).strftime('%Y-%m-%d'),
        'total_tickets': 2000,
        'available_tickets': 2000
    },
    {
        'id': 8,
        'title': 'Classical Music Evening',
        'description': 'A soulful evening of Indian classical music featuring maestros. Peaceful ambiance with traditional seating and acoustic perfection.',
        'category': 'Concert',
        'image_url': 'https://images.unsplash.com/photo-1514320291840-2e0a9bf2a9ae?auto=format&fit=crop&w=800&q=80',
        'price': '₹1,000 / ticket',
        'location': 'NCPA, Mumbai',
        'date': (date.today() + timedelta(days=25)).strftime('%Y-%m-%d'),
        'total_tickets': 300,
        'available_tickets': 300
    }
]
