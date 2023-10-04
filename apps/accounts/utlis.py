import re

def validate_email(email):
    # Define a regular expression pattern for the desired email format
    # pattern = r'^[a-zA-Z0-9._%+-]+@augustineuniversity\.edu\.ng$'
    pattern = r'^[a-zA-Z0-9]+@augustineuniversity\.edu\.ng$'

    # Use re.match to check if the email matches the pattern
    if re.match(pattern, email):
        return True
    else:
        return False

# Test the function with an example email
email_to_validate = "john.doe@augustineuniversity.edu.ng"
if validate_email(email_to_validate):
    print(f"{email_to_validate} is a valid email address.")
else:
    print(f"{email_to_validate} is not a valid email address.")
