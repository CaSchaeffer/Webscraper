import requests
from bs4 import BeautifulSoup

# Define the base URL of the website
base_url = "https://avagrar.de"

# Define the values to search for on the Website
search_terms = ["Roundup", "Movento OD", "Kerb FLO"]

def get_product_url():
    # Dictionary to store search terms and corresponding links
    search_links_dict = {}

    # Loop through the search terms, searches for found value on the website
    for row_index, search_term in enumerate(search_terms, start=1):
        # Create the complete URL with the search term
        url = f"{base_url}/search?sSearch={search_term}"

        # Send an HTTP GET request to the URL
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the HTML content of the page
            soup = BeautifulSoup(response.text, "html.parser")

            # Find and extract the title of the product, productname
            product_title_element = soup.find("a", class_="product--title")

            # Check if the product_title_element is found
            if product_title_element:
                # Extract the link from the href attribute
                product_link = product_title_element.get("href")

                # Store the link in the dictionary
                search_links_dict[search_term] = product_link

                # Print or use the link as needed
                print(f"Link for search term '{search_term}': {product_link}")
            else:
                print(f"No product title found for search term '{search_term}'.")
        else:
            print(f"Failed to retrieve the web page for search term '{search_term}'. Status code:", response.status_code)
    
    # Return the dictionary with search terms and links
    return search_links_dict

def extract_product_info(search_links_dict):
    for search_term, product_link in search_links_dict.items():
        # Construct the complete product URL
        url = product_link

        # Send an HTTP GET request to the URL
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the HTML content of the page
            soup = BeautifulSoup(response.text, "html.parser")

            # Extract values from the dropdown menu
            select_field = soup.find("div", class_="product--configurator")
            if select_field:
                dropdown_values = [option.text.strip() for option in select_field.find_all("option")]
                print(f"Dropdown Values for search term '{search_term}': {dropdown_values}")
            else:
                print(f"No dropdown menu found for search term '{search_term}'.")

# Extract item number
            item_number_element = soup.find("ul", class_="product--base-info list--unstyled")  # Find the correct ul element
            if item_number_element:
                # Find the li element with the specified class
                li_element = item_number_element.find("li", class_="base-info--entry entry--sku")
                if li_element:
                    # Find the span within the li element and extract its content
                    item_number_element_value = li_element.find("span", itemprop="sku").text.strip()
                    print(f"Item Number: {item_number_element_value}")
                else:
                    print("No li element found with the specified class.")
            else:
                print("No ul element found with the specified class.")

        else:
            print(f"Failed to retrieve the product page for search term '{search_term}'. Status code:", response.status_code)

# Call the function to get the dictionary of search terms and links
search_links_dict = get_product_url()

# Call the function to extract product information using the dictionary
extract_product_info(search_links_dict)
