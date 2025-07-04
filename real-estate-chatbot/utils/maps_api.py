# Mock functions for Google Maps API interactions

MOCK_NEARBY_PLACES = {
    "17.4748_78.3918": { # Lotus Villa coords
        "school": ["Oakridge International School (Kondapur)", "Chirec International School (Kondapur Branch)"],
        "hospital": ["Apollo Spectra Hospitals (Kondapur)", "KIMS Hospitals (Kondapur)"],
        "park": ["Botanical Garden", "Kondapur Park"]
    },
    "17.5079_78.3920": { # Green Valley Apartments coords
        "school": ["Delhi Public School (Miyapur)", "Vikas The Concept School (Miyapur)"],
        "hospital": ["Srikara Hospitals (Miyapur)", "Healix Hospital"],
        "park": ["Miyapur Park", "Nehru Zoological Park (Distant, for variety)"]
    },
    "17.4401_78.3489": { # Pearl Heights coords
        "school": ["Phoenix Greens International School (Gachibowli)", "Indus International School (Hyderabad)"],
        "hospital": ["Continental Hospitals (Gachibowli)", "AIG Hospitals"],
        "park": ["Gachibowli Park", "Bio Diversity Park"]
    },
    "17.4315_78.3999": { # Sunset Bungalow coords
        "school": ["Jubilee Hills Public School", "Bhartiya Vidya Bhavan's Public School"],
        "hospital": ["Apollo Hospitals (Jubilee Hills)", "Basavatarakam Indo American Cancer Hospital & Research Institute"],
        "park": ["KBR National Park", "Lotus Pond"]
    }
}

def get_nearby_places(latitude: float, longitude: float, place_type: str, property_name: str = "Unknown Property") -> list[str]:
    """
    Simulates fetching nearby places (e.g., schools, hospitals, parks)
    based on latitude, longitude, and place type.

    In a real scenario, this would call the Google Places API.
    For this PoC, it returns mock data.
    """
    print(f"[maps_api] Searching for {place_type} near {property_name} ({latitude}, {longitude})")

    # Try to find exact match for coordinates
    coord_key = f"{latitude}_{longitude}"
    if coord_key in MOCK_NEARBY_PLACES:
        return MOCK_NEARBY_PLACES[coord_key].get(place_type.lower(), [])

    # Fallback: If exact coordinates not found, try to provide some generic default
    # This part is more for robust mocking, a real API would handle unknown coords.
    if place_type.lower() == "school":
        return [f"Generic School near {property_name}", "Another Local School"]
    elif place_type.lower() == "hospital":
        return [f"General Hospital near {property_name}", "Community Clinic"]
    elif place_type.lower() == "park":
        return [f"Local Park near {property_name}"]

    return [f"No mock data for {place_type} near {property_name} at the given coordinates."]

if __name__ == '__main__':
    # Test cases
    print("Testing get_nearby_places for Lotus Villa (Kondapur):")
    # Coordinates for Lotus Villa from db/query.py
    lotus_villa_lat, lotus_villa_lon = 17.4748, 78.3918
    print("Schools:", get_nearby_places(lotus_villa_lat, lotus_villa_lon, "school", "Lotus Villa"))
    print("Hospitals:", get_nearby_places(lotus_villa_lat, lotus_villa_lon, "hospital", "Lotus Villa"))
    print("Parks:", get_nearby_places(lotus_villa_lat, lotus_villa_lon, "park", "Lotus Villa"))
    print("Restaurants (no mock data):", get_nearby_places(lotus_villa_lat, lotus_villa_lon, "restaurant", "Lotus Villa"))

    print("\nTesting get_nearby_places for a generic location (fallback):")
    generic_lat, generic_lon = 17.0000, 78.0000 # Some coords not in MOCK_NEARBY_PLACES
    print("Schools:", get_nearby_places(generic_lat, generic_lon, "school", "Generic Location"))
    print("Hospitals:", get_nearby_places(generic_lat, generic_lon, "hospital", "Generic Location"))
