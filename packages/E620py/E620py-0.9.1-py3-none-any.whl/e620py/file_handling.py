"""
Util functions for handling files and other local data
"""
#? i may need a module like this later on so im making the file now just in case

import os
import json
import hashlib
from . import exceptions as exceptions
from . import objects as ob
from .logging import main_log


def calculate_md5(file):
    #* this is supposed to be used as a helper function for upload_post, 
    #* but as uploading direct files are not working, this is not needed
    
    md5 = hashlib.md5()
    
    for byte_chunk in iter(lambda: file.read(4096), b""):
        md5.update(byte_chunk)
    return md5.hexdigest()
