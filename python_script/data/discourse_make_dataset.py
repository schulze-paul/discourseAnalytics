from data.discourse_downloader import DiscourseDownloader
from data.discourse_converter import DiscourseConverter
from data.discourse_data_loader import DiscourseDataLoader
from data.discourse_dataset import DiscourseDataset

class MakeDataset():

    def __init__(self, 
                 website_url,
                 dataset_folder="datasets\Discourse",
                 supress_output=True,
                 overwrite_html=False,
                 overwrite_json=False,
                 sleep_time=1,
                 ):

        self.downloader = DiscourseDownloader(website_url, dataset_folder=dataset_folder + "\html_files")
        _, profiles_html, post_histories_html = self.downloader(sleep_time=sleep_time, overwrite=overwrite_html, supress_output = supress_output)
        self.converter = DiscourseConverter(website_url, dataset_folder=dataset_folder +"\json_files")
        profiles_json, post_histories_json = self.converter(profiles_html, post_histories_html, overwrite=overwrite_json, supress_output=supress_output)
        self.dataLoader = DiscourseDataLoader()
        profiles, post_histories = self.dataLoader(profiles_json, post_histories_json)
        all_posts = self._combine_profiles_and_post_histories(profiles, post_histories)
        dataset = DiscourseDataset(all_posts)

        return dataset

    def _combine_profiles_and_post_histories(self, profiles, post_histories):
        # set all the information about the poster/profile in each dict of each post of that poster / profile
        
        assert len(profiles) == len(post_histories)
        all_posts = []
        for profile, post_history in zip(profiles, post_histories):
            for post in post_history:
                assert(post['username'] == post_history['username'])
                post.update(profile)
                all_posts.append(post)

        return all_posts


        