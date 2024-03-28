# Import libraries
import os
import xml.etree.ElementTree as ET

# Define the folder path
folder_path = "tipitaka-xml/romn"

# Create an empty string to store the text content
text_content = ""

# Loop through each file in the folder
for file_name in os.listdir(folder_path):
    # Check if the file is an XML file
    if file_name.endswith(".xml"):
        # Parse the XML file
        tree = ET.parse(os.path.join(folder_path, file_name))
        # Get the root element
        root = tree.getroot()
        # Get the text content of the root element and its descendants
        text_content += "".join(root.itertext()) + "\n"

# Save the text content to a file sample_pali.txt
with open("sample_pali.txt", "w", encoding="utf-8") as file:
    file.write(text_content)

# Print a message to indicate success
print("Text content saved to sample_pali.txt")
