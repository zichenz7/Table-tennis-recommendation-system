import requests
from bs4 import BeautifulSoup
import pandas as pd
import time


def get_rubber_data():
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'cache-control': 'max-age=0',
        'sec-ch-ua': '"Chromium";v="130", "Microsoft Edge";v="130", "Not?A_Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0',
        'referer': 'https://revspin.net/rubber/'
    }

    all_data = []
    page = 1

    while True:
        try:
            url = f'https://revspin.net/top-rubber/overall-desc.html?p={page}'
            print(f"\nCrawling Page {page} ...")

            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            table = soup.find('table', {'class': 'rubber-list'})

            if table is None:
                table = soup.find('table')

            if table is None or not table.find_all('tr')[1:]:
                print(f"Page {page} has no data, crawling is over")
                break

            # extract data
            page_data = []
            rows = table.find_all('tr')

            for row in rows[1:]:  # skip table head
                cols = row.find_all('td')
                if cols:
                    row_data = [col.text.strip() for col in cols]
                    page_data.append(row_data)

            if not page_data:
                print("no more data, crawling over")
                break

            all_data.extend(page_data)
            print(f"Page {page} successfully retrieves {len(page_data)} lines of data")

            page += 1
            time.sleep(2)

        except Exception as e:
            print(f"error while crawling page {page} : {str(e)}")
            break

    # column names
    columns = ['Rank', 'Rubber', 'Speed', 'Spin', 'Control', 'Tacky',
               'Weight', 'Sponge Hardness', 'Gears', 'Throw Angle',
               'Consistency', 'Durable', 'Overall', 'Ratings', 'Price']

    df = pd.DataFrame(all_data, columns=columns)

    # print total number of data crawled
    print(f"\n {len(df)} lines of data crawled")

    # save to a csv file
    df.to_csv('rubber_data.csv', index=False, encoding='utf-8-sig')
    print("data saved to rubber_data.csv")

    # print the first and last 5 lines as a preview
    print("\nfirst five lines：")
    print(df.head().to_string(index=False))
    print("\nlast five lines：")
    print(df.tail().to_string(index=False))

    return df


if __name__ == "__main__":
    df = get_rubber_data()