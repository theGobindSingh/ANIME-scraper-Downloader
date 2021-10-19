import os
import sys
import time
import json
import warnings
from urllib.parse import urlparse
from urllib.parse import parse_qs

try:
    import pip
except:
    print('PIP NOT INSTALLED!!! Kindly install pip correctly and then try again')
    time.sleep(2.5)
    sys.exit()

try:
    import requests #pip install requests
except:
    print('Request module not installed! Installing automatically.')
    os.system('python -m pip install requests')
    import requests #pip install requests
    
try:
    import lxml #pip install lxml
except:
    print('lxml module not installed! Installing automatically.')
    os.system('python -m pip install lxml')
    import lxml #pip install requests
    
try:
    from bs4 import BeautifulSoup #pip install BeautifulSoup4
except:
    print('Request module not installed! Installing automatically.')
    os.system('python -m pip install BeautifulSoup4')
    from bs4 import BeautifulSoup

try:
    import m3u8
except:
    print('m3u8 module not installed! Installing automatically.')
    os.system('python -m pip install m3u8')
    import m3u8

try:
    from tqdm import tqdm
except:
    print('tqdm module not installed! Installing automatically.')
    os.system('python -m pip install tqdm')
    from tqdm import tqdm

print("\n     ***************************     ")
print("     ***************************     ")
print("     WELCOME TO ANIME DOWNLOADER     ")
print("     ***************************     ")
print("     ***************************     \n")

print("Your files will be downloaded in a folder in your Documents.")
folder_name=str(input("[+] Please enter a name for your folder without any spaces: "))     #This folder will be created

locationPath = "Documents" #Change to Desktop if you want
docs = os.path.expanduser("~/"+locationPath).replace("\\","/") + "/" 
loc = docs+folder_name

pyname=os.path.basename(__file__)

wd=os.getcwd()

try:
    os.chdir(loc)
except:
    os.mkdir(loc)

print ("Save location: "+loc+"\n")

# Different proxies of Gogo anime 
servers = ["https://gogoanime.lol/","https://gogoanime2.org/"]
def selectProxy():
    try:
        for x in range(0,len(servers)):
            print(""+str(x+1)+": "+servers[x])
        url_src = servers[(int(input("\n[+] Enter the number of the desired server: ")))-1]
        return url_src
    except:
        print ("\nERROR! \nTry again!\n")
        return selectProxy()
url_src=selectProxy()

#Input for search
search = str(input("\n[+] Enter the Anime you want to search:  "))

if(search==""):
    print("\nNo Input Available. \nExiting the program.\n")
    time.sleep(2.5)
    sys.exit()

#for searching
if(url_src==servers[0]):
    searchPage1=BeautifulSoup(requests.get(url_src+"search.html?keyword="+search.replace(" ","%20")).text,"lxml")
    searchPage2=BeautifulSoup(requests.get(url_src+"search.html?keyword="+search.replace(" ","%20")+"&page=2").text,"lxml")
if(url_src==servers[1]):
    searchPage1=BeautifulSoup(requests.get(url_src+"search/"+search.replace(" ","%20")).text,"lxml")
    searchPage2=BeautifulSoup(requests.get(url_src+"search/"+search.replace(" ","%20")+"/2").text,"lxml")


# Extracting and displaying search results
# Also selecting a result
searchResult1=searchPage1.find_all('div', class_='img')
searchResult2=searchPage2.find_all('div', class_='img')
if(searchResult1==None or len(searchResult1)==0 or searchResult2==None or len(searchResult2)==0):
    print("Wrong input, please try again")
    time.sleep(1)
    os.chdir(wd)
    os.system("python "+pyname)
    sys.exit()
def pageChange(search_result,pg):
    for x in range(0,int(len(search_result))):
        sR=(search_result[x].find("a"))["title"]
        print (str(x+1)+": "+sR)
    if(pg==1):
        sI=input("\n[+] Enter the number of your desired search or leave blank for more results: ")
    if(pg==2):
        sI=input("\n[+] Enter the number of your desired search: ")
    if(sI=="" or sI==None):
        return pageChange(searchResult2,2)
    else:
        return [int(sI),search_result]
