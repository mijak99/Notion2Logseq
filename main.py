# Extracts markdown and non-markdown files from a zip file into separate directories.
# The markdown files are extracted into the './pages' directory, while non-markdown 
# files are extracted into the './assets' directory.

import sys
import os
import re
import zipfile
import argparse
import json

from FileDictionary import *
from NotionUtils import *
from Logger import *


class ZipfileLongPaths(zipfile.ZipFile):

    def winapi_path(dos_path, encoding=None):
        path = os.path.abspath(dos_path)
        if path.startswith("\\\\"):
            path = "\\\\?\\UNC\\" + path[2:]
        else:
            path = "\\\\?\\" + path 
        return path 

    def _extract_member(self, member, targetpath, pwd):
        targetpath = winapi_path(targetpath)
        return zipfile.ZipFile._extract_member(self, member, targetpath, pwd)


parser = argparse.ArgumentParser()
parser.add_argument('-d', '--destination_dir', default='./output2logseq', help='destination directory for extracted files')
parser.add_argument('-f', '--force', action='store_true', help='force overwrite of output directory')
parser.add_argument('zip_file_path', help='path to zip file')
args = parser.parse_args()

zip_file_path = args.zip_file_path
zip_file_basename = os.path.split(zip_file_path)[1]
(zip_name, _) = os.path.splitext(zip_file_basename)



# Check if destination directory exists
if os.path.exists(args.destination_dir):
    if (args.force):
        if (args.destination_dir != '.' or '..' in args.destination_dir): # don't delete current directory, or parent directory
            print(f'Forced overwriting of directory {args.destination_dir}')
            os.system(f'rm -rf {args.destination_dir}')
        else:
            print(f'Forced overwriting of current directory not allowed. Aborting.')
            sys.exit(1)
    else: 
        print(f'Destination directory {args.destination_dir} already exists. Use --force to overwrite.')
        sys.exit(1)
else:
    os.makedirs(args.destination_dir)


print(f'Extracting {zip_name} to {args.destination_dir}')
fileDictionary = FileDictionary(zip_name, args.destination_dir)


def fixpath(path):
    unicode = path.encode('unicode_escape').decode() # Step 1: Unicode
    file_path = os.path.abspath(os.path.normpath(unicode)) #Step 3 and 4: no forward slashes and absolute path
    return file_path


# Extract all files from the zip file
with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
    files = zip_ref.namelist()

    for file in files:
        fileInfo = fileDictionary.add_file(file)
        print("extracting file", file)

        try:

            # make some caveats for long paths on windows with the abspath
            zip_ref.extract(file, fixpath(fileInfo['dest_path']))
            #zip_ref.extract(file, os.path.abspath(fileInfo['dest_path']))
            # Rename file by removing trailing notion identifiers
            newName = f"{fileInfo['dest_path']}/{fileInfo['filename']}"
            rename_file_and_create_dirs(f"{fileInfo['dest_path']}/{file}", newName)
            # os.rename(f"{fileInfo['dest_path']}/{file}", newName)  
        except FileNotFoundError as e:
            print(f"\n An Error occured. Probably due to too long paths for windows: {file}, {newName}")
            print(f"Try running on WSL")

            exit(1)
        except OSError as e:
            # print(f"Error renaming {file}: {e}")
            log('Renaming error', f'{file}: {e}')
            pass

print("Doing post processing")

# Replace links to markdown files with links to html files
for file in files:
    fileInfo = fileDictionary.get_fileinfo(file)
    if file.endswith('.md'):
        log('1. Processed pages', f'[[{fileInfo["pagename"]}]]')
        markdown_file = f"{fileInfo['dest_path']}/{fileDictionary.get_filename(file)}"
        with open(markdown_file, 'r', encoding='utf-8') as f:
            content = f.read()
            f.close()

        (content, tag_count) = replace_notion_tags(content)
        links = get_all_markdown_links(content)
        # print(f'\n\nListing links in {fileInfo["pagename"]}: ', links)
        
        (content, count) = replace_notionlinks_with_logseqlinks(content, fileDictionary)
        (content, todo_count) = replace_notion_todos(content)
        (content, block_count) = replace_notion_blocks(content)
        content = fix_logseq_blocks(content)

        # print(f'New content: ', content)
        with open(markdown_file, 'w', encoding='utf-8') as f:
            f.write(content)
            f.close()

        # print(f'Wrote {count} links, {todo_count} todos, and {block_count} blocks to {fileInfo["pagename"]}\n\n')



    # Post processing
    # - Check for csv files in the root, and set tags and/or page properties per file

# print('\n\nFiles', json.dumps(fileDictionary.file_dict, indent=4))
# print('\n\nFiles', fileDictionary.keys())
# print('Pages', list(fileDictionary.get_pages()))

print(f'Done. Extracted files are in {args.destination_dir}')

now = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

with open(f'{args.destination_dir}/pages/NotionExport-{now}.md', 'w', encoding='utf-8') as f:
    print(f"# Notion Export done at {now}", file=f)
    print(f"notion2logseq:: {now}", file=f)
    print_report(file=f)
    f.close()

print_report(file=sys.stdout)