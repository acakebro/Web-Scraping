from bs4 import BeautifulSoup
import requests
from csv import writer
import time

secs = 5
url = "https://www.internsg.com/jobs/1/#isg-top"
page = requests.get(url)
# print(page) # This should return a response 200 --> one of the HTTP response status code codes
soup = BeautifulSoup(page.content, "html.parser")
print("soup parsed. Finding.....")
time.sleep(secs)
# lists = soup.find("div", class_="ast-row jobs-list py-3 px-3") # main box
print("Sections found")

print("Extracting data to csv....")
time.sleep(secs)
fileName = "latest_interns.csv"
with open(fileName, "w", encoding="utf-8") as f:  # encoding="utf8", newline="") as f:
    thewriter = writer(f)
    header = [
        "Date Posted",
        "Company",
        "Position",
        "Type",
        "Duration",
        "Link",
    ]
    thewriter.writerow(header)
    classes = [
        "ast-row list-even",
        "ast-row list-odd",
        "ast-row list-featured list-odd",
    ]
    lists = soup.find_all("div", class_=classes[0])
    for c in classes[1:]:
        # add on to the list of tags
        lists += soup.find_all("div", class_=c)

    for list in lists:
        # title = list.find("a", class_=False).text
        date = list.find("div", class_="ast-col-lg-1").text
        date = date[1:-2]
        date += " 22"  # date retrieved
        chunk = list.find("div", class_="ast-col-lg-3").text
        site = list.find("span").text
        company = chunk.replace(site, "")  # company retrieved
        position = list.a.text  # position retrieved
        link = list.a["href"]  # link retrieved
        type_ = list.find_all("span")[2].text
        duration = list.find("div", class_="job-listing-dt").text

        info = [
            date,
            company,
            position,
            type_,
            duration,
            link,
        ]  ## This is important because writer parses through it as a list
        # print(info)

        thewriter.writerow(info)

print(f"{fileName} successfully downloaded ")
# if __name__ == "__main__":
#     while True:
