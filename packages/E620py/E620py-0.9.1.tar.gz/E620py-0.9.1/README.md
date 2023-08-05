# E620py

E620py is a python library for interacting with the e621 api.

Here is an example of fetching a single post:
```python
>>> import e620py
>>> post = e620py.E6get().post_get("order:score", fetch_all=False, fetch_count=1)
>>> print(post[0].m_id)
2848682
```
Most functions have doc strings so its easy to quickly see how a function works without having to understand the spaghetti code 💀.

## Features
  Post:
  + Fetching
  + Uploading
  + Editing
  + Voting
  + Favorite and unfavorite
  + Downloading

  Pool:
  + Fetching (only one page at a time for now)
  + Creating
  + Editing
  + Downloading

 Note:
 The download functions do not have doc strings yet
