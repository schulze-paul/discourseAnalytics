from bs4 import BeautifulSoup as soup
from selenium import webdriver
import time
from datetime import datetime
import numpy as np
import json
from pathlib import Path
import logging
import progressbar
import io

progressbar.streams.wrap_stderr()
logging.basicConfig()

class DownloadUserData:

    
    def __init__(self, html_file_name):

        self.user_list_html_filename = 'datasets/Discourse/user_list/user_list.htm'
        self.user_base_data_filename = 'datasets/Discourse/users_base_data/user_data.json'
        self.user_base_data_list = []

    def __call__(self, overwrite_base_data_json=False):

        if not overwrite_base_data_json:
            # try to get userdata from json
            with open(self.user_base_data_filename, 'r') as user_base_data_json_file:
                self.user_base_data_list = json.loads(user_base_data_json_file.read())
            print("loading user base data from json")
        if overwrite_base_data_json:
            # get user base data and write to json
            self.user_base_data_list = self.get_users_base_data_from_html_users_list(self.user_list_html_filename)
            self.write_base_data_to_json(self.user_base_data_list)

        # get the post history and create html files
        self.get_post_history_and_write_to_html(self.user_base_data_list)

        # update user base data with time frame and post history reference 
        self.write_base_data_to_json(self.user_base_data_list)

    def get_users_base_data_from_html_users_list(self, html_file_name):

        users_data_list = []

        # make soup
        with open(html_file_name, 'rb') as users_html:
            self.users_soup = soup(users_html, "html.parser")

        # find all divs with the class user-detail
        user_divs = self.users_soup.find_all("div", {"class": "user-detail"})
        
        
        print("collecting user base data:")
        index = 0
        with progressbar.ProgressBar(max_value=len(user_divs)) as bar:
            for div in user_divs:
                # progress bar
                index = index + 1
                bar.update(index)
                
                
                user_data = {}

                # find the name
                text = div.get_text()
                username = text.splitlines()[2]
                user_data['username'] = username
                name = text.splitlines()[3]
                user_data['name'] = name
                
                # find out if member or director
                member = False
                director = False
                membertext = text.splitlines()[5]
                if membertext.startswith("M"):
                    member = True
                if membertext.startswith("D"):
                    director = True
                user_data['member'] = member
                user_data['director'] = director

                #get the link
                link = div.find_all("a", href=True)
                for element in link:
                    url = element['href']
                user_data['url'] = url

                users_data_list.append(user_data)

        return users_data_list
        
    def write_base_data_to_json(self, user_base_data_list):
        # dump all base user data in one json
        with open(self.user_base_data_filename, 'w') as outfile:
            json.dump(user_base_data_list, outfile)
    
    def get_post_history_and_write_to_html(self, user_base_data_list):
        """
        Goes through the user base data and sets attributes like join time, last post time,
        decides if the profile is outdated (last post older than 2020), or inactive (no posts).
        If profile is not outdated or inactive, it collects all the activity data from the profile 
        and writes it to a json file. The file name of the json is set in base user data dict.

        returns updated dict with timeframe and post history references
        """
        def set_time_frame(user_data):
            """
            get join date, last post times from user and decide if profile is inactive
            """ 
            user_html = self.get_html_from_url(user_data['url'])

            # create soup
            user_soup = soup(user_html, "html.parser")
            user_divs = user_soup.find_all("div", {"class": "secondary"})
            
            # get the time stamps 
            timestamp_list = []
            for div in user_divs:
                time_divs = div.find_all("span", {"class": "relative-date date"})
                for time_div in time_divs:
                    timestamp = int(time_div['data-time'])
                    timestamp_list.append(timestamp)
            
            # set the join time
            if len(timestamp_list) >=1:
                user_data['join'] = timestamp_list[0]
            else:
                user_data['join'] = None

            # set last post time, if there are any posts
            if len(timestamp_list) >= 3:
                user_data['last_post'] = timestamp_list[1]
            else:
                user_data['last_post'] = None

            # decide if profile is outdated
            if user_data['last_post'] != None:
                if datetime.fromtimestamp(user_data['last_post']/1000).year < 2020:
                    # if last post is older than 2020, its outdated:
                    user_data['outdated'] = True
                else:
                    user_data['outdated'] = False
            else:
                user_data['outdated'] = False

            return user_data
        
        def decode_post_history_html_to_json(post_history_html):
            
            def get_post_texts(activity_soup):
                post_text_list = []
                postings_htlms = activity_soup.find_all('p')
                for postings_htlm in postings_htlms: post_text_list.append(postings_htlm.get_text)
                return post_text_list
            
            def get_post_topics(activity_soup):
                post_topic_list = []
                topics_htlms = activity_soup.find_all('a', {'class': None})
                for topics_htlm in topics_htlms: post_topic_list.append(topics_htlm.get_text())
                return post_topic_list
            
            def get_post_times(activity_soup):
                post_time_list = []
                time_htlms = activity_soup.find_all('span', {'class': 'relative-date date'})
                for time_htlm in time_htlms: post_time_list.append(time_htlm.get('data-time'))
                return post_time_list
            
            def get_post_categories(activity_soup):
                post_category_list = []
                categories_htlms = activity_soup.find_all('span', {'class': 'category-name'})
                for categories_htlm in categories_htlms: post_category_list.append(categories_htlm.get_text())
                return post_category_list

            def get_post_link(activity_soup):
                return None

            post_history_list = []
            # make soup

            activity_soup = soup(post_history_html, "html.parser")
            
            post_texts = get_post_texts(activity_soup)
            post_topics = get_post_topics(activity_soup)
            post_times = get_post_times(activity_soup)
            post_categories = get_post_categories(activity_soup)
            print(len(post_texts))
            print(len(post_topics))
            print(len(post_times))
            print(len(post_categories))


            return
            # find all the posting divs
            post_divs = activity_soup.find_all("div", {"class": "user-stream-item item ember-view"})

            # go through each posting
            for post_div in post_divs:
                posting = {}
                
                
                
                # dicussion topic
                dicussion_topic_html = post_div.find_all("a", href=True)
                for element in dicussion_topic_html:
                    discussion_topic = element.get_text()
                posting['discussion_topic'] = discussion_topic
                print("DISCUSSION")
                print(discussion_topic)

                # post message
                post_message_html = post_div.find_all("p", {"class": "excerpt"})
                for element in post_message_html:
                    post_message = element.get_text()
                posting['message'] = post_message
                print("MESSAGE")
                print(post_message)

                # time
                time_html = post_div.find_all("span", {"class": "relative-date date"})
                for element in time_html:
                    timestamp = int(element['data-time'])
                #post_time = datetime.fromtimestamp(np.floor(timestamp/1000))
                posting['time'] = timestamp# datetime.strptime(str(post_time), '%Y-%m-%d %H:%M:%S')
                print("TIME")
                print(timestamp)

                # link 
                link_html = post_div.find_all("a", href=True)
                for element in link_html:
                    url = element['href']
                posting['url'] = 'https://discourse.southlondonmakerspace.org' + url
                print("URL")
                print(posting['url'])

                # category
                category_html = post_div.find_all("div", {"class": "category"})
                for element in category_html:
                    category = element.get_text()
                posting['category'] = category
                print("CATEGORY")
                print(category)

                post_history_list.append(posting)
            
            postings_json = json.dumps(post_history_list, indent = 4)

            return postings_json

        def write_post_history_to_html(post_history_json_filename, post_history_html):
            open(post_history_json_filename, 'x')
            with io.open(post_history_json_filename, 'w', encoding="utf-8") as outfile:
                outfile.write(post_history_html)
                outfile.close()


        print("downloading user post history to html:")

        # go through all the users and download post histories to html files
        for user_index in range(len(user_base_data_list)):
            user_data = user_base_data_list[user_index]
            print("user profile (" + str(user_index).zfill(4) + "/" + str(len(user_base_data_list)) + ")", end="") 
            print(" \"" + user_data['username'] + "\":", end="")

            # check if timeframe is set
            try:
                user_data["outdated"]
                time_frame_set = True
            except:
                time_frame_set = False

            if not time_frame_set:
                # set join date and last post
                user_data = set_time_frame(user_data)
            
            # decide if the post history of that user is needed:
            user_post_history_needed = True
            if user_data['outdated']:
                user_post_history_needed = False
                print(" is outdated.")
            if user_data['last_post'] == None or user_data['join'] == None:
                user_post_history_needed = False
                print(" has no activity.")

            # if we need the post history, check if it has been downloaded and saved already
            if user_post_history_needed:
                post_history_html_filename = "./datasets/Discourse/post_history/" + str(user_index).zfill(4) + ".html"
                
                # if file already exists, data has been downloaded
                if Path(post_history_html_filename).is_file():
                    data_has_been_downloaded = True
                    print(" data has been downloaded already.")
                else:
                    data_has_been_downloaded = False

                if not data_has_been_downloaded :
                    # download data and save to json
                    post_history_url = user_data['url'] + "/activity"
                    print(" downloading post history.", end="")
                    post_history_html = self.get_html_from_url(post_history_url)
                    print(" writing post history to html: " + post_history_html_filename)
                    write_post_history_to_html(post_history_html_filename, post_history_html)
                
            else:
                # if post history is not needed, file is not created
                user_data['post_history_filename'] = None    
            
            # update user base data in list
            user_base_data_list[user_index] = user_data
            # update user base data in json
            self.write_base_data_to_json(user_base_data_list)

        return user_base_data_list
            

    def get_html_from_url(self, url):
        """
        get the html file from a url with selenium including scrolling down
        """        
        def scroll_down(driver):
            """A method for scrolling the page."""

            # Get scroll height.
            last_height = driver.execute_script("return document.body.scrollHeight")
                
            while True:
                # Scroll down to the bottom.
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                # Wait to load the page.
                time.sleep(1)

                # Calculate new scroll height and compare with last scroll height.
                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:

                    break

                last_height = new_height

        # prepare the option for the chrome driver
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_experimental_option('excludeSwitches', ['enable-logging'])

        # start chrome browser
        driver = webdriver.Chrome("C:/Users/Thesis/chromedriver/chromedriver.exe", chrome_options=options)
        try:
            driver.get(url)
        except:
            print("chromedriver could not get page, skipping to next")
        scroll_down(driver)
        html = driver.page_source
        driver.quit()

        return html



    

    