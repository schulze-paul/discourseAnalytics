# discourseAnalytics


[Installation](#installation) | [How it works](#how-it-works) | [Initialization](#initialization) | [Filter](#filter) | [Search](#search) | [Sort](#sort) | [Print](#print) | [Activity Plot](#activity-plot)

Data analytics toolbox and data crawler in Python for Discourse.

The discourseAnalytics API makes it easy to *sort*, *filter* and *search* through posts and *display* or *plot* the data. 

## How it works

[selenium](https://selenium-python.readthedocs.io/installation.html) downloads the user data and public posts as `html` files. [BeautifulSoup4]() takes the `html` files and converts the data into python objects. The data is cached as `json` files and converted into a custom dataset format that is accessible via the discourseAnalytics API.

## Installation

### 1. Download

Download the latest release [here](download.com)

### 2. Run the App locally

Navigate to the downloaded `discourseAnalytics` folder and install the needed dependencies with 
```
pip install --upgrade --user -r requirements.txt
```

Discourse Analytics works best in a [Jupyter notebok](https://jupyter.org/) environment, but also works from the command line.

## Initialization

Import `discourseAnalytics` and initialize the dataset    
```python
from DiscourseAnalytics import DiscourseDataset

dataset = DiscourseDataset("discourse.website.com")
```

<p align="center">
<img  src="https://raw.githubusercontent.com/bl4ckp4nther4/discourseAnalytics/main/images/downloading_progress_bar.PNG" width="500">
</p>


discourseAnalytics downloads the user profiles and post histories into the folder `./datasets/Discourse/html_files`.
The downloaded files get scraped and packaged into one `json` file that contains all the available user information of every user.

Click on any of the headers to see more information: 

<details>
<summary><i>Download folder</i></summary>

 You can change the download folder to a custom folder with the argument `dataset_folder`.
```python
dataset = DiscourseDataset(discourse_website, dataset_folder='/home/user/Data/DiscourseDataset')
```
</details>

<details>
<summary><i>Download speed</i></summary>
 
  The download process can take some time. To speed things up, you can use the argument `sleep_time`. This changes the amount of seconds that `selenium` waits to load more content after scrolling to the bottom.  
```python
dataset = DiscourseDataset(discourse_website, sleep_time=1)
```
</details>

<details>
<summary><i>Redownload data</i></summary>

If the source files get corruped, the data can be redownloaded with the arguments `overwrite_html=True` and `overwrite_html=True`.  
```python
dataset = DiscourseDataset(discourse_website, overwrite_html=True, overwrite_json=True)  
```

</details>  

<details>
<summary><i>Detailed output</i></summary>

A more detailed output while downloading and scraping can be printed with the argument `supress_output=False`.  
```python
dataset = DiscourseDataset(discourse_website, supress_output=False)
```

</details>
  
## Filter

Calling the ```DiscourseDataset``` with a filter argument such as `username` returns a new instance of ```DiscourseDataset``` with the respective  subset of the posts.

```python
# all posts by user "JohnSmith"
posts_by_john = dataset(username="JohnSmith")

# all posts in topic "Hi I am John"
posts_in_hi = dataset(topic="Hi I am John")

# posts by user "JohnSmith" in the topic "Hi I am John"
posts_by_John_in_hi = dataset(username="JohnSmith", topic="Hi I am John")
```

Posts can be filtered by `username`, `full_name`, `topic` and `category`.  
And with time filter arguments such `post_before`, `post_after`, `join_before`, `join_after`, `last_post_before`, `last_post_after`, or a combination of the above


### Filter by Time 

The `DiscourseDataset` class can also filter posts according to different times. 
You can filter according to the post time, the join time and the last time a user posted something.

For this purpose, you need to hand over a `datetime` object in the call method of the `DiscourseDataset` class.

```python
# import datetime
import datetime.datetime as datetime

# create a datetime object
end_of_2007 = datetime.date(2007, 12, 31)

# pass datetime object and filter posts
posts_after_2007 = dataset(post_after=end_of_2007)
```


## Search

Posts can be searched with a keyword by calling `.search(keyword)`. All posts that contain the keyword in their `text`, `topic`, `category` or `username` are returned.

## Sort

## Print

Pretty printing the dataset.

<p align="center">
<img  src="https://raw.githubusercontent.com/bl4ckp4nther4/discourseAnalytics/main/images/display_function.PNG" width="500">
</p>

Pretty print
```python
print(dataset)
```

Display posts with hyperlinks to topics and users
```python
dataset.display()
```

Write html file of posts with hyperlinks to topics and users
```python
filename = 'my_posts

dataset.write('my_posts')
```

## Activity Plot

A histogram of post times sorted by month can be plotted with `.plot()`. The histogram can be given a title with `.plot(title="Title of Plot")`
