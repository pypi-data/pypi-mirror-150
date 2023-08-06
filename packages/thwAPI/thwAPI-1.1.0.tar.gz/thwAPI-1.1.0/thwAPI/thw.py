import requests # HTTP Requests Library
from progress.bar import ChargingBar # Adding progress bar
import json # For Writing to file

# Create The Hashnode Writeathon class (THW)
class THW:
    # Initialise the class constructor
    def __init__(self, url):
        self.api_url = url
        
        # Other optional instance variables
        self.possible_urls = []
        self.post_list_count = []
        self.posts = []
        self.total = 0
    
    # Connecting to the API    
    def connect(self):
        # Append the init url 
        self.possible_urls.append(self.api_url)
        for page in range(0,1000):
            # Let's dynamically create the URLS for our get requests
            next_urls = self.api_url + '?page=' + str(page) 
            self.possible_urls.append(next_urls)
        try: 
            for idx, url in enumerate(self.possible_urls):
                response = requests.get(url,
                headers={"Accept": "application/json"},
                )
                data = response.json()
                blog_posts = data['posts']
                
                # Get count of the posts on that page
                post_count = len(blog_posts)
                # Update our counter container 
                self.post_list_count.append(post_count)
                
                # Adding progress bar
                bar = ChargingBar(f"---- Getting Page {idx} Posts ---", max=post_count)
                for data in blog_posts:
                    # Get summary data from each post
                    article_title = data["title"]
                    pub_title = data["publication"]["title"]
                    domain = data["author"]["username"]
                    article_slug = domain + ".hashnode.dev/" + data["slug"]  
                    date_added = data["dateAdded"]
                    
                    self.posts.append((article_title, pub_title, article_slug, date_added))
                    bar.next()   
                bar.finish() 
                # Break from the for loop if no posts on that page
                if post_count == 0:
                    break  
            return "-- SUCCESSFULLY GOT ALL THE POSTS : SUMMARY IS READY ---"      
        except Exception as e:
            return f"ERROR :: {e}"
        
    # Get total count so far
    def count(self):
        self.connect()
        total_ = 0
        # print(self.post_list_count)
        total = [total_ := total_ + x for x in self.post_list_count][-1]
        return f"There are currently {total} posts written!"
    
    # Print The Posts
    def all_posts(self):
        self.connect()
        # print(self.posts)
        for idx, post in enumerate(self.posts):            
            print(idx, post)
            
    def dump_json(self):
        self.connect()
        
        blog_dict = {"posts": self.posts}
        blog_json = json.dumps(blog_dict)
        with open("main.json", "w+", encoding="utf-8") as file:
            json.dump(blog_json, file, ensure_ascii=False)
        print("--- File Created Successfully ---")
        
                  




        


