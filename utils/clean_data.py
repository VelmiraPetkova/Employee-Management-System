
# Function to clean names
def clean_name(name: object) -> object:
    try:
        name = name.strip().title()
        name_parts = name.split()

        if len(name_parts) == 2:
            return name
        else:
            raise ValueError  # Not enough parts to form first and last names

    except ValueError:
        print("Please enter a first and last name separated by a space.")

def clean_phone(phone):
    phone = phone.strip()
    return phone  # Return the valid phone number


def clean_civil_number(civil_number):
    civil_number = civil_number.strip()
    return civil_number  # Return the valid civil number


def clean_iban(iban):
    iban = iban.replace(' ', '').upper()
    return iban  # Return the valid IBAN
