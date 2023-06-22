# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BookscraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

def serialize_price(value):
    return f'£{str(value)}'
#some price fields value don't have pound symbol so we are adding it here

class BookItem(scrapy.Item):
    url: scrapy.Field()
    title: scrapy.Field()
    product_type: scrapy.Field()
    price_excl_tax: scrapy.Field(serializer = serialize_price)
    price_incl_tax: scrapy.Field()
    tax: scrapy.Field()
    availability: scrapy.Field()
    num_reviews: scrapy.Field()
    stars: scrapy.Field()
    category: scrapy.Field()
    description: scrapy.Field()
    price: scrapy.Field()
#we create this class to specify all the fields we are creating
#if there is any spelling mistake then we will give error message.
#if we don't create this class and if there is any spelling mistake in bookspider.py code then we won't get any error message then that field may not be uploaded to database