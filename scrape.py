from bs4 import BeautifulSoup
from requests import get
from os import makedirs
import time
import sys
import re


THREAD_URL = ""

def getURL():
    global THREAD_URL

    # sys.argv list always starts with filename.py
    if len(sys.argv) > 1:
        THREAD_URL = sys.argv[1]
    else: 
        sys.tracebacklimit = 0
        raise Exception("Expected URL to thread. Check correct usage.")

    return THREAD_URL

def getImages():
    global THREAD_URL
    imgs = []
    s = ""
    soup = BeautifulSoup(get(THREAD_URL).text, 'lxml')
    for a in soup.find_all('a', href=True):
        # 4chan uses 4 different servers to store images
        # However, all of the img hrefs start with //i
        if a['href'][0:3] == "//i":
            s = f"http://{a['href'][2:]}"
            if len(imgs) > 0:
                # only store img URL if it is not already in the imgs list.
                if imgs[-1] != s: imgs.append(s)
            else: imgs.append(s)
    
    return imgs, len(imgs)

def getThreadID():
    global THREAD_URL
    THREAD_ID = re.search("(?<=thread/)(.*)$", THREAD_URL).group(0)
    return THREAD_ID

def saveImages(image_list: list):
    filepath = f"Thread{getThreadID()}"
    makedirs(filepath, exist_ok=True)

    # enumerate through the image names
    for x, img in enumerate(image_list[0]):
        r = get(img)
        with open((f"{filepath}/{x}.jpg"), 'wb') as f:
            f.write(r.content)
        print(f"{x}.jpg saved. ({image_list[1] - x} images remaining)")

def main():

    getURL()
    saveImages(getImages())



if __name__ == "__main__":
    main()
    raise SystemExit
