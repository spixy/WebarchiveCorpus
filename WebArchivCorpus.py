import sys
import justext
import requests
from datetime import date

def printHelp():
    print("Usage: " + sys.argv[0] + " [web url] [date] [language]")
    print("  date        in 'yymmddhhmmss' format, default value is now (" + getToday() + ")")
    print("  language    default value is 'Czech'")
    exit()

def getToday():
    return date.today().strftime("%Y%m%d") + "000000"

def downloadWebsite(webUrl, dateTime):
    waybackUrl = "https://wayback.webarchiv.cz/wayback/" + dateTime + "/" + webUrl
    return requests.get(waybackUrl).text.encode('utf-8')

def printDoc(author, title, url):
    author = '' if author is None else 'author="' + author + '" '
    title = '' if title is None else 'title="' + title + '" '
    url = '' if url is None else 'url="' + url + '" '
    print('<doc ' + author + title + url + '>')

def printTag(tag, text):
    escaped_text = text.replace('<', '&lt;').replace('>', '&gt;').strip()
    print('<' + tag + '>')
    print(escaped_text)
    print('</' + tag + '>')

def printParagraphs(paragraphs, no_boilerplate):
    for paragraph in paragraphs:
        if paragraph['class'] != 'bad':
            if paragraph['heading']:
                tag = 'head'
            else:
                tag = 'p'
        else:
            if no_boilerplate:
                continue
            else:
                tag = 'b'
        printTag(tag, paragraph['text'])

if len(sys.argv) == 1:
    printHelp()

webUrl = sys.argv[1]
dateTime = sys.argv[2] if len(sys.argv) >= 3 else getToday()
language = sys.argv[3] if len(sys.argv) >= 4 else "Czech"

htmlContent = downloadWebsite(webUrl, dateTime)
paragraphs = justext.justext(htmlContent, justext.get_stoplist(language))

printDoc(None, None, webUrl)
printParagraphs(paragraphs, True)
print('</doc>')