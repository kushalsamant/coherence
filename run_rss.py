import requests  # Import the requests library for making HTTP requests
from feedgen.feed import FeedGenerator  # Import FeedGenerator from feedgen to create and manage RSS feeds
import time  # Import time module for sleep and time formatting functions

def generate_rss_from_product_pages(base_url, start_id=1, max_failures=10, output_file="rss.xml"):
    """
    Crawls product pages based on a numeric ID in the URL and generates an RSS feed.
    Saves the RSS.xml file after every successful product page found.

    :param base_url: URL pattern with a placeholder for product page ID 
                     (e.g., 'https://geometry.printify.me/products/{}')
    :param start_id: The starting product page ID
    :param max_failures: Stop after this many consecutive 404 responses
    :param output_file: The file path where the RSS feed is saved
    :return: FeedGenerator object containing the RSS feed entries
    """
    fg = FeedGenerator()  # Create an instance of FeedGenerator for building the RSS feed
    fg.title("RSS feed for Geometry Pop: The Printify Pop-Up Experience")  # Set the title of the RSS feed
    fg.link(href="https://geometry.printify.me")  # Set the main link associated with the feed
    fg.description("Step into the cutting-edge world of design with Geometry Pop: The Printify Pop-Up Experience. Curated directly from geometry.printify.me, this magazine brings together an exclusive collection of products showcasing bold geometric aesthetics in apparel, accessories, home décor, and more. Discover innovative prints, striking patterns, and creative designs that merge art with everyday functionality.")  # Provide a description for the feed
    
    product_page_id = start_id  # Initialize the product page ID counter to the starting value
    consecutive_failures = 1  # Initialize a counter for consecutive failed (404 or error) page fetches
    
    while consecutive_failures < max_failures:  # Loop until the number of consecutive failures reaches the maximum allowed
        url = base_url.format(product_page_id)  # Format the URL with the current product page ID
        print(f"Fetching {url}...")  # Print a message indicating the URL being fetched
        
        try:
            response = requests.get(url, timeout=10)  # Attempt to fetch the product page with a 10-second timeout
        except Exception as e:  # Handle any exceptions (e.g., network errors)
            print(f"Error fetching {url}: {e}")  # Print the error encountered during the fetch
            consecutive_failures += 1  # Increment the failure counter
            product_page_id += 1  # Move on to the next product page ID
            continue  # Skip the rest of the loop and continue with the next iteration
        
        if response.status_code == 200:  # If the product page is successfully fetched (HTTP 200 OK)
            print(f"Product Page found: {url}")  # Print confirmation that the product page was found
            consecutive_failures = 0  # Reset the consecutive failures counter because a valid page was found

            fe = fg.add_entry()  # Add a new entry to the RSS feed
            fe.title(f"Product Page {product_page_id}")  # Set the title of the RSS entry to include the product page ID
            fe.link(href=url)  # Set the link of the RSS entry to the product page URL
            pub_date = time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime())  # Format the current GMT time for the pubDate field
            fe.pubDate(pub_date)  # Assign the formatted publication date to the RSS entry
            fe.description(f"Product page for Product Page ID {product_page_id}")  # Set a description for the RSS entry
            
            fg.rss_file(output_file)  # Save the current state of the RSS feed to the output file
        elif response.status_code == 404:  # If the product page returns a 404 Not Found status
            print(f"Product Page not found (404): {url}")  # Print that the product page was not found
            consecutive_failures += 1  # Increment the consecutive failures counter
        else:  # If any other HTTP status code is returned
            print(f"Error: {url} returned status {response.status_code}")  # Print the unexpected status code
            consecutive_failures += 1  # Increment the consecutive failures counter
        
        product_page_id += 1  # Increment the product page ID to try the next page
        time.sleep(0.5)  # Pause for 0.5 seconds to avoid overwhelming the server with requests
    
    return fg  # Return the FeedGenerator object containing all the RSS feed entries

if __name__ == "__main__":  # This block runs if the script is executed directly
    base_url = "https://geometry.printify.me/products/{}"  # Define the base URL pattern with a placeholder for product page ID
    output_file = "rss.xml"  # Specify the name of the output RSS file
    fg = generate_rss_from_product_pages(base_url, start_id=1, max_failures=10, output_file=output_file)  # Generate the RSS feed from product pages
    print(f"RSS feed saved to {output_file}")  # Print a confirmation message indicating where the RSS feed was saved
