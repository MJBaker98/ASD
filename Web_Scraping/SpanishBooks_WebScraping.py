import requests
from bs4 import BeautifulSoup
import PyPDF2
from io import BytesIO

# Get the HTML of the website
url = 'https://elestudiantedigital.com/libros-pdf/'
titleList = []
buttonList = []

response = requests.get(url)
html = response.content

# Create a Beautiful Soup object
soup = BeautifulSoup(html, 'html.parser')
embed_element = soup.find_all("a")
allBookText = ""

for link in embed_element:
    if ('.pdf' in link.get('href', [])):
        currentURL = link.get('href')
        print(f"Reading text from PDF: {currentURL}")
 
        # Get PDF object for link
        pdf_response = requests.get(currentURL)
        pdf_content = pdf_response.content
        pdf_reader = PyPDF2.PdfFileReader(BytesIO(pdf_content))
        for page_num in range(pdf_reader.numPages):
            if page_num == 0 or page_num == 1:
                continue
            elif page_num == pdf_reader.numPages-1:
                page = pdf_reader.getPage(page_num)
                currentPageText = page.extract_text()
                pageTextVector = currentPageText.split()
                try:
                    FIN_ind = pageTextVector.index('FIN')
                except:
                    FIN_ind = -1
                
                if FIN_ind != -1:
                    cleaned_pageText = " ".join(pageTextVector[2:FIN_ind])
                else:
                    cleaned_pageText = " ".join(pageTextVector[2:-1])

                allBookText += cleaned_pageText
            else:
                page = pdf_reader.getPage(page_num)
                currentPageText = page.extract_text()
                pageTextVector = currentPageText.split()
                cleaned_pageText = " ".join(pageTextVector[2:-1])
                allBookText += cleaned_pageText

outFileLocation = '//Users//michael//Documents//Programming//Python//Web_Scraping//Classic_Books.txt'
fileID = open(outFileLocation,'w')
fileID.write(allBookText)
fileID.close()

