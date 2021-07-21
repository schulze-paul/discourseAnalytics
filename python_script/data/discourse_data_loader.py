import json

class DiscourseDataLoader():
    """
    
    """
    profiles = []
    post_histories = []


    def __init__(self):
        pass


    def __call__(self, profiles_json_list, post_histories_json_list):
        # loads the data from json files into memory

        def timestamps_to_integer(dict):
            # data at these key need to be converted to integer
            timestamp_keys = ['post_timestamp', 'join_timestamp', 'last_post_timestamp']

            # changing string to int
            updated_dict = {}
            for timestamp_key in timestamp_keys:
                if timestamp_key in dict:
                    updated_dict[timestamp_key] = int(dict[timestamp_key])
            dict.update(updated_dict)


            return dict
        
        # sorting both lists
        post_histories_json_list = sorted(post_histories_json_list)
        profiles_json_list = sorted(profiles_json_list)

        for profile_path in profiles_json_list:
            with open(profile_path) as jsonFile:
                profile = json.load(jsonFile)
                jsonFile.close()

                profile = timestamps_to_integer(profile)
            
            self.profiles.append(profile)


        for post_history_path in post_histories_json_list:
            with open(post_history_path) as jsonFile:
                post_history = json.load(jsonFile)
                jsonFile.close()

            
            # changing string to int
            new_post_history = []
            for post in post_history:
                post = timestamps_to_integer(post)
                new_post_history.append(post)

            self.post_histories.append(new_post_history)


        posts = self._combine_profiles_and_post_histories( self.profiles, self.post_histories)

        return posts



    def _combine_profiles_and_post_histories(self, profiles, post_histories):
        # set all the information about the poster/profile in each dict of each post of that poster / profile
        
        assert len(profiles) == len(post_histories)
        all_posts = []
        for profile, post_history in zip(profiles, post_histories):
            for post in post_history:
                print(post['username'] + " " + profile['username'])
                assert(post['username'] == profile['username'])
                post.update(profile)
                all_posts.append(post)
            if 'empty' in profile and len(post_history) == 0:
                all_posts.append(profile)


        return all_posts
