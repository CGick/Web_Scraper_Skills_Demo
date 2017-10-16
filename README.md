# Python Web Scraper Skills Demo
This is a Python web scraper that leverages requests, BeautifulSoup,
boto3, smtplib and fuzzyparsers to extract newsroom articles from
FINRA's website, and automaticly populates a no sql AWS DynamoDB table.
It also allows users to register their email with AWS SES which allow
them to receive emails from the program.
It then sends an email notification via AWS SES SMTP protocol to
registered users.

This demo uses resources form Amazon Web Services.
Users will be allowed to access these resources via the AWS Management
Console by logging in under the supplied temporary user credentials.

* url: https://chrisgick.signin.aws.amazon.com/console


## Demo Flow
See an end to end demo with `run.py`

### OR

For a more granular view of the process:
1. Register and email with `register_email_address.py`
2. Scrape FINRA website with `finra_scraper.py`
3. Send email alerts with `email_alerter.py`
