import os  # For interacting with the file system (e.g., reading sitemap files)
import xml.etree.ElementTree as ET  # For parsing XML files (sitemaps)
import requests  # For making HTTP requests to fetch product pages
from bs4 import BeautifulSoup  # For extracting titles and descriptions from product pages
from feedgen.feed import FeedGenerator  # For generating an RSS feed

class SitemapToRSS:
    def __init__(self, sitemap_folder="sitemap", output_file="rss.xml"):
        """
        Initializes the SitemapToRSS generator.
        :param sitemap_folder: Directory containing sitemap.xml files.
        :param output_file: The filename where the generated RSS feed will be saved.
        """
        self.sitemap_folder = sitemap_folder  # Directory that contains multiple sitemap XML files
        self.output_file = output_file  # Output file where the generated RSS feed will be saved
        self.fg = FeedGenerator()  # Initialize the FeedGenerator object to build the RSS feed

        # Set up metadata for the RSS feed
        self.fg.title("Our Printify Pop-Up Experience By Geometry")  # Title of the RSS feed
        self.fg.link(href="https://geometry.printify.me")  # Link to the main website
        self.fg.description(
            "Step into the cutting-edge world of design with Our Printify Pop-Up Experience By Geometry. "
            "Curated directly from geometry.printify.me, this magazine brings together an exclusive collection of "
            "products showcasing bold geometric aesthetics in apparel, accessories, home décor, and more. "
            "Discover innovative prints, striking patterns, and creative designs that merge art with everyday functionality."
        )  # Description of the RSS feed

        # Add an Atom self-link so aggregators know where to find the RSS feed
        self.fg.link(href="https://raw.githubusercontent.com/kushalsamant/kushalsamant.github.io/refs/heads/main/marketing/rss.xml", rel="self", type="application/rss+xml")

    def parse_sitemap(self, sitemap_path):
        """
        Parses a sitemap XML file and extracts product URLs.
        :param sitemap_path: Path to the sitemap XML file.
        :return: A list of extracted product URLs.
        """
        ns = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}  # Define the standard namespace for sitemaps
        urls = []  # List to store extracted URLs

        try:
            tree = ET.parse(sitemap_path)  # Load and parse the sitemap XML file
            root = tree.getroot()  # Get the root element of the XML tree

            # Iterate over all <url> elements in the sitemap
            for url_elem in root.findall("ns:url", ns):
                loc_elem = url_elem.find("ns:loc", ns)  # Find the <loc> element inside <url>
                if loc_elem is not None:  # Ensure the <loc> element exists
                    url = loc_elem.text.strip()  # Extract the URL
                    if "/product/" in url:  # Filter only product pages (ignore other links)
                        urls.append(url)  # Store the extracted product URL
        except Exception as e:
            print(f"Error parsing {sitemap_path}: {e}")  # Log errors if sitemap parsing fails
        return urls  # Return the list of extracted product URLs

    def fetch_page_info(self, url):
        """
        Fetches the product page and extracts the title and meta description.
        :param url: The URL of the product page.
        :return: A tuple containing (title, description).
        """
        try:
            response = requests.get(url, timeout=10)  # Fetch the product page with a timeout of 10 seconds
            if response.status_code == 200:  # If the request is successful
                soup = BeautifulSoup(response.text, "html.parser")  # Parse the HTML content using BeautifulSoup

                # Extract the title from the <title> tag in the page
                title = soup.title.string.strip() if soup.title else "No Title Available"

                # Extract the meta description from <meta name="description"> if available
                meta_desc = soup.find("meta", attrs={"name": "description"})
                description = meta_desc["content"].strip() if meta_desc and "content" in meta_desc.attrs else "No description available"

                return title, description  # Return extracted title and description
            else:
                print(f"Failed to fetch {url}. Status code: {response.status_code}")
                return "Untitled Product", "Description not found."  # Default values if request fails
        except requests.RequestException as e:  # Handle network-related exceptions
            print(f"Error fetching {url}: {e}")
            return "Error Fetching Page", "Network error occurred."  # Default values in case of failure

    def save_rss(self):
        """
        Saves the RSS feed to the output file immediately after processing each sitemap.
        This prevents data loss if the script is interrupted.
        """
        self.fg.rss_file(self.output_file, pretty=True)  # Write the RSS feed to the file with pretty formatting
        print(f"RSS feed updated and saved: {self.output_file}")  # Confirm that the RSS file has been saved

    def generate_rss_from_sitemaps(self):
        """
        Generates an RSS feed by extracting product URLs from all sitemap.xml files in the folder.
        """
        total_urls = 0  # Counter to track total URLs processed

        # Process all .xml files in the sitemap directory
        for filename in os.listdir(self.sitemap_folder):
            if filename.endswith(".xml"):  # Ensure we only process XML files
                sitemap_path = os.path.join(self.sitemap_folder, filename)  # Get the full path to the sitemap file
                print(f"Processing sitemap: {sitemap_path}")  # Print which file is being processed

                urls = self.parse_sitemap(sitemap_path)  # Extract product URLs from the sitemap
                total_urls += len(urls)  # Update the total URL count

                # Create RSS feed entries for each extracted URL
                for url in urls:
                    title, description = self.fetch_page_info(url)  # Fetch title and description from the product page

                    fe = self.fg.add_entry()  # Create a new RSS entry
                    fe.title(title)  # Set the title for the RSS entry
                    fe.link(href=url)  # Set the link for the RSS entry
                    fe.guid(url, permalink=True)  # Ensure each entry has a unique GUID (prevents duplicate detection)
                    fe.description(description)  # Set the description for the RSS entry

                # Save the RSS feed immediately after processing each sitemap file
                self.save_rss()

        print(f"Total products added to RSS: {total_urls}")  # Print the total number of URLs processed

if __name__ == "__main__":
    # Create an instance of the SitemapToRSS generator, specifying the sitemap folder and output RSS file
    generator = SitemapToRSS(sitemap_folder="sitemap", output_file="rss.xml")

    # Generate the RSS feed by processing all sitemap.xml files in the sitemap folder
    generator.generate_rss_from_sitemaps()
