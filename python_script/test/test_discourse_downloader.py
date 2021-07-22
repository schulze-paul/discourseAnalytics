import unittest
from python_script.data.website_base_data import WEBSITE_URL
from python_script.data.discourse_downloader import DiscourseDownloader
import os
import shutil
from pathlib import Path

class TestDiscourseDownloader(unittest.TestCase):
    

    def setUp(self):
        # testing folder
        self.testing_folder = os.path.join("python_script","test")
        
        # folder with the prepared html files
        self.html_folder = os.path.join(self.testing_folder, "test_discourse_downloader")
        
        # temporary folder
        self.temp_folder = os.path.join(self.testing_folder,"temp")

        # folder where the html files will be downloaded to
        self.download_folder = os.path.join(self.testing_folder,"temp","html_files")
        self.download_folder_profiles = os.path.join(self.testing_folder,"temp","html_files", "profiles")
        self.download_folder_post_histories = os.path.join(self.testing_folder,"temp","html_files", "post_histories")
        # create download folders
        os.makedirs(self.download_folder)
        os.makedirs(self.download_folder_profiles)
        os.makedirs(self.download_folder_post_histories)

        self.downloader = DiscourseDownloader(WEBSITE_URL, dataset_folder=self.download_folder)

        # start browser
        self.downloader._start_chrome_browser()


    def test_get_html_from_url(self):
        self.downloader._get_html_from_url(self.downloader.website_url, sleep_time=0)
    
    
    def test_download_user_list(self):
        # TODO: i dont know how to test this method other than this
        self.downloader._download_user_list(sleep_time=0)

    def test_download_user_data(self):
        # predefined short user list and download from that one
        self.downloader.user_list_html_filepath = os.path.join(self.testing_folder, "test_discourse_downloader", "user_list_1.html")
        
        # test downloader
        self.downloader._download_user_data(sleep_time=0, overwrite=False)
        
        # test file names
        downloaded_profile_filename = os.path.join(self.download_folder, "profiles", "Matt_Cliffe.html")
        downloaded_post_history_filename = os.path.join(self.download_folder, "post_histories", "Matt_Cliffe.html")
        files = [downloaded_profile_filename, downloaded_post_history_filename]
        
        for file in files:
            self.assertTrue(Path(file).is_file())
            
            # test file contents
            self.assertFalse(os.stat(file).st_size == 0)

    def tearDown(self):
        # remove contents of download folder
        shutil.rmtree(self.temp_folder)

        # quit browser
        self.downloader._quit_chrome_browser()

if __name__ == '__main__':
    unittest.main()