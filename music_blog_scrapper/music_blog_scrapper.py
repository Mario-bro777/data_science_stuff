import requests
from bs4 import BeautifulSoup
import time
import re

response = requests.get('https://odeonmusic.blogspot.com')
soup = BeautifulSoup(response.text, 'html.parser')
soup.title.text

#first page parsing
posts_raw = soup.find_all('div', 'post-outer')

#post parsing (drop first 3 posts)
posts_parsed = [{'timestamp':post.find('abbr').get('title'), 
              'title':post.find('h3', 'post-title entry-title').text.strip(), 
              'link':post.find('h3', 'post-title entry-title').find('a').get('href')} for post in posts_raw[3:]]

with open('odeon_posts.csv', 'a') as f:
    for post in posts_parsed:
        f.write(post['timestamp'] + '\t' + post['title'] + '\t' + post['link'] + '\n')
        

next_page = soup.find('a', 'blog-pager-older-link').get('href') 
#wall_pages = []

try:
  while next_page is not None:
      #wall_pages.append(next_page)
      
      #other pages parsing
      response = requests.get(next_page)
      soup = BeautifulSoup(response.text, 'html.parser')

      posts_raw = soup.find_all('div', 'post-outer')
      
      posts_parsed = [{'timestamp':post.find('abbr').get('title'), 
                     'title':post.find('h3', 'post-title entry-title').text.strip(), 
                     'link':post.find('h3', 'post-title entry-title').find('a').get('href')} for post in posts_raw]
      #post_list.extend(entry)
      
      #get link to next page and reaching the end of wall check
      next_page = soup.find('a', 'blog-pager-older-link')
      if next_page is not None:
          next_page = next_page.get('href')
      else:
          print('wall is over')
          break

      #save to file posts from page and current page
      with open('odeon_wall.txt', 'a') as f:
        f.write(next_page + '\n')
      with open('odeon_posts.csv', 'a') as f:
        for post in posts_parsed:
            f.write(post['timestamp'] + '\t' + post['title'] + '\t' + post['link'] + '\n')
        
      #pages_num -= 1
      time.sleep(1)
finally:
  with open('odeon_wall.txt', 'a') as f:
    f.write('\n'.join(wall_pages))
