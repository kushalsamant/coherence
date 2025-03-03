import os  # Library for interacting with the file system
import requests  # Library for sending HTTP requests
from bs4 import BeautifulSoup  # Library for parsing HTML content
from urllib.parse import urljoin  # Helper function to resolve relative URLs
import time  # For pausing execution and generating timestamps
import xml.etree.ElementTree as ET  # For creating and manipulating XML files
import json  # For reading and writing JSON data (used for checkpointing)


class ResumableXMLSitemapGenerator:
    def __init__(self, base_url, output_prefix="sitemap", output_dir="sitemap", checkpoint_file="checkpoint.json", segment_size=10000):
        """
        Initializes the sitemap generator.
        :param base_url: URL template with a placeholder for numeric IDs (e.g., 'https://example.com/products/{}').
        :param output_prefix: Prefix for the sitemap file names (e.g., 'sitemap').
        :param output_dir: Directory where sitemap files will be saved.
        :param checkpoint_file: File to save and load progress.
        :param segment_size: Maximum number of URLs per sitemap file.
        """
        self.base_url = base_url
        self.output_prefix = output_prefix
        self.output_dir = output_dir
        self.checkpoint_file = checkpoint_file
        self.segment_size = segment_size
        self.visited_urls = []  # List to hold URLs collected during crawling
        self.api_call_count = 0  # Counter to track the number of API calls

        # Ensure the output directory exists
        os.makedirs(self.output_dir, exist_ok=True)

        # Load progress (current page ID and file index) from the checkpoint file
        self.current_id, self.file_index = self.load_checkpoint()

    def load_checkpoint(self):
        """Loads the last saved progress from the checkpoint file."""
        try:
            with open(self.checkpoint_file, "r", encoding="utf-8") as file:
                checkpoint = json.load(file)
                return checkpoint.get("current_id", 1), checkpoint.get("file_index", 1)
        except (FileNotFoundError, json.JSONDecodeError):  # Handle cases where file doesn't exist or is invalid
            return 1, 1  # Default values if no checkpoint is found

    def save_checkpoint(self):
        """Saves the current progress (page ID and file index) to the checkpoint file."""
        try:
            with open(self.checkpoint_file, "w", encoding="utf-8") as file:
                json.dump({"current_id": self.current_id, "file_index": self.file_index}, file, indent=4)
        except Exception as e:
            print(f"Error saving checkpoint: {e}")  # Log errors if checkpoint saving fails

    def save_segmented_sitemap(self):
        """
        Saves collected URLs to an XML sitemap file in the specified output directory and starts a new segment.
        """
        # Generate the full path for the current segment
        filename = os.path.join(self.output_dir, f"{self.output_prefix}{self.file_index}.xml")
        
        # Create the XML structure for the sitemap
        urlset = ET.Element("urlset", xmlns="http://www.sitemap.org/schemas/sitemap/0.9")
        for url in sorted(self.visited_urls):  # Sort URLs for consistent ordering
            url_element = ET.SubElement(urlset, "url")  # Add a <url> element for each URL
            loc = ET.SubElement(url_element, "loc")
            loc.text = url  # Set the <loc> element to the URL
            lastmod = ET.SubElement(url_element, "lastmod")
            lastmod.text = time.strftime("%Y-%m-%d")  # Set the last modification date
            changefreq = ET.SubElement(url_element, "changefreq")
            changefreq.text = "daily"  # Set the change frequency to daily
            priority = ET.SubElement(url_element, "priority")
            priority.text = "0.8"  # Set a default priority value
        
        # Write the XML to the file
        tree = ET.ElementTree(urlset)
        tree.write(filename, encoding="utf-8", xml_declaration=True)
        print(f"Saved {len(self.visited_urls)} URLs to {filename}")

        # Reset the URL list for the next segment
        self.visited_urls.clear()
        self.file_index += 1  # Increment the file index

    def fetch_page(self, url):
        """Fetches a page's content via HTTP."""
        self.api_call_count += 1  # Increment the counter for API calls
        try:
            response = requests.get(url, timeout=10)  # Send an HTTP GET request with a timeout
            if response.status_code == 200:
                print(f"Successfully fetched: {url}")
                return response.text  # Return the page's content
            elif response.status_code == 404:
                print(f"Page not found (404): {url}")
                return None
            else:
                print(f"Failed to fetch {url}. Status code: {response.status_code}")
                return None
        except requests.RequestException as e:  # Handle network-related errors
            print(f"Error fetching {url}: {e}")
            return None

    def extract_links(self, page_content, base_url):
        """Extracts all links from the given page content."""
        soup = BeautifulSoup(page_content, "html.parser")  # Parse the HTML content
        links = set()

        # Find all anchor tags with href attributes
        for anchor in soup.find_all("a", href=True):
            link = urljoin(base_url, anchor["href"])  # Convert relative URLs to absolute
            if link.startswith("http"):  # Ensure only absolute URLs are added
                links.add(link)

        return links

    def crawl_page(self, page_id):
        """Crawls a single page by ID, collects links, and saves segments as needed."""
        url = self.base_url.format(page_id)  # Construct the URL for the page
        if url in self.visited_urls:  # Skip already visited URLs
            print(f"Skipping already visited URL: {url}")
            return

        print(f"Crawling: {url}")
        page_content = self.fetch_page(url)  # Fetch the page content

        if page_content:
            new_links = self.extract_links(page_content, url)  # Extract links from the page
            self.visited_urls.extend(new_links)  # Add new links to the visited list

            # Save a segment if the URL count reaches the threshold
            if len(self.visited_urls) >= self.segment_size:
                self.save_segmented_sitemap()

            # Pause after every 300 API calls to avoid overloading the server
            if self.api_call_count % 300 == 0:
                print("Pausing for 60 seconds after 300 API calls...")
                time.sleep(60)

    def start_crawl(self):
        """Starts the crawling process, resuming from the last saved checkpoint."""
        try:
            while True:
                self.crawl_page(self.current_id)  # Crawl the current page by ID

                # Save any remaining URLs in the current segment
                if len(self.visited_urls) > 0:
                    self.save_segmented_sitemap()

                # Save progress and increment the page ID
                self.save_checkpoint()
                self.current_id += 1
        except KeyboardInterrupt:  # Handle interruption gracefully
            print("Crawling interrupted. Saving progress...")
            self.save_checkpoint()


if __name__ == "__main__":
    # Base URL with a placeholder for the product ID
    base_url = "https://geometry.printify.me/products/{}"

    # Create and start the sitemap generator
    crawler = ResumableXMLSitemapGenerator(
        base_url, output_prefix="sitemap", output_dir="sitemap", checkpoint_file="checkpoint.json", segment_size=10000
    )
    crawler.start_crawl()  # Begin crawling
