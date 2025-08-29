import re
from bs4 import BeautifulSoup
import os

# Directory path
directory = r"C:\Users\vilny\Desktop\Новая папка (7)"

# List of auxiliary pages to exclude from "Read Next"
auxiliary_pages = ['index.html', 'articles.html', 'about.html', 'contact.html', 'privacy.html', 'terms.html']

# Function to minify HTML content
def minify_html(html_content):
    minified = re.sub(r'\s*\n\s*', '\n', html_content.strip())
    minified = re.sub(r'\s{2,}', ' ', minified)
    return minified

# Function to get list of HTML files from directory
def get_html_pages(directory):
    html_pages = []
    print(f"Scanning directory: {directory}")
    for filename in os.listdir(directory):
        is_html = filename.lower().endswith('.html')
        is_auxiliary = any(filename.lower() == aux_page.lower() for aux_page in auxiliary_pages)
        if is_html and not is_auxiliary:
            html_pages.append(filename)
            print(f"Added to html_pages: {filename}")
        else:
            print(f"Excluded from html_pages: {filename} (Is HTML: {is_html}, Is Auxiliary: {is_auxiliary})")
    return sorted(html_pages)

# Function to modify HTML
def modify_html(html_content, filename, html_pages):
    try:
        soup = BeautifulSoup(html_content, 'html.parser')

        # Remove <script src="script.js">
        script_tag = soup.find('script', src='script.js')
        if script_tag:
            script_tag.decompose()
            print(f"Removed script.js from {filename}")

        # Remove search bar
        search_bar = soup.find('div', class_='search-bar')
        if search_bar:
            search_bar.decompose()
            print(f"Removed search-bar div in {filename}")
        else:
            print(f"Warning: No search-bar div found in {filename}")

        # Remove external links but keep text
        for a_tag in soup.find_all('a'):
            if a_tag.get('href', '').startswith('http'):
                a_tag.replace_with(a_tag.text)
                print(f"Removed external link in {filename}: {a_tag.text}")

        # Ensure only "Home" in nav-links
        nav_links = soup.find('ul', class_='nav-links')
        if nav_links:
            nav_links.clear()
            new_li = soup.new_tag('li')
            new_a = soup.new_tag('a', href='index.html')
            new_a.string = 'Home'
            new_li.append(new_a)
            nav_links.append(new_li)
            print(f"Cleared nav-links and added Home link in {filename}")
        else:
            print(f"Warning: No nav-links found in {filename}")

        # Check footer-links
        footer_links = soup.find('ul', class_='footer-links')
        if not footer_links:
            print(f"Warning: No footer-links class found in {filename}")
        else:
            print(f"Confirmed footer-links class in {filename}")

        # Add "Read Next" section for non-auxiliary pages
        is_auxiliary = any(filename.lower() == aux_page.lower() for aux_page in auxiliary_pages)
        if not is_auxiliary:
            read_next_section = soup.find('section', id='read-next')
            if read_next_section:
                read_next_section.decompose()
            read_next_section = soup.new_tag('section', id='read-next')
            soup.find('body').append(read_next_section)

            new_h2 = soup.new_tag('h2')
            new_h2.string = "Read Next"
            read_next_section.append(new_h2)
            
            label = soup.new_tag('label')
            label.string = "Select a cryptocurrency to view its price prediction:"
            read_next_section.append(label)

            select = soup.new_tag('select', onchange="if (this.value) window.location.href=this.value")
            placeholder = soup.new_tag('option', value="", selected=True, disabled=True)
            placeholder.string = "Choose a cryptocurrency"
            select.append(placeholder)

            print(f"Adding dropdown options for {filename}:")
            for page in html_pages:
                if page.lower() != filename.lower():
                    page_name = page.replace('.html', '', 1).replace('.HTML', '', 1).replace('-', ' ').title()
                    option = soup.new_tag('option', value=page)
                    option.string = page_name
                    select.append(option)
                    print(f"  Added option: {page_name} ({page})")
                else:
                    print(f"  Skipped current file: {page}")

            read_next_section.append(select)
            print(f"Updated Read Next section in {filename} with {len([p for p in html_pages if p.lower() != filename.lower()])} options")

        return minify_html(str(soup))
    except Exception as e:
        return f"Error modifying {filename}: {str(e)}"

# Process all HTML files
def process_all_articles(directory):
    print(f"Checking directory: {directory}")
    if not os.path.exists(directory):
        print(f"Error: Directory '{directory}' does not exist.")
        return
    if not os.path.isdir(directory):
        print(f"Error: '{directory}' is not a directory.")
        return

    html_pages = get_html_pages(directory)
    print(f"Total HTML files for dropdown: {len(html_pages)}")
    print(f"html_pages list: {html_pages}")

    for filename in html_pages:
        file_path = os.path.join(directory, filename)
        print(f"Processing file: {filename}")
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                html = f.read()
            print(f"Read file: {filename}")
            modified_html = modify_html(html, filename, html_pages)
            if isinstance(modified_html, str) and not modified_html.startswith("Error"):
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(modified_html)
                print(f"Successfully modified and minified {filename}")
            else:
                print(f"Failed to modify {filename}: {modified_html}")
        except UnicodeDecodeError as e:
            print(f"Encoding error in {filename}: {str(e)}. Try a different encoding.")
        except Exception as e:
            print(f"Error processing {filename}: {str(e)}")

if __name__ == "__main__":
    process_all_articles(directory)