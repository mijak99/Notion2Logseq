
# Summary

This project converts Notion pages to Logseq journal format to enable migrating from Notion to Logseq.

- Converts Notion pages to Logseq journal format
- Enables migrating from Notion to Logseq

# Requirements

- Will probably need long paths enabled on Windows
  https://www.autodesk.com/support/technical/article/caas/sfdcarticles/sfdcarticles/The-Windows-10-default-path-length-limitation-MAX-PATH-is-256-characters.html

## Features

- Removes the notion IDs from filenames
- Maintains the links between markdown pages, replacing notion-formatted links with logseq-formatted links
- Warns for links that are not maintained
- Maintains image links
- Maintains asset links
- Converts notion tasks to logseq todos, maintaining state
- Converts notion blocks to logseq blocks. Blocks currently supported
  - aside
- Page properties from Notion DB entries
- Creates a page containing a summary, called Notion Export <date and time>


## How to use

- Export from notion. To keep assets and filenames unique, use subdirectories for pages when exporting
- Run `python main.py path/to/your/notion-export.zip`
- Then copy/move the 'pages' and 'assets' folders into your logseq graph root folder

# Disclaimer
- Use at your own risk. I am not responsible for any damages to your data.

