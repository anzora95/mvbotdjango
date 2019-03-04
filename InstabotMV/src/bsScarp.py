from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup


def scrapImg(username):
    my_url = 'https://www.instagram.com/%s/' % (username)

    uClient= uReq(my_url)
    page_html = uClient.read()
    s=soup(page_html, "html.parser")
    containers=s.findAll("meta",{"property":"og:image"})
    tag = containers[0]
    tag2=str(tag)
    url = tag2.replace('<meta content="', '')
    link=url.replace('" property="og:image"/>','')
    return(link)

def scrap_us(username):
    my_url = 'https://www.instagram.com/%s/' % (username)
#    return(us_info)

    uClient= uReq(my_url)
    page_html = uClient.read()
    s=soup(page_html, "html.parser")
    container=s.findAll("meta",{"property":"og:description"})
    valor=str(container).replace('[<meta content="', '')
    valor2=valor[0:33]
    ul=valor2.split(" ")
    return(ul)