searchSelect = pageChange(searchResult1,1)
try:
    final_Select = str( searchSelect[1][searchSelect[0]-1].find("a")["title"] )
    print("\nYou chose: \n" + final_Select )
    finalSelect = ""
    for s in final_Select.lower():
        charIntFS=ord(s)
        if(charIntFS==32): 
            finalSelect=finalSelect+"-" #for spcae
        elif((charIntFS>=48 and charIntFS<=57) or (charIntFS>=65 and charIntFS<=90) or (charIntFS>=97 and charIntFS<=122)):
            finalSelect=finalSelect+s #for alpha-numeric chars
        else:
            finalSelect=finalSelect+"" #for everything else
except:
    print ("\nERROR! \nExiting the program.\n")
    time.sleep(2.5)
    sys.exit()

# Number of episodes
if(url_src==servers[0]):
    movie_id=BeautifulSoup(requests.get(url_src+"category/"+finalSelect).text,"lxml").find(attrs={"id":"movie_id"}).get("value")
    alias_anime=BeautifulSoup(requests.get(url_src+"category/"+finalSelect).text,"lxml").find(attrs={"id":"alias_anime"}).get("value")
    lolEpURL = url_src+"ajax/load_list_episode?ep_start=0&ep_end=999999999&id="+movie_id+"&default_ep=0&alias="+alias_anime
    numEp = len(BeautifulSoup(requests.get(lolEpURL).text,"lxml").find_all("a"))
if(url_src==servers[1]):
    lolEpURL = url_src+"anime/"+finalSelect
    numEp = len(BeautifulSoup(requests.get(lolEpURL).text,"lxml").find("div",attrs={"id":"load_ep"}).find_all("a"))

print("\nNumber of episodes available: \n"+str(numEp))


# Selecting episodes to download
startEp=1
endEp=1
if not( numEp == 1 ):
    print ("\nEnter number of episodes you want to download:\nThe downloads are in good quality so it may take some time, Please be patient.\nSuggestion: Don't go beyond 10 - the software may crash\n")
    print ("\nIf you want to download just one episode, put the same episode number as Starting and Ending Episode")

    try:
        startEp=int(input("\n[+] Starting episode: "))
    except:
        print ("\nERROR! \nExiting the program.\n")
        time.sleep(2.5)
        sys.exit()
    try:
        endEp=int(input("\n[+] Ending episode: "))
    except:
        print ("\nERROR! \nExiting the program.\n")
        time.sleep(2.5)
        sys.exit()
else:
    print ("Downloading the only episode available.:\nThe downloads are in good quality so it may take some time, Please be patient.")

#Preferred quality of episodes
def quali():
    Reso = input("\n[+] Enter your preffered quality < 1080, 720, 480, 320 >, \nLeave Blank for max quality available: ")
    if Reso=="":
        Reso=int(1080)
    else:
        if Reso[0]=="1":
            Reso=int(1080)
            print("\nPreffered Quality set to - 1080p")
        elif Reso[0]=="7":
            Reso=int(720)
            print("\nPreffered Quality set to - 720p")
        elif Reso[0]=="4":
            Reso=int(480)
            print("\nPreffered Quality set to - 480p")
        elif Reso[0]=="3":
            Reso=int(320)
            print("\nPreffered Quality set to - 320p")
        else:
            print("\nError!\nTry Again!")
            quali()
    return Reso
reso=int(quali())

print("\nFYI: You can watch the episodes even while it is downloading.\n")

