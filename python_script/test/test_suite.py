import unittest
from python_script.test.test_discourse_downloader import TestDiscourseDownloader
from python_script.test.test_discourse_converter import TestDiscourseConverter
from python_script.test.test_discourse_data_loader import TestDiscourseDataLoader


def all_tests_suite():
    suite = unittest.TestSuite()
    suite.addTest(TestDiscourseDownloader('test_get_html_from_url'))
    suite.addTest(TestDiscourseDownloader('test_download_user_list'))
    suite.addTest(TestDiscourseDownloader('test_download_user_data'))


    suite.addTest(TestDiscourseConverter('test_converter'))
    suite.addTest(TestDiscourseDataLoader('test_widget_resize'))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(all_tests_suite())