
import os
import re
import hashlib
import shutil
from Logger import *


def remove_notion_ids(filename, is_dir):
    # Cleans up Notion export zip file names by removing trailing 
    # random character strings added by Notion export
    pattern = r"(.+)\s([a-z0-9]{32})\.md$"  # only check md files for now
    match = re.match(pattern, filename)
    # print("filename is ", filename)
    if match is not None:
        if is_dir:
            new_name = match.group(1)
        else:
            new_name = match.group(1) + ".md"
    else:
        new_name = filename
    # print("new name is ", new_name)
    return new_name

def shorten_path(longpathname):
    # shorten a long filename to a unique name
    # by replacing the path before the filename with a hash of the path,  
    # while keeping the filename and the extension 
    # eg: path/subfolder/name.md -> 123456789012345678901234567/name.md
    # eg: path/subfolder/name2.md -> 123456789012345678901234567/name2.md

    path, filename = os.path.split(longpathname)
    hash_str = hashlib.md5(path.encode()).hexdigest()
    log('99. Hashes to the original paths', f'{hash_str}: {path}')
    return f"{hash_str}/{filename}"

def rename_file_and_create_dirs(old_path, new_path):
    new_dir = os.path.dirname(new_path)
    if not os.path.exists(new_dir):
        os.makedirs(new_dir)
    shutil.move(old_path, new_path)
    old_dir = os.path.dirname(old_path)
    if not os.listdir(old_dir):
        os.removedirs(old_dir)


class FileDictionary:
    
    def __init__(self, basename, dest_dir):
        self.file_dict = {}
        self.basename = basename
        self.dest_dir = dest_dir
        self.markdown_files = []
        self.pages = []


        
    def add_file(self, filename):
        if filename not in self.file_dict:
            # print(f'Adding filename {filename}')
            basename = os.path.split(filename)[1]
            (_, ext) = os.path.splitext(basename)
            isAsset = (ext != '.md')
            cleaned = remove_notion_ids(filename, False)

            pagename = os.path.splitext(os.path.split(cleaned)[1])[0]
            if isAsset:
                destpath = f'{self.dest_dir}/assets/{self.basename}'
            else:
                destpath = f'{self.dest_dir}/pages/{self.basename}'


            self.pages.append(pagename)
            
            self.file_dict[filename] = {
                'original_filename': filename, # the original filename, with the path
                'basename': basename, # the original filename, without the path
                'ext': ext, # extension
                'path': os.path.dirname(filename), # the original path in the zip
                'dest_path': destpath, # the destination dir in logseq repo
                'filename': shorten_path(cleaned), # the filename in the logseq repo without the notion identifiers and shorter
                'pagename': pagename,  # the name of the page in logseq
                'isAsset' : isAsset
            }
            if (cleaned in self.file_dict and self.file_dict[cleaned]!= self.file_dict[filename]):
                print(f'ERROR -- Cleaning caused Duplicate filename {filename}')
                print(f'Duplicate filename {self.file_dict[cleaned]}')
                print(f'Duplicate filename {self.file_dict[cleaned]}')
                raise Exception('Duplicate filename')
            
            if (filename.endswith('.md')):
                self.markdown_files.append(filename)

            # print(f'Entered filename {self.file_dict[filename]}')
        else:
            print(f'Duplicate filename {filename}')
            
        return self.file_dict[filename]

    def has_page(self, pagename):
        return pagename in self.pages

    def get_pages(self):
        return self.pages

    def find_file(self, filename):
        if filename in self.file_dict:
            return self.file_dict[filename]
        else:
            # search for filename in original basenames
            for file_info in self.file_dict.values():
                if file_info['basename'] == filename:
                    return file_info
                elif file_info['original_filename'].endswith(filename):
                    return file_info
            
        return None
        
            

    def keys(self) : 
        return self.file_dict.keys()
    
    def get_basename(self, filename):
        return self.file_dict[filename]['basename']
    
    def get_ext(self, filename):
        return self.file_dict[filename]['ext']
    
    def get_path(self, filename):
        return self.file_dict[filename]['path']
    
    def get_filename(self, filename):
        return self.file_dict[filename]['filename']
    
    def get_fileinfo(self, filename):
        return self.file_dict[filename]

    def get_pagename(self, filename):
        return self.file_dict[filename]['pagename']
        
