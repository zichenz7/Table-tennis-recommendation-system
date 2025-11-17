import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def get_blade_data():
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0',
        'referer': 'https://revspin.net/top-blade/overall-desc.html'
    }

    all_data = []
    page = 1

    while True:
        try:
            url = f'https://revspin.net/top-blade/overall-desc.html?p={page}'
            print(f"\nScraping page {page}...")

            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            table = soup.find('table', {'class': 'blade-list'})

            if table is None:
                table = soup.find('table')

            if table is None:
                print(f"No table found on page {page}, ending scrape.")
                break

            # Extract data
            page_data = []
            rows = table.find_all('tr')

            # If there are no data rows on this page, we have reached the last page
            if len(rows) <= 1:
                print("No more data available, ending scrape.")
                break

            for row in rows[1:]:  # Skip the header row
                cols = row.find_all('td')
                if cols:
                    row_data = [col.text.strip() for col in cols]
                    page_data.append(row_data)

            all_data.extend(page_data)
            print(f"Successfully scraped {len(page_data)} records from page {page}")

            page += 1
            time.sleep(2)  # Add delay to avoid requests being too fast

        except Exception as e:
            print(f"Error scraping page {page}: {str(e)}")
            break

    # Create DataFrame
    columns = ['Rank', 'Blade', 'Speed', 'Control', 'Stiffness',
               'Hardness', 'Consistency', 'Overall', 'Ratings', 'Price']
    df = pd.DataFrame(all_data, columns=columns)

    # Print total number of records
    print(f"\nTotal of {len(df)} records scraped")

    # Save to CSV file
    df.to_csv('blade_data.csv', index=False, encoding='utf-8-sig')
    print("Data saved to blade_data.csv")

    # Print first 5 and last 5 rows as preview
    print("\nFirst 5 rows of data:")
    print(df.head().to_string(index=False))
    print("\nLast 5 rows of data:")
    print(df.tail().to_string(index=False))

    return df

if __name__ == "__main__":
    df = get_blade_data()
