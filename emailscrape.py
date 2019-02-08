import requests
import re
import threading

# defining files and dividing directories list into two for threading
f = open('emails.txt', 'w+')
item = open('dir.txt', 'r')
dirsread = item.read().splitlines()
dirs1 = dirsread[:int((len(dirsread)/2))]
dirs2 = dirsread[int((len(dirsread)/2)):]
url_input = input('Website to scrape from: ')
url = 'https://' + url_input


# takes url and directory section and returns status code and thread ID, writing emails found to file
def scrape(url_arg, dirs):
    end = []
    for i in dirs:
        r = requests.get(url_arg + '/' + i) # use raise_for_status() to cut out 404s
        print(threading.current_thread()) # to check the threading is actually working
        if r.status_code == 200:
            print("Directory {}, status code: {}".format(i, r.status_code))
            end.append(emailfinder(r.text))
        else:
            print("Directory {}, status code: {}".format(i, r.status_code))
    for v in end:
            for l in v:
                    f.write(l + '\n')
        
def emailfinder(text):
    return re.findall(r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", text)
# added threading for each half of the directories
Thread1 = threading.Thread(group=None, target=scrape, args=(url, dirs1))
Thread2 = threading.Thread(group=None, target=scrape, args=(url, dirs2))
Thread1.start()
Thread2.start()
