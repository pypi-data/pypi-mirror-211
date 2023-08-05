"""
Contains objects and types commonly used in e620py modules
"""

from . import api

class PostObject:
    def __init__(self):
        # metadata vars, most strings are None when first initialized since the values when fetched can be null if there was no data attached
        self.m_id = int()
        self.m_created_at = str()
        self.m_updated_at = str()
        self.m_data = {
            'width': int(),
            'height': int(),
            'ext': str(),
            'size': int(),
            'md5': str(),
            'url': None,
        }
        self.m_preview_data = {
            'width': int(),
            'height': int(),
            'url': None,
        }
        self.m_thumbnail_data = {
            'has': bool(),
            'width': int(),
            'height': int(),
            'url': None,
        }
        self.m_fav_count = int()
        self.m_score = {
            'up': int(),
            'down': int(),
            'total': int(),
        }
        self.m_tags = {
            'general': [],
            'species': [],
            'character': [],
            'copyright': [],
            'artist': [],
            'invalid': [],
            'lore': [],
            'meta': [],
        }
        self.m_locked_tags = []
        self.m_change_seq = int()
        self.m_flags = {
            'pending': bool(),
            'flagged': bool(),
            'note_locked': bool(),
            'status_locked': bool(),
            'rating_locked': bool(),
            'deleted': bool(),
        }
        self.m_rating = str()
        self.m_sources = []
        self.m_pools = []
        # parent id is None when initialized as it can be either "null" or an int
        self.m_relationships = {
            'parent_id': None,
            'has_children': bool(),
            'has_active_children': bool(),
            'children': []
        }
        self.m_approver_id = None
        self.m_uploader_id = int()
        self.m_description = None
        self.m_comment_count = int()
        self.m_favorited = bool()
        # only video posts have a duration, so until a video post's data is assigned, it remains as None
        self.m_duration = None
        
        # non metadata vars
        self.is_blacklisted = bool()
        self.no_data_url = bool()
        self.data_url_replaced = False
        self.is_downloaded = False
        self.filename = None
        
    def set_post_data(self, dict_post, serialized_post_obj=False):
        """
        The set_post function takes a dictionary of post data and sets the values of the Post object to those values.
        The function is used when creating a new Post object from an existing post, or when updating an existing Post object with new data.
        
        :param dict_post: Used to Set the values of the post object.
        :return: Nothing, but it does set the values of all the metadata variables in a post object.
        """
        
        #? i may change the way i store some of the values in the future
        self.m_id = dict_post['id']
        self.m_created_at = dict_post['created_at']
        self.m_updated_at = dict_post['updated_at']
        
        self.m_data = dict_post['file']
        self.m_preview_data = dict_post['preview']
        self.m_thumbnail_data = dict_post['sample']
        
        self.m_fav_count = dict_post['fav_count']
        
        self.m_score = dict_post['score']
        self.m_tags = dict_post['tags']
        
        self.m_locked_tags = dict_post['locked_tags']
        self.m_change_seq = dict_post['change_seq']
        
        self.m_flags = dict_post['flags']
        
        self.m_rating = dict_post['rating']
        self.m_sources = dict_post['sources']
        self.m_pools = dict_post['pools']
        
        self.m_relationships = dict_post['relationships']
        
        self.m_approver_id = dict_post['approver_id']
        self.m_uploader_id = dict_post['uploader_id']
        self.m_description = dict_post['description']
        self.m_comment_count = dict_post['comment_count']
        self.m_favorited = dict_post['is_favorited']
        self.m_duration = dict_post['duration']
        
        self.check_data_url()
        
        if serialized_post_obj:
            self.is_blacklisted = dict_post['is_blacklisted']
            self.no_data_url = dict_post['no_data_url']
            self.data_url_replaced = dict_post['data_url_replaced']
            self.is_downloaded = dict_post['is_downloaded']
            self.filename = dict_post['filename']
            return
        
        self.filename = f"{str(self.m_id)}.{self.m_data['ext']}"
        
    def post_obj_to_dict(self) -> dict:
        """
        Returns this post instance as a dictionary.
        """
        
        return {'id': self.m_id,
                'created_at': self.m_created_at,
                'updated_at': self.m_updated_at,
                'file': self.m_data,
                'preview': self.m_preview_data,
                'sample': self.m_thumbnail_data,
                'fav_count': self.m_fav_count,
                'score': self.m_score,
                'tags': self.m_tags,
                'locked_tags': self.m_locked_tags,
                'change_seq': self.m_change_seq,
                'flags': self.m_flags,
                'rating': self.m_rating,
                'sources': self.m_sources,
                'pools': self.m_pools,
                'relationships': self.m_relationships,
                'approver_id': self.m_approver_id,
                'uploader_id': self.m_uploader_id,
                'description': self.m_description,
                'comment_count': self.m_comment_count,
                'is_favorited': self.m_favorited,
                'duration': self.m_duration,
                
                'is_blacklisted': self.is_blacklisted,
                'no_data_url': self.no_data_url,
                'data_url_replaced': self.data_url_replaced,
                'is_downloaded': self.is_downloaded,
                'filename': self.filename,
                }

    def check_data_url(self):
        """
        The check_data_url function checks to see if the data url is a string. If it is not, then it checks to see if the preview data url is a string.
        If that is also not true, then no_data_url becomes True and returns nothing. Otherwise, the data url 
        becomes equal to the preview url, and data_url_replaced becomes True.
        
        :return: Nothing.
        """
        
        if type(self.m_data['url']) != str:
            if type(self.m_preview_data['url']) != str:
                self.no_data_url = True
                return
            
            self.m_data['url'] = self.m_preview_data['url']
            self.data_url_replaced = True
        else:
            return


