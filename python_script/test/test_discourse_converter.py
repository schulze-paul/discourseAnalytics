import unittest
from python_script.data.discourse_converter import DiscourseConverter
from python_script.data.website_base_data import WEBSITE_URL
import os
import shutil
from pathlib import Path
import json

class TestDiscourseConverter(unittest.TestCase):

    def setUp(self):
        
        def set_up_folders(self):
            # testing folder
            self.testing_folder = os.path.join("python_script","test")
            # source files folder:
            self.html_folder = os.path.join(self.testing_folder, "test_discourse_converter", "html_files")
            # output files folder:
            self.temp_folder = os.path.join(self.testing_folder, "temp")
            self.json_folder = os.path.join(self.temp_folder, "json_files")

            
        # set up folders 
        set_up_folders(self)
        self.converter = DiscourseConverter(WEBSITE_URL, dataset_folder=self.json_folder)
        self.converter._set_up_folders()

    def test_convert_user_profiles(self):
        profiles_html = [os.path.join(self.html_folder, "profiles", "Matt_Cliffe.html")]
        self.converter._convert_user_profiles(profiles_html)
        
        # test filenames
        out_files = [os.path.join(self.json_folder, "profiles", "Matt_Cliffe.json")]
        for file in out_files:
            self.assertTrue(Path(file).is_file())
            
        # test file content
        file_content_1 = {}
        file_content_1['username'] = "Matt_Cliffe"
        file_content_1['full_name'] = "Matt_Cliffe"
        file_content_1['member_status'] = "Member"
        file_content_1['join_timestamp'] = "1550691826355"
        file_content_1['last_post_timestamp'] = "1556527466920"
        expected_file_contents = [file_content_1]

        for file_path, expected_content in zip(out_files, expected_file_contents):
            with open(file_path) as file:
                file_content = json.load(file)
            self.assertTrue(file_content, expected_content)

    def test_convert_post_histories(self):
        post_histories_html = [os.path.join(self.html_folder, "post_histories", "Matt_Cliffe.html")]
        self.converter._convert_post_histories(post_histories_html)
        
        # test filenames
        out_files = [os.path.join(self.json_folder, "post_histories", "Matt_Cliffe.json")]
        for file in out_files:
            self.assertTrue(Path(file).is_file())
            
        # test file content
        expected_file_content_1 = []
        post_1 = {}
        post_1['username'] = "Matt_Cliffe"
        post_1['topic'] = "Joining"
        post_1['topic_link'] = self.converter.website_url + "/t/joining-space/12505"
        post_1['category'] = "Admin"
        post_1['post_timestamp'] = "1550859165213"
        post_1['text'] = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
        expected_file_content_1.append(post_1)
        expected_file_contents = [expected_file_content_1]

        for file_path, expected_content in zip(out_files, expected_file_contents):
            with open(file_path) as file:
                file_content = json.load(file)
            
            file_last_post = file_content[len(file_content)-1]

            # go through the dict and check every value
            for expected_key, expected_value in expected_content[0].items():
                self.assertEqual(file_last_post[expected_key], expected_value)

    def test_overwriting(self):
        
        file_path = os.path.join(self.temp_folder, "overwrite_test.json")
        # write a json file
        self.converter._write_data_to_json_file(file_path, {'text': "not overwritten"}, overwrite=False)
        # write again to same file, no overwriting
        self.converter._write_data_to_json_file(file_path, {'text': "overwritten"}, overwrite=False)
        # load file contents
        json_file = open(file_path, 'rb')
        file_content = json.load(json_file)
        self.assertEqual(file_content['text'] , "not overwritten")
        json_file.close()

        # write again to same file, overwriting
        self.converter._write_data_to_json_file(file_path, {'text': "overwritten"}, overwrite=True)
        # load file contents
        json_file = open(file_path, 'rb')
        file_content = json.load(json_file)
        self.assertEqual(file_content['text'] , "overwritten")
        json_file.close()

    def tearDown(self):
        # remove contents of download folder
        shutil.rmtree(self.temp_folder)


if __name__ == '__main__':
    unittest.main()