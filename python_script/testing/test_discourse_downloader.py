import unittest
import importlib
importlib.import_module('data.website_base_data')
from data.website_base_data import WEBSITE_URL
from data.discourse_downloader import DiscourseDownloader
import os
import shutil

class TestDiscourseDownloader(unittest.TestCase):
    
    def setUp(self):
        # testing folder
        self.testing_folder = os.path.join("python_script","testing")
        # folder with the prepared html files
        self.html_folder = os.path.join(self.testing_folder, "test_discourse_downloader")
        # folder where the html files will be downloaded to
        self.download_folder = os.path.join(self.testing_folder,"temp","html_files")
        # create download folder
        os.mkdirs(self.download_folder)

        self.downloader = DiscourseDownloader(WEBSITE_URL, dataset_folder=self.download_folder)


    def test_get_html_from_url(self):
        self.downloader.get_html_from_url(self.downloader.website_url, sleep_time=0)

    def test_download_user_list(self):
        # TODO: i dont know how to test this method other than this

        self.downloader._download_user_list(sleep_time=0)

    def test_download_user_list(self):
        # TODO: set up a predefined short user list and download that one
        # test: filenames
        # test: contents of files 
        pass

    def tearDown(self):
        # remove contents of download folder
        shutil.rmtree(self.download_folder)