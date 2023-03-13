from mongoengine import *

connect(host="mongodb+srv://mrpchulkov:pNMopFLl4bnWZ2VN@web-module8.be50r1x.mongodb.net/scraping_results", ssl=True)


class Authors(Document):
    fullname = StringField(required=True)
    borndate = StringField(max_length=50)
    location = StringField()
    description = StringField()


class Quotes(Document):
    tags = ListField(StringField())
    author = ReferenceField(Authors, dbref=False, reverse_delete_rule=CASCADE)
    quote = StringField()
    meta = {'allow_inheritance': True}




