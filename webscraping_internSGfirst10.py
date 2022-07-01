from bs4 import BeautifulSoup
import requests
from csv import writer
import time


def find_jobs():
    pages = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]  # number of pages to loop through
    secs = 5  # wait time

    ## Creating csv file (Remember to indent code following the with statement to prevent I/O error)
    fileName = "latest_interns.csv"
    with open(
        fileName, "w", encoding="utf-8"
    ) as f:  # encoding="utf8", newline="") as f:
        thewriter = writer(f)
        header = ["Date Posted", "Company", "Position", "Type", "Duration", "Link"]
        thewriter.writerow(header)
        classes = [
            "ast-row list-even",
            "ast-row list-odd",
            "ast-row list-featured list-odd",
            "ast-row list-featured list-even",
        ]

        ## Looping through the different pages of the search site
        for i in pages:
            url = "https://www.internsg.com/jobs/" + str(i) + "/#isg-top"
            page = requests.get(url)
            # print(page) # This should return a response 200 --> one of the HTTP response status code codes
            soup = BeautifulSoup(page.content, "html.parser")

            print("soup parsed. Finding.....")
            time.sleep(secs)
            lists = soup.find_all("div", class_=classes[0])
            for c in classes[1:]:
                # add on to the list of tags
                lists += soup.find_all("div", class_=c)

            print("Extracting data to csv....")
            time.sleep(secs)
            for list in lists:
                # title = list.find("a", class_=False).text
                date = list.find("div", class_="ast-col-lg-1").text
                date = date.strip()
                date += " 22"  # date retrieved
                chunk = list.find("div", class_="ast-col-lg-3").text
                site = list.find("span").text
                company = chunk.replace(site, "")  # company retrieved
                position = list.a.text  # position retrieved
                link = list.a["href"]  # link retrieved
                type_ = list.find_all("span")[2].text  # type retrieved
                duration = list.find(
                    "div", class_="job-listing-dt"
                ).text  # duration retrieved

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
            print(f"{fileName} page {i} successfully downloaded ")


# script will only run again after 10 minutes for constant update.
if __name__ == "__main__":
    while True:
        find_jobs()
        time_wait = 10
        print(f"Waiting {time_wait} minutes...")
        time.sleep(time_wait * 60)
