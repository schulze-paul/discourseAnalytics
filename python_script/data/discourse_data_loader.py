import json
import os
from pathlib import Path
import sys
import io

class DiscourseDataLoader():
    """
    Discourse data loader class
    Loads the data from json files
    """
    profiles = []
    post_histories = []


    def __init__(self, dataset_folder=os.path.join("datasets","Discourse","json_files")):
        """
        Set up the data loader
        
        Input:
        :param dataset_folder: string, the location of the dataset
        """
        self.dataset_folder = dataset_folder


    def __call__(self, profiles_json_list=None, post_histories_json_list=None, overwrite=False) -> list:
        """
        Loads the data from json files into memory
        
        Input:
        :param profiles_json_list: list of strings, locations of the profile json files
        :param post_histories_json_list: list of strings, locations of the post history json files
        """


        # try to load data directy from the dataset.json file
        if profiles_json_list is None and post_histories_json_list is None:
            # get data directly from the dataset file
            filename = os.path.join(self.dataset_folder, "dataset.json")
            if Path(filename).is_file():
                with open(filename) as datasetFile:
                    posts = json.load(datasetFile)
                    datasetFile.close()
                    return posts

        # overwrite protection
        if overwrite:
            confirm = self.query_yes_no("Confirm overwriting dataset json")
            if confirm:
                overwrite = True
            if not confirm:
                overwrite = False
        
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

        # write all profile data into each post datapoint for that username
        posts = self._combine_profiles_and_post_histories(self.profiles, self.post_histories)

        self._write_data_to_json_file(os.path.join(self.dataset_folder, "dataset.json"), posts, overwrite=overwrite)

        return posts


    def _combine_profiles_and_post_histories(self, profiles: list, post_histories: list) -> list:
        # set all the information about the poster/profile in each dict of each post of that poster / profile
        
        assert len(profiles) == len(post_histories)
        all_posts = []
        for profile, post_history in zip(profiles, post_histories):
            
            # check if post history is empty
            if len(post_history) == 0:
                profile.update({'empty': True})
                all_posts.append(profile)
            if len(post_history) > 0:
                profile.update({'empty': False})

            
            for post in post_history:
                assert(post['username'] == profile['username'])
                post.update(profile)
                all_posts.append(post)

        return all_posts

    # ====================================================================================== #
    # JSON HANDLER:                                                                          #
    # ====================================================================================== #

    @staticmethod
    def _write_data_to_json_file(filename: str, data, overwrite: bool):
        """
        Writes a json file to disk.

        Input:
        :param filename: string, path to file
        :param data: list, dict, ... , data that should be written to disk
        :param overwrite: boolean, should the file be overwritten if it already exists
        """
        # convert data to json
        json_string = json.dumps(data)

        if Path(filename).is_file() and not overwrite:
            # html file already exists, dont overwrite
            pass
        elif not Path(filename).is_file():
            # write to file
            open(filename, 'x') # create file
            with io.open(filename, 'w') as outfile:
                outfile.write(json_string)
                outfile.close()            
        elif Path(filename).is_file() and overwrite:
            # html file should be overwritten
            with io.open(filename, 'w') as outfile:
                outfile.write(json_string)
                outfile.close()


    # ====================================================================================== #
    # USER INTERFACE:                                                                        #
    # ====================================================================================== #

    @staticmethod
    def query_yes_no(question: str, default="no"):
        """Ask a yes/no question via raw_input() and return their answer.

        "question" is a string that is presented to the user.
        "default" is the presumed answer if the user just hits <Enter>.
                It must be "yes" (the default), "no" or None (meaning
                an answer is required of the user).

        The "answer" return value is True for "yes" or False for "no".
        """
        valid = {"yes": True, "y": True, "ye": True, "no": False, "n": False}
        if default is None:
            prompt = " [y/n] "
        elif default == "yes":
            prompt = " [Y/n] "
        elif default == "no":
            prompt = " [y/N] "
        else:
            raise ValueError("invalid default answer: '%s'" % default)

        while True:
            sys.stdout.write(question + prompt)
            choice = input().lower()
            if default is not None and choice == "":
                return valid[default]
            elif choice in valid:
                return valid[choice]
            else:
                sys.stdout.write("Please respond with 'yes' or 'no' " "(or 'y' or 'n').\n")