# DiscourseAnalytics

Data Analytics Suite for Discourse Forum data


## Functionality

### Initilization

The Dataset is initialized with the URL to a discourse forum, for example: `dataset = DiscourseDataset('twittercommunity.com')`.
DiscourseAnalytics downloads all profile data as html files with `selenium` and pulls the data with `beautifulsoup 4`.
The resulting DiscourseDataset Object contains all accessible information about posts and profiles.

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
