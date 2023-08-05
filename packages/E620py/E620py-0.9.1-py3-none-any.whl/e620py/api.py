"""
Contains classes and methods that directly interact with the e621 api (post fetching, up-voting, etc)
"""

from . import objects as ob
from . import exceptions, file_handling
from .logging import main_log
from .networking import ConnectionHandler

default_session = ConnectionHandler()


class E6Get:
    def __init__(self, session=default_session):
        # ? this class is finished for now, but i may add some extra functions later on

        self.e6get_log = main_log.getChild("E6Get")
        self.session = session

    def __single_page_post_get(
        self, tags, fetch_count=320, override_get_options=None, override_endpoint=None
    ) -> list: 
        """
        Retrieves a list of posts from the e621 API that match the given tags, with an optional limit of `fetch_count`. 

        Args:
            - tags (str): The tags to use in the search query.
            - fetch_count (int): The number of posts to retrieve, with a maximum limit of 320. Default is 320.
            - override_get_options (dict): Optional dictionary of additional GET parameters to replace the default in the API request.
            - override_endpoint (str): Optional endpoint to override the default "/posts.json" endpoint.

        Returns:
            A list of PostObject instances representing the retrieved posts.

        Raises:
            - NoResults: If there are no posts that match the given search query.
        """

        if fetch_count > 320:
            fetch_count = 320
            self.e6get_log.warning("Fetch count over limit, reduced to 320")

        # * i do this to allow for reusing the normal post get methods with favorites_fetch as its pretty much the same
        endpoint = "/posts.json"
        if override_endpoint != None:
            endpoint = override_endpoint

        if override_get_options != None:
            self.e6get_log.debug(
                f"get options overridden. options: {override_get_options}"
            )
            request = self.session.get_request(endpoint, override_get_options)['posts']
        else:
            request = self.session.get_request(
                endpoint, {'tags': tags, 'limit': fetch_count}
            )['posts']

        if len(request) < 1:
            raise exceptions.NoResults(
                "Nobody here but us chickens!", f"Search terms: {tags}"
            )

        posts = []
        for post in request:
            post_object = ob.PostObject()
            post_object.set_post_data(post)
            posts.append(post_object)
        return posts

    def __looped_post_get(
        self,
        tags,
        fetch_all,
        fetch_count=420,
        override_get_options=None,
        override_endpoint=None,
    ) -> list:
        """
        Retrieves a list of posts from the e621 API that match the given tags, with the option to fetch all posts or a specified number of posts.

        Args:
            - tags (str): The tags to use in the search query.
            - fetch_all (bool): If True, fetches all posts that match the given search query. If False, fetches `fetch_count` posts at most.
            - fetch_count (int): The number of posts to retrieve. Default is 420.
            - override_get_options (dict): Optional dictionary of additional GET parameters to replace the default in the API request.
            - override_endpoint (str): Optional endpoint to override the default "/posts.json" endpoint.

        Returns:
            A list of PostObject instances representing the retrieved posts.

        Raises:
            - NoResults: If there are no posts that match the given search query.
        """

        def get_last_post_id(list_of_posts) -> int:
            return list_of_posts[len(list_of_posts) - 1].m_id

        def fetch_loop_limited(initial_fetch) -> list:

            post_list = initial_fetch

            while len(post_list) < fetch_count:
                current_last_post_id = get_last_post_id(post_list)
                get_options = {
                    'tags': tags,
                    'limit': page_size,
                    'page': f"b{current_last_post_id}",
                }
                if override_get_options != None:
                    get_options = override_get_options

                try:
                    loop_post_list = self.__single_page_post_get(
                        tags, page_size, get_options, override_endpoint
                    )
                except exceptions.NoResults:
                    self.e6get_log.warning(f"Failed to fetch all {fetch_count} posts")
                    break

                for post in loop_post_list:
                    if len(post_list) >= fetch_count:
                        break

                    post_list.append(post)

            self.e6get_log.info(f"Loop done! Fetched {len(post_list)} posts")
            return post_list

        def fetch_loop_all(initial_fetch):

            post_list = initial_fetch

            while True:
                current_last_post_id = get_last_post_id(post_list)
                get_options = {
                    'tags': tags,
                    'limit': page_size,
                    'page': f"b{current_last_post_id}",
                }
                if override_get_options != None:
                    get_options = override_get_options

                try:
                    loop_post_list = self.__single_page_post_get(
                        tags, page_size, get_options, override_endpoint
                    )
                except exceptions.NoResults:
                    self.e6get_log.info(f"Loop done! Fetched {len(post_list)} posts")
                    return post_list

                for post in loop_post_list:
                    post_list.append(post)

        page_size = 320
        request = self.__single_page_post_get(
            tags, page_size, override_get_options, override_endpoint
        )
        initial_post_fetch = []

        for post in request:
            if len(initial_post_fetch) >= fetch_count and not fetch_all:
                self.e6get_log.info("Initial fetch was over fetch count")
                return initial_post_fetch

            initial_post_fetch.append(post)

        if not fetch_all:
            return fetch_loop_limited(initial_post_fetch)
        return fetch_loop_all(initial_post_fetch)

    def post_get(self, tags, fetch_all, fetch_count=320) -> list:
        """
        Retrieves a list of posts from the e621 API that match the given tags, with the option to fetch all posts or a specified number of posts.

        Args:
            - tags (str): The tags to use in the search query.
            - fetch_all (bool): If True, fetches all posts that match the given search query. If False, fetches `fetch_count` posts at most.
            - fetch_count (int): The number of posts to retrieve. Default is 320.

        Returns:
            A list of PostObject instances representing the retrieved posts.

        Raises:
            - NoResults: If there are no posts that match the given search query.
        """

        if fetch_count > 320 or fetch_all:
            self.e6get_log.debug("Using looped post get")
            return self.__looped_post_get(tags, fetch_all, fetch_count)
        return self.__single_page_post_get(tags, fetch_count)

    def favorites_get(self, username=None, fetch_all=True, fetch_count=320) -> list:
        """
        Retrieves favorite posts from the e621 API for a given user or the currently authenticated user if the session is authenticated.
        
        Args:
            - username (str): The username of the user whose favorite posts should be retrieved.
                If not provided and the session is not authenticated, an AuthError will be raised.
            - fetch_all (bool): Indicates whether to fetch all favorite posts or just 'fetch_count' posts. Defaults to True.
            - fetch_count (int): The number of posts to retrieve. Default is 320.
        
        Returns:
            A list of PostObject instances representing the retrieved posts.
            
        Raises:
            - AuthError: If the session is not authenticated and username is not provided
            - NoResults: If there are no posts that match the given search query.
        """
        self.e6get_log.warning('favorites_get is deprecated, if you want to fetch favorites, use the regular post_get and append "fav:[user here]" to the tags arg')

        endpoint = "/favorites.json"
        tags = "order:id"
        get_options = {'limit': fetch_count}

        if username == None and self.session.auth == False:
            self.e6get_log.error("No username provided and not logged in")
            raise exceptions.AuthError("No username provided and not logged in")

        if username != None:
            get_options = {'limit': fetch_count, 'user_id': username}

        if fetch_all:
            fetch_count = 320

        if fetch_count > 320 or fetch_all:
            self.e6get_log.debug("Using looped post get")
            return self.__looped_post_get(
                tags, fetch_all, fetch_count, get_options, endpoint
            )
        return self.__single_page_post_get(tags, fetch_count, get_options, endpoint)

    def pool_get(
        self,
        search,
        search_type='name_matches',
        category=None,
        order='updated_at',
        is_active=None,
    ) -> list:
        """
        Retrieves a list of pool objects from the e621 API based on a given search query and filter parameters.
        
        Args:
            - search (str): The search query to use for finding pools
            - search_type (str): The type of search query to use, has multiple options. Defaults to 'name_matches'
                options: 'name_matches' 'id' 'description_matches' 'creator_name' 'creator_id'
            - category (str): The category to filter pools by. Has two options, 'series' and 'category', keeping the option on None searches both (i think?). Defaults to None
            - order (str): The order that pools should be returned, has multiple options. Defaults to 'updated_at'
            - is_active (bool): Filter results by whether the pool is active or not. Defaults to None.
            
        Returns:
            A list of pool objects representing the retrieved posts. 
            
        Raises:
            - NoResults: If there are no posts that match the given search query.
        
        """
        # ? i may include a looped variant for getting more then a page of pools at some point
        
        get_options = {
            f"search[{search_type}]": search,
            'search[category]': category,
            'search[order]': order,
        }
        
        if is_active != None:
            get_options = {**get_options, 'search[is_active]': str(is_active).lower()}

        request = self.session.get_request("/pools.json", get_options)

        if len(request) < 1:
            raise exceptions.NoResults(
                "Nobody here but us chickens!", f"Search terms: {search}"
            )

        pools = []
        for pool in request:
            pool_object = ob.PoolObject()
            pool_object.set_pool_data(pool)
            pools.append(pool_object)
        return pools


