import boto3
from botocore.exceptions import ClientError
from decouple import config
from flask_restful.representations import json

from SESTempEmail.template import template_contract, template_name


# Initialize the boto3 SES client

class SEService:
    def __init__(self):
        self.create_client()

    def create_client(self):
        self.ses_client = boto3.client('ses',
                                       region_name=config("BUCKET_REGION"),
                                       aws_access_key_id=config("AWS_KEY"),
                                       aws_secret_access_key=config("ASW_SECRET")
                                       )

    # Create the template in SES
    def create_template(self):
        try:
            response = self.ses_client.create_template(Template = template_contract)
            return "Template Created:", response
        except ClientError as e:
            if e.response['Error']['Code'] == "AlreadyExists":
                pass
            else:
                raise

    def verify_email_identity(self, email):
        try:

            response = self.ses_client.verify_email_identity(
                EmailAddress=email
            )
            print(f"Verification email sent to {email}.")
            return response
        except ClientError as e:
            print(f"Error verifying email: {e}")
            return None

    def send_email(self, name, recipient):
        # Data to fill in the template placeholders
        template_data = {
            'name': name,
            #'link': link
        }

        # Send an email using the template
        email =config("EMAIL")  # Your verified SES email
        try:
            response = self.ses_client.send_templated_email(
                Source=email,
                Destination={
                    'ToAddresses': [recipient],
                },
                Template=template_name,
                TemplateData=json.dumps(template_data)  # Template data to replace placeholders
            )
            print("Email sent:", response)
        except ClientError as e:
            print(f"Error sending email: {e}")