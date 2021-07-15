from bs4 import BeautifulSoup as soup
from pathlib import Path
import json
import io
import os
import re

class DiscourseConverter():
    """
    Discourse converter class
    Defines a converter that takes html files from a Discourse website 
    and converts it into json files 
    """

    user_profile_json_filepath_list = []
    user_post_history_json_filepath_list = []

    def __init__(self, website_url, user_profile_html_filepath_list, user_post_history_html_filepath_list, dataset_folder="datasets/Discourse/json_files"):
        self.website_url = website_url
        self.user_profile_html_filepath_list = user_profile_html_filepath_list
        self.user_post_history_html_filepath_list = user_post_history_html_filepath_list
        self.dataset_folder = dataset_folder
        
    def __call__(self, overwrite=False):
        """
        Convert the html files for the user profiles and 
        post histories into json files.

        Input:
        :param overwrite: boolean, should the json files be overwritten.    
        """
        self._convert_user_profiles(overwrite)
        self._convert_post_histories(overwrite)

        return self.user_profile_json_filepath_list, self.user_post_history_json_filepath_list

    # ====================================================================================== #
    # CONVERTERS:                                                                            #
    # ====================================================================================== #

    def _convert_user_profiles(self, overwrite=False):
        
        def get_username(profile_soup):
            username_h1 = profile_soup.find('h1', {'class': 'username'})
            username_with_whitespace = username_h1.get_text()
            return username_with_whitespace.replace(" ", "")

        def get_full_name(profile_soup):
            full_name_h2 = profile_soup.find('h2', {'class': 'full-name'})
            return full_name_h2.get_text()

        def get_member_status(profile_soup):
            member_status_h3 = profile_soup.find('h3')
            return member_status_h3.get_text()

        def get_join_time(profile_soup):
            secondary_div = profile_soup.find('div', {'class': 'secondary'})
            divs_in_secondary_div = secondary_div.find_all('div')
            for div in divs_in_secondary_div:
                if div.find('dt').get_text() == "Joined":
                    return div.find('span').get('data-time')
            return None

        def get_last_post_time(profile_soup):
            secondary_div = profile_soup.find('div', {'class': 'secondary'})
            divs_in_secondary_div = secondary_div.find_all('div')
            for div in divs_in_secondary_div:
                if div.find('dt').get_text() == "Last Post":
                    return div.find('span').get('data-time')
            return None
        
        profile_dict_list = []

        for profile_html_filepath in self.user_profile_html_filepath_list:
            
            # read the html file
            user_profile_html = open(profile_html_filepath, 'rb')
            
            # create soup
            profile_soup = soup(user_profile_html, "html.parser")

            # extract data from soup
            profile_dict = {}
            profile_dict['username'] = get_username(profile_soup)                
            profile_dict['full_name'] = get_full_name(profile_soup)
            profile_dict['member_status'] = get_member_status(profile_soup)
            profile_dict['join_time'] = get_join_time(profile_soup)
            profile_dict['last_post_time'] = get_last_post_time(profile_soup)

            profile_dict_list.append(profile_dict)

            # save filepath
            profile_json_filepath = self.dataset_folder + "/profiles/" + profile_dict['username'] + ".json"
            self.user_profile_json_filepath_list.append(profile_json_filepath) # save filepath
            self._write_data_to_json_file(profile_json_filepath, profile_dict, overwrite)

    def _convert_post_histories(self, overwrite=False):
        
        def get_username_from_filepath(filepath):
            result = re.search("(post_histories\/)\w+",  filepath)
            return result.group(0)[15:len(filepath)-6]

        def get_post_topic(post_soup):
            title_span = post_soup.find('span', {'class': 'title'})
            return title_span.find('a').get_text()

        def get_post_topic_link(post_soup):
            title_span = post_soup.find('span', {'class': 'title'})
            return title_span.find('a').get('href')

        def get_post_category(post_soup):
            category_span = post_soup.find('span', {'class': 'category-name'})
            return category_span.get_text()

        def get_post_time(post_soup):
            time_span = post_soup.find('span', {'class':'relative-date date'})
            return time_span.get('data-time')

        def get_post_text(post_soup):
            excerpt_p = post_soup.find('p', {'class': 'excerpt'})
            return excerpt_p.get_text()

        for post_history_html_filepath in self.user_post_history_html_filepath_list:
            
            post_history_list = []

            # read the html file
            user_post_history_html = open(post_history_html_filepath, 'rb')
            
            # create soup
            post_history_soup = soup(user_post_history_html, "html.parser")
            all_posts_soup = post_history_soup.find_all('div', {'class': 'user-stream-item item ember-view'})

            for post_soup in all_posts_soup:

                post_dict = {}
                post_dict['topic'] = get_post_topic(post_soup)
                post_dict['topic_link'] = self.website_url + get_post_topic_link(post_soup)
                post_dict['category'] = get_post_category(post_soup)
                post_dict['time'] = get_post_time(post_soup)
                post_dict['text'] = get_post_text(post_soup)

                post_history_list.append(post_dict)

            # write post history to json file
            username = get_username_from_filepath(post_history_html_filepath)
            post_history_json_filepath = os.path.join(self.dataset_folder, "post_histories", username + ".json")
            self.user_post_history_json_filepath_list.append(post_history_json_filepath) # save filepath
            self._write_data_to_json_file(post_history_json_filepath, post_history_list, overwrite)
        
    # ====================================================================================== #
    # JSON HANDLER:                                                                         #
    # ====================================================================================== #

    def _write_data_to_json_file(self, filename, data, overwrite):
        """
        Writes a json file to disk.

        Input:
        :param filename: string, path to file
        :param data: list, dict, ... , data that should be written to disk
        :param overwrite: boolean, should the file be overwritten if it already exists
        """
        # convert data to json
        json_string = json.dumps(data)

        if Path(filename).is_file() and not overwrite:
            # html file already exists, dont overwrite
            pass
        elif not Path(filename).is_file():
            # write to file
            open(filename, 'x') # create file
            with io.open(filename, 'w') as outfile:
                outfile.write(json_string)
                outfile.close()            
        elif Path(filename).is_file() and overwrite:
            # html file should be overwritten
            with io.open(filename, 'w') as outfile:
                outfile.write(json_string)
                outfile.close()
    