class E6Post:
    def __init__(self, logged_in_session):

        self.e6post_log = main_log.getChild("E6Post")
        self.session = logged_in_session

    def vote_post(self, post_id, score) -> dict:
        """
        Upvotes, downvotes, or clears the vote of a post with the given 'post_id'.

        Args:
            - post_id (int): The ID of the post to vote on.
            - score (int): The score to assign to the post. Possible values are 1 (upvote),
                -1 (downvote), and repeating the same vote will clear it.

        Returns:
            A dictionary containing the details of the vote, including the post ID and the
            score assigned to it.
        """

        url_endpoint = f"/posts/{post_id}/votes.json"

        request = self.session.post_request(url_endpoint, {'score': int(score)})

        if request['our_score'] == 1:
            self.e6post_log.info(f"Up voted post {post_id}")

        elif request['our_score'] == -1:
            self.e6post_log.info(f"Down voted post {post_id}")

        elif request['our_score'] == 0:
            self.e6post_log.info(f"Cleared vote of post {post_id}")

        return request

    def favorite_post(self, post_id) -> bool:
        """
        Sends a request to favorite the specified post.
        
        Args:
            - post_id (int): The ID of the post to be favorited.
            
        Returns:
            - True if the request is successful.
            - False if the post is already favorited.
            
        Raises:
            - NetworkError: If there is a unknown network error.
        """
        
        try:
            self.session.post_request("/favorites.json", {'post_id': int(post_id)})

        except exceptions.NetworkError as error:
            error_request = error.args[1]

            if error_request.status_code == 422:
                self.e6post_log.warning(f"Post {post_id} already favorited")
                return False
            raise error

        self.e6post_log.info(f"Post {post_id} favorited")
        return True

    def unfavorite_post(self, post_id):
        """
        Sends a request to remove the specified post from the user's favorites list.
        
        Args:
            - post_id (int): The ID of the post to remove from favorites.
            
        Returns:
            - None
        
        Raises:
            - NetworkError: If there is a unknown network error.
        """
        
        # ? i may need to implement some extra check to make sure that a post actually got unfavorited

        self.session.delete_request(f"/favorites/{post_id}.json")
        self.e6post_log.info(f"Post {post_id} unfavorited")

    def upload_post(
        self,
        tags,
        rating,
        source,
        description=None,
        file=None,
        direct_url=None,
        parent_id=None,
    ):
        """
        Uploads a post to e621.

        Args:
            - tags (str): The tags to apply to the post.
            - rating (str): The rating of the post.
            - source (str): The source of the post. Can be an empty string
            - description (str, optional): A description of the post. Defaults to None.
            - file (file, optional): A file object to upload. Defaults to None.
            - direct_url (str, optional): A direct URL to the file to upload. Defaults to None.
            - parent_id (int, optional): The ID of the post's parent post. Defaults to None.

        Returns:
            - dict: A dictionary containing the response from the API.
        """

        post_data = {
            'upload[tag_string]': tags,
            'upload[rating]': rating,
            'upload[source]': source,
            'upload[description]': description,
            'upload[parent_id]': parent_id,
        }

        if file != None:
            post_file = {'upload[file]': file}

        elif direct_url != None:
            post_data = {**post_data, 'upload[direct_url]': direct_url}

        else:
            self.e6post_log.error("Uploading post failed, no file given or direct url")
            return

        request = self.session.post_request("/uploads.json", data=post_data, files=post_file)

        self.e6post_log.info(f"Post uploaded successfully! Id: {request['post_id']}")
        return request

    def edit_post(
        self,
        post_id,
        tag_string_diff=None,
        source_diff=None,
        parent_id=None,
        description=None,
        rating=None,
        edit_reason=None,
    ) -> dict:
        """
        Edit a post with the given 'post_id'.

        Args:
            - post_id (int): The ID of the post to edit.
            - tag_string_diff (str): A string containing the changes to the post's tags. The string should
                be formatted as a diff, where tags to be added are written normally and tags
                to be removed are prefixed with a `-` character, e.g. "new_tag -old_tag".
            - source_diff (str): A string containing the changes to the post's source URL.
                Formatted the same as the tag_string_diff arg.
            - parent_id (int): The ID of the post that this post should be a child of, if any.
            - description (str): The new description for the post.
            - rating (str): The new rating for the post. Valid values are "s", "q", and "e".
            - edit_reason (str): A description of the reason for the edit.

        Returns:
            dict: A dictionary containing information about the edited post. The dictionary has the
            same layout as a post returned by the post_get method in E6Get
        """

        self.e6post_log.info(f"Editing post {post_id}")
        url_endpoint = f"/posts/{post_id}.json"
        options = {
            'post[tag_string_diff]': tag_string_diff,
            'post[source_diff]': source_diff,
            'post[parent_id]': parent_id,
            'post[description]': description,
            'post[rating]': rating,
            'post[edit_reason]': edit_reason,
        }

        return self.session.patch_request(url_endpoint, options)

    def create_pool(self, name, description, category=None, post_ids=None):
        """
        Creates a new pool.
        
        Args:
            - name (str): The name of the new pool.
            - description (str): A description of the new pool.
            - category (str): The category of the new pool.
            - post_ids (str): A space separated list of post IDs to add to the new pool.
            
        Returns:
            A dictionary containing the details of the created pool.
        """

        options = {
            'pool[name]': name,
            'pool[description]': description,
            'pool[category]': category,
            'pool[post_ids_string]': post_ids,
        }

        return self.session.post_request("/pools.json", options)

    def edit_pool(
        self,
        pool_id,
        name=None,
        description=None,
        category=None,
        post_ids=None,
        is_active=None,
    ):
        """
        Updates an existing pool on e621 with the specified 'pool_id'.

        Args:
            pool_id (int): The ID of the pool to update.
            name (str, optional): The new name for the pool.
            description (str, optional): The new description for the pool.
            category (str, optional): The new category for the pool.
            post_ids (str, optional): The new space separated list of post IDs to include in the pool.
            is_active (bool, optional): Whether the pool should be active or not.

        Returns:
            - dict or bool: If successful, returns a dictionary with information about the edited pool.
                Otherwise, returns False. If an error occurs, a log entry will be created.
        """

        endpoint = f"/pools/{pool_id}.json"
        options = {
            'pool[name]': name,
            'pool[description]': description,
            'pool[category]': category,
            'pool[post_ids]': post_ids,
            'pool[is_active]': is_active,
        }

        try:
            request = self.session.put_request(endpoint, options)

        except exceptions.InvalidServerResponse as error:
            error_request = error.args[1]

            if error_request.status_code == 204:
                self.e6post_log.info(f"Pool {pool_id} updated")
                return request

            self.e6post_log.warning("An error occurred while updating a pool")
            self.e6post_log.debug(f"request status code: {error_request.status_code}")
            return False
