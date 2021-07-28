from re import search
from python_script.data.discourse_downloader import DiscourseDownloader
from python_script.data.discourse_converter import DiscourseConverter
from python_script.data.discourse_data_loader import DiscourseDataLoader
import os
from datetime import date, datetime
import numpy as np
import sys
from pathlib import Path


class DiscourseDataset():

    def __init__(self,
                 postsOrWebsiteUrl,
                 dataset_folder=os.path.join("datasets","Discourse"),
                 supress_output=True,
                 overwrite_html=False,
                 overwrite_json=False,
                 sleep_time=1
                 ):

        # initialize with downloader
        if type(postsOrWebsiteUrl) is str:
            website_url = postsOrWebsiteUrl
            # download html files and json files and make posts dataset
            posts = self._make_dataset(website_url, dataset_folder=dataset_folder, supress_output=supress_output, overwrite_html=overwrite_html, overwrite_json=overwrite_json, sleep_time=sleep_time) 
        
        # initialize with posts
        if type(postsOrWebsiteUrl) is list:
            posts = postsOrWebsiteUrl

        if type(postsOrWebsiteUrl) is not str and type(postsOrWebsiteUrl) is not list:
            raise TypeError('Dataset is was not initialized with string or list but with ' + str(type(postsOrWebsiteUrl)))

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

        return self.filter_posts(username, full_name, join_before, join_after, last_post_before, last_post_after, member_status, topic, topic_link, post_before, post_after, text, category, empty)

    def filter_posts(self, username, full_name, join_before, join_after, last_post_before, last_post_after, member_status, topic, topic_link, post_before, post_after, text, category, empty):
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
        filtered_posts = self._search_for_post(dict_to_search_for, self.posts)

        # return dataset of filtered posts
        return DiscourseDataset(filtered_posts)

    def __iter__(self):
        if self.posts is not None:
            return iter(self.posts)

    def __len__(self):
        if self.posts is not None:
            return len(self.posts) 

    def __getitem__(self, key):
        if isinstance(key, int) or isinstance(key, slice):
            # if key is integer, return item from list
            return self.posts[key]

        else: 
            # return unique list with key property from the posts
            return list(set([post[key] for post in self.posts if key in post]))
        
    def __eq__(self, obj):
        return self.posts == obj.posts

    @staticmethod
    def _make_dataset(website_url,
                 dataset_folder=os.path.join("datasets","Discourse"),
                 supress_output=True,
                 overwrite_html=False,
                 overwrite_json=False,
                 overwrite_dataset=False,
                 sleep_time=1
                 ):
        
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

    def find(self, text=None, topic=None):
        pass
    
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
            filtered_posts = [post for post in posts if all((post[target_key] == target_value) for target_key, target_value in search_dict.items())] 
            return filtered_posts
        else:
            # do recursive search until all timestamp searches have been resolved
            for key in time_search_keys:
                # go through all the possible timestamp keys
                if key in search_dict:
                    # if the key is in the search dict, do the timestamp search
                    return timestamp_search(key, search_dict, posts)

    @staticmethod
    def datetime_to_timestamp(datetime_object):
        return np.floor(datetime.timestamp(datetime_object)*1000)
    
    @staticmethod
    def timestamp_to_datetime(timestamp):
        if type(timestamp) is int:
            return np.floor(datetime.fromtimestamp(timestamp/1000))
        if type(timestamp) is list:
            return [datetime.fromtimestamp(np.floor(stamp/1000)) for stamp in timestamp]

    def __str__(self):
        
        def print_table(myDict, colList=None):
            """ 
            Pretty print a list of dictionaries (myDict) as a dynamically sized table.
            If column names (colList) aren't specified, they will show in random order.
            Author: Thierry Husson - Use it as you want but don't blame me.
            """
            lines = []

            if not colList: colList = list(myDict[0].keys() if myDict else [])
            myList = [colList] # 1st row = header
            for item in myDict: myList.append([str(item[col] if item[col] is not None else '') for col in colList])
            colSize = [max(map(len,col)) for col in zip(*myList)]
            formatStr = ' | '.join(["{{:<{}}}".format(i) for i in colSize])
            myList.insert(1, ['-' * i for i in colSize]) # Seperating line
            for item in myList: lines.append(formatStr.format(*item))
            
            return lines
        

        def _convert_timestamps_to_datetime(dict_list):
            # printing datetime objects instead of timestamp
            new_dict_list = dict_list.copy()
            
            timestamp_keys = ['post_timestamp', 'join_timestamp', 'last_post_timestamp']
            datetime_keys = ['post_time', 'join_time', 'last_post_time']
            
            for post in new_dict_list:
                for timestamp_key, datetime_key in zip(timestamp_keys, datetime_keys):
                    post[datetime_key] = datetime.fromtimestamp(np.floor(post[timestamp_key]/1000)).strftime("%Y-%m-%d %H:%M")
                    post.pop(timestamp_key)
                

            return new_dict_list

        #posts = _convert_timestamps_to_datetime(self.posts)
        #lines = print_table(posts)
        #posts_table_string = "\n".join(lines)

        return str(self.posts)


from python_script.data.website_base_data import WEBSITE_URL
if __name__ == '__main__':
    dataset = DiscourseDataset(WEBSITE_URL)