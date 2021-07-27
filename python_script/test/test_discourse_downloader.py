import unittest
from python_script.data.website_base_data import WEBSITE_URL
from python_script.data.discourse_downloader import DiscourseDownloader
import os
import shutil
from pathlib import Path

class TestDiscourseDownloader(unittest.TestCase):
    
    def setUp(self):

        def set_up_folders(self):
            # testing folder
            self.testing_folder = os.path.join("python_script","test")
            
            # folder with the prepared html files
            self.html_folder = os.path.join(self.testing_folder, "test_discourse_downloader")
            
            # temporary folder
            self.temp_folder = os.path.join(self.testing_folder,"temp")

            # folder where the html files will be downloaded to
            self.download_folder = os.path.join(self.testing_folder,"temp","html_files")

        set_up_folders(self)
        
        self.downloader = DiscourseDownloader(WEBSITE_URL, dataset_folder=self.download_folder)

        # start browser
        self.downloader._set_up_folders()
        self.downloader._start_chrome_browser()

    def test_get_html_from_url(self):
        self.downloader._get_html_from_url(self.downloader.website_url, sleep_time=0)
    
    def test_download_user_data(self):
        # predefined short user list and download from that one
        self.downloader.user_list_html_filepath = os.path.join(self.testing_folder, "test_discourse_downloader", "user_list_1.html")
        
        # test downloader
        self.downloader._download_user_data(sleep_time=0, overwrite=False, supress_output=True)
        
        # test file names
        downloaded_profile_filename = os.path.join(self.download_folder, "profiles", "Matt_Cliffe.html")
        downloaded_post_history_filename = os.path.join(self.download_folder, "post_histories", "Matt_Cliffe.html")
        files = [downloaded_profile_filename, downloaded_post_history_filename]
        
        for file in files:
            self.assertTrue(Path(file).is_file())
            
            # test file contents
            self.assertFalse(os.stat(file).st_size == 0)

    def test_overwriting(self):
        
        filepath = os.path.join(self.download_folder, "overwrite_test.html")
        # write an html file
        self.downloader._write_html_to_file(filepath, "not overwritten")
        # write again to same file, no overwriting
        self.downloader._write_html_to_file(filepath, "overwritten")
        # load file contents
        html = open(filepath, 'rb')
        html_string = html.read()
        self.assertEqual(html_string.decode("utf-8") , "not overwritten")
        html.close()

        # write again to same file, overwriting
        self.downloader._write_html_to_file(filepath, "overwritten", overwrite=True)
        # load file contents
        html = open(filepath, 'rb')
        html_string = html.read()
        self.assertEqual(html_string.decode("utf-8") , "overwritten")
        html.close()
    
    def test_get_user_links(self):
        filepath = os.path.join(self.html_folder, "user_list_2.html")
        user_list_html = open(filepath, 'rb')
        user_links = self.downloader.get_user_links(user_list_html)

        self.assertEqual(user_links, ["/u/Lorraine_Fossi", "/u/Chris_Ross_Jackson", "/u/Diego_Luiz", "/u/John_Robertson", "/u/Lewisbellerina"]) 

    def test_get_user_name_from_profile_link(self):
        profile_link = "/u/Matt_Cliffe"
        username = self.downloader.get_user_name_from_profile_link(profile_link)

        self.assertEqual(username, "/u/Matt_Cliffe")

    def tearDown(self):
        # remove contents of download folder
        shutil.rmtree(self.temp_folder)

        # quit browser
        self.downloader._quit_chrome_browser()

if __name__ == '__main__':
    unittest.main()