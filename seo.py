import requests
from bs4 import BeautifulSoup
import csv
import re
import matplotlib.pyplot as plt

# Function to fetch HTML content of a webpage
def fetch_html(url):
    try:
        response = requests.get(url)
        return response.text
    except Exception as e:
        print("Error fetching HTML:", e)
        return None

# Function to extract title and meta description from HTML
def extract_metadata(html):
    try:
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.find('title').text.strip() if soup.find('title') else None
        meta_description = soup.find('meta', attrs={'name': 'description'})
        meta_description = meta_description['content'].strip() if meta_description else None
        return title, meta_description
    except Exception as e:
        print("Error extracting metadata:", e)
        return None, None

# Function to analyze keyword density
def analyze_keyword_density(html, keyword):
    try:
        soup = BeautifulSoup(html, 'html.parser')
        text = soup.get_text().lower()
        keyword_count = text.count(keyword.lower())
        total_words = len(text.split())
        density = (keyword_count / total_words) * 100
        return density
    except Exception as e:
        print("Error analyzing keyword density:", e)
        return None

# Function to analyze page speed
def analyze_page_speed(url):
    try:
        response = requests.get(url)
        return response.elapsed.total_seconds()
    except Exception as e:
        print("Error analyzing page speed:", e)
        return None

# Function to check mobile responsiveness
def check_mobile_responsiveness(html):
    try:
        soup = BeautifulSoup(html, 'html.parser')
        viewport = soup.find('meta', attrs={'name': 'viewport'})
        return viewport is not None
    except Exception as e:
        print("Error checking mobile responsiveness:", e)
        return None

# Function to check presence of structured data
def check_structured_data(html):
    try:
        soup = BeautifulSoup(html, 'html.parser')
        structured_data = soup.find_all('script', attrs={'type': 'application/ld+json'})
        return len(structured_data) > 0
    except Exception as e:
        print("Error checking structured data:", e)
        return None

# Function to extract email addresses from the webpage
def extract_emails(html):
    try:
        emails = re.findall(r'[\w\.-]+@[\w\.-]+', html)
        return emails
    except Exception as e:
        print("Error extracting emails:", e)
        return []

# Main function to execute the SEO analysis, export to CSV, and generate interactive charts
def main():
    url = input("Enter the URL of the website: ")
    keyword = input("Enter the keyword to analyze density: ")

    html = fetch_html(url)
    if html:
        title, meta_description = extract_metadata(html)
        keyword_density = analyze_keyword_density(html, keyword)
        page_speed = analyze_page_speed(url)
        mobile_responsive = check_mobile_responsiveness(html)
        structured_data = check_structured_data(html)
        emails = extract_emails(html)

        # Exporting results to CSV
        with open('seo_analysis_results.csv', 'w', newline='') as csvfile:
            fieldnames = ['URL', 'Title', 'Meta Description', 'Keyword', 'Keyword Density',
                          'Page Speed (s)', 'Mobile Responsive', 'Structured Data', 'Emails']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow({'URL': url, 'Title': title, 'Meta Description': meta_description,
                             'Keyword': keyword, 'Keyword Density': keyword_density,
                             'Page Speed (s)': page_speed, 'Mobile Responsive': mobile_responsive,
                             'Structured Data': structured_data, 'Emails': ', '.join(emails)})

        # Generating interactive charts
        labels = ['Keyword Density', 'Page Speed', 'Mobile Responsive', 'Structured Data']
        values = [keyword_density, page_speed, mobile_responsive, structured_data]

        plt.bar(labels, values)
        plt.title('SEO Analysis')
        plt.xlabel('Metrics')
        plt.ylabel('Values')
        plt.show()

        print("SEO analysis results exported to 'seo_analysis_results.csv'.")

if __name__ == "__main__":
    main()
