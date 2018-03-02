from bs4 import BeautifulSoup
import requests
import json
import datetime as dt

def extract_performances(soup):
    performances = []
    for table_wrap in soup.find_all('div', {"class": "row"}):
        event_name_element = table_wrap.find('div', {"class": "custom-table-title"})
        if event_name_element is not None:
            event_name = event_name_element.find('h3').text.strip()
            table = table_wrap.find('table')
            table_features = [feature.text.strip() for feature in table.find('thead').find_all('th')]
            table_features.append("EVENT")
            table_rows = [[data.text.strip() for data in row.find_all('td')] for row in table.find('tbody').find_all('tr')]
            table_performances = [dict(zip(table_features, table_row)) for table_row in table_rows]
            for table_performance in table_performances:
                table_performance["EVENT"] = event_name
            performances.extend(table_performances);
    return performances

def get_soup_for_page(page):
    req = requests.get(page)
    page_data = req.text
    soup = BeautifulSoup(page_data, "html5lib")
    return soup

def clean_performances(performances):
    for performance in performances:
        if "MEET DATE" in performance:
            old_date = performance["MEET DATE"]
            new_date = dt.datetime.strptime(old_date, '%b %d, %Y').strftime('%m/%d/%y')
            performance["MEET DATE"] = new_date
        if "ATHLETE" in performance:
            name = performance["ATHLETE"]
            [last_name, first_name] = name.split(", ")
            del performance["ATHLETE"]
            performance["FIRST NAME"] = first_name
            performance["LAST NAME"] = last_name
        if "" in performance:
            del performance[""]

if __name__ == "__main__":
    results = [
        {"season": "2014 Indoor", "link": "https://www.tfrrs.org/all_performances/MA_college_m_Tufts.html?list_hnd=1148&season_hnd=236"},
        {"season": "2014 Outdoor", "link": "https://www.tfrrs.org/all_performances/MA_college_m_Tufts.html?list_hnd=1251&season_hnd=256"},
        {"season": "2015 Indoor", "link": "https://www.tfrrs.org/all_performances/MA_college_m_Tufts.html?list_hnd=1429&season_hnd=276"},
        {"season": "2015 Outdoor", "link": "https://www.tfrrs.org/all_performances/MA_college_m_Tufts.html?list_hnd=1552&season_hnd=303"},
        {"season": "2016 Indoor", "link": "https://www.tfrrs.org/all_performances/MA_college_m_Tufts.html?list_hnd=1587&season_hnd=309"},
        {"season": "2016 Outdoor", "link": "https://www.tfrrs.org/all_performances/MA_college_m_Tufts.html?list_hnd=1587&season_hnd=336"},
        {"season": "2017 Indoor", "link": "https://www.tfrrs.org/all_performances/MA_college_m_Tufts.html?list_hnd=1793&season_hnd=346"},
        {"season": "2017 Outdoor", "link": "https://www.tfrrs.org/all_performances/MA_college_m_Tufts.html?list_hnd=1915&season_hnd=377"},
        {"season": "2018 Indoor", "link": "https://xc.tfrrs.org/all_performances/MA_college_m_Tufts.html?list_hnd=2120&season_hnd=388"}
    ]

    all_performances = []
    for result in results:
        print("Loading Season: ", result["season"])
        soup = get_soup_for_page(result["link"])
        page_performances = extract_performances(soup)
        all_performances.extend(page_performances)

    print("Cleaning Data")
    clean_performances(all_performances)

    output_filename = "data.json"
    with open(output_filename, 'w') as output_file:
        json.dump(all_performances, output_file)

    print("Complete")
