try:
    import os
    import sys
    import time
    import requests #pip install requests
    import json
    from bs4 import BeautifulSoup #pip install BeautifulSoup4
except:
    print('Some modules are not installed! Installing them automatically.')
    os.system('python -m pip install requests')
    os.system('python -m pip install BeautifulSoup4')

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
noet=noet.get_text()
noe=""
for i in range(noet.index('-')+1,len(noet)):
    noe+=str(noet[i])

noe = int(noe)

print("Number of episodes available: "+str(noe)+"\n")

print ("Enter number of episodes you want to download:\nThe downloads are in good quality so it may take some time, Please be patient.\nSuggestion: Don't go beyond 20 or the software may crash\n")

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

print("")

for i in range(sepi,eepi+1):
    temp2=BeautifulSoup(requests.get(url_src+anime+"-episode-"+str(i)).text,"lxml").find("div",class_="play-video").find("iframe")
    temp2=str(temp2["src"])
    temp2=temp2.replace("//gogo-play.net/streaming.php","")
    urlfj="https://gogo-play.net/ajax.php"+temp2+"&refer=none"
    jsonfd=json.loads(requests.get(urlfj,headers=headers).text)
    url_dl=(str(jsonfd["source"][0]["file"]))
    print("Downloading episode "+str(i)+".....")
    with open(os.path.join(loc,aniold+"Episode "+str(i)+".mp4"),"wb") as f:
        f.write(requests.get(url_dl).content) 
        f.close()
