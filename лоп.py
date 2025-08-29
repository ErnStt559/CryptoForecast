import os
import re

# Specify the folder path containing your HTML files
folder_path = r"C:\Users\vilny\Desktop\crypto2.0"  # Replace with your actual folder path, e.g., C:\\Users\\YourName\\website or /home/user/website

# Patterns to remove
search_bar_pattern = r'<div class="search-bar">\s*<input id="search" placeholder="Search cryptocurrencies..." type="text"/>\s*</div>'
link_pattern = r'<a\s+[^>]*href="https://botsfolio\.com/crypto/[^"]*/price-prediction"[^>]*>.*?</a>'

# Function to process a single file
def remove_elements(file_path):
    try:
        # Read the file content
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # Remove the search bar div and botsfolio price prediction links
        new_content = re.sub(search_bar_pattern, '', content, flags=re.DOTALL)
        new_content = re.sub(link_pattern, '', new_content, flags=re.DOTALL)

        # Only write back if content has changed
        if new_content != content:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(new_content)
            print(f"Updated: {file_path}")
        else:
            print(f"No changes needed: {file_path}")
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

# Walk through the folder and process all HTML files
for root, dirs, files in os.walk(folder_path):
    for file in files:
        if file.endswith('.html'):
            file_path = os.path.join(root, file)
            remove_elements(file_path)

print("Processing complete.")