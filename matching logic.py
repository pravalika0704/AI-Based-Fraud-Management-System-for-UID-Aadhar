import re
from difflib import SequenceMatcher

# Function to normalize address
def normalize_address(address):
    address = re.sub(r'\b(Marg|Lane|Township)\b', '', address, flags=re.IGNORECASE)
    address = re.sub(r'\W+', ' ', address)
    return address.strip().lower()

# Function to check exact letter match
def exact_letter_match(name1, name2):
    return name1.lower() == name2.lower()

# Function to check abbreviated name match
def abbreviated_name_match(name1, name2):
    name1_parts = name1.split()
    name2_parts = name2.split()
    if len(name1_parts) == 2 and len(name2_parts) == 2:
        return (name1_parts[0][0].lower() == name2_parts[0][0].lower() and
                name1_parts[1].lower() == name2_parts[1].lower())
    return False

# Function to check ignoring middle names match
def ignore_middle_names(name1, name2):
    parts1 = name1.split()
    parts2 = name2.split()
    if len(parts1) == 2 and len(parts2) == 3:
        return parts1[0].lower() == parts2[0].lower() and parts1[1].lower() == parts2[2].lower()
    if len(parts1) == 3 and len(parts2) == 2:
        return parts1[0].lower() == parts2[0].lower() and parts1[2].lower() == parts2[1].lower()
    return False

# Function to check matching any part of the name
def match_any_part(name1, name2):
    parts1 = name1.lower().split()
    parts2 = name2.lower().split()
    return any(part in parts2 for part in parts1) or any(part in parts1 for part in parts2)

# Function to check circular match
def circular_match(name1, name2):
    return set(name1.lower().split()) == set(name2.lower().split())

# Function to check single letter abbreviation match
def single_letter_abbreviation(name1, name2):
    parts1 = name1.split()
    parts2 = name2.split()
    if len(parts1) == 2 and len(parts2) == 2:
        return (parts1[0][0].lower() == parts2[0][0].lower() and
                parts1[1].lower() == parts2[1].lower())
    return False

# Function to match names based on various rules
def name_match(input_name, extracted_name):
    if exact_letter_match(input_name, extracted_name):
        return True
    if abbreviated_name_match(input_name, extracted_name):
        return True
    if ignore_middle_names(input_name, extracted_name):
        return True
    if match_any_part(input_name, extracted_name):
        return True
    if circular_match(input_name, extracted_name):
        return True
    if single_letter_abbreviation(input_name, extracted_name):
        return True
    return False

# Function to calculate similarity ratio
def similarity_ratio(a, b):
    return SequenceMatcher(None, a, b).ratio()

# Function to match addresses based on normalization and field-specific matching
def address_match(input_address, extracted_address, cutoff=70):
    input_address = normalize_address(input_address)
    extracted_address = normalize_address(extracted_address)

    input_fields = input_address.split()
    extracted_fields = extracted_address.split()

    match_score = 0
    total_weight = 0

    for field in input_fields:
        max_score = max([similarity_ratio(field, efield) for efield in extracted_fields])
        match_score += max_score * 100
        total_weight += 100

    final_score = (match_score / total_weight) * 100

    pincode_match = (re.search(r'\d+', input_address) and re.search(r'\d+', extracted_address) and 
                     re.search(r'\d+', input_address).group() == re.search(r'\d+', extracted_address).group())
    if pincode_match and final_score >= cutoff:
        return True
    return False

# Function to check UID match
def uid_match(input_uid, extracted_uid):
    return input_uid == extracted_uid

# Function to evaluate overall match
def overall_match(input_name, extracted_name, input_address, extracted_address, input_uid, extracted_uid):
    name_result = name_match(input_name, extracted_name)
    address_result = address_match(input_address, extracted_address)
    uid_result = uid_match(input_uid, extracted_uid)
    return name_result and address_result and uid_result

# Example usage and test cases
test_cases = [
    ("Rahul Dwivedi", "Rahul D", "B-404,4th floor,kphb,kphb colony entrance,Tower,hyderabad,Telangana,500001", "kphb colony entrance,Tower,hyderabad,Telangana,500001", "9860 03559198", "9860 0355 9198"),
    ("Pushpam Kumar","Kumar", "ward-10,1st,Rampur Dilawar,Vaishali,Near Hospital,Patna,Bihar-844124","Vaishali,Bihar-844124", "9103 5715 3824", "9103 5715 3824"),
    ("Adhithya","Aditya","Bilai,Durg,Chattisgarh,490006","Bilai,Durg","8028 5266 0990","8028 5266 0990")
    
]

for input_name, extracted_name, input_address, extracted_address, input_uid, extracted_uid in test_cases:
    print(f"Testing: {input_name} vs {extracted_name}, {input_address} vs {extracted_address}, {input_uid} vs {extracted_uid}")
    print(f"Name Match: {name_match(input_name, extracted_name)}")
    print(f"Address Match: {address_match(input_address, extracted_address)}")
    print(f"UID Match: {uid_match(input_uid, extracted_uid)}")
    print(f"Overall Match: {overall_match(input_name, extracted_name, input_address, extracted_address, input_uid, extracted_uid)}")


