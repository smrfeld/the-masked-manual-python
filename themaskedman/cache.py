import os
from pathlib import Path
import shutil
from distutils.dir_util import copy_tree

class Cache:

    def __init__(self):

        self.cache_dir = "cache"
        self.cache_bkup_dir = "cache_bkup"
        Path(self.cache_dir).mkdir(parents=True, exist_ok=True)

    def get_cache_fname_fda(self) -> str:
        return self.cache_dir + "/cache_fda.txt"

    def get_cache_fname_cdc(self, letter : str) -> str:
        return self.cache_dir + "/cache_cdc_%s.txt" % letter

    def get_cache_fname_open_fda(self) -> str:
        return self.cache_dir + "/cache_open_fda.txt"

    def remove_bkup_cache_if_exists(self):

        # Check exists
        isdir = os.path.isdir(self.cache_bkup_dir)
        if not isdir:
            return  
        
        # Delete
        shutil.rmtree(self.cache_bkup_dir)

        print("Removed backup cache dir: %s" % self.cache_bkup_dir)

    def move_cache_to_bkup_if_exists(self):
        print("Backing up cache in case this fails....")

        # Check exists
        isdir = os.path.isdir(self.cache_dir)
        if not isdir:
            print("No directory: %s to cache!" % self.cache_dir)
            return  
        
        # Remove backup cache if exists
        self.remove_bkup_cache_if_exists()

        # Copy
        Path(self.cache_bkup_dir).mkdir(parents=True, exist_ok=True)
        copy_tree(self.cache_dir, self.cache_bkup_dir)
        print("Copied cache: %s to backup: %s" % (self.cache_dir, self.cache_bkup_dir))

        # Recreate empty cache dir
        Path(self.cache_dir).mkdir(parents=True, exist_ok=True)

    def move_bkup_cache_back(self):
        print("Moving backup cache back...")

        # Check backup exists
        isdir = os.path.isdir(self.cache_bkup_dir)
        if not isdir:
            raise ValueError("Backup cache: %s does not exist!" % self.cache_bkup_dir)

        # Remove cache dir if exists
        isdir = os.path.isdir(self.cache_dir)
        if isdir:
            shutil.rmtree(self.cache_dir)  
        
        # Copy
        Path(self.cache_dir).mkdir(parents=True, exist_ok=True)
        copy_tree(self.cache_bkup_dir, self.cache_dir)

        print("Copied to cache dir: %s from backup: %s" % (self.cache_dir, self.cache_bkup_dir))
