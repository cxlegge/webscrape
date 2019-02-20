import requests
import re
import threading

# defining files and dividing directories list into two for threading
f = open('emails.txt', 'w+')
item = open('dir.txt', 'r')
dirsread = item.read().splitlines()
url_input = input('Website to scrape from: ')
url = 'https://' + url_input
added=[]

# takes url and directory section and returns status code and thread ID, writing emails found to file
def scrape(url_arg, dirs):
    end = []
    for i in dirs:
        r = requests.get(url_arg + '/' + i)
        # only runs if status code is 200 ie OK
        if r.status_code == 200:
            print("Directory {}, status code: {}".format(i, r.status_code))
            end.append(emailfinder(r.text))
        else:
            print("Directory {}, status code: {}".format(i, r.status_code))
    # to store emails that have already been added to avoid duplicates
    for v in end:
        for l in v:
            # duplication check
            if l in added:
                continue
            else:
                f.write(l + '\n')
                # add to added to avoid duplication
                added.append(l)
    # causes the thread to quit
    print("{} duplicate(s) found".format(len(added)))
    return
    
def emailfinder(text):
    return re.findall(r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.(?!jpeg|png|px)[a-zA-Z0-9-.]+)", text)
# added threading for each half of the directories
Thread1 = threading.Thread(group=None, target=scrape, args=(url, dirsread[:int((len(dirsread)/2))]))
Thread2 = threading.Thread(group=None, target=scrape, args=(url, dirsread[int((len(dirsread)/2)):]))
Thread1.start()
Thread2.start()
