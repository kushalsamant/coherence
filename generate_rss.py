import os
import xml.etree.ElementTree as ET
from feedgen.feed import FeedGenerator

# Directory containing your sitemap files
SITEMAP_DIR = "sitemaps"
# Base URL for your website (update as needed)
BASE_URL = "https://geometry.printify.me/products"

# Initialize the RSS feed generator
fg = FeedGenerator()
fg.title("RSS feed for Geometry Pop: The Printify Pop-Up Experience")
fg.link(href=BASE_URL)
fg.description("Step into the cutting-edge world of design with Geometry Pop: The Printify Pop-Up Experience. Curated directly from geometry.printify.me, this magazine brings together an exclusive collection of products showcasing bold geometric aesthetics in apparel, accessories, home décor, and more. Discover innovative prints, striking patterns, and creative designs that merge art with everyday functionality.")

# Define the sitemap namespace (usually this is the standard one)
ns = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}

# Iterate over each XML file in the sitemap directory
for filename in os.listdir(SITEMAP_DIR):
    if filename.endswith(".xml"):
        filepath = os.path.join(SITEMAP_DIR, filename)
        try:
            tree = ET.parse(filepath)
            root = tree.getroot()
            # Loop through each <url> element and extract the <loc> value
            for url_elem in root.findall("ns:url", ns):
                loc_elem = url_elem.find("ns:loc", ns)
                if loc_elem is not None:
                    url = loc_elem.text.strip()
                    # Create an entry in the RSS feed
                    fe = fg.add_entry()
                    fe.title(url)  # You can use a different title if available
                    fe.link(href=url)
                    fe.description("Visit " + url)
        except Exception as e:
            print(f"Error processing {filename}: {e}")

# Save the generated RSS feed to rss.xml
rss_file = "rss.xml"
fg.rss_file(rss_file)
print("RSS feed generated successfully: " + rss_file)
