import requests
from bs4 import BeautifulSoup

# the radioambulante names for the files are all the same, so maybe i can automate this to get a huge set of word data quickly

# Get the HTML of the website
url = 'https://radioambulante.org/category/audio/episodios'
titleList = []
buttonList = []

response = requests.get(url)
html = response.content

# Create a Beautiful Soup object
soup = BeautifulSoup(html, 'html.parser')

Articles = soup.find_all('a',itemprop='url')
buttonsForPages = soup.find_all('a',class_="inactive")

ArticleLinks = [str(x) for x in Articles]
ButtonLinks = [str(x) for x in buttonsForPages]
noImages = [s for s in ArticleLinks if s.startswith('<img') is False and 'audio' in s and 'category' not in s]

for F in noImages:
    splitAthref_articles = F.split('href=')
    if len(splitAthref_articles) != 0:
        splitAtItemprop_articles = splitAthref_articles[1].split(' itemprop')
        if splitAtItemprop_articles[0][1:-1] not in titleList:
            titleList.append(splitAtItemprop_articles[0][1:-1])
    else:
        continue

for B in ButtonLinks:
    splitAthref = B.split('href=')
    if len(splitAthref) != 0:
        splitAtItemprop = splitAthref[1].split(' itemprop')
        if splitAtItemprop[0][1:-1] not in buttonList:
            buttonList.append(splitAtItemprop[0][1:-1])

# after this I have a list of links that are themselves html pointers to other pages full of articles
# loop through these, run the same algorithm again
for Link in buttonList:
    # loop through buttons and get more titles
    print(f"on link: {Link}")
    response = requests.get(Link)
    html = response.content

    # Create a Beautiful Soup object
    soup = BeautifulSoup(html, 'html.parser')

    Articles = soup.find_all('a',itemprop='url')

    ArticleLinks = [str(x) for x in Articles]
    noImages = [s for s in ArticleLinks if s.startswith('<img') is False and 'audio' in s and 'category' not in s]

    for F in noImages:
        splitAthref_articles = F.split('href=')
        if len(splitAthref_articles) != 0:
            splitAtItemprop_articles = splitAthref_articles[1].split(' itemprop')
            if splitAtItemprop_articles[0][1:-1] not in titleList:
                titleList.append(splitAtItemprop_articles[0][1:-1])
        else:
            continue

# Now we have a whole bunch of html links that each point to an article on the website 
# We need to dig one level deeper to get to the transcripts
transcripList = []
MasterTextList = []

for T in titleList:
    print(f"at title: {T}")
    response = requests.get(T)
    html = response.content

    # Create a Beautiful Soup object
    soup = BeautifulSoup(html, 'html.parser')

    Articles = soup.find_all('a')

    ArticleLinks = [str(x) for x in Articles]
    noImages = [s for s in ArticleLinks if s.startswith('<img') is False and 'transcripción' in s and 'category' not in s]
    # somehow this worked exactly

    if len(noImages) == 1:
        splitAthref_transcripts = noImages[0].split('href="')
        if len(splitAthref_transcripts) != 0:
            splitAtItemprop_transcripts = splitAthref_transcripts[1].split('"')
            if splitAtItemprop_transcripts[0] not in titleList:
                currentTranscript = splitAtItemprop_transcripts[0]
                transcripList.append(currentTranscript)
    else:
        continue
    
    print(f"getting transcription data from file {currentTranscript}")
    try:
        transcripts_response = requests.get(currentTranscript)
        transcripts_html = transcripts_response.content

        # Create a Beautiful Soup object
        soup = BeautifulSoup(transcripts_html, 'html.parser')

        transcriptText = soup.find_all('p')
        # Extract the text from the elements
        text = ''.join([text_element.get_text() for text_element in transcriptText])
        MasterTextList.append(text)
    except:
        continue

MasterText = " ".join(MasterTextList)

outFileLocation = '//Users//michael//Documents//Programming//Python//Simple_AutoComplete//Transcripts.txt'
fileID = open(outFileLocation,'w')
fileID.write(MasterText)
fileID.close()