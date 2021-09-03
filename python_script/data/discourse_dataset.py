from python_script.data.discourse_downloader import DiscourseDownloader
from python_script.data.discourse_converter import DiscourseConverter
from python_script.data.discourse_data_loader import DiscourseDataLoader
import os
import io
import sys
import copy
from pathlib import Path
import numpy as np
from IPython.core.display import display, HTML
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator

class DiscourseDataset():
    """
    Discourse dataset class
    Defines a dataset that can be filtered and plotted 
    """

    # ====================================================================================== #
    # USER INTERACTION:                                                                      #
    # ====================================================================================== #

    def __init__(self,
                 website_url,
                 posts=None,
                 dataset_folder=os.path.join("datasets","Discourse"),
                 supress_output=True,
                 overwrite_html=False,
                 overwrite_json=False,
                 sleep_time=1
                 ):
        """
        Parameters:
        :param posts: list, post dictionaries
        :param website_url: string, the base url of the discourse website
        :param dataset_folder: string, the location of the dataset
        :param supress_output: bool, if the output should be supressed
        :param overwrite_html: bool, if the html files should be overwritten
        :param overwrite_json: bool, if the json files should be overwritten
        :param sleep_time: int, time in seconds that the web crawler should wait for the page to load
        """

        self.website_url = website_url
        self.dataset_folder = dataset_folder

        # initialize with downloader
        if posts is None:
            # download html files and json files and make posts dataset
            posts = self._make_dataset(website_url, dataset_folder=dataset_folder, supress_output=supress_output, overwrite_html=overwrite_html, overwrite_json=overwrite_json, sleep_time=sleep_time) 
        
        # sort posts by post times
        sorted_posts = sorted(posts, key=lambda p: p.get('post_timestamp', sys.maxsize))
        self.posts = sorted_posts

    def __call__(self, 
               username=None,
               full_name=None,
               join_before=None,
               join_after=None,
               last_post_before=None,
               last_post_after=None,
               member_status=None,
               topic=None,
               topic_link=None,
               post_before=None,
               post_after=None,
               text=None,
               category = None,
               empty=None
               ):
        """
        Get dataset with posts filtered according to the parameters 
        
        Parameters:
        :param username: str
        :param full_name: str
        :param join_before: Datetime
        :param join_after: Datetime
        :param last_post_before: Datetime
        :param last_post_after: Datetime
        :param member_status: str
        :param topic: str
        :param topic_link: str
        :param post_before: Datetime
        :param post_after: Datetime
        :param text: str
        :param category: str
        :param empty: bool
        """

        posts = self._filter_posts(username, full_name, join_before, join_after, last_post_before, last_post_after, member_status, topic, topic_link, post_before, post_after, text, category, empty)
        return DiscourseDataset(self.website_url, posts=posts)

    def __iter__(self) -> iter:
        if self.posts is not None:
            return iter(self.posts)

    def __len__(self) -> int:
        if self.posts is not None:
            return len(self.posts) 

    def __getitem__(self, key: int or slice or str) -> list or dict:
        # if key is integer or slice, return item(s) from list
        if isinstance(key, int) or isinstance(key, slice):
            return self.posts[key]

        # if key is string, return unique list with key property from the posts
        if isinstance(key, str): 
            return list(set([post[key] for post in self.posts if key in post]))
        
    def __eq__(self, obj) -> bool:
        # compare posts of dataset
        return self.posts == obj.posts

    def __str__(self) -> str:
        """
        Pretty prints post topic, username, time and text 
        """
        def get_post_time(post):
            return str(self.timestamp_to_datetime(post['post_timestamp']))

        # go through posts and post one by one, sorted by date
        sorted_posts = sorted(self.posts, key=lambda p: p.get('post_timestamp', sys.maxsize), reverse=True)
        
        string_list = []
        for post in sorted_posts:
            header = post['topic'] + " | " + post['username'] + " | "  + get_post_time(post)
            text =  (post['text'] + "\n")

            string_list.append(header)
            string_list.append(text)
        
        return "\n".join(string_list)

    def search(self, *strings):
        """
        Finds posts with string in the text or as topic.

        Parameters:
        :param args: str or list, looking for this string in either text or topic
        """

        posts = copy.deepcopy(self.posts) # returns new dataset, so copy of posts is required
        
        strings = [string.lower() for string in strings] # ignore case(upper/lower)
        posts = [post for post in posts if 'text' in post and 'topic' in post and post['text'] is not None and post['topic'] is not None ]
        posts = [post for post in posts if any([string in post['text'].lower() or string in post['topic'].lower() or [string in post['username'].lower() for string in strings])]

        return DiscourseDataset(self.website_url, posts=posts)
    
    def display(self):
        display(HTML(self._create_posts_html()))

    def write(self, filename: str, overwrite=False):
        """
        Writes an html to disk.

        Input:
        :param filename: string, path to file
        :param html: html file, file that should be written to disk
        :param overwrite: boolean, should the file be overwritten if it already exists
        """
        html = self._create_posts_html()
        html = html.replace("’", "'") # replacing for compatibilty
        filepath = os.path.join(self.dataset_folder, filename + ".html")

        if Path(filepath).is_file() and not overwrite:
            # html file already exists, dont overwrite
            pass
        elif not Path(filepath).is_file():
            # write to file
            open(filepath, 'x') # create file
            with io.open(filepath, 'w', encoding="utf-8") as outfile:
                outfile.write(html)
                outfile.close()            
        elif Path(filepath).is_file() and overwrite:
            # html file should be overwritten
            with io.open(filepath, 'w', encoding="utf-8") as outfile:
                outfile.write(html)
                outfile.close()

    # ====================================================================================== #
    # INITIALIZATION:                                                                        #
    # ====================================================================================== #

    @staticmethod
    def _make_dataset(website_url: str,
                 dataset_folder=os.path.join("datasets","Discourse"),
                 supress_output=True,
                 overwrite_html=False,
                 overwrite_json=False,
                 overwrite_dataset=False,
                 sleep_time=1
                 ) -> list:
        
        # load data directly from dataset file
        filename = os.path.join(dataset_folder,"json_files", "dataset.json")
        if all([not overwrite_html, not overwrite_json, not overwrite_dataset]) and Path(filename).is_file():
            dataLoader = DiscourseDataLoader(dataset_folder=os.path.join(dataset_folder,"json_files"))
            directly_loaded_posts = dataLoader()
            if directly_loaded_posts is not None: return directly_loaded_posts


        downloader = DiscourseDownloader(website_url, dataset_folder=os.path.join(dataset_folder, "html_files"))
        _, profiles_html, post_histories_html = downloader(sleep_time=sleep_time, overwrite=overwrite_html, supress_output = supress_output)
        
        converter = DiscourseConverter(website_url, dataset_folder=os.path.join(dataset_folder,"json_files"))
        profiles_json, post_histories_json = converter(profiles_html, post_histories_html, overwrite=overwrite_json, supress_output=supress_output)
            
        dataLoader = DiscourseDataLoader(dataset_folder=os.path.join(dataset_folder,"json_files"))
        indirectly_loaded_posts = dataLoader(profiles_json, post_histories_json, overwrite=overwrite_dataset)

        return indirectly_loaded_posts

    # ====================================================================================== #
    # FILTER POSTS:                                                                          #
    # ====================================================================================== #

    def _search_for_post(self, search_dict, posts):
        """
        recursively searches for posts with the specified properties and returns new list
        """
        def timestamp_search(search_key, search_dict, posts):
            if search_key[0:4] == 'post': post_key = 'post_timestamp'
            if search_key[0:4] == 'join': post_key = 'join_timestamp'
            if search_key[0:9] == 'last_post': post_key = 'last_post_timestamp'
            if search_key[len(search_key) - 6:] == 'before': before_after = 'before'
            if search_key[len(search_key) - 5:] == 'after': before_after = 'after'

            # remove dicts that dont have the post key
            posts = [post for post in posts if post_key in post]

            # searches for timestamps before or after at the specified key
            if before_after == 'before':
                new_posts = [post for post in posts if post[post_key] < search_dict[search_key]]
            if before_after == 'after':
                new_posts = [post for post in posts if post[post_key] > search_dict[search_key]]
            
            # search for dict with the remaining search keys and values
            search_dict.pop(search_key)
            return self._search_for_post(search_dict, new_posts)

        time_search_keys = ['post_before', 'post_after', 'join_before', 'join_afer', 'last_post_before', 'last_post_after']
        

        if search_dict == {}: return posts

        if all((time_key not in search_dict) for time_key in time_search_keys):
            # do normal dict search, recursion terminated
            
            # check if the keys are in the posts
            filtered_posts = [post for post in posts if all((target_key in post) for target_key, _ in search_dict.items())] 
            # filter the posts, check if the post has the target value or if the post is in the list of target values            
            filtered_posts = [post for post in filtered_posts if all(((post[target_key] == target_value) or (post[target_key] in target_value)) for target_key, target_value in search_dict.items())]
                    
            return filtered_posts
        
        else:
            # do recursive search until all timestamp searches have been resolved
            for key in time_search_keys:
                # go through all the possible timestamp keys
                if key in search_dict:
                    # if the key is in the search dict, do the timestamp search
                    return timestamp_search(key, search_dict, posts)

    def _filter_posts(self, username, full_name, join_before, join_after, last_post_before, last_post_after, member_status, topic, topic_link, post_before, post_after, text, category, empty):
        """
        filter posts according to the specified parameters
        
        Input:
        string
        """
        
        
        filter_parameters = [username, 
                     full_name, 
                     join_before, 
                     join_after, 
                     last_post_before, 
                     last_post_after, 
                     member_status, 
                     topic, 
                     topic_link, 
                     post_before, 
                     post_after,
                     text,
                     category,
                     empty]
        time_parameters = [join_before, 
                          join_after, 
                          last_post_before, 
                          last_post_after, 
                          post_before, 
                          post_after]
        
        keys = ['username',
                'full_name', 
                'join_before', 
                'join_after', 
                'last_post_before', 
                'last_post_after', 
                'member_status', 
                'topic', 
                'topic_link', 
                'post_before', 
                'post_after',
                'text',
                'category',
                'empty']
        time_keys = ['join_before', 
                     'join_after', 
                     'last_post_before', 
                     'last_post_after', 
                     'post_before', 
                     'post_after']

        # build dict to search for 
        dict_to_search_for = {}
        for argument, key in zip(filter_parameters, keys):
            if argument is not None:
                dict_to_search_for[key] = argument

        # convert datetime objects to timestamps
        for argument, key in zip(time_parameters, time_keys):
            if argument is not None:
                dict_to_search_for[key] = self.datetime_to_timestamp(argument)        

        # filter posts
        posts = copy.deepcopy(self.posts) # returns new list, so copy of posts is required
        filtered_posts = self._search_for_post(dict_to_search_for, posts)

        # return dataset of filtered posts
        return filtered_posts
    
    # ====================================================================================== #
    # PLOTTING:                                                                            #
    # ====================================================================================== #
    
    def plot(self, title=None):
        """
        Plots a histogram of post times with months as bins
        """
        
        def get_month_ticks(datetimes: list) -> list:
            datetimes = sorted(datetimes)

            first_month = sorted(datetimes)[0].month
            first_year = sorted(datetimes)[0].year
            last_month = sorted(datetimes)[len(datetimes)-1].month
            last_year = sorted(datetimes)[len(datetimes)-1].year
            
            month = first_month
            year = first_year

            months = []
            years = []
            while year < last_year or (year == last_year and month <= last_month):
                months.append(month)
                years.append(year)
                if month == 12:
                    month = 1
                    year = year + 1
                else:
                    month = month + 1 
            
            month_year = [str(month).zfill(2) + "\n'" + str(year)[2:] for year, month in zip(years, months)]
            return month_year

        def get_number_month_bins(datetimes: list) -> int:
            num_bins = len(get_month_ticks(datetimes))
            return num_bins

        datetimes = self.timestamp_to_datetime(self['post_timestamp'])
        fig = plt.figure(figsize=(18,6))
        n, bins, patches = plt.hist(datetimes, get_number_month_bins(datetimes))
        print("n")
        print(n)
        print("patches")
        print(patches)

        # define minor ticks and draw a grid with them
        minor_locator = AutoMinorLocator(2)
        plt.gca().xaxis.set_minor_locator(minor_locator)
        plt.grid(which='minor', color='white', lw = 0.5)
        
        # x ticks
        xticks = [(bins[idx+1] + value)/2 for idx, value in enumerate(bins[:-1])]
        xticks_labels = get_month_ticks(datetimes)
        plt.xticks(xticks, labels = xticks_labels)
        
        # labels and title
        plt.xlabel('month\nyear')
        plt.ylabel('Number of Posts')

        if title is None:
            plt.title('Number of Posts per Month')
        else:
            plt.title(title)
        plt.show()

    def _create_posts_html(self):
        """
        Pretty prints post topic, username, time and text with hyperlinks 
        """
        def get_post_topic_tag(post):
            return "<a href=" + post['topic_link'] + ">" + post['topic'] + "</a>"

        def get_profile_html_tag(post):
            return "<a href=" + self.website_url + "/u/" + post['username'] + ">" + post['username'] + "</a>"

        def get_post_time(post):
            return str(self.timestamp_to_datetime(post['post_timestamp']))

        # go through posts and post one by one, sorted by date
        sorted_posts = sorted(self.posts, key=lambda p: p.get('post_timestamp', sys.maxsize), reverse=True)
        
        html_strings = []
        for post in sorted_posts:
            if post['text'] is not None:
                html_strings.append(get_post_topic_tag(post) + " | " + get_profile_html_tag(post) + " | " + get_post_time(post))
                html_strings.append("<p>" + post['text'] + "</p>")

        posts_html = "\n".join(html_strings)

        return posts_html

    # ====================================================================================== #
    # TIMESTAMPS:                                                                            #
    # ====================================================================================== #
    
    @staticmethod
    def datetime_to_timestamp(datetime_object: datetime) -> int:
        return np.floor(datetime.timestamp(datetime_object)*1000)
    
    @staticmethod
    def timestamp_to_datetime(timestamp: int) -> datetime:
        if type(timestamp) is int:
            return datetime.fromtimestamp(np.floor(timestamp/1000))
        if type(timestamp) is list:
            return [datetime.fromtimestamp(np.floor(stamp/1000)) for stamp in timestamp]

from python_script.data.website_base_data import WEBSITE_URL
if __name__ == '__main__':
    dataset = DiscourseDataset(WEBSITE_URL)
