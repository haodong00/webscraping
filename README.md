# Blog Post 2 Web Scraping IMDB for Fav Film 

---
layout: post
title: Blog Post 2 Web Scraping IMDB for Fav Film 
---
In this Blog Post, I will use webscraping to figure out things about my favorite TV series "Euphoria". Euphoria is a 2 seasons 16 episodes TV follows a group of high school students as they navigate love and friendships in a world of drugs, sex, trauma and social media. 

<h1>1. Setup </h1>

<h2>1.1 Locate the Starting IMDB Page</h2>

The IMDB post page for Euphoria is at:

```
https://www.imdb.com/title/tt8772296/
```
<h2>1.2. Dry-Run Navigation</h2>
First, click on the Cast & Crew link. This will take you to a page with URL of the form:

```
<original_url>fullcredits/
```
For example, the Cast & Crew link for the TV "Euphoria" is as follows:

```
https://www.imdb.com/title/tt8772296/fullcredits/
```

Then, we scroll down until we see the Series Cast section. We then click on the portrait of one of the actors, and the browser will take us to a page with different-looking URL, for example below is Zendaya's page:

```
https://www.imdb.com/name/nm3918035/
```

<h2>1.3 Initialize the Project</h2>

1. Create a new GitHub repository, and sync it with GitHub Desktop.
2. Open a terminal in the location of your repository on your laptop, and type:

```
conda activate PIC16B
scrapy startproject IMDB_scraper
cd IMDB_scraper
```

This will create quite a lot of files, but you don’t really need to touch most of them.

<h2>1.4 Tweak Settings</h2>

For now, add the following line to the file settings.py:

```python
CLOSESPIDER_PAGECOUNT = 20
```

This line just prevents your scraper from downloading too much data while you’re still testing things out. You’ll remove this line later.

<h1>2. Write Your Scraper</h1>

Now, we begin to write our scraper!

First, we create a file called imdb_spider.py inside the spiders directory. And we add the following code in this file:

```python
# to run 
# scrapy crawl imdb_spider -o movies.csv

import scrapy

class ImdbSpider(scrapy.Spider):
    name = 'imdb_spider'
    
    start_urls = ['https://www.imdb.com/title/tt8772296/']
```

The start_urls in the above function is the URL corresponding to our favorite movie or TV shows. For me rn, this URL is heading to "Euphoria".

<h2>2.1 Parse</h2>

Then, we implement our first parsing methods for the class. In this method, we assume that we are on "Euphoria" page, and we navigate to the Cast & Crew page. Once we navigate to this page, the next method *parse_full_credits(self, response)* will be called automatically.

```python
 def parse(self, response):
        """
        This method tells the spider what to do 
        when we get into the website
        """
  
        # url is the Cast & Crew page of the movie
        url = response.url + "fullcredits"
  
        # called function use scrapy.Request method 
        yield scrapy.Request(url, callback = self.parse_full_credits)
```

<h2>2.2 Parse_full_credits</h2>

After we complete the *Parse()* function, we will jump to the second method
*parse_full_credits()*. This function assume that we are currently on the page of Cast&Crew. The goal of this function is to locate the list of each actor on the page, and it will then call the next method *parse_actor_page()*.

```python
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
```

<h2>2.3 Parse Actor Page </h2>

Then we come to the third function. *parse_actor_page(self, response)* should assume that you start on the page of an actor. It should yield a dictionary with two key-value pairs, of the form {"actor" : actor_name, "movie_or_TV_name" : movie_or_TV_name}. The method should yield one such dictionary for each of the movies or TV shows on which that actor has worked. 

```python
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
```


<h1>3. Make Your Recommendations</h1>

Once we’ve completed the above process, our spider is ready for testing. Firstly, comment out the line:

```python
CLOSESPIDER_PAGECOUNT = 20
```

Then, use the command:
```
scrapy crawl imdb_spider -o results.csv
```
After we run the above code, our results will be saved as a CSV file call *results.csv*, with a column of actor names and another column of names of movies or TV shows.

```python
import pandas as pd
data = pd.read_csv("results.csv")
df = data['movie_name'].value_counts().reset_index()
df = df.rename(columns={'index': 'Movie_or_TV_name', 
                        'movie_or_TV_name': 'number of shared actors'})
df[0:12]
```

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Movie_or_TV_name</th>
      <th>number of shared actors</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Euphoria</td>
      <td>382</td>
    </tr>
    <tr>
      <th>1</th>
      <td>NCIS</td>
      <td>26</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Criminal Minds</td>
      <td>24</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Shameless</td>
      <td>23</td>
    </tr>
    <tr>
      <th>4</th>
      <td>9-1-1</td>
      <td>21</td>
    </tr>
    <tr>
      <th>5</th>
      <td>The Rookie</td>
      <td>19</td>
    </tr>
    <tr>
      <th>6</th>
      <td>S.W.A.T.</td>
      <td>19</td>
    </tr>
    <tr>
      <th>7</th>
      <td>Entertainment Tonight</td>
      <td>19</td>
    </tr>
    <tr>
      <th>8</th>
      <td>Castle</td>
      <td>18</td>
    </tr>
    <tr>
      <th>9</th>
      <td>This Is Us</td>
      <td>17</td>
    </tr>
    <tr>
      <th>10</th>
      <td>NCIS: Los Angeles</td>
      <td>17</td>
    </tr>
    <tr>
      <th>11</th>
      <td>Jimmy Kimmel Live!</td>
      <td>16</td>
    </tr>
  </tbody>
</table>
</div>

From the above table we can see that the cast of Euphoria also collaborated in other film or TV works. Criminal Minds and Shameless are well-known works that we are familiar with. I can't wait to find some familiar casts in these TV series.
