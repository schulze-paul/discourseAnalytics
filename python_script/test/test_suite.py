import unittest
from python_script.test.test_discourse_downloader import TestDiscourseDownloader
from python_script.test.test_discourse_converter import TestDiscourseConverter
from python_script.test.test_discourse_data_loader import TestDiscourseDataLoader
from python_script.test.test_discourse_dataset import TestDiscourseDataset


def all_tests_suite():
    suite = unittest.TestSuite()
    
    suite.addTest(TestDiscourseDownloader('test_get_html_from_url'))
    suite.addTest(TestDiscourseDownloader('test_download_user_list'))
    suite.addTest(TestDiscourseDownloader('test_download_user_data'))
    suite.addTest(TestDiscourseDownloader('test_overwriting'))

    suite.addTest(TestDiscourseConverter('test_convert_user_profiles'))
    suite.addTest(TestDiscourseConverter('test_convert_post_histories'))
    suite.addTest(TestDiscourseConverter('test_overwriting'))
    
    suite.addTest(TestDiscourseDataLoader('test_timestamps_to_integer'))
    suite.addTest(TestDiscourseDataLoader('test_call'))
    
    suite.addTest(TestDiscourseDataset('test_print_table'))
    suite.addTest(TestDiscourseDataset('test_call'))
    
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(all_tests_suite())