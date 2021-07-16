import importlib
importlib.import_module('data.website_base_data')
from data.website_base_data import WEBSITE_URL
from data.discourse_make_dataset import MakeDataset

dataset = MakeDataset(WEBSITE_URL)
dataset()