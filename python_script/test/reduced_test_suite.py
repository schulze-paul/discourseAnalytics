import unittest
from python_script.test.test_discourse_downloader import TestDiscourseDownloader
from python_script.test.test_discourse_converter import TestDiscourseConverter
from python_script.test.test_discourse_data_loader import TestDiscourseDataLoader
from python_script.test.test_discourse_dataset import TestDiscourseDataset


def all_tests_suite():
    suite = unittest.TestSuite()
    
    # suite.addTest(TestDiscourseDownloader('test_get_html_from_url'))
    # suite.addTest(TestDiscourseDownloader('test_download_user_data'))
    # suite.addTest(TestDiscourseDownloader('test_overwriting'))
    suite.addTest(TestDiscourseDownloader('test_get_user_links'))
    suite.addTest(TestDiscourseDownloader('test_get_user_links'))

    # suite.addTest(TestDiscourseConverter('test_convert_user_profiles'))
    # suite.addTest(TestDiscourseConverter('test_convert_post_histories'))
    # suite.addTest(TestDiscourseConverter('test_overwriting'))
    suite.addTest(TestDiscourseConverter('test_get_username_from_profile_filepath'))
    suite.addTest(TestDiscourseConverter('test_get_username'))
    suite.addTest(TestDiscourseConverter('test_get_full_name'))
    suite.addTest(TestDiscourseConverter('test_get_member_status'))
    suite.addTest(TestDiscourseConverter('test_get_join_time'))
    suite.addTest(TestDiscourseConverter('test_get_last_post_time'))
    suite.addTest(TestDiscourseConverter('test_get_username_from_post_history_filepath'))
    suite.addTest(TestDiscourseConverter('test_get_post_topic'))
    suite.addTest(TestDiscourseConverter('test_get_post_topic_link'))
    suite.addTest(TestDiscourseConverter('test_get_post_category'))
    suite.addTest(TestDiscourseConverter('test_get_post_time'))
    suite.addTest(TestDiscourseConverter('test_get_post_text'))
    
    suite.addTest(TestDiscourseDataLoader('test_call'))
    
    suite.addTest(TestDiscourseDataset('test_call'))
    
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(all_tests_suite())