"""
Provides functions for downloading posts and other data
"""
#? the functions here will be made after the main api is done
#* this whole module is honestly quite shit, im gonna rewrite it at some point. this actually hurts looking at :skull_emoguy:

import httpx
import os
import logging
import json
from . import objects as ob
from . import exceptions
from .logging import main_log


class Downloader:
    def __init__(self, download_path=None, metadata_path=None, keep_metadata=False, make_folders=True, check_for_updated_posts=False):
        self.download_log = main_log.getChild('downloader')
        self.init_path = os.getcwd()
        self.keep_metadata = keep_metadata
        self.check_for_updated_posts = check_for_updated_posts
        
        if download_path == None:
            self.download_path = self.init_path
        else:
            if not os.path.isdir(download_path):
                self.download_log.error("Invalid path")
                raise exceptions.InvalidPath(download_path)
            self.download_path = download_path
            
        if metadata_path == None:
            self.metadata_path = self.init_path
        else:
            if not os.path.isdir(metadata_path):
                self.download_log.error("Invalid path")
                raise exceptions.InvalidPath(metadata_path)
            self.metadata_path = metadata_path
        
        if make_folders == None:
            self.post_download_path = self.download_path
            self.pool_download_path = self.download_path
        else:
            self.create_download_dirs()

    def __save_post_metadata(self, post):
        
        self.download_log.debug(f"Saving metadata for post {post.m_id}")
        previous_dir = os.getcwd()
        os.chdir(self.metadata_path)
        
        with open(str(post.m_id) + "-metadata.json", 'w') as file:
            json.dump(post.post_obj_to_dict(), file, indent=1)
        os.chdir(previous_dir)
        
    def __save_pool_post_metadata(self, post, pool_metadata_folder):
        
        self.download_log.debug(f"Saving metadata for post {post.m_id}")
        previous_dir = os.getcwd()
        os.chdir(pool_metadata_folder)
        
        with open(str(post.m_id) + "-metadata.json", 'w') as file:
            json.dump(post.post_obj_to_dict(), file, indent=1)
        os.chdir(previous_dir)
        
    def __save_pool_metadata(self, pool):
        
        self.download_log.debug(f"Saving metadata for pool {pool.m_id}")
        
        with open(str(pool.m_name) + "-metadata.json", 'w') as file:
            json.dump(pool.pool_obj_to_dict(), file, indent=1)

    def __single_post_download(self, post, skip_downloaded_check=False):
            
        self.download_log.info(f"Downloading post: {post.m_id}")
        
        if os.path.isfile(post.filename) and not skip_downloaded_check:
            self.download_log.info(f"Post {post.m_id} already saved")
            return False, "already saved"

        try:
            with httpx.stream("GET", post.m_data['url']) as download:
                with open(post.filename, 'wb') as file:
                    
                    for chunk in download.iter_bytes():
                        file.write(chunk)
                        
        except httpx.InvalidURL:
            self.download_log.warning(f"Post {post.m_id} has no valid url")
            return False, "invalid url"
        
        return True, ""
    
    def __single_pool_download(self, pool, skip_downloaded_check=False, save_old_posts=False):
    
        self.download_log.info(f"Downloading pool: {pool.m_id}")
        
        if os.path.isdir(pool.folder_name) and not skip_downloaded_check:
            self.download_log.info(f"Pool {pool.m_id} already saved")
            return False
        
        previous_dir = os.getcwd()
        os.mkdir(pool.folder_name)
        os.chdir(pool.folder_name)
        pool_folder = os.getcwd()
        
        if self.keep_metadata:
            pool_metadata_folder = "Post metadata"
            os.mkdir(pool_metadata_folder)
        
        pool.get_posts()
        for post in pool.posts:
            result = self.__single_post_download(post)
            if not result[0] and result[1] != "invalid url":
                if not self.check_for_updated_posts:
                    continue
                self.post_updater(post, save_old_posts, posts_folder=pool_folder)
                
            elif result[1] == "invalid url":
                continue
                
            post.is_downloaded = True
            if self.keep_metadata:
                self.__save_pool_post_metadata(post, "Post metadata")
        
        os.chdir(previous_dir)
        return True
    
    def create_download_dirs(self):
        try:
            self.download_log.debug("Making download path")
            os.mkdir(self.download_path)
        except FileExistsError:
            self.download_log.debug("Download path already exists")

        try:
            self.download_log.debug("Making post download path")
            os.mkdir(os.path.join(self.download_path, "Posts"))
        except FileExistsError:
            self.download_log.debug("Posts download path already exists")
        self.post_download_path = os.path.join(self.download_path, "Posts")
        
        try:
            self.download_log.debug("Making pool download path")
            os.mkdir(os.path.join(self.download_path, "Pools"))
        except FileExistsError:
            self.download_log.debug("Pools download path already exists")
        self.pool_download_path = os.path.join(self.download_path, "Pools")

        if self.metadata_path == self.init_path:
            try:
                self.download_log.debug("Making metadata path")
                os.mkdir(os.path.join(self.download_path, "Metadata"))
            except FileExistsError:
                self.download_log.debug("Metadata path already exists")
            self.metadata_path = os.path.join(self.download_path, "Metadata")
                
    def post_updater(self, post, save_old=False, posts_folder=None):
        
        self.download_log.info(f"Updating post {post.m_id}")
        
        posts_check_folder = self.post_download_path
        if posts_folder != None:
            if not os.path.isdir(posts_folder):
                self.download_log.error("Invalid path")
                raise exceptions.InvalidPath(posts_folder)
            posts_check_folder = posts_folder
        
        previous_dir = os.getcwd()
        os.chdir(self.metadata_path)
        metadata_filename = str(post.m_id) + "-metadata.json"
        
        if not os.path.isfile(metadata_filename):
            self.download_log.warning(f"No metadata file found for {post.m_id}")
            raise exceptions.NoMetadata
        with open (metadata_filename, "r") as metadata_file:
            decoded_metadata = json.load(metadata_file)
        decoded_post = ob.PostObject()
        decoded_post.set_post_data(decoded_metadata, True)
        
        if decoded_metadata.m_change_seq == post.m_change_seq:
            return False
        
        if save_old:
            with open ("old-" + metadata_filename, "w") as file:
                old_post = ob.PostObject()
                old_post.set_post_data(decoded_metadata, True)
                old_post.filename = "old-" + decoded_post.filename
                json.dump(old_post.post_obj_to_dict(), file, indent=1)
            
            os.chdir(posts_check_folder)
            os.rename(decoded_post.filename, "old-" + decoded_post.filename)
        
        os.chdir(posts_check_folder)
        self.__single_post_download(post, True)
        self.__save_post_metadata(post)
        os.chdir(previous_dir)
        return True
    
    def post_download(self, posts, save_old_posts=False):
            
        previous_dir = os.getcwd()
        os.chdir(self.post_download_path)
        
        for post in posts:
            result = self.__single_post_download(post)
            
            if not result:
                if not self.check_for_updated_posts:
                    continue
                self.post_updater(post, save_old_posts)
                
            post.is_downloaded = True
            if self.keep_metadata:
                self.__save_post_metadata(post)
            os.chdir(previous_dir)
    
    def pool_download(self, pools, save_old_posts=False):
        
        previous_dir = os.getcwd()
        os.chdir(self.pool_download_path)
        
        for pool in pools:
            self.__single_pool_download(pool, save_old_posts=save_old_posts)
            pool.is_downloaded = True
            
            if self.keep_metadata:
                self.__save_pool_metadata(pool)
        os.chdir(previous_dir)
