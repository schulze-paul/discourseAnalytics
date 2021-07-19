from bs4 import BeautifulSoup as soup
from pathlib import Path
import json
import io
import os
import re
from tqdm import tqdm

class DiscourseConverter():
    """
    Discourse converter class
    Defines a converter that takes html files from a Discourse website 
    and converts it into json files 
    """

    user_profile_json_filepath_list = []
    user_post_history_json_filepath_list = []

    def __init__(self, website_url, dataset_folder="datasets/Discourse/json_files"):
        self.website_url = website_url
        self.dataset_folder = dataset_folder
        
    def __call__(self, user_profile_html_filepath_list, user_post_history_html_filepath_list, overwrite=False, supress_output=False):
        """
        Convert the html files for the user profiles and 
        post histories into json files.

        Input:
        :param overwrite: boolean, should the json files be overwritten.    
        """
        self._convert_user_profiles(user_profile_html_filepath_list, overwrite, supress_output)
        self._convert_post_histories(user_post_history_html_filepath_list, overwrite, supress_output)

        return self.user_profile_json_filepath_list, self.user_post_history_json_filepath_list

    # ====================================================================================== #
    # CONVERTERS:                                                                            #
    # ====================================================================================== #

    def _convert_user_profiles(self, user_profile_html_filepath_list, overwrite=False, supress_output=True):
        
        print("saving user profiles json:")

        def get_username_from_filepath(filepath):
            result = re.search(r'(profiles\\)\w+',  filepath)
            return result.group(0)[9:len(filepath)-6]

        def get_username(profile_soup):
            username_h1 = profile_soup.find('h1', {'class': 'username'})
            if username_h1 is None: return None
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
            if secondary_div is None: return None
            divs_in_secondary_div = secondary_div.find_all('div')
            for div in divs_in_secondary_div:
                if div.find('dt').get_text() == "Joined":
                    return div.find('span').get('data-time')
            return None

        def get_last_post_time(profile_soup):
            secondary_div = profile_soup.find('div', {'class': 'secondary'})
            if secondary_div is None: return None
            divs_in_secondary_div = secondary_div.find_all('div')
            for div in divs_in_secondary_div:
                if div.find('dt').get_text() == "Last Post":
                    return div.find('span').get('data-time')
            return None
        
        for index, profile_html_filepath in enumerate(tqdm(user_profile_html_filepath_list)):
            
            username = get_username_from_filepath(profile_html_filepath)

            profile_json_filepath = self.dataset_folder + "/profiles/" + username + ".json"
            self.user_profile_json_filepath_list.append(profile_json_filepath) # save filepath
            
            # print progress update
            if not supress_output: print("( " + str(index+1).zfill(4) + " / " + str(len(user_profile_html_filepath_list)) + " ): " + username )
            
            #check if file exists
            if not Path(profile_json_filepath).is_file() or overwrite:
                
                # read the html file
                user_profile_html = open(profile_html_filepath, 'rb')
                
                # create soup
                profile_soup = soup(user_profile_html, "html.parser")
                profile_dict = {}
                
                # check if profile is empty
                if get_username(profile_soup) is not None:
                    # extract data from soup
                    profile_dict['username'] = get_username(profile_soup)                
                    profile_dict['full_name'] = get_full_name(profile_soup)
                    profile_dict['member_status'] = get_member_status(profile_soup)
                    profile_dict['join_timestamp'] = get_join_time(profile_soup)
                    profile_dict['last_post_timestamp'] = get_last_post_time(profile_soup)
                else:
                    profile_dict['username'] = username
                    profile_dict['empty'] = True

                self._write_data_to_json_file(profile_json_filepath, profile_dict, overwrite)

    def _convert_post_histories(self, user_post_history_html_filepath_list, overwrite=False, supress_output=True):
        
        print("saving post histories json:")

        def get_username_from_filepath(filepath):
            result = re.search(r'(post_histories\\)\w+',  filepath)
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

        for index, post_history_html_filepath in enumerate(tqdm(user_post_history_html_filepath_list)):
            
            username = get_username_from_filepath(post_history_html_filepath)

            post_history_json_filepath = self.dataset_folder + "/post_histories/" + username + ".json"
            self.user_post_history_json_filepath_list.append(post_history_json_filepath) # save filepath
            
            # print progress update
            if not supress_output: print("( " + str(index+1).zfill(4) + " / " + str(len(user_post_history_html_filepath_list)) + " ): " + username )
            
            #check if file exists
            if not Path(post_history_json_filepath).is_file() or overwrite:

                # read the html file
                user_post_history_html = open(post_history_html_filepath, 'rb')
                
                # create soup
                post_history_soup = soup(user_post_history_html, "html.parser")
                all_posts_soup = post_history_soup.find_all('div', {'class': 'user-stream-item item ember-view'})

                post_history_list = []

                # check if profile is empty
                if all_posts_soup is not None:
                    for post_soup in all_posts_soup:
                        post_dict = {}
                        post_dict['username'] = username
                        post_dict['topic'] = get_post_topic(post_soup)
                        post_dict['topic_link'] = self.website_url + get_post_topic_link(post_soup)
                        post_dict['category'] = get_post_category(post_soup)
                        post_dict['post_timestamp'] = get_post_time(post_soup)
                        post_dict['text'] = get_post_text(post_soup)

                        post_history_list.append(post_dict)

                # write post history to json file
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
    