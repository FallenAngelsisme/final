ELEMENT_CHART = {
    "Fire":     {"strong": ["Grass"], "weak": ["Water"]},
    "Water":    {"strong": ["Fire"], "weak": ["Grass"]},
    "Grass":    {"strong": ["Water"], "weak": ["Fire"]},
    "Electric": {"strong": ["Water"], "weak": []},
    "Normal":   {"strong": [], "weak": []}
}

def compute_element_multiplier(attacker_element, defender_element):
    if defender_element in ELEMENT_CHART[attacker_element]["strong"]:
        return 1.5
    if defender_element in ELEMENT_CHART[attacker_element]["weak"]:
        return 0.5
    return 1.0