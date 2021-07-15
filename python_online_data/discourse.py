# imports
import importlib
importlib.import_module('website_base_data')
from website_base_data import WEBSITE_URL
from discourse_downloader import DiscourseDownloader
from discourse_converter import DiscourseConverter


# download
download = DiscourseDownloader(WEBSITE_URL)
_, profiles, post_histories = download()

# convert to json
converter = DiscourseConverter(WEBSITE_URL, profiles, post_histories)
converter()

# make dataset
