from utils.web_scraper import Web_Scraper
from bs4 import BeautifulSoup
from boto3.session import Session
from config import settings

# AWS resources
AWS_SESSION = Session(
    region_name="us-east-1",
    profile_name="scraper_demo"
)
DYNAMODB = AWS_SESSION.resource('dynamodb')

# Root site URL
host = 'https://www.finra.org'


def get_news_releases():
    """
    Uses a custom web scraper to retrieve html form web site

    :returns: string html of site
    """
    scraper = Web_Scraper(host)
    html = scraper.get_html("/newsroom/newsreleases")
    return html


def get_article_list(html):
    """
    Uses BeautifulSoup to navigate and parse supplied html page

    :param html: html string of site to parse
    :return: list of extracted variable dictionaries
    """
    soup = BeautifulSoup(html.content, "html.parser")
    content = soup.article.findAll("ul")[0]
    stories = []
    for row in content:
        if row.find('span') == -1:
            continue
        else:
            story = {
                "date_posted": row.find('span').text,
                "headline": row.find('a').text,
                "story_endpoint": row.find('a').get('href')
            }

            stories.append(story)
    return stories


def write_to_dynamodb(list_of_articles):
    """
    Takes a list of variables dictionaries and writes them to dynamodb

    :param list_of_articles: list of dictionaries
    :return: list of responses from dynamodb put_item
    """
    table = DYNAMODB.Table(settings.NEWS_TABLE)
    response_log = []
    for item in list_of_articles:
        response = table.put_item(
            Item={
                "headline": item['headline'],
                "date_posted": item['date_posted'],
                "link": host + item['story_endpoint']
            }
        )
        response_log.append(response)
    return response_log


def scrape_finra():
    """
    Scrapes FINRA web site to gather newsroom articles and populate
    DynamoDB
    """
    page = get_news_releases()
    articles = get_article_list(page)
    log_items = write_to_dynamodb(articles)
    for log in log_items:
        print log


if __name__ == "__main__":
    scrape_finra()
