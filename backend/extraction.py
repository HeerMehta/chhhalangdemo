import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin

# Function to fetch and parse the HTML content of a webpage
def fetch_page_content(url):
    try:
        # Send an HTTP request to fetch the page content
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP errors
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

# Function to extract the relevant data (title, paragraphs, and links)
def extract_data(html_content, base_url):
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Extract title
    title = soup.title.string if soup.title else "No title found"
    
    # Extract paragraphs
    paragraphs = [p.get_text() for p in soup.find_all('p')]
    
    # Extract links (href attribute of 'a' tags)
    links = [urljoin(base_url, a['href']) for a in soup.find_all('a', href=True)]
    
    return {
        'title': title,
        'paragraphs': paragraphs,
        'links': links
    }

# Function to save extracted data to a text file
def save_data_to_file(data, file_name):
    with open(file_name, 'w', encoding='utf-8') as f:
        f.write(f"Title: {data['title']}\n\n")
        f.write("Paragraphs:\n")
        for para in data['paragraphs']:
            f.write(para + "\n\n")
        f.write("Links:\n")
        for link in data['links']:
            f.write(link + "\n")

# Main crawler function that combines fetching, extracting, and saving data
def crawl_website(url, output_file):
    print(f"Starting to crawl {url}")
    
    # Fetch the page content
    html_content = fetch_page_content(url)
    
    if html_content:
        # Extract the relevant data
        extracted_data = extract_data(html_content, url)
        
        # Save the data to a file
        save_data_to_file(extracted_data, output_file)
        print(f"Data saved to {output_file}")
    else:
        print("Failed to fetch or parse the webpage.")

# Example usage
if _name_ == "_main_":
    website_url = "https://www.geeksforgeeks.org/artificial-neural-networks-and-its-applications/"  # Replace with your target URL
    output_filename = "scraped_data.txt"
    
    crawl_website(website_url, output_filename)