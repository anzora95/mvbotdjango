from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

def scrapUsr(username):
    my_url = 'https://www.instagram.com/%s/' % (username)
    replace3=', 1,143 Following, 209 Posts - See Instagram photos and videos from Ariel Zelaya (@arielzelayat)" property="og:description"/>'

    us_info=[]

    uClient= uReq(my_url)
    page_html = uClient.read()
    s=soup(page_html, "html.parser")
    imgContain=s.findAll("meta",{"property":"og:image"})
    namecontain=s.findAll("meta",{"property":"og:title"})
    fo_contain=s.findAll("meta",{"property":"og:description"})

    parseado=[]
    parseado.append(imgContain[0])
    parseado.append(namecontain[0])
    parseado.append(fo_contain[0])

    tag=[]
    for x in parseado:
        tag.append(str(x).replace('<meta content="', ''))
    
    us_info.append(str(tag[0]).replace('" property="og:image"/>',''))
    us_info.append(str(tag[1]).replace(' • Instagram photos and videos" property="og:title"/>',''))
    us_info.append(str(tag[2]).replace(', 1,143 Following, 209 Posts - See Instagram photos and videos from',''))

    valor=str(us_info[2])
    valor2=valor.replace('" property="og:description"/>','')
    valor3=valor2[0:14]
    us_info[2]=valor3
    return(us_info)