class PoolObject:
    def __init__(self):
        # metadata vars
        self.m_id = int()
        self.m_name = str()
        self.m_created_at = str()
        self.m_updated_at = str()
        self.m_creator_id = int()
        self.m_creator_name = str()
        self.m_description = None
        self.m_is_active = bool()
        self.m_category = None
        self.m_post_count = int()
        self.m_post_ids = []
        
        self.is_downloaded = False
        self.folder_name = None
        self.posts = []
        
    def set_pool_data(self, list_pool, serialized_pool_obj=False):
        
        self.m_id = list_pool['id']
        self.m_name = list_pool['name']
        self.m_created_at = list_pool['created_at']
        self.m_updated_at = list_pool['updated_at']
        self.m_creator_id = list_pool['creator_id']
        self.m_creator_name = list_pool['creator_name']
        self.m_description = list_pool['description']
        self.m_is_active = list_pool['is_active']
        self.m_category = list_pool['category']
        self.m_post_count = list_pool['post_count']
        self.m_post_ids = list_pool['post_ids']
        
        if serialized_pool_obj:
            self.is_downloaded = list_pool['is_downloaded']
            self.folder_name = list_pool['folder_name']
            
            posts = list_pool['posts']
            obj_posts = []
            
            for post in posts:
                post_obj = PostObject().set_post_data(post, True)
                obj_posts.append(post_obj)
            self.posts = obj_posts
            return
        
        self.folder_name = self.m_name
        
    def get_posts(self):
        """
        Gets all posts in the pool and adds them to the "posts" parameter
        """
        
        self.posts = api.E6Get().post_get(f"pool:{self.m_id}", True)
        
    def pool_obj_to_dict(self) -> dict:
        """
        Returns this pool instance as a dictionary.
        """
        posts = self.posts
        dict_posts = []
        for post in posts:
            post_dict = post.post_obj_to_dict()
            dict_posts.append(post_dict)
        
        return {
            'id': self.m_id,
            'name': self.m_name,
            'created_at': self.m_created_at,
            'updated_at': self.m_updated_at,
            'creator_id': self.m_creator_id,
            'creator_name': self.m_creator_name,
            'description': self.m_description,
            'is_active': self.m_is_active,
            'category': self.m_category,
            'post_count': self.m_post_count,
            'post_ids': self.m_post_ids,
            'is_downloaded': self.is_downloaded,
            'folder_name': self.folder_name,
            'posts': dict_posts,
        }
