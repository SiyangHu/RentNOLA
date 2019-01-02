from bs4 import BeautifulSoup
import requests
import csv


# Crawling url
url = "http://bj.58.com/pinpaigongyu/pn/{page}/?minprice=2000_4000"

# Set initial page to 0
page = 0

# Set csv writer to record entries within acceptable price range
csv_file = open("rent.csv","w") 
csv_writer = csv.writer(csv_file, delimiter=',')

while True:
    page += 1
    print("fetch: ", url.format(page=page))
    response = requests.get(url.format(page=page))
    html = BeautifulSoup(response.text)
    house_list = html.select(".list > li")

    # Break when reach the end of the list
    if not house_list:
        break

    for house in house_list:
        house_title = house.select("h2")[0].string
        house_url = "http://bj.58.com/%s"%(house.select("a")[0]["href"])
        house_info_list = house_title.split()

        # Select the address for apartment, removing the name of the apartment
        if "公寓" in house_info_list[1] or "青年社区" in house_info_list[1]:
            house_location = house_info_list[0]
        else:
            house_location = house_info_list[1]

        house_money = house.select(".money")[0].select("b")[0].string
        csv_writer.writerow([house_title, house_location, house_money, house_url])

csv_file.close()