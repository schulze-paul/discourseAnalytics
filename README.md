# discourseAnalytics

Data analytics and suite for discourse.

## Installation

### Download

Download the latest release [here](download.com)

### Run the App locally

Navigate to the downloaded `discourseAnalytics` folder and install the needed dependencies with 
```
pip install --upgrade --user -r requirements.txt
```

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

  
### Download speed

The download process can take some time. To speed things up you can use the argument `sleep_time`, which changes the amount of seconds that `selenium` waits to load more content after scrolling to the bottom.  
```python
dataset = DiscourseDataset(discourse_website, sleep_time=1)
```

### Redownload Data 

If the source files get corruped, the data can be redownloaded with the arguments `overwrite_html=True` and `overwrite_html=True`.  
```python
dataset = DiscourseDataset(discourse_website, overwrite_html=True, overwrite_json=True)  
```

### Print Detailed Output

A more detailed output while downloading and scraping can be printed with the argument `supress_output=False`.  
```python
dataset = DiscourseDataset(discourse_website, supress_output=False)
```

## Analytics Toolbox


### Filtering Posts

Calling the ```DiscourseDataset``` with a filter argument such as `username` returns a new instance of ```DiscourseDataset``` with the respective  subset of the posts.


Posts ca be filtered by `username`, `full_name`, `topic` and `category`.

For example calling `dataset(username="JohnDoe")` returns an instance with all the posts from the user with the username `JohnDoe`, or `dataset(topic="Hi I am Joe")` returns an instance with all the posts from the topic `Hi I am Joe`. These can be combined, so that `dataset(username="JohnDoe", topic="Hi I am Joe")` returns all posts by the user `JohnDoe` under the topic `Hi I am Joe`.

#### Filtering by Time 

The `DiscourseDataset` class can also filter posts according to different times. 
You can filter according to the post time with `post_before` and `post_after`, according to the join time of the user with `join_before` and `join_after` and according to the last time a user posted with `last_post_before` and `last_post_after`.

For this purpose, you need to hand over a `datetime` object in the call method of the `DiscourseDataset` class.

```python
# import datetime
import datetime.datetime as datetime

# create a datetime object
end_of_2007 = datetime.date(2007, 12, 31)


# pass datetime object and filter posts
posts_after_2007 = dataset(post_after=end_of_2007)
```

#### Example

```python
>>> dataset.display()
Hi, I am Joe | JoeSmith | 2019-04-29 10:44:26  
Hello, this is me, I am Joe

Hi, I am Joe | john_doe | 2019-04-29 10:34:07  
Hi Joe, nice to meet you

Hi, I am Joe | JoeSmith | 2019-04-27 12:19:41  
Thank you nice to meet you too

>>> posts_by_JoeSmith = dataset(username="JoeSmith")
>>> posts_by_JoeSmith.display()
Hi, I am Joe | JoeSmith | 2019-04-29 10:44:26  
Hello, this is me, I am Joe

Hi, I am Joe | JoeSmith | 2019-04-27 12:19:41  
Thank you nice to meet you too
```

#### Filtering by username, full name, topic, category

The `DiscourseDataset` class can filter posts according to the username, the full name, the topic and the category. 

For example calling `dataset(username="JohnDoe")` returns an instance with all the posts from the user with the username `JohnDoe`, or `dataset(topic="Hi I am Joe")` returns an instance with all the posts from the topic `Hi I am Joe`.


#### Filtering by time


```python
# create a datetime object
end_of_2007 = datetime.date(2007, 12, 31)
# pass datetime object and filter posts
posts_after_2007 = dataset(post_after=end_of_2007)
```

#### Searching for posts

Posts can be searched with a keyword by calling `.search("keyword")`. All posts that contain the "keyword" are returned

### Output

#### Writing / Displaying list of posts

A list of the posts can be displayed with `.display()` or written to an `html` file with `.write(filename)`. 
The posts are sorted by post time.
The `html` file can be overwritten with `.write(filename, overwrite=True)`

<p align="center">
<img  src="https://raw.githubusercontent.com/bl4ckp4nther4/discourseAnalytics/main/images/display_function.PNG" width="500">
</p>


#### Plotting a histogram of post times

A histogram of post times sorted by month can be plotted with `.plot()`. The histogram can be given a title with `.plot(title="Title of Plot")`
