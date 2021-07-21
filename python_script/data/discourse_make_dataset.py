from python_script.data.discourse_downloader import DiscourseDownloader
from python_script.data.discourse_converter import DiscourseConverter
from python_script.data.discourse_data_loader import DiscourseDataLoader
from python_script.data.discourse_dataset import DiscourseDataset
import os

class MakeDataset():

    def __init__(self):
        pass

    def __call__(self, 
                 website_url,
                 dataset_folder=os.path.join("datasets","Discourse"),
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
        all_posts = self.dataLoader(profiles_json, post_histories_json)
        
        dataset = DiscourseDataset(all_posts)

        return dataset

    

        