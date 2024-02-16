
# Validates the name of the player whose stats are being requested. It formats the name
# in the format the suffix needs to be in for basketball-reference.com.
def validate_name(name):

    if not isinstance(name, str) or ' ' not in name:
        return [False, "Invalid input. Please provide a string containing a space."]
    
    parts = name.split(' ')
    first_name = parts[0]
    last_name = parts[1]
    
    if len(last_name) > 5:
        lname_substring = last_name[:5]
    else:
        lname_substring = last_name
    
    fname_substring = first_name[:2]
    
    result = lname_substring + fname_substring
    return [True, result]

