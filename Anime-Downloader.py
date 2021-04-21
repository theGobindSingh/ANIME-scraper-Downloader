import os
import sys
import time
import json
import webbrowser
import warnings



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
folder_name=str(input("[+] Please enter a name for your folder without any spaces: "))     #This folder will be created in Documents

docs = os.path.expanduser("~/Documents").replace("\\","/") + "/" #Change to Desktop if you want
loc = docs+folder_name

url_src="https://www1.gogoanime.ai/"  #Change the proxy website if not working

pyname=os.path.basename(__file__)

wd=os.getcwd()

try:
    os.chdir(loc)
except:
    os.mkdir(loc)

print ("Save location: "+loc+"\n")

search = str(input("[+] Enter the Anime you want to search:  "))
if(search==""):
    print("\nNo Input Available. \nExiting the program.\n")
    time.sleep(2.5)
    sys.exit()

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'}

soup1=BeautifulSoup(requests.get(url_src+"search.html?keyword="+search.replace(" ","%20")).text,"lxml")
temp1=soup1.find_all('div', class_='img')

if(temp1==None or len(temp1)==0):
    print("Wrong input, please try again")
    time.sleep(1)
    os.chdir(wd)
    os.system("python "+pyname)
    sys.exit()

for x in range(0,int(len(temp1))):
    temp2=(temp1[x].find("a"))["title"]
    print (str(x+1)+": "+temp2)

try:
    c1=int(input("\n[+] Please Enter the number prior to your desiered Result:  "))
    aniold = str( temp1[c1-1].find("a")["title"] )
    print("\nYou chose: \n" + aniold )
    aniold = aniold.lower()
except:
    print ("\nERROR! \nExiting the program.\n")
    time.sleep(2.5)
    sys.exit()

anime=""
for i in range(0,int(len(aniold))):
    if( (ord(aniold[i]) < 97 or ord(aniold[i]) > 122) and (ord(aniold[i]) < 48 or ord(aniold[i]) > 57) ):
        if (len(anime)>0 and (not(anime[len(anime)-1] == "-")) and (not(i==int(len(aniold))-1))):
            anime=anime+"-"
    else:
        anime=anime+aniold[i]


noe_link=url_src+"/category/"+anime
noet=(BeautifulSoup(requests.get(noe_link).text,"lxml")).find("div", class_="anime_video_body").find_all("li")
noet=noet[len(noet)-1]
noet=str(noet.get_text())
noe=""
if (noet.find("-")==-1):
    noe=noet
else:
    for i in range(noet.index('-')+1,len(noet)):
        noe+=str(noet[i])
noe=str(int(noe))
print("Number of episodes available: "+str(noe)+"\n")

sepi=int(1)
eepi=int(1)

if not( int(noe) == int(1) ):
    print ("Enter number of episodes you want to download:\nThe downloads are in good quality so it may take some time, Please be patient.\nEach episode may be up to 500mb.\nSuggestion: Don't go beyond 10 or the software may crash\n")
    print ("If you want to download just one episode, put the same episode number as Starting and Ending Episode")

    try:
        sepi=int(input("[+] Starting episode: "))
    except:
        print ("\nERROR! \nExiting the program.\n")
        time.sleep(2.5)
        sys.exit()
    try:
        eepi=int(input("[+] Ending episode: "))
    except:
        print ("\nERROR! \nExiting the program.\n")
        time.sleep(2.5)
        sys.exit()
else:
    print ("Downloading the only episode available.:\nThe downloads are in good quality so it may take some time, Please be patient.")



print("")

for i in range(sepi,eepi+1):
    print("Downloading episode "+str(i)+".....")
    temp2=BeautifulSoup(requests.get(url_src+anime+"-episode-"+str(i)).text,"lxml").find("div",class_="play-video").find("iframe")
    temp2=str(temp2["src"])
    temp2=temp2.replace("//gogo-play.net/streaming.php","")
    urlfj="https://gogo-play.net/ajax.php"+temp2+"&refer=none"
    jsonfd=json.loads(requests.get(urlfj,headers=headers).text)
    url_dl=(str(jsonfd["source"][0]["file"]))
    if not("cloud9xx" in url_dl):
        with open(os.path.join(loc,aniold+"Episode "+str(i)+".mp4"),"wb") as f:
            tempp=requests.get(url_dl,stream=True)
            #fost="{l_bar}" #: %(percent)3d%%" #[%(bar)s] %(current)d/%(max)d [%(elapsed).1f s] [eta %(eta_avg).0f+-%(eta_stddev).0f s]"
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore")
                for chunk in tqdm(iterable=tempp.iter_content(chunk_size=1024),desc="",total=int(tempp.headers["Content-Length"])/1024,unit="KB",unit_divisor=1024,unit_scale=1,postfix="",bar_format="{l_bar}"):
                    if chunk:
                        #print(chunk)
                        #f.write(tempp.content) 
                        pass
            f.close()
    else:
        print("\nWarning: This episode was blocked. \n\nNow downloading an alternate file.\nThis download will be very slow;\nBut you can watch it while it is downloading.\n")
        yon=input("[+] Do you wish to continue? Enter (y/n)   ").lower()[0]
        if (yon=="y" or yon=="" or yon==None):
            print("\nDownloading this episode... Please wait...\n")
            rcld=requests.get(url_dl)
            m3u8_master=m3u8.loads(rcld.text).data["playlists"]
            urlc=url_dl
            urlc=urlc.replace(str(urlc[urlc.rfind('/')+1:]),str(m3u8_master[0]["uri"]))
            temp3=m3u8.loads(requests.get(urlc).text).data["segments"]
            with open(os.path.join(loc,aniold+"Episode "+str(i)+".ts"),"wb") as f:
                for i in tqdm(range(0,len(temp3)),bar_format="{l_bar}"):
                    m3u8_play=temp3[i]["uri"]
                    urlcc=url_dl
                    urlcc=urlcc.replace(str(urlcc[urlcc.rfind('/')+1:]),str(m3u8_play))
                    f.write(requests.get(urlcc).content) 
                f.close()
        else:
            print("Ok. Skipping episode "+str(i)+".")
print("\n***** THANKYOU. HAVE A NICE DAY. *****\n\n")
time.sleep(2)
