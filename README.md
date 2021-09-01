# DiscourseAnalytics

Data Analytics Suite for Discourse Forum data


## Functionality

### Initilization

The Dataset is initialized with the URL to a discourse forum, for example: `dataset = DiscourseDataset('twittercommunity.com')`.
DiscourseAnalytics downloads all profile data as html files with `selenium` and pulls the data with `beautifulsoup 4`.
The resulting DiscourseDataset Object contains all accessible information about posts and profiles.

### Filtering Posts

Calling the resulting DiscourseDataset class object instance returns a new instance of DiscourseDataset with a subset of the posts.

#### Filtering by username, full name, topic, category

The dataset class can filter posts with  
For example calling `dataset(username="JohnDoe")` returns an instance with all the posts from the user with the username `JohnDoe`, or `dataset(topic="Hi I am Joe")` returns an instance with all the posts from the topic `Hi I am Joe'.

#### Filtering by timeframe

