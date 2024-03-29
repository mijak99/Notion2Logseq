
# Summary

This project converts Notion pages to Logseq journal format to enable migrating from Notion to Logseq.

- Converts Notion pages to Logseq journal format
- Enables migrating from Notion to Logseq

# Requirements

- If your notion zip contains long filenames, you may need to use long paths enabled on Windows.
  - This is a windows limitation. 
  - To fix (at your own risk, if you don't know what you are doing) :
    - Start Regedit 
    - In HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\FileSystem...
    - Select the entry named: LongPathsEnabled    (DWORD (32-bit) if you have to create it)
    - Set the value to 1
    - Restart windows, or (if you are lucky) just the relevant processes


## How to use

- Export from notion. To keep assets and filenames unique, use subdirectories for pages when exporting
- Run `python main.py path/to/your/notion-export.zip`
  - This will create a `output2logseq` folder where files will be extracted and processed.
- Then copy/move the 'pages' and 'assets' folders into your logseq graph root folder

```
usage: main.py [-h] [-d DESTINATION_DIR] [-f] zip_file_path

positional arguments:
  zip_file_path         path to zip file

options:
  -h, --help            show this help message and exit
  -d DESTINATION_DIR, --destination_dir DESTINATION_DIR
                        destination directory for extracted files
  -f, --force           force overwrite of output directory
  
```


## Features

- Removes the notion IDs from filenames, and makes paths shorter
- Maintains the links between markdown pages, replacing notion-formatted links with logseq-formatted links
  - This ususally works well, but notion allows weird things to happen, so it's not 100% reliable.
- Maintains image links
- Maintains asset links
- Converts notion tasks to logseq todos, maintaining state
- Converts notion blocks to logseq blocks. Blocks currently supported
  - aside
- Page properties from Notion DB entries
- Also creates a page containing a summary, called **Notion Export <YYYYMMDD HHMMSS>**
  - Includes warning for links to notion pages that where not included in the export


# Do you like it? 
- https://www.patreon.com/mijak/shop/show-your-appreciation-100543

# Disclaimer
- Use at your own risk. I am not responsible for any damages to your data.

# Development notes


## To test
- python -m unittest discover

