# discourseAnalytics

Data Analytics Suite for Discourse Forum data

## Installation

### Download

Download the latest release here

### Run the App locally

Install the needed dependencies with 
```
pip install --upgrade --user -r requirements.txt
```

Navigate to the `discourseAnalytics` folder and import `discourseAnalytics` with  
```python
from DiscourseAnalytics import DiscourseDataset
```

## Initialization

Initialize the dataset with  
```python
# initialize dataset by downloading data
discourse_website = "website.com"  
dataset = DiscourseDataset(discourse_website)
```

discourseAnalytics downloads the user profiles and post histories.
The downloaded files get scraped and packaged into one `json` file that contains all the available user information of every user.

<img align="center" src="https://raw.githubusercontent.com/bl4ckp4nther4/discourseAnalytics/main/images/downloading_progress_bar.PNG" width="300">

### Download speed

This process can take some time. It can be sped up with the argument `sleep_time` by lowering the amount of time that `selenium` waits to load more content after scrolling to the bottom.  
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

## Analytics


### Filtering Posts

Calling the resulting `DiscourseDataset` class object instance returns a new instance of DiscourseDataset with a subset of the posts.

#### Filtering by username, full name, topic, category

The `DiscourseDataset` class can filter posts according to the username, the full name, the topic and the category. 

For example calling `dataset(username="JohnDoe")` returns an instance with all the posts from the user with the username `JohnDoe`, or `dataset(topic="Hi I am Joe")` returns an instance with all the posts from the topic `Hi I am Joe`.

These can be combined, so that `dataset(username="JohnDoe", topic="Hi I am Joe")` returns all posts by the user `JohnDoe` under the topic `Hi I am Joe`.

#### Filtering by time

The `DiscourseDataset` class can also filter posts according to the time of posts. 
For this purpose, we need to hand over a `datetime` object in the call method of the `DiscourseDataset` class.
We can filter according to the post time with `post_before` and `post_after`, according to the join time of the user with `join_before` and `join_after` and according to the last time a user posted with `last_post_before` and `last_post_after`.

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

> <a href=website.com/topic>Topic 1</a> | <a href=website.com/u/username>UserName</a>
> 
> This is a post text.
> 
> <a href=website.com/topic>Topic 2</a> | <a href=website.com/u/username>UserName</a>
> 
> This is another post text.

#### Plotting a histogram of post times

A histogram of post times sorted by month can be plotted with `.plot()`. The histogram can be given a title with `.plot(title="Title of Plot")`
