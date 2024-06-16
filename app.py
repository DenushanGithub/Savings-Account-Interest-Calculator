from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def index():
    url = 'https://www.highinterestsavings.ca/chart/'
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find('table')

        if table:
            headers = [th.text.strip() for th in table.find_all('th')]
            rows = [[td.text.strip() for td in tr.find_all('td')] for tr in table.find_all('tr')[1:]]

            # Identify columns with no headers
            columns_to_remove = [index for index, header in enumerate(headers) if header == '']
            
            # Remove columns with no headers from headers
            headers = [header for header in headers if header != '']

            # Remove columns with no headers from each row
            for row in rows:
                for index in sorted(columns_to_remove, reverse=True):
                    row.pop(index)

            # Rename "CU" to "Credit Union" and "Excl" to "Exclusions"
            headers = ['Credit Union' if header == 'CU' else 'Exclusions' if header == 'Excl' else header for header in headers]

            # Sort rows by the "Rate" column in descending order
            rate_index = headers.index('Rate')
            rows.sort(key=lambda x: float(x[rate_index].strip('%')), reverse=True)

            # Add a new column for checkboxes
            headers.append('Compare')
            for row in rows:
                row.append('<input type="checkbox" class="rate-checkbox" data-rate="{}">'.format(row[rate_index]))
        else:
            headers = []
            rows = []
    else:
        headers = []
        rows = []

    table_html = render_table(headers, rows)

    return render_template('index.html', table_html=table_html)

def render_table(headers, rows):
    table = '<table border="1"><thead><tr>'
    table += ''.join(f'<th>{header}</th>' for header in headers)
    table += '</tr></thead><tbody>'
    for row in rows:
        table += '<tr>' + ''.join(f'<td>{cell}</td>' for cell in row) + '</tr>'
    table += '</tbody></table>'
    return table

if __name__ == '__main__':
    app.run(debug=True)
