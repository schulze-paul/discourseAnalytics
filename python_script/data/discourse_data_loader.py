import json

class DiscourseDataLoader():
    """
    
    """
    profiles = []
    post_histories = []


    def __init__(self):
        pass


    def __call__(self, profiles_json_list, post_histories_json_list):
        
        for profile_path in profiles_json_list:
            with open(profile_path) as jsonFile:
                profile = json.load(jsonFile)
                jsonFile.close()

            self.profiles.append(profile)

        for post_history_path in post_histories_json_list:
            with open(post_history_path) as jsonFile:
                post_history = json.load(jsonFile)
                jsonFile.close()

            self.post_histories.append(post_history)

        return self.profiles, self.post_histories