import scrapy
from bookscraper.items import BookItem


class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"] 
    #allowed_domains prevents the spider from going on scraping 100s of website linked to our scraping website
    start_urls = ["https://books.toscrape.com/"]
    #this is the first url that the spider starts to scrap and we can have multiple urls.

    def parse(self, response):
        books = response.css('article.product_pod')
        for book in books:
            relative_url = response.css('h3 a').attrib['href']
            #so there are over 50 pages having 20 books each
            #also each book has its own page with further details
            #here we are trying to get the each book url

            if 'catalogue/' in relative_url:
            #some of the pages don't 'catalogue/' in the relative_url so we need to add it
            #if we don't then scrapy will not scrape data from all the pages
                book_url = 'https://books.toscrape.com/' + relative_url
                #relative_url only give second half of the url so we are adding the first part to it
            else:
                book_url = 'https://books.toscrape.com/catalogue/' + relative_url
            yield scrapy.Request(book_url, callback=self.parse_book_page)
            #we tell scrapy to go to the next page url using response.follow
            #once we get response back from the url, the callback function will start the parse function that pulls the name, price and url of the book

        next_page = response.css('li.next a ::attr(href)').get()
        if next_page is not None:
            if 'catalogue/' in next_page:
            #some of the pages don't 'catalogue/' in the next page url so we need to add it
            #if we don't then scrapy will not scrapy data from all the pages
                next_page_url = 'https://books.toscrape.com/' + next_page
            else:
                next_page_url = 'https://books.toscrape.com/catalogue/' + next_page
            
            yield response.follow(next_page_url, callback=self.parse)

    def parse_book_page(self,response):
        #book = response.css("div.product_main")[0]
        table_rows = response.css("table tr")
        book_item = BookItem()

        
        book_item['url'] = response.url,
        book_item['title'] = response.css('.product_main h1::text').get(),
        book_item['product_type'] = table_rows[1].css('td::text').get(),
        book_item['price_excl_tax'] = table_rows[2].css('td::text').get(),
        book_item['price_incl_tax'] = table_rows[3].css('td::text').get(),
        book_item['tax'] = table_rows[4].css('td::text').get(),
        book_item['availability'] = table_rows[5].css('td::text').get(),
        book_item['num_reviews'] = table_rows[6].css('td::text').get(),
        book_item['stars'] = response.css('p.star-rating').attrib['class'],
        book_item['category'] = response.xpath("//ul[@class='breadcrumb']/li[@class='active']/preceding-sibling::li[1]/a/text()").get(),
        book_item['description'] = response.xpath("//div[@id='product_description']/following-sibling::p/text()").get(),
        book_item['price'] = response.css('p.price_color::text').get()
        
        yield{}
    

#Set-Location 'D:\Courses\YT FreeCodeCamp Scrapy Course\Part-2\bookscraper'
#.\venv\Scripts\activate