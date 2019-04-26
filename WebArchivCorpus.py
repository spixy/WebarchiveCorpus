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
    return date.today().strftime("%y%m%d") + "000000"

def downloadWebsite(webUrl, dateTime):
    waybackUrl = "https://wayback.webarchiv.cz/wayback/" + dateTime + "/" + webUrl
    return requests.get(waybackUrl).text.encode('utf-8')

def html_escape(text):
    return text.replace('<', '&lt;').replace('>', '&gt;')

def writeToOutput(paragraphs, no_boilerplate):
    for paragraph in paragraphs:
        if paragraph['class'] != 'bad':
            if paragraph['heading']:
                tag = 'h'
            else:
                tag = 'p'
        else:
            if no_boilerplate:
                continue
            else:
                tag = 'b'
        escaped_paragraph = html_escape(paragraph['text']).strip()
        print('<' + tag + '>')
        print(escaped_paragraph)

if len(sys.argv) == 1:
    printHelp()

webUrl = sys.argv[1]
dateTime = sys.argv[2] if len(sys.argv) >= 3 else getToday()
language = sys.argv[3] if len(sys.argv) >= 4 else "Czech"

htmlContent = downloadWebsite(webUrl, dateTime)

paragraphs = justext.justext(htmlContent, justext.get_stoplist(language))

writeToOutput(paragraphs, False)