#Downloading Episodes
if(url_src==servers[0]):
    print("\nSetting server 1 for download.")
    tempStart=startEp
    try:
        for k in range(startEp,endEp+1):
            print("\nDownloading episode "+int(k)+"...")
            epURL=url_src+finalSelect+"-episode-"+str(k) # Episode URL
            iFrame=BeautifulSoup(requests.get(epURL).text,"lxml").find("iframe").get("src")   # Getting iFrame source
            headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36","x-requested-with": "XMLHttpRequest","accept": "application/json, text/javascript, */*; q=0.01","accept-encoding": "gzip","accept-language":"en-US,en;q=0.9","referer": iFrame,"sec-fetch-dest": "empty","sec-fetch-mode": "cors","sec-fetch-site": "same-origin","sec-gpc": "1","referrer": iFrame}
            iFrameRes = requests.get(iFrame.replace("/e/","/info/")+"&skey=dcb0a59359d3f732f8b545fd2908e497", headers=headers,params={"referrer": iFrame}) # Getting m3u8 links
            iFrameRes.encoding="gzip"
            m3u8_Link = (json.loads(iFrameRes.text)["media"]["sources"][0]["file"]).replace("list.m3u8#.mp4","hls/")
            def quality(resolution): #for checking preffered or best available quality
                if (requests.get(m3u8_Link+str(resolution)+"/"+str(resolution)+".m3u8",headers=headers).status_code == 200):
                    return resolution
                else:
                    if resolution==720:
                        return quality(480)
                    elif resolution==480:
                        return quality(360)
                    else:
                        print ("\nERROR! \n")
                        return 0
            resolution=quality(reso)
            if resolution==0:
                print ("\nError!\nSkipping this episode.")
                continue
            try:
                m3u8_MAIN=m3u8_Link+str(resolution)+"/"+str(resolution)+".m3u8"
                m3u8_obj = m3u8.load(m3u8_MAIN)
                with warnings.catch_warnings():
                    warnings.filterwarnings("ignore")
                    with open(os.path.join(loc,final_Select+" Episode "+str(k)+".ts"),"wb") as f:
                        for i in tqdm(m3u8_obj.segments,unit="%",unit_scale=True,bar_format="{l_bar}{bar}| [{elapsed}]",postfix=""):
                            f.write(   requests.get(   m3u8_MAIN.replace(  str(resolution)+".m3u8",  i.uri), stream=True   ).content) 
                        f.close()
            except:
                print ("\nError!\nSkipping this episode.")
                continue
            tempStart=k
            print("Successfully downloaded!\n")
    except:
        print("\nSomething went wrong! Changing server!")
        startEp=tempStart
        url_src=servers[1] 

if(url_src==servers[1]):
    print("\nSetting server 2 for download.")
    tempStart=startEp
    try:
        for k in range(startEp,endEp+1):
            print("\nDownloading episode "+str(k)+"...")
            epURL=url_src+"watch/"+finalSelect+"/"+str(k) # Episode URL
            iFrame1=("https:"+BeautifulSoup(requests.get(epURL).text,"lxml").find("iframe").get("src"))   # getting link for id for video window
            id_URL= parse_qs(urlparse(iFrame1).query)['id'][0] # getting id for video window
            url_video=url_src+"embed/"+id_URL # url for video window
            print(url_video)
            videoPage=str(requests.get(url_video).content) # Video Page HTML
            # Getting m3u8 link
            s=int(videoPage.index("\"file\": ")) + 10 # m3u8 link - start index
            c=videoPage[s] # character on that index
            m3u8_Link="" # final link
            while not(c=="'"): # loop till it finds a ' character
                m3u8_Link=m3u8_Link+videoPage[s]
                s+=1
                c=videoPage[s]
            m3u8_Link=m3u8_Link.replace("\\","")
            headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"}
            try:
                m3u8_obj=m3u8.load(m3u8_Link)
                with warnings.catch_warnings():
                    warnings.filterwarnings("ignore")
                    with open(os.path.join(loc,final_Select+" Episode "+str(k)+".ts"),"wb") as f:
                        for i in tqdm(m3u8_obj.segments,unit="%",unit_scale=True,bar_format="{l_bar}{bar}| [{elapsed}]",postfix=""):
                            f.write(   requests.get(   m3u8_Link.replace(  "index.m3u8",  i.uri), headers=headers ,stream=True   ).content) 
                        f.close()
            except:
                print ("\nError!\nSkipping this episode.")
                continue
            tempStart=k
            print("Successfully downloaded!\n")
    except:
        print("\nSomething went wrong!")
        time.sleep(2.5)
        sys.exit()


print("\n***** THANKYOU. HAVE A NICE DAY. *****\n")
print("\n*************** ~GOBIND **************\n\n")
time.sleep(2)
