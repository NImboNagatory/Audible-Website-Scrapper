from data.dict import link_morf
from requests import get, utils
from bs4 import BeautifulSoup
from csv import writer, reader, DictWriter, DictReader


def create_csv(data):
    movie_info = ["Book_name", "Rating", "Release_date", "Author",
                  "Narator", "Running_time", "Language"]
    with open('dict.csv', 'w') as csvfile:
        Writer = DictWriter(csvfile, fieldnames=movie_info)
        Writer.writeheader()
        Writer.writerows(data)


def prepare_bea_soup(website):
    soup = BeautifulSoup(website, 'html.parser')
    ul = soup.select("#product-list-a11y-skiplink-target > span > ul")
    lis = []
    for li in ul:
        inner_ul = li.select("#product-list-a11y-skiplink-target > span > ul > li")
        for inner_li in inner_ul:
            try:
                book_name = str(inner_li.select("h3 > a")[0].text)
            except IndexError:
                book_name = None
            try:
                rating = str(inner_li.select(
                    "#product-list-a11y-skiplink-target > span > ul > li > div > div.bc-col-responsive.bc-spacing-top-none > div > div.bc-col-responsive.bc-col-6 > div > div > span > ul > li.bc-list-item.ratingsLabel > span.bc-text.bc-pub-offscreen")[
                                 0].text)
            except IndexError:
                rating = None
            try:
                release_date = str(inner_li.select(
                    "#product-list-a11y-skiplink-target > span > ul > li > div > div.bc-col-responsive.bc-spacing-top-none > div > div.bc-col-responsive.bc-col-6 > div > div > span > ul > li.bc-list-item.releaseDateLabel > span")[
                                       0].text).replace(" ", "").replace("\n", "").split(":")[1]
            except IndexError:
                release_date = None
            try:
                author = inner_li.select(
                    "#product-list-a11y-skiplink-target > span > ul > li > div > div.bc-col-responsive.bc-spacing-top-none > div > div.bc-col-responsive.bc-col-6 > div > div > span > ul > li.bc-list-item.authorLabel > span > a")[
                    0].text
            except IndexError:
                author = None
            try:
                narator = inner_li.select(
                    "#product-list-a11y-skiplink-target > span > ul > li > div > div.bc-col-responsive.bc-spacing-top-none > div > div.bc-col-responsive.bc-col-6 > div > div > span > ul > li.bc-list-item.narratorLabel > span > a")[
                    0].text
            except IndexError:
                narator = None
            try:
                running_time = inner_li.select(
                    "#product-list-a11y-skiplink-target > span > ul > li > div > div.bc-col-responsive.bc-spacing-top-none > div > div.bc-col-responsive.bc-col-6 > div > div > span > ul > li.bc-list-item.runtimeLabel > span")[
                    0].text
            except IndexError:
                running_time = None
            try:
                language = inner_li.select(
                    "#product-list-a11y-skiplink-target > span > ul > li > div > div.bc-col-responsive.bc-spacing-top-none > div > div.bc-col-responsive.bc-col-6 > div > div > span > ul > li.bc-list-item.languageLabel > span")[
                    0].text.replace(" ", "").replace("\n", "").split(":")[1]
            except IndexError:
                language = None
            lis.append({"Book_name": book_name, "Rating": rating, "Release_date": release_date, "Author": author,
                    "Narator": narator, "Running_time": running_time, "Language": language})
    print(lis)
    return lis


def get_response():
    headers = utils.default_headers()

    headers.update(
        {
            'User-Agent': 'My User Agent 1.0',
        }
    )
    lis = []
    page_num = 1
    for char in range(0, 24):
        print(f"Processing page {page_num}")
        response = get(link_morf(char), headers=headers)
        data = prepare_bea_soup(response.text)
        lis += data
        print(f"Processing done on page {page_num}\n")
        page_num += 1

    create_csv(lis)


def read_csv():
    with open('dict.csv') as csv_file:
        input_file = DictReader(csv_file)
        for row in input_file:
            print(row)
        return input_file
