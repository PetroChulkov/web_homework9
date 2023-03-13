from models import Quotes, Authors
import redis
from redis_lru import RedisLRU

client = redis.StrictRedis(host="localhost", port=6379, password=None)
cache = RedisLRU(client)

quotes = Quotes.objects()

@cache
def name_search(name):
    result = []
    authors = Authors.objects(fullname__istartswith=name)
    for author in authors:
        quotes = Quotes.objects(author=author.id)
        for quote in quotes:
            result.append(quote.quote)
    return f' List of quotes: \n {result} \n by: {author.fullname}'


@cache
def tag_search(tag):
    quotes = Quotes.objects(tags__istartswith=tag)
    result = []
    for quote in quotes:
        result.append(quote.quote)
    return f' List of quotes: \n {result} \n by tag: {tag}'


@cache
def multiple_tags(tags):
    tags = tags.split(',')
    result = []

    quotes = Quotes.objects(tags__in=tags)
    for quote in quotes:
        result.append(quote.quote)
    return f' List of quotes:\n {result} \n by tags: {tags}'

commands = {
    'name': name_search,
    'tag': tag_search,
    'tags': multiple_tags
}

def main():
    while True:
        query = input('Input data for search, please: ')
        if query.split(':')[0] == 'exit':
            break
        for key in commands:
            if query.split(':')[0] == key:
                print(commands.get(key)(query.split(':')[1]))


if __name__ == '__main__':
    main()




