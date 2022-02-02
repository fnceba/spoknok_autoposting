import requests
import datetime
import time
import sys
import os
import re
from telethon.sync import TelegramClient, events
from seleniumwire import webdriver
import cv2
import difflib
import telebot

chanNum=0
mins=26
waitt=27

chan = ['goodnightlittleones','testgoos']
headers = {'accept':'*/*','accept-encoding':'gzip, deflate, br','accept-language':'en-US,en;q=0.9,ru;q=0.8','cache-control':'no-cache','origin':'https://telik.top','pragma':'no-cache','referer':'https://telik.top/karusel/','sec-fetch-dest': 'empty', 'sec-fetch-mode': 'cors','sec-fetch-site': 'cross-site','user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36 Edg/84.0.522.40}'}

bot_logger = telebot.TeleBot('')
def botlog(texttosend):
    bot_logger.send_message(307518206, 'Spoknok: '+texttosend)
botlog('hey')
def CompareHash(hash2,j):
    #hash1='0000000000000000011100000111110000111100001000000000000000000000'#REKlama
    hash1=['0000001101011010000110000001100000011000000110000000000000000000','0000001100111110011111100011110000111100000110000011110000000000'][j]
    l=len(hash1)
    i=0
    count=0
    while i<l:
        count+=int(hash1[i]!=hash2[i])
        i=i+1
    return count

def findthis():
    sec=[]
    cap = cv2.VideoCapture('/home/sapron/spoknok/vid.mp4')
    amount_of_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    print(amount_of_frames)
    i=500
    j=0
    while i < int(amount_of_frames):
        cap.set(cv2.CAP_PROP_POS_FRAMES, i-1)
        res, frame = cap.read()
        resized = cv2.resize(frame, (8,8), interpolation = cv2.INTER_AREA) #Уменьшим картинку
        gray_image = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY) #Переведем в черно-белый формат
        avg=gray_image.mean() #Среднее значение пикселя
        ret, threshold_image = cv2.threshold(gray_image, avg, 255, 0) #Бинаризация по порогу
        #Рассчитаем хэш
        _hash=""
        for x in range(8):
            for y in range(8):
                val=threshold_image[x,y]
                if val==255:
                    _hash=_hash+"1"
                else:
                    _hash=_hash+"0"
        comp=CompareHash(_hash,j)
        if comp<4:
            sec.append(i/25)
            #print(f'startframe={i}; {i/25}; {comp}')
            i+=8*60*25
            if j==1:
                j=2
                break
            j=1
        i+=40
    if j==2:
        return f'-ss {sec[0]-13} -t {sec[1]+15 - sec[0]}'
    return f'-ss {sec[0]-13} -t {(i-40)/25+15 - sec[0]}'

def geti():
    while True:
        cont=''
        try:
            cont=str(requests.get(mpdurl, headers=headers).content)
            return re.search(r'-1k-\$Number\$\.m4s" startNumber="(\d+)',cont).group(1)
        except:
            botlog('geti error')
            print('!!!geti error ',cont)
            if datetime.datetime.now().minute < waitt+2:
                sys.exit(155)
            return 0


while True:
    #opt = webdriver.ChromeOptions()
    #opt.add_argument("--no-sandbox")
    #opt.add_argument('--headless')
    #opt.add_argument("--disable-gpu")
    #opt.add_argument('--ignore-certificate-errors')
    #opt.add_argument('--ignore-ssl-errors')
    sw_options = {
        'connection_timeout': 20
    }
    print('launching browser')
    #driver = webdriver.Chrome(chrome_options=opt, seleniumwire_options=sw_options)

    opts = webdriver.FirefoxOptions()
    opts.add_argument("--headless")
    driver = webdriver.Firefox(firefox_options=opts)
    try:
        print('trying\n')
        driver.get('https://ru.spbtv.com/channels/karusel')#'https://spbtvonline.ru/kanaly-tv/karusel.html')
        time.sleep(10)
        driver.find_element_by_xpath('//*[@id="app"]/div/div/div[2]/main/div[1]/div/div/div/div/span/span[5]/div/div/button').click()
        time.sleep(60)
        mpdurl=''
        for request in driver.requests:
            print(request.url)
            if '.mpd' in request.url:
                mpdurl=request.url
                #print(mpdurl, request.params)
                botlog('mpd done')
                break
        driver.quit()
        print(mpdurl)
        ipv5 = re.search(r'(.+)\.mpd',mpdurl).group(1)
        break
    except Exception as e:
        print('(selen) err: '+str(e))
        driver.quit()
        time.sleep(10)
        pass

