from datetime import date

class DiscourseDataset():

    def __init__(self, posts):
        self.posts = posts


    def __call__(self, 
               username=None,
               full_name=None,
               join_before=None,
               join_after=None,
               last_post_before=None,
               last_post_after=None,
               member_status=None,
               topic=None,
               topic_link=None,
               post_before=None,
               post_after=None,
               text=None,
               category = None
               ):
        """
        
        """
        
        def search_for(target_dict, list):
            """
            recursively searches for posts with the specified properties and returns new list
            """
            def timestamp_search(before_after, key, target_key, target_dict, list):
                # searches for timestamps before or after at the specified key
                if before_after == 'before':
                    new_list = [item for item in list if item[key] < target_dict[target_key]]
                    target_dict.pop([target_key])
                    return search_for(target_dict, new_list)
                if before_after == 'after':
                    new_list = [item for item in list if item[key] > target_dict[target_key]]
                    target_dict.pop([target_key])
                    return search_for(target_dict, new_list)


            if 'post_before' not in target_dict and 'post_after' not in target_dict and 'join_before' not in target_dict and 'join_afer' not in target_dict and 'last_post_before' not in target_dict and 'last_post_after' not in target_dict:
                # do normal dict search, recursion terminated
                 return [item for item in list if all((item[target_key] == target_value) for target_key, target_value in target_dict.items())] 

            else:
                # filters posts to before and after and then searches for the other properties
    
                if 'post_before' in target_dict:
                    timestamp_search('before', 'post_timestamp', 'post_before', target_dict, list)
                if 'post_after' in target_dict:
                    timestamp_search('after', 'post_timestamp', 'post_after', target_dict, list)

                if 'join_before' in target_dict:
                    timestamp_search('before', 'join_timestamp', 'join_before', target_dict, list)
                if 'join_after' in target_dict:
                    timestamp_search('after', 'join_timestamp', 'join_after', target_dict, list)
    
                if 'last_post_before' in target_dict:
                    timestamp_search('before', 'last_post_timestamp', 'last_post_before', target_dict, list)
                if 'join_after' in target_dict:
                    timestamp_search('after', 'last_post_timestamp', 'last_post_after', target_dict, list)

        arguments = [username, 
                     full_name, 
                     datetime.timestamp(join_before), 
                     datetime.timestamp(join_after), 
                     datetime.timestamp(last_post_before), 
                     datetime.timestamp(last_post_after), 
                     member_status, 
                     topic, 
                     topic_link, 
                     datetime.timestamp(post_before), 
                     datetime.timestamp(post_after),
                     text,
                     category]

        keys = ['username',
                'full_name', 
                'join_before', 
                'join_after', 
                'last_post_before', 
                'last_post_after', 
                'member_status', 
                'topic', 
                'topic_link', 
                'post_before', 
                'post_after',
                'text',
                'category']
            
        # build dict to search for 
        dict_to_search_for = {}
        for argument, key in arguments, keys:
            if argument is not None:
                dict_to_search_for[key] = argument

        # filter posts
        filtered_posts = search_for(dict_to_search_for, self.posts)

        # return dataset of filtered posts
        return DiscourseDataset(filtered_posts)

    def __iter__(self):
        return iter(self.posts)

    def __len__(self):
        return len(self.posts)

    def __getitem__(self, key):
        if isinstance(key, int):
            # if key is integer, return item from list
            return self.posts[key]

        else: 
            # return unique list with key property from the posts
            list(set([post[key] for post in self.posts if key in post]))

    def __str__(self):
        def _convert_timestamps_to_datetime(dict_list):
            new_dict_list = dict_list.copy()
            
            timestamp_keys = ['post_timestamp', 'join_timestamp', 'last_post_timestamp']
            datetime_keys = ['post_time', 'join_time', 'last_post_time']
            
            for post in dict_list:
                for timestamp_key, datetime_key in zip(timestamp_keys, datetime_keys):
                    post[datetime_key] = date.fromtimestamp(post[timestamp_key])
                    post.pop(datetime_key)

            return new_dict_list

        return str(_convert_timestamps_to_datetime(self.posts))
        
