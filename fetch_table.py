import requests
from bs4 import BeautifulSoup

# URL of the webpage to fetch
url = 'https://www.highinterestsavings.ca/chart/'

# Send a GET request to the URL
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find the table in the HTML (Assuming the table has a class or id we can target)
    table = soup.find('table')  # Modify this selector based on actual HTML structure
    
    if table:
        # Extract table headers
        headers = []
        for th in table.find_all('th'):
            headers.append(th.text.strip())

        # Extract table rows
        rows = []
        for tr in table.find_all('tr')[1:]:  # Skip the header row
            cells = tr.find_all('td')
            row = [cell.text.strip() for cell in cells]
            rows.append(row)

        # Print the table headers and rows (for demonstration)
        print(headers)
        for row in rows:
            print(row)
    else:
        print('Table not found on the page.')
else:
    print(f'Failed to retrieve the webpage. Status code: {response.status_code}')
