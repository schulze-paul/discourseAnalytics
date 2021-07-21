from selenium import webdriver
import time
import io
import os
import re
from pathlib import Path
from bs4 import BeautifulSoup as soup
from tqdm.notebook import tqdm


class DiscourseDownloader():
    """
    Discourse downloader class
    Defines a downloader for user profiles and post histories of a Discourse website
    """

    user_list_html_filepath = None
    user_profile_filepath_list = []
    user_post_history_filepath_list = []

    def __init__(self, website_url, dataset_folder=os.path.join("datasets","Discourse","html_files")):
        self.website_url = website_url
        self.dataset_folder = dataset_folder

    def __call__(self, sleep_time, overwrite=False, supress_output=False):
        """
        Download the html files for:
        - the user list
        - profiles
        - post histories

        Input:
        :param overwrite: boolean, should the html files be overwritten.
        """

        # download data
        self._download_user_list(sleep_time, overwrite, supress_output)
        self._download_user_data(sleep_time, overwrite, supress_output)

        return self.user_list_html_filepath, self.user_profile_filepath_list, self.user_post_history_filepath_list

    # ====================================================================================== #
    # DOWNLOADERS:                                                                           #
    # ====================================================================================== #

    def _download_user_list(self, sleep_time, overwrite=False, supress_output=False):
        """
        Download the html files for the user list
        
        Input:
        :param overwrite_user_list: boolean, should the user list html file be overwritten
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
            self._write_html_to_file(self.user_list_html_filepath, user_list_html, overwrite)

    def _download_user_data(self, sleep_time, overwrite=False, supress_output=False):
        """
        Download the html files for profiles and post histories

        Input:
        :param overwrite_user_data: boolean, should the user data html file be overwritten
        """

        def get_user_links(user_list_html):
            """
            get the links to user profiles from the html file
            
            Input:
            :param user_list_html: html file of the users list of the discourse page

            Output:
            list of links to the user profiles, strings
            """
            user_link_list = []
            
            # make soup from user list html
            user_list_soup = soup(user_list_html, 'html.parser')

            # find the links in the soup
            username_spans = user_list_soup.find_all('span', {'class': 'username'}) # get a list with all the username spans

            for span in username_spans: 
                # get the link from each span separately
                hyperlink = span.find('a')
                link = hyperlink.get('href')
                user_link_list.append(link)
            
            return user_link_list

        def get_user_name_from_profile_link(profile_link):
            return profile_link[46:]
            

        # get the links to the profiles first
        if self.user_list_html_filepath is None:
            self._download_user_list()
        
        # open the html file of the user list and get the profile links
        with open(self.user_list_html_filepath, 'rb') as user_list_html:
            user_links = get_user_links(user_list_html)

        # go through each profile link and download the profile html and the post history html        
        for index, profile_link in enumerate(tqdm(user_links, desc="downloading user data")):
            
            # get user name and file names
            username = get_user_name_from_profile_link(profile_link)
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
    # HTML HANDLERS:                                                                           #
    # ====================================================================================== #

    def _get_html_from_url(self, url, sleep_time=1):
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
                time.sleep(sleep_time)

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
        print(url)
        try:
            driver.get(url)
        except Exception as e:
            print(e)
            print("chromedriver could not get page, skipping to next")
            return None
        scroll_down(driver)
        html = driver.page_source
        driver.quit()

        return html

    def _write_html_to_file(self, filename, html, overwrite=False):
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