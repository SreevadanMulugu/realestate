# Mock database for real estate properties
MOCK_DB = {
    "Lotus Villa": {
        "price": "₹75 Lakhs",
        "location": "Kondapur, Hyderabad",
        "latitude": 17.4748,
        "longitude": 78.3918,
        "description": "A beautiful villa with modern amenities and a serene environment.",
        "type": "villa"
    },
    "Green Valley Apartments": {
        "price": "₹55 Lakhs",
        "location": "Miyapur, Hyderabad",
        "latitude": 17.5079,
        "longitude": 78.3920,
        "description": "Spacious apartments with great connectivity and nearby parks.",
        "type": "apartment"
    },
    "Pearl Heights": {
        "price": "₹1.2 Crores",
        "location": "Gachibowli, Hyderabad",
        "latitude": 17.4401,
        "longitude": 78.3489,
        "description": "Luxury apartments in the heart of the IT corridor, offering premium facilities.",
        "type": "apartment"
    },
    "Sunset Bungalow": {
        "price": "₹90 Lakhs",
        "location": "Jubilee Hills, Hyderabad",
        "latitude": 17.4315,
        "longitude": 78.3999,
        "description": "An independent bungalow with a private garden and classic architecture.",
        "type": "bungalow"
    }
}

def get_property_details_by_name(property_name: str) -> dict | None:
    """
    Fetches all details of a property by its name.
    Returns a dictionary of property details if found, else None.
    """
    return MOCK_DB.get(property_name)

def get_property_location_by_name(property_name: str) -> dict | None:
    """
    Fetches the location (latitude and longitude) of a property by its name.
    Returns a dictionary {'latitude': float, 'longitude': float} if found, else None.
    """
    property_info = MOCK_DB.get(property_name)
    if property_info and "latitude" in property_info and "longitude" in property_info:
        return {
            "latitude": property_info["latitude"],
            "longitude": property_info["longitude"],
            "location_name": property_info["location"]
        }
    return None

def get_all_property_names() -> list[str]:
    """
    Returns a list of all property names in the database.
    """
    return list(MOCK_DB.keys())

if __name__ == '__main__':
    # Test cases
    print("Testing get_property_details_by_name:")
    print("Lotus Villa:", get_property_details_by_name("Lotus Villa"))
    print("Unknown Property:", get_property_details_by_name("Unknown Property"))

    print("\nTesting get_property_location_by_name:")
    print("Green Valley Apartments:", get_property_location_by_name("Green Valley Apartments"))
    print("Sunset Bungalow (No Lat/Long initially, let's assume):")
    # Temporarily remove lat/long for testing this case if needed, then add back
    # original_sunset = MOCK_DB.get("Sunset Bungalow", {}).copy()
    # if "latitude" in MOCK_DB.get("Sunset Bungalow", {}): del MOCK_DB["Sunset Bungalow"]["latitude"]
    # if "longitude" in MOCK_DB.get("Sunset Bungalow", {}): del MOCK_DB["Sunset Bungalow"]["longitude"]
    # print("Sunset Bungalow:", get_property_location_by_name("Sunset Bungalow"))
    # MOCK_DB["Sunset Bungalow"] = original_sunset # Restore
    print("Unknown Property:", get_property_location_by_name("Unknown Property"))

    print("\nTesting get_all_property_names:")
    print(get_all_property_names())
