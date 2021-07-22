import unittest
from python_script.data.website_base_data import WEBSITE_URL
from python_script.data.discourse_data_loader import DiscourseDataLoader
from python_script.data.discourse_converter import DiscourseConverter
import os
import shutil
import json

class TestDiscourseDataLoader(unittest.TestCase):
    
    def setUp(self):
        def set_up_folders(self):
            # testing folder
            self.testing_folder = os.path.join("python_script","test")
            
            # folder with the prepared json files
            self.json_folder = os.path.join(self.testing_folder, "test_discourse_data_loader")

        set_up_folders(self)
        
        self.data_loader = DiscourseDataLoader()



    def test_timestamps_to_integer(self):
        test_dicts = [{'join_timestamp': "1550691826355", 'test_1': "500"}, {'join_timestamp': '1550691826355', 'test_2': 'text','last_post_timestamp': '1556527466920'}, {'join_timestamp': '1550691826355', 'last_post_timestamp': '1556527466920', 'post_timestamp': '1556072740741'} ]

        for test_dict in test_dicts:
            converted_dict = self.data_loader.timestamps_to_integer(test_dict)
            if 'join_timestamp' in test_dict:
                self.assertEqual(converted_dict['join_timestamp'], 1550691826355)
            if 'test_1' in test_dict:
                self.assertEqual(converted_dict['test_1'], "500")
            if 'test_2' in test_dict:
                self.assertEqual(converted_dict['test_2'], "text")
            if 'last_post_timestamp' in test_dict:
                self.assertEqual(converted_dict['last_post_timestamp'], 1556527466920)
            if 'post_timestamp' in test_dict:
                self.assertEqual(converted_dict['post_timestamp'], 1556072740741)

    def test_call(self):
        # load prepared profile and post history json files
        profiles = [os.path.join(self.json_folder, "json_files", "profiles", "Matt_Cliffe.json")]
        post_histories = [os.path.join(self.json_folder, "json_files", "post_histories", "Matt_Cliffe.json")]
        
        posts = self.data_loader(profiles, post_histories)
        
        post = posts[len(posts)-1]

        self.assertEqual(post['username'], "Matt_Cliffe")
        self.assertEqual(post['full_name'], "Matt Cliffe")
        self.assertEqual(post['member_status'], "Not Member")
        self.assertEqual(post['join_timestamp'], 1550691826355)
        self.assertEqual(post['last_post_timestamp'], 1556527466920)
        self.assertEqual(post['topic'], "Joining South London Makerspace")
        self.assertEqual(post['topic_link'], "https://discourse.southlondonmakerspace.org/t/joining-south-london-makerspace/1234")
        self.assertEqual(post['category'], "Admin")
        self.assertEqual(post['post_timestamp'], 1550859165213)
        self.assertEqual(post['text'], "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.")
