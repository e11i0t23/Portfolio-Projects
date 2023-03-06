import re

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from .models import Entry



def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    return list(e.title for e in Entry.objects.all())


def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    # We remove any attempt to add html code in markdown
    content = re.sub(r"<[\s\S]*?>([\s\S]*?)<\/[\s\S]*?>", r'\1', content)
    
    filename = f"entries/{title}.md"
    try: 
        e = Entry.objects.get(title=title)
        e.content = content
        e.save()
    except Entry.DoesNotExist: 
        e = Entry(title=title, content=content)
        e.save()


def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        e = Entry.objects.get(title=title)
        return e.content
    except Entry.DoesNotExist:
        return None

def markdown2html(entry):
    """
    Converts a markdown file into a renderable html section
    """
    html = get_entry(entry).expandtabs(4)


    # Unordered Lists basic implmentaions

    listarray = html.split('\n')
    lists=[]
    currrentIndent = 0
    list = str
    list = None
    startLine = 0 
    arraylen = len(listarray)
    for i in range(0, arraylen):
        line = listarray[i]
        print(line)
        if re.search(r'^\s{0,}\* ', line):
            print("a")
            if list is None:
                startLine = i
                list = "<ul>\n"
            indent = myround(len(re.sub('^(\s{0,})\* .*$', r'\1', line)))
            content = re.sub('^\s{0,}\* (.*)$', r'\1', line)
            if indent>currrentIndent:
                while currrentIndent != indent:
                    list += "<ul>\n"
                    currrentIndent += 4
            elif indent<currrentIndent:
                while currrentIndent != indent:
                    list += "</ul>\n"
                    currrentIndent -= 4
            list += f"<li>{content}</li>"
            print("b")
            if i==(arraylen-1):
                list += "</ul>\n"
                while currrentIndent != 0:
                    list += "</ul>\n"
                    currrentIndent -= 4
                lists.append([startLine, i+1, list])
        
        else:
            if list is not None:
                list += "</ul>\n"
                while currrentIndent != 0:
                    print(currrentIndent)
                    list += "</ul>\n"
                    currrentIndent -= 4
                lists.append([startLine, i, list])
                list = None

    if len(lists)>0:
        for l in reversed(lists):
            listarray[l[0]]=l[2]
            del listarray[(l[0]+1):l[1]]
        html = '\n'.join(listarray)
        
    # Initially i tried to use regex for lists but this implmentation was strugling to deal with inden 

    # if re.search(r'[\n\*(^\n*?)\n*]{2,}', html):
    #     html = re.sub('^\* ([^\n]*?)\n', r'<li>\1</li>\n', html, flags=re.M)
    #     html = re.sub('^\s{4}\* ([^\n]*)$\n', r'<lir>\1</lir>\n', html, flags=re.M)
    #     html = re.sub('((\n<lir>[\s\S]*?<\/lir>$){1,})', r'<ulr>\1</ulr>', html, flags=re.M)
    #     html = re.sub('((<li>[\s\S]*((<\/ulr>(?!\n<li>))|(<\/li>(?!\n<ulr>)))){1,})', r'<ul>\1</ul>', html, flags=re.M)
    #     html = re.sub('<lir>', '<li>', html)
    #     html = re.sub('</lir>', '</li>', html)
    #     html = re.sub('<ulr>', '<ul>', html)
    #     html = re.sub('</ulr>', '</ul>', html)

    # Headings h6 through h1
    html = re.sub('(###### )(^\n*?)(\n)', r'<h6>\2</h6>\n', html)
    html = re.sub('(##### )([^\n]*?)(\n)', r'<h5>\2</h5>\n', html)
    html = re.sub('(#### )([^\n]*?)(\n)', r'<h4>\2</h4>\n', html)
    html = re.sub('(### )([^\n]*?)(\n)', r'<h3>\2</h3>\n', html)
    html = re.sub('(## )([^\n]*?)(\n)', r'<h2>\2</h2>\n', html)
    html = re.sub('(# )([^\n]*?)(\n)', r'<h1>\2</h1><br>', html)
    # Line Breaks
    html = re.sub(' {2,}\n', r'<br>', html)
    # Horizontel Rules
    html = re.sub('\n[-*_]{3,}\n', r'<hr>', html)
    #Bold and Italics
    html = re.sub('\*\*(.*?)\*\*', r'<strong>\1</strong>', html)
    html = re.sub('__(.*?)__', r'<strong>\1</strong>', html)
    html = re.sub('\*(.*?)\*', r'<em>\1</em>', html)
    html = re.sub('_(.*?)_', r'<em>\1</em>', html)
    # Paragraph tags
    html = re.sub('(<\/ul>|<\/h[1-6]>|<hr>)(.*$)\n((([A-Za-z])|(<a)|(<strong)|(<em)).*)((?!<h[1-6]>)|<ul>|\n\n|<hr>)', r'\1\2<p>\3</p>\9', html, flags=re.M)
    # Links: url and email links
    html = re.sub('(\[)(.*?)(\]\()(.*?)(\))', r'<a href="\4">\2</a>', html)
    html = re.sub('<(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})>', r'<a href=\1>\1</a>', html)
    html = re.sub('<(\S+@\S+\.\S+)>', r'<a href=mailto:\1>\1</a>', html)

    print(html)
    return html


def myround(n, base=4):
    return base * round(n/base)
