import os  # For interacting with the file system (reading/writing files)
import time  # For generating timestamps and adding delays
import xml.etree.ElementTree as ET  # For parsing XML files (sitemap)
from urllib.parse import urljoin  # To resolve relative URLs (if needed)
import json  # For reading/writing JSON data (could be used for checkpointing if desired)
from feedgen.feed import FeedGenerator  # For creating and managing RSS feeds

class RSSFromsitemapGenerator:
    def __init__(self, sitemap_folder="sitemap", output_file="rss.xml"):
        """
        Initializes the RSS feed generator.
        :param sitemap_folder: Directory containing sitemap.xml files.
        :param output_file: The filename where the generated RSS feed will be saved.
        """
        self.sitemap_folder = sitemap_folder  # Folder containing sitemap XML files
        self.output_file = output_file  # Output RSS feed file
        self.fg = FeedGenerator()  # Initialize the FeedGenerator object
        
        # Set the basic metadata for the RSS feed
        self.fg.title("Our Printify Pop-Up Experience By Geometry")  # Feed title
        self.fg.link(href="https://geometry.printify.me")  # Primary link for the feed (usually your site)
        self.fg.description("Step into the cutting-edge world of design with Our Printify Pop-Up Experience By Geometry. Curated directly from geometry.printify.me, this magazine brings together an exclusive collection of products showcasing bold geometric aesthetics in apparel, accessories, home décor, and more. Discover innovative prints, striking patterns, and creative designs that merge art with everyday functionality.")  # Feed description
        
        # Add the self-referencing atom:link element for best practices
        # Replace the href value with the actual URL where the RSS feed is hosted.
        self.fg.link(href="http://yourdomain.com/rss.xml", rel="self", type="application/rss+xml")
    
    def generate_rss_from_sitemap(self):
        """Generates an RSS feed by parsing all sitemap.xml files in the sitemap folder."""
        # Define the namespace for sitemap (used in sitemap XML files)
        ns = {'ns': 'http://www.sitemap.org/schemas/sitemap/0.9'}
        total_urls = 0  # Counter to track total URLs processed
        
        # List all files in the sitemap folder
        for filename in os.listdir(self.sitemap_folder):
            # Process only XML files
            if filename.endswith(".xml"):
                filepath = os.path.join(self.sitemap_folder, filename)  # Full path to the sitemap file
                print(f"Processing sitemap file: {filepath}")
                try:
                    # Parse the XML file
                    tree = ET.parse(filepath)
                    root = tree.getroot()
                    
                    # Iterate over each <url> element in the sitemap using the defined namespace
                    for url_elem in root.findall("ns:url", ns):
                        # Find the <loc> element that contains the URL
                        loc_elem = url_elem.find("ns:loc", ns)
                        if loc_elem is not None:
                            url = loc_elem.text.strip()  # Get the URL text and remove any extra spaces
                            
                            # Create a new RSS feed entry for this URL
                            fe = self.fg.add_entry()
                            fe.title(url)  # Use the URL as the title (or customize if additional info is available)
                            fe.link(href=url)  # Set the link of the entry to the URL
                            fe.guid(url, permalink=True)  # Add a unique, permanent GUID (using the URL)
                            
                            # Set the publication date to the current GMT time (for this example)
                            pub_date = time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime())
                            fe.pubDate(pub_date)
                            
                            # Add a basic description for the entry (customize as needed)
                            fe.description(f"URL extracted from sitemap: {url}")
                            total_urls += 1  # Increment the URL counter
                except Exception as e:
                    # Log any errors encountered while processing the sitemap file
                    print(f"Error processing {filepath}: {e}")
        
        print(f"Total URLs processed: {total_urls}")
        # Save the aggregated RSS feed to the output file with pretty formatting enabled
        self.fg.rss_file(self.output_file, pretty=True)
        print(f"RSS feed saved to {self.output_file}")

if __name__ == "__main__":
    # Specify the folder containing your sitemap.xml files and the desired output RSS file
    generator = RSSFromsitemapGenerator(sitemap_folder="sitemap", output_file="rss.xml")
    # Generate the RSS feed by reading all sitemap files from the folder
    generator.generate_rss_from_sitemap()
