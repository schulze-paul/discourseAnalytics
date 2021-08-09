from IPython.core.display import HTML
from selenium import webdriver
import time
import io
import os
from pathlib import Path
from bs4 import BeautifulSoup as soup
from tqdm.notebook import tqdm
import shutil
import sys

class DiscourseDownloader():
    """
    Discourse downloader class
    Defines a downloader for user profiles and post histories of a Discourse website
    """

    user_list_html_filepath = None
    user_profile_filepath_list = []
    user_post_history_filepath_list = []

    def __init__(self, website_url: str, dataset_folder=os.path.join("datasets","Discourse","html_files")):
        """
        Set up the downloader

        Input:
        :param website_url: string, the url of the discourse website
        :param dataset_folder: string, the location of the dataset
        """
        
        self.website_url = website_url
        self.dataset_folder = dataset_folder

    def __call__(self, sleep_time: int, overwrite=False, supress_output=False):
        """
        Download the html files for:
        - the user list
        - profiles
        - post histories

        Input:
        :param sleep_time: float, time that the browser waits for the page to update after scrolling
        :param overwrite: boolean, should list html files be overwritten
        :param supress_output: boolean, should the detailed output print be supressed?
        """


        if overwrite:
            confirm = self.query_yes_no("Confirm overwriting html data")
            if confirm:
                overwrite = True
            if not confirm:
                overwrite = False 

        self._set_up_folders(overwrite)
        self._start_chrome_browser()
        self._download_user_list(sleep_time, overwrite, supress_output)
        self._download_user_data(sleep_time, overwrite, supress_output)
        self._quit_chrome_browser()

        return self.user_list_html_filepath, self.user_profile_filepath_list, self.user_post_history_filepath_list

    # ====================================================================================== #
    # DOWNLOADERS:                                                                           #
    # ====================================================================================== #

    def _download_user_list(self, sleep_time: int, overwrite=False, supress_output=False):
        """
        Download the html file of the user list
        
        Input:
        :param sleep_time: float, time that the browser waits for the page to update after scrolling
        :param overwrite: boolean, should the html file be overwritten
        :param supress_output: boolean, should the detailed output print be supressed?
        """
        # downloads the user list html
        self.user_list_html_filepath = os.path.join(self.dataset_folder, "user_list.html")
        
        # check if file already exists
        if Path(self.user_list_html_filepath).is_file() and not overwrite:
            # html file already exists, dont overwrite
            if not supress_output: print("user_data_html already exists, skipping download")
        else:
            if Path(self.user_list_html_filepath).is_file() and overwrite:
                # html file should be overwritten
                if not supress_output: print("downloading and overwriting user_data_html")
            if not Path(self.user_list_html_filepath).is_file():
                # html file not found
                if not supress_output: print("user_data_html not found, downloading...")

            # download user list html from website and write to file
            user_list_url = self.website_url + "/u?period=all"
            user_list_html = self._get_html_from_url(user_list_url, sleep_time)
            if user_list_html is not None:
                self._write_html_to_file(self.user_list_html_filepath, user_list_html, overwrite)
            
    def _download_user_data(self, sleep_time: int, overwrite=False, supress_output=False):
        """
        Download the html files for profiles and post histories

        Input:
        :param sleep_time: float, time that the browser waits for the page to update after scrolling
        :param overwrite: boolean, should the html files be overwritten
        :param supress_output: boolean, should the detailed output print be supressed?
        """

        # get the links to the profiles first
        if self.user_list_html_filepath is None:
            self._download_user_list()
        
        # open the html file of the user list and get the profile links
        with open(self.user_list_html_filepath, 'rb') as user_list_html:
            user_links = self.get_user_links(user_list_html)

        # go through each profile link and download the profile html and the post history html        
        for index, profile_link in enumerate(tqdm(user_links, desc="downloading user data")):
            
            # get user name and file names
            username = self.get_user_name_from_profile_link(profile_link)
            profile_filepath = os.path.join(self.dataset_folder, "profiles", username + ".html")
            post_history_filepath = os.path.join(self.dataset_folder, "post_histories", username + ".html")

            # save filepaths
            self.user_profile_filepath_list.append(profile_filepath)
            self.user_post_history_filepath_list.append(post_history_filepath)

            # print progress update
            if not supress_output: print("( " + str(index+1).zfill(4) + " / " + str(len(user_links)) + " ): " + username )

            # check if files exist already
            if Path(profile_filepath).is_file() and Path(post_history_filepath).is_file() and not overwrite:
                # dont overwrite:
                if not supress_output: print("files already exist, skipping download")
            else:    
                # profile:
                if not supress_output: print("downloading profile html...")
                profile_html = self._get_html_from_url(self.website_url + profile_link)
                if profile_html is not None: # check for connection
                    self._write_html_to_file(profile_filepath, profile_html, overwrite)

                # post history:
                post_history_link = profile_link + "/activity"
                if not supress_output: print("downloading post history html...")
                post_history_html = self._get_html_from_url(self.website_url + post_history_link, sleep_time)
                if post_history_html is not None: # check for connection
                    self._write_html_to_file(post_history_filepath, post_history_html, overwrite)
            
    # ====================================================================================== #
    # HTML HANDLER / DRIVER:                                                                 #
    # ====================================================================================== #

    def _set_up_folders(self, overwrite: bool):
        html_folder_profiles = os.path.join(self.dataset_folder, "profiles")
        html_folder_post_histories = os.path.join(self.dataset_folder, "post_histories")
        if overwrite:
            shutil.rmtree(html_folder_profiles)
            shutil.rmtree(html_folder_post_histories)
                    
        if not os.path.isdir(html_folder_profiles):
            os.makedirs(html_folder_profiles)
        if not os.path.isdir(html_folder_post_histories):
            os.makedirs(html_folder_post_histories)

    def _start_chrome_browser(self):
        # prepare the options for the chrome driver
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_experimental_option('excludeSwitches', ['enable-logging'])

        # start chrome browser
        self.driver = webdriver.Chrome("C:/Users/Thesis/chromedriver/chromedriver.exe", options=options)
        
    def _quit_chrome_browser(self):
        self.driver.quit()

    def _scroll_down(self, sleep_time: int):
            """A method for scrolling the page."""

            # Get scroll height.
            last_height = self.driver.execute_script("return document.body.scrollHeight")
                
            while True:
                # Scroll down to the bottom.
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                # Wait to load the page.
                time.sleep(sleep_time)

                # Calculate new scroll height and compare with last scroll height.
                new_height = self.driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:

                    break

                last_height = new_height

    def _get_html_from_url(self, url, sleep_time=1):
        """
        get the html file from a url with selenium including scrolling down
        """        
        try:
            self.driver.get(url)
        except Exception as e:
            print(e)
            print("chromedriver could not get page, skipping to next")
            return None
        self._scroll_down(sleep_time)
        html = self.driver.page_source
        
        if html != "<html><head></head><body></body></html>":
            return html
        else:
            print("chromedriver could not get page, skipping to next")
            return None

    @staticmethod
    def _write_html_to_file(filename: str, html: HTML, overwrite=False):
        """
        Writes an html to disk.

        Input:
        :param filename: string, path to file
        :param html: html file, file that should be written to disk
        :param overwrite: boolean, should the file be overwritten if it already exists
        """
        if Path(filename).is_file() and not overwrite:
            # html file already exists, dont overwrite
            pass
        elif not Path(filename).is_file():
            # write to file
            open(filename, 'x') # create file
            with io.open(filename, 'w', encoding="utf-8") as outfile:
                outfile.write(html)
                outfile.close()            
        elif Path(filename).is_file() and overwrite:
            # html file should be overwritten
            with io.open(filename, 'w', encoding="utf-8") as outfile:
                outfile.write(html)
                outfile.close()

    # ====================================================================================== #
    # HELPERS:                                                                               #
    # ====================================================================================== #


    @staticmethod
    def get_user_links(users: HTML) -> list:
        """
        get the links to user profiles from the html file
        
        Input:
        :param user_list_html: html file of the users list of the discourse page

        Output:
        list of links to the user profiles, strings
        """
        user_link_list = []
        
        # make soup from user list html
        user_list_soup = soup(users, 'html.parser')

        # find the links in the soup
        username_spans = user_list_soup.find_all('span', {'class': 'username'}) # get a list with all the username spans

        for span in username_spans: 
            # get the link from each span separately
            hyperlink = span.find('a')
            link = hyperlink.get('href')
            user_link_list.append(link)
        
        return user_link_list

    @staticmethod
    def get_user_name_from_profile_link(profile_link: str) -> str:
        return profile_link[3:]

    # ====================================================================================== #
    # USER INTERFACE:                                                                        #
    # ====================================================================================== #

    @staticmethod
    def query_yes_no(question, default="no"):
        """Ask a yes/no question via raw_input() and return their answer.

        "question" is a string that is presented to the user.
        "default" is the presumed answer if the user just hits <Enter>.
                It must be "yes" (the default), "no" or None (meaning
                an answer is required of the user).

        The "answer" return value is True for "yes" or False for "no".
        """
        valid = {"yes": True, "y": True, "ye": True, "no": False, "n": False}
        if default is None:
            prompt = " [y/n] "
        elif default == "yes":
            prompt = " [Y/n] "
        elif default == "no":
            prompt = " [y/N] "
        else:
            raise ValueError("invalid default answer: '%s'" % default)

        while True:
            sys.stdout.write(question + prompt)
            choice = input().lower()
            if default is not None and choice == "":
                return valid[default]
            elif choice in valid:
                return valid[choice]
            else:
                sys.stdout.write("Please respond with 'yes' or 'no' " "(or 'y' or 'n').\n")