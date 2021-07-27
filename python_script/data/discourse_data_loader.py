import json

class DiscourseDataLoader():
    """
    Discourse data loader class
    Loads the data from json files
    """
    profiles = []
    post_histories = []


    def __init__(self):
        """
        Set up the downloader

        """

    def __call__(self, profiles_json_list, post_histories_json_list):
        """
        Loads the data from json files into memory
        
        Input:
        :param profiles_json_list: list of strings, locations of the profile json files
        :param post_histories_json_list: list of strings, locations of the post history json files
        """
        
        # sorting both lists
        post_histories_json_list = sorted(post_histories_json_list)
        profiles_json_list = sorted(profiles_json_list)
        
        # loading the profile files
        for profile_path in profiles_json_list:
            with open(profile_path) as jsonFile:
                profile = json.load(jsonFile)
                jsonFile.close()

            self.profiles.append(profile)

        # loading the post history files
        for post_history_path in post_histories_json_list:
            with open(post_history_path) as jsonFile:
                post_history = json.load(jsonFile)
                jsonFile.close()

            self.post_histories.append(post_history)


        posts = self._combine_profiles_and_post_histories( self.profiles, self.post_histories)

        return posts


    def _combine_profiles_and_post_histories(self, profiles, post_histories):
        # set all the information about the poster/profile in each dict of each post of that poster / profile
        
        assert len(profiles) == len(post_histories)
        all_posts = []
        for profile, post_history in zip(profiles, post_histories):
            for post in post_history:
                assert(post['username'] == profile['username'])
                post.update(profile)
                all_posts.append(post)
            if 'empty' in profile and len(post_history) == 0:
                all_posts.append(profile)


        return all_posts
