from .blog import blog,article
from .client import frontpage
from pprint import pprint

content = blog('blog')
def list_articles():
    return content.list_articles()
def display_titles():
    pprint(content.return_titles())
def print_article(title):
    for item in content.blogs:
        if item.title==title:
            item.raw_output()
def print_article_by_id(id):
    item = content.blogs[id]
    item.raw_output()
def client():
    frontpage()