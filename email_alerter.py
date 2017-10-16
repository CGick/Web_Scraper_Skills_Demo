import smtplib
import datetime

from email.mime.text import MIMEText
from boto3.session import Session
from fuzzyparsers import parse_date
from config import settings


# AWS resources
AWS_SESSION = Session(
    region_name="us-east-1",
    aws_access_key_id=settings.DEMO_ACCESS_KEY,
    aws_secret_access_key=settings.DEMO_SECRET_ACCESS_KEY
)
DYNAMODB = AWS_SESSION.resource('dynamodb')



def get_news_updates():
    """
    Retrieves news articles from DynamoDB

    :return: list of dictionaries containing news article headlines,
    date_posted, and links
    """
    table = DYNAMODB.Table(settings.NEWS_TABLE)
    stories = table.scan()
    return stories["Items"]


def build_message(list_of_stories):
    """
    Takes a list of news article dictionaries and creates an email body
    of article updates sorted by posted date

    :param list_of_stories: list of article dictionaries
    :return: string formatted email body
    """
    msg = ""
    list_of_dates = []
    for story in list_of_stories:
        if parse_date(story['date_posted']) not in list_of_dates:
            date = parse_date(story['date_posted'])
            list_of_dates.append(date)
        else:
            continue

    for date in sorted(list_of_dates):
        msg += datetime.date.strftime(date, "%B %d, %Y\n")
        for story in list_of_stories:
            if parse_date(story['date_posted']) == date:
                msg += "\t{}\n".format(
                    story['headline'].encode(
                        'ascii', "ignore"
                    )
                )
                msg += "\t{}\n\n".format(
                    story['link'].encode(
                        'ascii', "ignore"
                    )
                )
    return msg


def get_news_alert_users():
    """
    Retrieves list of user names and email addresses from DynamoDB

    :return: list of dictionaries of user names and email addresses
    """
    table = DYNAMODB.Table(settings.USERS_TABLE)
    users = table.scan()
    return users['Items']


def send_email(message, recipient):
    """
    Uses AWS Simple Email Service SMTP protocol to send emails to
    registered alert users

    :param message: string message used to populate email body
    :param recipient: dictionary of user name and email address
    """
    text = "Dear {},\n" \
           "\n" \
           "Here are some new news articles from FINRA. Check the out" \
           "bellow.\n" \
           "\n" \
           "{}" \
           "Best regards,\n" \
           "Chris Gick".format(recipient['name'], message)

    msg = MIMEText(text)

    msg['Subject'] = "Gick Chris Skills Demo"
    msg['To'] = recipient['email_address']
    msg['From'] = settings.OUTBOUND_EMAIL_ADDRESS

    s = smtplib.SMTP("email-smtp.us-east-1.amazonaws.com", 587)
    s.ehlo()
    s.starttls()
    s.login(settings.AWS_SMTP["Username"], settings.AWS_SMTP["Password"])
    s.sendmail(
        settings.OUTBOUND_EMAIL_ADDRESS,
        [recipient['email_address']],
        msg.as_string()
    )
    s.close()


def emailer():
    """
    Module looks for news articles in DynamoDB and notifies registered
    users by email that new articles are available for viewing
    """
    updates = get_news_updates()
    msg = build_message(updates)
    alert_users = get_news_alert_users()
    for user in alert_users:
        send_email(msg, user)


if __name__ == "__main__":
    emailer()
