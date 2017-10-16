from register_email_address import register_user
from finra_scraper import scrape_finra
from email_alerter import emailer

def main():
    print "First, register an email."
    raw_input("Hit <ENTER> to continue.")
    register_user()
    print "Next, scrape FINRA website."
    raw_input("Hit <ENTER> to continue.")
    scrape_finra()
    print "Finally, send out email alert."
    raw_input("Hit <ENTER> to continue.")
    emailer()

if __name__ == "__main__":
    main()