import requests
from bs4 import BeautifulSoup
import time

PARSER = "html.parser"
url = "https://ffxiv.consolegameswiki.com/wiki/Job"
parent_url = "https://ffxiv.consolegameswiki.com"

page = requests.get(url)
soup = BeautifulSoup(page.content, PARSER)
looking_for_jobs_on_headers = soup.find_all("h4")
# test = [header.find("span", class_="mw-headline")["id"] for header in looking_for_jobs_on_headers]
# print(test[:-1])

job_actions = {}

def write_as_json():
    import json
    from datetime import datetime

    with open(f"job_actions.json", "w") as f:
        json.dump(job_actions, f)

def job_html_class(job):
    if job in ['Paladin', 'Warrior', 'Dark_Knight', 'Gunbreaker', ]:
        return "tanker-role actions table"
    elif job in ['White_Mage', 'Scholar', 'Astrologian', 'Sage', ]:
        return "healer-role actions table"
    elif job in ['Monk', 'Dragoon', 'Ninja', 'Samurai', 'Reaper',
                 'Bard', 'Machinist', 'Dancer', 'Black_Mage', 'Summoner', 'Red_Mage']:
        return "dps-role actions table"
    else:
        raise NotImplementedError

HEADERS = ['Action', 'Level', 'Type', 'MP', 'Casting', 'Recast', 'Description']

def get_my_actions():
    for header in looking_for_jobs_on_headers[:-1]:
        span_with_job_id = header.find("span", class_="mw-headline")
        job = span_with_job_id["id"]
        print(f"Starting {job}")
        t_0 = time.time()
        job_url = f"{parent_url}/wiki/{job}"
        job_actions[job] = []
        job_page = requests.get(job_url, timeout=None)
        job_soup = BeautifulSoup(job_page.content, PARSER)
        tables = job_soup.find_all("table")
        table = None
        for tabl in tables:
            try:
                class_ = tabl["class"]
                # print(class_)
                if "actions" in class_ and "table" in class_:
                    table = tabl
                    break
            except KeyError as _:
                print("Don't care")
                continue

        # print(table)
        # assert False
        row_data = table.find_all("tr")[1:]
        for row in row_data:
            offset = 0
            action_href = ""
            row_dict = {}
            for i, td in enumerate(row.find_all("td")):
                if i in [1, 2]:
                    offset += 1
                    continue
                j = i - offset
                data = ""
                if i == 0:
                    desired_a = td.find_all("a")[-1]
                    action_href = desired_a["href"]
                    data = desired_a.get_text()
                elif j == 6:
                    data = td.get_text().strip()
                    action_url = f"{parent_url}{action_href}"
                    action_page = requests.get(action_url)
                    action_soup = BeautifulSoup(action_page.content, PARSER)
                    blockquotes = action_soup.find("blockquote")
                    dl = blockquotes.find("dl")
                    if dl is not None:
                        dds = dl.find_all("dd")
                        for dd in dds:
                            data = f"{data} {dd.get_text().strip()}."
                else:
                    data = td.get_text()
                row_dict[HEADERS[i - offset]] = data.replace(u"\xa0", u" ").strip()
            job_actions[job].append(row_dict)
        t_1 = time.time()
        print(f"Done with {job} ")
        print(f"Scraping took {t_1 - t_0:.2f} seconds.\n")
    write_as_json()

if __name__ == "__main__":
    get_my_actions()