from models import Authors, Quotes
import json


def create():
    with open('authors.json') as f:
        templates = json.load(f)


    for items in templates:
        Authors(fullname=items.get('fullname'), borndate=items.get('born_date'), location=items.get('born_location'), description=items.get('description')).save()


    with open('quotes.json') as f:
        templates = json.load(f)

    for items in templates:
        authors = Authors.objects(fullname=items.get('author'))
        for author in authors:
                Quotes(tags=items.get('tags'), author=author.id, quote=items.get('quote')).save()

if __name__ == '__main__':
    create()