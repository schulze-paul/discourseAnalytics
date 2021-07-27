from python_script.data.discourse_dataset import DiscourseDataset

import unittest
import datetime


class TestDiscourseDataset(unittest.TestCase):

    def setUp(self):
        
        def set_up_posts():
            post_1 = {'username': "John_Doe", 
                      'full_name': "John Doe", 
                      'join_timestamp': 1577836800000, 
                      'last_post_timestamp': 1609459200000, 
                      'member_status': "Member", 
                      'topic': "Big Topic", 
                      'topic_link': "link.com/1", 
                      'post_timestamp': 1609459200000,
                      'text': "admin 123",
                      'category': "Admin"
                      }
            post_2 = {'username': "John_Smith", 
                      'full_name': "John Smith", 
                      'join_timestamp': 1577836800000, 
                      'last_post_timestamp': 1609459200000, 
                      'member_status': "Not Member", 
                      'topic': "Big Games", 
                      'topic_link': "link.com/2", 
                      'post_timestamp': 1609459200000,
                      'text': "game 123",
                      'category': "Games"
                      }
            post_3 = {'username': "John_Doe", 
                      'full_name': "John Doe", 
                      'join_timestamp': 1577836800000, 
                      'last_post_timestamp': 1609459200000, 
                      'member_status': "Member", 
                      'topic': "Big Games", 
                      'topic_link': "link.com/3", 
                      'post_timestamp': 1577836800000,
                      'text': "game 1",
                      'category': "Games"
                      }

            return [post_1, post_2, post_3]

        self.posts = set_up_posts()
        self.dataset = DiscourseDataset(self.posts)


    def test_print_table(self):
        print("")
        print(self.dataset)
    
    def test_call(self):
        print("")
        self.dataset(topic='Big Games')