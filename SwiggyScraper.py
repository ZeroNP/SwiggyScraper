import requests
from bs4 import BeautifulSoup
import json

out_file=open("swiggy_restaurants_pune.json","a")

for i in range(1,18):
    print("Accessing Page: ",i)
    content = requests.get("https://www.swiggy.com/pune?page={}".format(i)).content
    soup = BeautifulSoup(content,"lxml")
    divs = soup.findAll("div",attrs={"class":"_1HEuF"})
    for div in divs:
        details=dict()
        details['name']=div.find("div",attrs={"class":"nA6kb"}).text
        details['speciality']=div.find("div",attrs={"class":"_1gURR"}).text
        itemslist = []
        line = div.find("div",attrs={"class":"_3Mn31"})
        for item in line.findAll("div"):
            itemslist.append(item.text)
        details['rating'] = itemslist[0]
        details['delivery_time'] = itemslist[2]
        details['pricing'] = itemslist[4].replace("\u20b9","Rs. ")
        details['offer']=" "
        details['conditions']=" "
        if div.find("span",attrs={"class":"sNAfh"}):
            details['offer'] = div.find("span",attrs={"class":"sNAfh"}).text.replace("\u20b9","Rs. ")
        if div.find("div",attrs={"class":"_2IOFO"}):
            details['conditions'] = div.find("div",attrs={"class":"_2IOFO"}).text.replace("\u20b9","Rs. ")
        json.dump(details,out_file)
        out_file.write(",\n")
out_file.close()
