from boto3.session import Session
from boto3 import client

# AWS resources
demo_access_key = "AKIAITB7G536WCOBIHDA"
demo_secret_access_key = "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"
AWS_SESSION = Session(
    region_name="us-east-1",
    aws_access_key_id=demo_access_key,
    aws_secret_access_key=demo_secret_access_key
)
DYNAMODB = AWS_SESSION.resource('dynamodb')
SES = AWS_SESSION.client('ses')
USERS_TABLE = "email_alert_users"



def get_user_email():
    """
    Prompts user to enter name and email address

    :return: dictionary of user name and email address
    """
    print "Register email alert user by entering name and email address"
    name = raw_input("Enter name: ")
    email = raw_input("Enter email: ")
    user = {
        "name": name,
        "email_address": email
    }
    return user


def verify_email(user):
    """
    Registers users email address with AWS Simple Email Service
    to allow user to receive emails for this demo and adds the
    user to Email Alert Users Dynamodb table

    :param user: dictionary of user name and email address
    """
    verify = SES.verify_email_identity(
        EmailAddress=user['email_address']
    )
    table = DYNAMODB.Table(USERS_TABLE)
    response = table.put_item(
        Item={
            "email_address": user['email_address'],
            "name": user['name']
        }
    )


def register_user():
    """
    Run register user to create an email alert user and register
    email address to allow user to receive messages from other modules
    in this demo
    """
    user = get_user_email()
    verify_email(user)
    print "Check your email for a message\n" \
          "from: Amazon Web Services\n" \
          "subject: Email Address Verification Request\n" \
          "and click on the link to verify your email address"


if __name__ == "__main__":
    register_user()
