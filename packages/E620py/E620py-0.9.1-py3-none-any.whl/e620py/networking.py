"""
Handles the actual requests being made and checking the responses for errors
"""

import httpx
import json
from . import objects as ob
from . import __user_agent__, base_url, exceptions
from .logging import main_log


class ConnectionHandler:
    """
    Handles connecting to e621 and verifying if a request was actually successful or not and handling authentication
    """
    #? i may want to merge most of the networking functions into one as most of it is the same with slight modifications

    def __init__(self, url=base_url):

        self.connection_handler_log = main_log.getChild("Connection_Handler")

        self.url = url
        self.user_agent = {'user-agent': __user_agent__}
        try:
            httpx.get(url=self.url, headers=self.user_agent)
        except httpx.ConnectError as error:
            self.connection_handler_log.error(
                "Something went wrong while connecting to url, check your internet and try again"
            )
            raise exceptions.NetworkError(
                "Something went wrong while connecting to url", error
            )

        self.auth = False
        self.session = httpx.Client()
        self.session.headers.update(self.user_agent)

    def update_auth(self, username, api_key) -> bool:
        """
        The update_auth function updates the session with a new username and api key.
            It does this by making a request to the favorites endpoint, which requires authentication.
            If the request is successful, it updates the session with the new auth.

        :param username: Used to Set the username for the session.
        :param api_key: Used to Authenticate the user.
        :return: True if auth is valid, otherwise False
        """

        request = httpx.get(
            url=f"{self.url}/favorites.json",
            headers=self.user_agent,
            auth=(username, api_key),
        )

        if request.status_code == 401:
            self.connection_handler_log.error(
                "Auth not valid, check username and api_key"
            )
            return False

        self.session.auth = (username, api_key)
        self.auth = True
        self.connection_handler_log.info(f"Auth valid, now logged in as {username}")
        return True

    def raise_network_error(self, request, error, request_type):

        self.connection_handler_log.critical(
            f"{request_type} request failed. Http status code: {request.status_code}"
        )
        self.connection_handler_log.debug(f"Request text: {request.text}")
        raise exceptions.NetworkError(error, request)

    def get_request(self, url_endpoint, options) -> dict:
        """
        The get_request function is used to make a GET request to the API.
            It takes in two parameters:
                url_endpoint - The endpoint of the URL that you want to access. For example, if you wanted
                to fetch posts, your url_endpoint would be "/posts.json".

                options - A dictionary containing any query parameters that you want to include in your request.

            This function returns a dict object containing all of the data returned by the API.
        """

        try:
            request = self.session.get(url=self.url + url_endpoint, params=options)
            request.raise_for_status()

        except httpx.HTTPError as error:
            self.raise_network_error(request, error, "Get")

        return json.loads(request.text)

    def post_request(self, url_endpoint, data=None, files=None):

        try:
            if files != None:
                request = self.session.post(url=self.url + url_endpoint, files=files, data=data)
            else:
                request = self.session.post(url=self.url + url_endpoint, data=data)
            request.raise_for_status()

        except httpx.HTTPError as error:
            self.raise_network_error(request, error, "Post")

        return json.loads(request.text)

    def delete_request(self, url_endpoint):
        # * this function does not come with an options parameter, but if need be i can add one later

        try:
            request = self.session.delete(url=self.url + url_endpoint)
            request.raise_for_status()

        except httpx.HTTPError as error:
            self.raise_network_error(request, error, "Delete")

        try:
            return json.loads(request.text)

        except json.JSONDecodeError:
            self.connection_handler_log.critical("Non json content")
            raise exceptions.InvalidServerResponse("Non json content", request)

    def patch_request(self, url_endpoint, options):

        try:
            request = self.session.patch(url=self.url + url_endpoint, params=options)
            request.raise_for_status()

        except httpx.HTTPError() as error:
            self.raise_network_error(request, error, "Patch")

        try:
            return json.loads(request.text)

        except json.JSONDecodeError:
            self.connection_handler_log.critical("Non json content")
            raise exceptions.InvalidServerResponse("Non json content", request)
        
    def put_request(self, url_endpoint, options):

        try:
            request = self.session.put(url=self.url + url_endpoint, params=options)
            request.raise_for_status()

        except httpx.HTTPError() as error:
            self.raise_network_error(request, error, "Put")

        try:
            return json.loads(request.text)

        except json.JSONDecodeError:
            self.connection_handler_log.debug("Non json content")
            raise exceptions.InvalidServerResponse("Non json content", request)
