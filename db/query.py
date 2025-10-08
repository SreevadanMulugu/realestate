import sqlite3
import os
import json
from typing import List, Dict, Optional
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), 'properties.db')

# Initialize DB and sample data if not exists
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS properties (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE,
        price TEXT,
        location TEXT,
        description TEXT,
        bedrooms INTEGER,
        bathrooms INTEGER,
        area_sqft INTEGER,
        property_type TEXT,
        image_url TEXT,
        contact_info TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # Insert sample data if table is empty
    c.execute('SELECT COUNT(*) FROM properties')
    if c.fetchone()[0] == 0:
        c.executemany('INSERT INTO properties (name, price, location, description, bedrooms, bathrooms, area_sqft, property_type, image_url, contact_info) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', [
            ('Lotus Villa', '₹80 Lakhs', 'Gachibowli, Hyderabad', 'Luxurious 3BHK villa with modern amenities and beautiful garden', 3, 3, 2500, 'Villa', 'https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=400', '+91-9876543210'),
            ('Green Valley Apartments', '₹55 Lakhs', 'Miyapur, Hyderabad', 'Spacious 2BHK apartment with city view and amenities', 2, 2, 1200, 'Apartment', 'https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?w=400', '+91-9876543211'),
            ('Pearl Heights', '₹70 Lakhs', 'Kondapur, Hyderabad', 'Premium 3BHK apartment with luxury finishes', 3, 3, 1800, 'Apartment', 'https://images.unsplash.com/photo-1512917774080-9991f1c4c750?w=400', '+91-9876543212'),
            ('Sunset Gardens', '₹45 Lakhs', 'Hitech City, Hyderabad', 'Cozy 2BHK apartment near tech hub', 2, 2, 1100, 'Apartment', 'https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=400', '+91-9876543213'),
            ('Royal Palace', '₹1.2 Crores', 'Banjara Hills, Hyderabad', 'Exclusive 4BHK villa with private pool', 4, 4, 3500, 'Villa', 'https://images.unsplash.com/photo-1613490493576-7fde63acd811?w=400', '+91-9876543214'),
        ])
    conn.commit()
    conn.close()

def get_all_properties() -> List[Dict]:
    """Get all properties from database"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''SELECT id, name, price, location, description, bedrooms, bathrooms, area_sqft, property_type, image_url, contact_info, created_at 
                 FROM properties ORDER BY created_at DESC''')
    properties = []
    for row in c.fetchall():
        properties.append({
            'id': row[0],
            'name': row[1],
            'price': row[2],
            'location': row[3],
            'description': row[4],
            'bedrooms': row[5],
            'bathrooms': row[6],
            'area_sqft': row[7],
            'property_type': row[8],
            'image_url': row[9],
            'contact_info': row[10],
            'created_at': row[11]
        })
    conn.close()
    return properties

def get_property_by_id(property_id: int) -> Optional[Dict]:
    """Get property by ID"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''SELECT id, name, price, location, description, bedrooms, bathrooms, area_sqft, property_type, image_url, contact_info, created_at 
                 FROM properties WHERE id = ?''', (property_id,))
    row = c.fetchone()
    conn.close()
    
    if row:
        return {
            'id': row[0],
            'name': row[1],
            'price': row[2],
            'location': row[3],
            'description': row[4],
            'bedrooms': row[5],
            'bathrooms': row[6],
            'area_sqft': row[7],
            'property_type': row[8],
            'image_url': row[9],
            'contact_info': row[10],
            'created_at': row[11]
        }
    return None

def search_properties(query: str) -> List[Dict]:
    """Search properties by name, location, or type"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    search_term = f"%{query.lower()}%"
    c.execute('''SELECT id, name, price, location, description, bedrooms, bathrooms, area_sqft, property_type, image_url, contact_info, created_at 
                 FROM properties WHERE LOWER(name) LIKE ? OR LOWER(location) LIKE ? OR LOWER(property_type) LIKE ? ORDER BY created_at DESC''', 
              (search_term, search_term, search_term))
    properties = []
    for row in c.fetchall():
        properties.append({
            'id': row[0],
            'name': row[1],
            'price': row[2],
            'location': row[3],
            'description': row[4],
            'bedrooms': row[5],
            'bathrooms': row[6],
            'area_sqft': row[7],
            'property_type': row[8],
            'image_url': row[9],
            'contact_info': row[10],
            'created_at': row[11]
        })
    conn.close()
    return properties

def add_property(property_data: Dict) -> bool:
    """Add new property to database"""
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('''INSERT INTO properties (name, price, location, description, bedrooms, bathrooms, area_sqft, property_type, image_url, contact_info) 
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                  (property_data['name'], property_data['price'], property_data['location'], 
                   property_data['description'], property_data['bedrooms'], property_data['bathrooms'],
                   property_data['area_sqft'], property_data['property_type'], 
                   property_data['image_url'], property_data['contact_info']))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error adding property: {e}")
        return False

def update_property(property_id: int, property_data: Dict) -> bool:
    """Update existing property"""
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('''UPDATE properties SET name=?, price=?, location=?, description=?, bedrooms=?, bathrooms=?, 
                     area_sqft=?, property_type=?, image_url=?, contact_info=?, updated_at=CURRENT_TIMESTAMP 
                     WHERE id=?''',
                  (property_data['name'], property_data['price'], property_data['location'], 
                   property_data['description'], property_data['bedrooms'], property_data['bathrooms'],
                   property_data['area_sqft'], property_data['property_type'], 
                   property_data['image_url'], property_data['contact_info'], property_id))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error updating property: {e}")
        return False

def delete_property(property_id: int) -> bool:
    """Delete property by ID"""
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('DELETE FROM properties WHERE id = ?', (property_id,))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error deleting property: {e}")
        return False

# Legacy function for backward compatibility
def get_property_info(message: str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    message_lower = message.lower()
    c.execute('SELECT name, price, location FROM properties')
    for name, price, location in c.fetchall():
        if name.lower() in message_lower:
            conn.close()
            return {'name': name.title(), 'price': price, 'location': location}
    conn.close()
    return None 

init_db() 