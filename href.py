
def format_href_for_static(file_name):
    from bs4 import BeautifulSoup
    from os import path
    # Open and read the HTML file
    directory = path.dirname(__file__)

    file_path = path.join(directory, file_name)

    with open(file_path, 'r') as file:
        content = file.read()

    # Parse the HTML content
    soup = BeautifulSoup(content, 'html.parser')

    # Update all <a> tags with href attributes
    for tag in soup.find_all(href=True):
        original_path = tag['href']
        tag['href'] = f"{{% static '{original_path}' %}}"

    # Save the updated content back to the file
    with open(file_path, 'w') as file:
        file.write(str(soup))

    print("All href paths updated to use {% static %}.")


def format_src_for_static(file_name):
    from bs4 import BeautifulSoup
    from os import path

    # Get the directory of the script
    directory = path.dirname(__file__)

    # Path to the HTML file
    file_path = path.join(directory, file_name)

    # Open and read the HTML file
    with open(file_path, 'r') as file:
        content = file.read()

    # Parse the HTML content
    soup = BeautifulSoup(content, 'html.parser')

    # Update all tags with src attributes
    for tag in soup.find_all(src=True):
        original_path = tag['src']
        tag['src'] = f"{{% static '{original_path}' %}}"

    # Save the updated content back to the file
    with open(file_path, 'w') as file:
        file.write(str(soup))

    print("All src paths updated to use {% static %}.")


format_src_for_static(file_name='what-we.html')
