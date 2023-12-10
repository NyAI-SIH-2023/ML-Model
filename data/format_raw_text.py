import re
import os

'''
    formats acts text by adding new lines after section endings
    source for acts : https://www.indiakanoon.org || https://www.indiacode.nic.in/
'''
def format_legal_text(input_text):
    section_pattern = re.compile(r'(\b\d+\.\s+[A-Z][^.]*\.)')

    # Find all matches of the pattern
    matches = section_pattern.findall(input_text)

    # Split the text based on section endings
    sections = re.split(section_pattern, input_text)

    # Join sections with new lines, preserving titles
    formatted_text = ''
    for i in range(len(sections)):
        if sections[i] in matches:
            formatted_text += sections[i]
        else:
            formatted_text += sections[i] + '\n' + '\n'

    return formatted_text
cwd = os.getcwd()
input_path = os.path.join(cwd,'raw data/delhi_rent_control.txt') #change input paths accordingly
output_path = os.path.join(cwd,'raw data/formatted_delhi_rent_control.txt')

with open(input_path, 'r') as file:
    input_text = file.read()

formatted_text = format_legal_text(input_text)

print(formatted_text)
with open(output_path, 'w') as file:
    file.write(formatted_text)

