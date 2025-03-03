import requests  # Library to send HTTP requests
import json  # Library to handle JSON file operations
from bs4 import BeautifulSoup  # Library to parse HTML content
from urllib.parse import urljoin  # Utility to join relative URLs with base URLs
import time  # Library to introduce delays

class URLCrawler:
    def __init__(self, base_url, output_file="url.json", start_id=1):
        """
        Initialize the URL crawler with the base URL, output file, and starting ID.
        :param base_url: The base URL with a placeholder for the numeric ID (e.g., 'https://geometry.printify.me/products/{}')
        :param output_file: File to store visited URLs in alphanumerical order
        :param start_id: Starting product ID
        """
        self.base_url = base_url  # Base URL for product pages
        self.output_file = output_file  # File to save the crawled URLs
        self.current_id = start_id  # Starting product ID for crawling
        self.visited_urls = self.load_visited_urls()  # Load previously visited URLs from the output file
        self.api_call_count = 0  # Counter to track the number of API calls

    def load_visited_urls(self):
        """Load previously visited URLs from the JSON file."""
        try:
            # Open the JSON file and load its content into a set
            with open(self.output_file, "r", encoding="utf-8") as file:
                return set(json.load(file).get("urls", []))
        except (FileNotFoundError, json.JSONDecodeError):
            # Return an empty set if the file does not exist or cannot be read
            return set()

    def save_visited_urls(self):
        """Save visited URLs to the JSON file in alphanumerical order."""
        try:
            # Open the output file in write mode and dump sorted URLs into it
            with open(self.output_file, "w", encoding="utf-8") as file:
                sorted_urls = sorted(self.visited_urls)  # Sort URLs alphanumerically
                json.dump({"urls": sorted_urls}, file, indent=4)  # Write URLs in JSON format
        except Exception as e:
            # Print an error message if saving fails
            print(f"Error saving URLs to {self.output_file}: {e}")

    def fetch_page(self, url):
        """Fetch a page and return the response if valid."""
        self.api_call_count += 1  # Increment the API call counter
        try:
            # Send a GET request to the given URL with a 10-second timeout
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                # Return the page content if the status code is 200 (OK)
                print(f"Successfully fetched: {url}")
                return response.text
            elif response.status_code == 404:
                # Return None if the status code is 404 (Not Found)
                print(f"Page not found (404): {url}")
                return None
            else:
                # Print an error message for other status codes
                print(f"Failed to fetch {url}. Status code: {response.status_code}")
                return None
        except requests.RequestException as e:
            # Handle exceptions that occur during the request
            print(f"Error fetching {url}: {e}")
            return None

    def extract_links(self, page_content, base_url):
        """Extract all links from a page using BeautifulSoup."""
        soup = BeautifulSoup(page_content, "html.parser")  # Parse the HTML content
        links = set()  # Initialize a set to store extracted links

        # Find all anchor tags with href attributes
        for anchor in soup.find_all("a", href=True):
            # Convert relative URLs to absolute URLs using urljoin
            link = urljoin(base_url, anchor["href"])
            if link.startswith("http"):  # Ensure only full URLs are added
                links.add(link)

        return links  # Return the set of extracted links

    def crawl_page(self, page_id):
        """Crawl the page and save the URLs to the JSON file."""
        # Generate the product URL by formatting the base URL with the current page ID
        url = self.base_url.format(page_id)
        if url in self.visited_urls:
            # Skip crawling if the URL is already visited
            print(f"Skipping already visited URL: {url}")
            return

        print(f"Crawling: {url}")  # Log the crawling action
        page_content = self.fetch_page(url)  # Fetch the page content

        if page_content:
            # Extract links and add them to the visited set
            new_links = self.extract_links(page_content, url)
            self.visited_urls.update(new_links)  # Update the visited URLs set
            self.save_visited_urls()  # Save the updated URLs immediately

            # Optional: Pause after every 100 API calls to avoid server overload
            if self.api_call_count % 100 == 0:
                print("Pausing for 60 seconds after 100 API calls...")
                time.sleep(60)

    def start_crawl(self):
        """Start crawling from the given base URL."""
        while True:
            # Crawl the page with the current ID
            self.crawl_page(self.current_id)

            # Increment the page ID to move to the next product page
            self.current_id += 1


if __name__ == "__main__":
    # Base URL with a placeholder for the product ID
    base_url = "https://geometry.printify.me/products/{}"

    # Create a crawler instance starting from product ID 1
    crawler = URLCrawler(base_url, output_file="url.json", start_id=1)
    crawler.start_crawl()  # Start the crawling process
