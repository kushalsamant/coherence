import requests  # Import the requests library for making HTTP requests to fetch product pages
from feedgen.feed import FeedGenerator  # Import FeedGenerator from the feedgen library to create and manage RSS feeds
import time  # Import the time module for sleep delays and time formatting functions

def generate_rss_from_product_pages(base_url, start_id=1, max_failures=10, output_file="rss.xml"):
    """
    Crawls product pages based on a numeric ID in the URL and generates an RSS feed.
    Saves the RSS.xml file after every successful product page found.
    
    A 60 seconds delay is added after every 300 product page attempts.
    
    Parameters:
      - base_url: A URL pattern with a placeholder for the product page ID (e.g., 'https://geometry.printify.me/products/{}')
      - start_id: The starting product page ID (default is 1)
      - max_failures: The process stops after this many consecutive 404 responses or errors (default is 10)
      - output_file: The file path where the RSS feed is saved (default is "rss.xml")
      
    Returns:
      - A FeedGenerator object containing all the RSS feed entries
    """
    fg = FeedGenerator()  # Create an instance of FeedGenerator to build the RSS feed
    fg.title("RSS feed for Geometry Pop: The Printify Pop-Up Experience")  # Set the title of the RSS feed
    fg.link(href="https://geometry.printify.me")  # Set the main link associated with the feed
    fg.description("Step into the cutting-edge world of design with Geometry Pop: The Printify Pop-Up Experience. Curated directly from geometry.printify.me, this magazine brings together an exclusive collection of products showcasing bold geometric aesthetics in apparel, accessories, home décor, and more. Discover innovative prints, striking patterns, and creative designs that merge art with everyday functionality.")  
    # Set the description of the RSS feed
    
    product_page_id = start_id  # Initialize the product page ID counter with the starting ID
    consecutive_failures = 1  # Initialize a counter for consecutive failures (HTTP 404 or other errors)
    count = 0  # Initialize a counter to track the total number of product page attempts

    # Continue looping until the number of consecutive failures reaches the maximum allowed
    while consecutive_failures < max_failures:
        url = base_url.format(product_page_id)  # Format the URL by inserting the current product page ID
        print(f"Fetching {url}...")  # Print a message to indicate which URL is being fetched

        try:
            response = requests.get(url, timeout=10)  # Attempt to fetch the product page with a 10-second timeout
        except Exception as e:  # Catch any exceptions (e.g., network errors)
            print(f"Error fetching {url}: {e}")  # Print the error message
            consecutive_failures += 1  # Increment the failure counter due to the error
            product_page_id += 1  # Move to the next product page ID
            count += 1  # Increment the overall count of attempts
            continue  # Skip the remaining code in this iteration and continue with the next product page

        if response.status_code == 200:  # If the page is successfully fetched (HTTP 200 OK)
            print(f"Product Page found: {url}")  # Print confirmation that the product page was found
            consecutive_failures = 0  # Reset the consecutive failures counter since a valid page was found

            fe = fg.add_entry()  # Add a new entry to the RSS feed
            fe.title(f"Product Page {product_page_id}")  # Set the entry's title using the product page ID
            fe.link(href=url)  # Set the entry's link to the URL of the product page
            # Format the current GMT time as a string for the publication date (pubDate) field
            pub_date = time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime())
            fe.pubDate(pub_date)  # Assign the formatted publication date to the RSS entry
            fe.description(f"Product page for Product Page ID {product_page_id}")  # Set a description for the RSS entry
            
            # Save the current state of the RSS feed to the output file in a formatted (pretty) manner
            fg.rss_file(output_file, pretty=True)
        elif response.status_code == 404:  # If the product page is not found (HTTP 404)
            print(f"Product Page not found (404): {url}")  # Print that the product page was not found
            consecutive_failures += 1  # Increment the consecutive failures counter
        else:  # For any other unexpected HTTP status codes
            print(f"Error: {url} returned status {response.status_code}")  # Print the status code error
            consecutive_failures += 1  # Increment the failure counter
        
        product_page_id += 1  # Increment the product page ID for the next iteration
        count += 1  # Increment the overall count of attempted pages
        
        # After every 300 product page attempts, pause for 60 seconds
        if count % 300 == 0:
            print("Processed 300 product pages. Waiting for 60 seconds...")
            time.sleep(60)  # Wait for 60 seconds
        
        time.sleep(0.5)  # Pause for 0.5 seconds between requests to avoid overwhelming the server
    
    return fg  # Return the FeedGenerator object containing all the added RSS entries

if __name__ == "__main__":  # If this script is executed directly (not imported as a module)
    base_url = "https://geometry.printify.me/products/{}"  # Define the base URL pattern with a placeholder for product page IDs
    output_file = "rss.xml"  # Specify the name of the output file for the RSS feed
    # Call the function to generate the RSS feed, starting at product page ID 1 and stopping after 10 consecutive failures
    fg = generate_rss_from_product_pages(base_url, start_id=1, max_failures=10, output_file=output_file)
    print(f"RSS feed saved to {output_file}")  # Print a confirmation message indicating where the RSS feed was saved