m4svidurl = lambda x: ipv5+'-vid-inadv-trid1-1k-'+str(x)+'.m4s'
m4saudurl = lambda x: ipv5+'-aud-inadv-trid2-1k-'+str(x)+'.m4s'

while datetime.datetime.now().minute < waitt:
    time.sleep(10)

print('started'+ str(datetime.datetime.now()))
botlog('started')
with open("/home/sapron/spoknok/aud.m4s",'wb') as f:
    f.write(requests.get(m4saudurl('init'), headers=headers).content)
with open("/home/sapron/spoknok/vid.m4s",'wb') as f:
    f.write(requests.get(m4svidurl('init'), headers=headers).content)

i=int(geti())
x = datetime.datetime.now().minute
while abs(datetime.datetime.now().minute - x)<mins:
    if i<int(geti())+6:
        with open("/home/sapron/spoknok/aud.m4s",'ab') as f:
            f.write(requests.get(m4saudurl(i), headers=headers).content)
        with open("/home/sapron/spoknok/vid.m4s",'ab') as f:
            f.write(requests.get(m4svidurl(i), headers=headers).content)
        i+=1
    else:
        time.sleep(2)

os.system(f'ffmpeg -y -i /home/sapron/spoknok/aud.m4s -i /home/sapron/spoknok/vid.m4s -vcodec copy /home/sapron/spoknok/vid.mp4')

#################----------------------------
'''
name = 'Спокойной ночи, малыши! '
try:
    name = name + re.search(r'Спокойной ночи, малыши! \((.*?\.)', requests.get('https://tv.mail.ru/moskva/channel/1162/',headers=headers).text).group(1)
except:
    pass
print(name)
with TelegramClient('anon', , ) as client:
    client.send_file(chan[chanNum], '/home/sapron/spoknok/vid.mp4', caption=name,thumb='/home/sapron/spoknok/th.jpg', supports_streaming=True)
'''
#################-----------------------------

botlog('vid generated')
os.system(f'ffmpeg -y {findthis()} -i /home/sapron/spoknok/vid.mp4 -vcodec copy /home/sapron/spoknok/video.mp4')

#findthis()

today_date = datetime.date.today()
name = f"Выпуск от {today_date.day} " + ['января','февраля','марта','апреля','мая','июня','июля','августа','сентября','октября','ноября','декабря'][today_date.month-1]
try:
    namedobav = re.search(r'Спокойной ночи, малыши! \((.*?)\.', requests.get('https://tv.mail.ru/moskva/channel/1162/',headers=headers).text).group(1)
    if len(namedobav)< 80:
        name += ": " + namedobav
except:
    pass
cap_preview = cv2.VideoCapture("video.mp4")

# get total number of frames
totalFrames = cap_preview.get(cv2.CAP_PROP_FRAME_COUNT)
myFrameNumber = 9000
# check for valid frame number
if myFrameNumber >= 0 & myFrameNumber <= totalFrames:
    # set frame position
    cap_preview.set(cv2.CAP_PROP_POS_FRAMES,myFrameNumber)

ret_nenujnoe, frame = cap_preview.read()
cv2.imwrite("/home/sapron/spoknok/thumbsup.jpg", frame)

botlog(name)
with TelegramClient('anon', , ) as client:
    client.send_file(chan[chanNum], '/home/sapron/spoknok/video.mp4', caption=name,thumb='/home/sapron/spoknok/thumbsup.jpg', supports_streaming=True)

