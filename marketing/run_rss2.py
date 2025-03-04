import os
import xml.etree.ElementTree as ET
import requests
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator

class SitemapToRSS:
    def __init__(self, sitemap_folder="sitemap", output_file="rss.xml"):
        """
        Converts sitemap.xml files into an RSS feed.
        :param sitemap_folder: Directory containing sitemap.xml files.
        :param output_file: The filename where the generated RSS feed will be saved.
        """
        self.sitemap_folder = sitemap_folder  # Folder containing sitemap XML files
        self.output_file = output_file  # Output RSS feed file
        self.fg = FeedGenerator()  # Initialize FeedGenerator for RSS feed

        # Set RSS metadata
        self.fg.title("Our Printify Pop-Up Experience By Geometry")
        self.fg.link(href="https://geometry.printify.me")
        self.fg.description("Step into the cutting-edge world of design with Our Printify Pop-Up Experience By Geometry. Curated directly from geometry.printify.me, this magazine brings together an exclusive collection of products showcasing bold geometric aesthetics in apparel, accessories, home décor, and more. Discover innovative prints, striking patterns, and creative designs that merge art with everyday functionality.")

        # Add Atom self-link
        self.fg.link(href="https://kvshvl.in/marketing/rss.xml", rel="self", type="application/rss+xml")

    def parse_sitemap(self, sitemap_path):
        """Parses a sitemap XML file and extracts product URLs."""
        ns = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}  # Sitemap namespace
        urls = []  # List of extracted product URLs

        try:
            tree = ET.parse(sitemap_path)  # Load and parse the sitemap XML
            root = tree.getroot()

            for url_elem in root.findall("ns:url", ns):  # Iterate over all <url> elements
                loc_elem = url_elem.find("ns:loc", ns)  # Get <loc> element
                if loc_elem is not None:
                    url = loc_elem.text.strip()
                    if "/product/" in url:  # Filter only product pages
                        urls.append(url)
        except Exception as e:
            print(f"Error parsing {sitemap_path}: {e}")
        return urls

    def fetch_page_info(self, url):
        """Fetches the product page and extracts the title and meta description."""
        try:
            response = requests.get(url, timeout=10)  # Fetch the webpage
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")

                # Extract title
                title = soup.title.string.strip() if soup.title else "No Title"

                # Extract meta description
                meta_desc = soup.find("meta", attrs={"name": "description"})
                description = meta_desc["content"].strip() if meta_desc and "content" in meta_desc.attrs else "No description available"

                return title, description
            else:
                print(f"Failed to fetch {url}. Status code: {response.status_code}")
                return "Untitled Product", "Description not found."
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return "Error Fetching Page", "Network error occurred."

    def save_rss(self):
        """Saves the current RSS feed to the output file."""
        self.fg.rss_file(self.output_file, pretty=True)
        print(f"RSS feed saved as {self.output_file}")

    def generate_rss_from_sitemaps(self):
        """Generates an RSS feed by extracting product URLs from sitemaps."""
        total_urls = 0

        # Loop through sitemap XML files
        for filename in os.listdir(self.sitemap_folder):
            if filename.endswith(".xml"):
                sitemap_path = os.path.join(self.sitemap_folder, filename)
                print(f"Processing: {sitemap_path}")

                urls = self.parse_sitemap(sitemap_path)  # Extract product URLs
                total_urls += len(urls)

                # Add RSS entries for each URL
                for url in urls:
                    title, description = self.fetch_page_info(url)

                    fe = self.fg.add_entry()
                    fe.title(title)
                    fe.link(href=url)
                    fe.guid(url, permalink=True)
                    fe.description(description)

                # Save RSS immediately after processing each sitemap
                self.save_rss()

        print(f"Total products added to RSS: {total_urls}")

if __name__ == "__main__":
    generator = SitemapToRSS(sitemap_folder="sitemap", output_file="rss.xml")
    generator.generate_rss_from_sitemaps()
