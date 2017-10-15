# Finra_Skill_Demo
This is a skills demo repo for FINRA

This demo uses resources form Amazon Web Services.
To access these AWS resources you can log into the AWS Management console
using the following account credentials

    url: https://chrisgick.signin.aws.amazon.com/console
    account_alias: chrisgick
    user: finra_demo_user
    password: Password1

## Demo Flow
1. Register and email with `register_email_address.py`
2. Scrape FINRA website with `finra_scraper.py`
3. Send email alerts with `email_alerter.py`