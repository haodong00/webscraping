
import scrapy

class ImdbSpider(scrapy.Spider):
    name = 'imdb_spider'
    
    start_urls = ['https://www.imdb.com/title/tt8772296/']

    def parse(self, response):
        """
        This method tells the spider what to do 
        when we get into the website
        """
  
        # url is the Cast & Crew page of the movie
        url = response.url + "fullcredits"
  
        # called function use scrapy.Request method 
        yield scrapy.Request(url, callback = self.parse_full_credits)
    
    def parse_full_credits(self, response):
        """
        This function parse the series cast page for the movie,
        and it will then navigate to each actor's page
        """
  
        # create a list of relative paths
        path = [a.attrib["href"] for a in response.css("td.primary_photo a")]
  
        # yield the request to next function by each actor

        for list in path:
            url = "https://www.imdb.com" + list
            yield scrapy.Request(url, callback = self.parse_actor_page)

    def parse_actor_page(self, response):
        """
        This function parse the actors page,
          and it yield these actors' and movies' names
          as a dictionary with two key-value pairs.
        """
  
        # get the actors' names
        actor_name = response.css("span.itemprop::text").get()
  
        # get the movies or TV shows which the actor has worked
        movies_list = response.css("div.filmo-row b a::text").getall()

        # make the actors' names and tv_movies to a dictionary
        for i in movies_list:
          yield {
            "actor": actor_name,
             "movie_or_TV_name": i
             }






  




