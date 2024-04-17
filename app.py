from webDriver import *
import urllib.request
import time
import os
import threading
import numpy



def main(uidList: str,position:dict):
    driver = WebDriver().startDriver(position)
    for uid in uidList:
        uid = uid.strip()
        driver.get(f'https://www.facebook.com/{uid}')
        if 'You must log in to continue.' in driver.page_source or 'Bạn phải đăng nhập để tiếp tục.' in driver.page_source:
            with open('fail.txt', 'a+', encoding='utf-8') as f:
                f.write(f'{uid}\n')
            continue
        maxWait = 30
        time.sleep(1)
        while True:
            try:
                cover = [i.get_attribute('src') for i in driver.find_elements(By.TAG_NAME, 'img') if str(
                    i.get_attribute('data-imgperflogname')) == 'profileCoverPhoto']
                avt = [i.get_attribute('xlink:href') for i in driver.find_elements(By.TAG_NAME, 'image') if str(
                    i.get_attribute('x')) == '8' or str(i.get_attribute('x')) == '0']
                if avt == []:
                    maxWait -= 1
                    if maxWait == 0:
                        with open('error.txt', 'a+', encoding='utf-8') as f:
                            f.write(f'{uid}\n')
                        with open('debug.log', 'a+', encoding='utf-8') as f:
                            f.write(f'{str(e)}\n')
                        break
                    else:
                        continue
                if 'Link to open profile cover photo' in driver.page_source and cover == []:
                    continue
                if cover:
                    try:
                        threading.Thread(target=urllib.request.urlretrieve, args=(cover[0], f'cover/{uid}.jpg',)).start()
                    except:pass
                try:
                    threading.Thread(target=urllib.request.urlretrieve, args=(avt[0], f'avatar/{uid}.jpg',)).start()
                except:pass
                break
            except Exception as e:
                maxWait -= 1
                if maxWait == 0:
                    with open('error.txt', 'a+', encoding='utf-8') as f:
                        f.write(f'{uid}\n')
                    with open('debug.log', 'a+', encoding='utf-8') as f:
                        f.write(f'{str(e)}\n')
                    break
                continue
    driver.quit()


with open('uids.txt', 'r', encoding='utf-8') as f:
    uids = f.readlines()
if os.path.exists('cover') == False:
    os.mkdir('cover')
if os.path.exists('avatar') == False:
    os.mkdir('avatar')

threads = int(input('SỐ LUỒNG :').strip())
datas = list(numpy.array_split(uids,threads))
position = getWindowPositionTypeStack(threads+2, 500, 500, 250)
i = 0
for data in datas:
    t = threading.Thread(target=main,args=(data,position[i]))
    t.setName(str(i))
    t.start()
    i+=1
    time.sleep(0.5)