
import re
from Logger import *
from urllib import parse



# find all notion tags at the beginning of the file content, and replace them with logseq tags
# Expect the first line to be starting with a header. Logseq don't use headers, so let's remove it and store it as a property
import unittest

def replace_notion_tags(content):
    lines = content.split('\n')
    count = 0

    if len(lines) > 1 and lines[1] == '':
        del lines[1] 

    if lines[0].startswith('# '):
        replacement = f"notion-heading:: {lines[0][2:]}"
        lines[0] = replacement
        count += 1

    def removespaces(matchobj):
        tag = matchobj.group(1).replace(' ', '-')
        value = matchobj.group(2)
        return f'{tag}::{value}'

    # now replace tags
    line = 1
    while line < len(lines) and (':' in lines[line]):
        tagpattern = r'^([\w\s]+[^\:]+):(.*)$'
        replacement = re.sub(tagpattern, removespaces, lines[line])
        lines[line] = replacement
        count += 1
        line += 1


    return ('\n'.join(lines), count)




# Extract all markdown links from the file
# returns a list of tuples (original_link, text, href)
def get_all_markdown_links(content):
  links = []
  
  pattern = r'!?\[([^\]\[]*?)\]\((.+?)\)' # find links in the file
  for match in re.finditer(pattern, content):
    href = parse.unquote(match.group(2))
    # print(f'Found link {href}')
    text = match.group(1)
    text = href if text == '' else text
    links.append((match.group(0), text, href))
  
  return links


# Replace links in the file with links to the extracted files
# returns the new content and the number of links replaced
def replace_notionlinks_with_logseqlinks(content, fileDictionary):

    links = get_all_markdown_links(content)
    count = 0
    for (original_link, text, href) in links:
        fileInfo = fileDictionary.find_file(href)
        if fileInfo is not None:
            if fileInfo['ext'] == '.md':
                fileInfo = fileDictionary.find_file(href)
                if fileInfo is not None:
                    # replace markdown links of existing pages to logseq format
                    content = content.replace(original_link, f"[[{fileInfo['pagename']}]]")
                    # print (f"Replaced {original_link} with [[{fileInfo['pagename']}]]")
                    count += 1

                else:
                    print(f"Skipping not-found link {href}")
            elif fileInfo['isAsset']:
                # replace markdown links of existing pages to logseq format

                # for attachements, logseq weirdly takes '../assets/subfolders/asset.png' to link to 'assets'
                # regardles of where the original file is located. Makes it easier for us
                destination = f"../assets/{fileDictionary.basename}/{fileInfo['filename']}"
                replacement = f"{'!' if original_link.startswith('!') else ''}[{text}]({destination})"

                content = content.replace(original_link, replacement)
                # print (f"Replaced {original_link} with {replacement}")

                count += 1
            else:
                print(f"Skipping non-md link {href}")
        elif href.startswith('https://www.notion.so/'):
            log('2. Detected links to unexported Notion files', f'{href}')
            #print(f"** WARNING ** Found link to unexported notion page {href}")
        

    return (content, count)
    


def replace_notion_todos(content):
    # Replace notion todo with logseq todo
    (content, count) = re.subn(r' \[ \] ', f" TODO ", content)
    (content, count2) = re.subn(r' \[x\] ', f" DONE ", content, flags=re.IGNORECASE)

    return (content, count+count2)

def replace_notion_blocks(content):
    (content, count) = re.subn(r'^\<aside\>', f"#+BEGIN_TIP", content, flags=re.IGNORECASE | re.MULTILINE)
    (content, count2) = re.subn(r'^\<\/aside\>', f"#+END_TIP", content, flags=re.IGNORECASE | re.MULTILINE)

    return (content, count+count2)

def fix_logseq_blocks(content):
    # logseq uses bullets to indicate new paragraphs where notion uses double \n
    # but ignore pages with block quotes
    if ('```' not in content): 
        content = re.sub(r'\n\n(\w)', r'\n\n- \1', content)
    return content