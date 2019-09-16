import sys
import argparse
import justext
import requests
from datetime import date

def createArgParser():
    "Creates argument parser"
    
    currentDate = date.today().strftime("%Y%m%d") + "000000"
    ap = argparse.ArgumentParser()
    ap.add_argument("websiteUrl", nargs=1)
    ap.add_argument("-d", "--date", required=False, help="in 'yymmddhhmmss' format, default value is current date (" + currentDate + ")", default=currentDate)
    ap.add_argument("-l", "--lang", required=False, help="language, default value is 'Czech'", default="Czech")
    ap.add_argument("-b", "--boilerplate", required=False, help="enables boilerplate tags", action="store_true")
    return ap

def downloadWebsite(webUrl, dateTime):
    "Retrieves website content from wayback archive"

    waybackUrl = "https://wayback.webarchiv.cz/wayback/" + dateTime + "/" + webUrl
    return requests.get(waybackUrl).text.encode('utf-8')

def printDoc(author, title, url):
    "Creates and prints starting <doc> tag"

    author = '' if author is None else 'author="' + author + '" '
    title = '' if title is None else 'title="' + title + '" '
    url = '' if url is None else 'url="' + url + '" '
    print('<doc ' + author + title + url + '>')

def printTag(tag, text):
    "Prints tag with inner text content"

    escaped_text = text.replace('<', '&lt;').replace('>', '&gt;').strip()
    print('<' + tag + '>')
    print(escaped_text)
    print('</' + tag + '>')

def printParagraphs(paragraphs, boilerplate):
    "Prints paragraphs (including boilerplates if set)"

    for paragraph in paragraphs:
        if paragraph['class'] != 'bad':
            if paragraph['heading']:
                tag = 'head'
            else:
                tag = 'p'
        else:
            if boilerplate:
                tag = 'b'
            else:
                continue
        printTag(tag, paragraph['text'])

ap = createArgParser()

# Exit if no arguments
if len(sys.argv) == 1:
    ap.print_help()
    exit()

# Set parameters
args = vars(ap.parse_args())

webUrl = args["websiteUrl"][0]
dateTime = args["date"]
language = args["lang"]
boilerplate = args["boilerplate"]

# Download website
htmlContent = downloadWebsite(webUrl, dateTime)

# Get paragraphs from jusText
paragraphs = justext.justext(htmlContent, justext.get_stoplist(language))

# Print paragraphs
printDoc(None, None, webUrl)
printParagraphs(paragraphs, boilerplate)
print('</doc>')