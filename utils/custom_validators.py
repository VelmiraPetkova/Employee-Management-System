from password_strength import PasswordPolicy
from marshmallow import ValidationError
import re

from werkzeug.exceptions import BadRequest, NotFound

from models import UserModel
from utils.clean_data import *

MIN_LENGHT = 4
MAX_LENGHT = 20
VALID_DOMAIN = (".com", ".bg", ".net", ".org")
valid_name_email = r'(\w+)'
valid_domain_email = r'(\..+)$'

policy = PasswordPolicy.from_names(
    uppercase=1,  # need min. 1 uppercase letters
    numbers=1,  # need min. 1 digits
    special=1,  # need min. 1 special characters
    nonletters=1,  # need min. 1 non-letter characters (digits, specials, anything)
)

NAME_PATTERN = re.compile(r"^[A-Z][a-zA-Z' -]*$")
PHONE_PATTERN = re.compile(r"^\+?[1-9]\d{1,14}$|^(\(?\d{3}\)?[-.\s]?)?\d{3}[-.\s]?\d{4}$")
CIVIL_NUMBER_PATTERN = re.compile(r"^\d{8,12}$")
IBAN_PATTERN= re.compile(r"^[A-Z]{2}\d{2}[A-Z0-9]{1,30}$")


def email_is_valid(email):
    if email.count("@") > 1:
        raise ValidationError("Email should contain only one @ symbol!")

    email_name, domain = email.split("@")

    if len(email_name) < MIN_LENGHT:
        raise ValidationError("Email must be more than 4 characters")
    elif len(email_name) > MAX_LENGHT:
        raise ValidationError("Email must be less than 12 characters")

    matches_domain = re.findall(valid_domain_email, domain)
    if matches_domain[0] not in VALID_DOMAIN:
        raise ValidationError("Domain must be one of the following: .com, .bg, .org, .net")

    matches = re.findall(valid_name_email, email_name)

    if matches[0] != email_name:
        raise ValidationError("Email can contain only letters, digits and underscores!")


def validate_password(value):
    errors = policy.test(value)
    if errors:
        raise ValidationError(f"Not a valid password")


def validate_name(name):
    name = clean_name(name)
    if not re.fullmatch(NAME_PATTERN, name):
        raise ValidationError(f"Not a valid name")


def validate_phone(phone):
    phone = clean_phone(phone)
    if not re.fullmatch(PHONE_PATTERN, phone):
        raise ValidationError(f"Not a valid phone number")


def validate_civil_number(civil_number):
    civil_number = clean_civil_number(civil_number)
    if not re.fullmatch(CIVIL_NUMBER_PATTERN, civil_number):
        raise ValidationError(f"Not a valid civil or national ID number")

def validate_iban(iban):
    iban= clean_iban(iban)
    if not re.fullmatch(IBAN_PATTERN, iban):
        raise ValidationError(f"IBAN is invalid")


def validate_work_hours(work_hours):
    if 0.1 >work_hours > 8.0:
        raise ValidationError(f"Work hours must be between 0 and 8")
