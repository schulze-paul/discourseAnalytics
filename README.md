# repository_forum


Web scaping tool to collect data from a discourse forum.
The tool automatically downloads all user profiles and posts with `selenium`.
The downloaded `html` files are then analysed using `beautifulsoup 4`.
The extracted information is saved as `json` file and then loaded as `dataset` object.

The `dataset` object contains all posts and can be filtered and  printed as a table.
