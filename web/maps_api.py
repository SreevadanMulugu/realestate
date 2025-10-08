# Simulated Google Places API for PoC

def get_nearby_landmarks(location: str):
    # In a real app, call Google Places API here
    if 'Gachibowli' in location:
        return ['Oakridge International School', 'AIG Hospital', 'Inorbit Mall']
    elif 'Miyapur' in location:
        return ['Kennedy High School', 'SLG Hospital', 'Miyapur Metro Station']
    elif 'Kondapur' in location:
        return ['Chirec International School', 'KIMS Hospital', 'Botanical Garden']
    else:
        return ['No landmarks found'] 