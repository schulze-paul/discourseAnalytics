from data.discourse_downloader import DiscourseDownloader
from data.discourse_converter import DiscourseConverter
from data.discourse_data_loader import DiscourseDataLoader


class MakeDataset():

    def __init__(self, 
                 website_url,
                 dataset_folder="datasets\Discourse", 
                 ):

        self.downloader = DiscourseDownloader(website_url, dataset_folder=dataset_folder + "\html_files")
        self.converter = DiscourseConverter(website_url, dataset_folder=dataset_folder +"\json_files")
        self.dataLoader = DiscourseDataLoader()

    def __call__(self,
                 supress_output=True,
                 overwrite_html=False,
                 overwrite_json=False,
                 sleep_time=1,
                 ):
        
        print("downloading html data...")
        _, profiles_html, post_histories_html = self.downloader(sleep_time=sleep_time, overwrite=overwrite_html, supress_output = supress_output)
        
        print("converting to json...")
        profiles_json, post_histories_json = self.converter(profiles_html, post_histories_html, overwrite=overwrite_json, supress_output=supress_output)

        print("loading data...")
        profiles, post_histories = self.dataLoader(profiles_json, post_histories_json)
    

    def _combine_profiles_and_post_histories(self, profiles, post_histories):
        # set all the information about the poster/profile in each dict of each post of that poster / profile
        pass
        