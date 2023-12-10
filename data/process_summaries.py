import re 
import os 
import pandas as pd

cwd = os.getcwd()
input_path_text = os.path.join(cwd,'raw data/formatted_delhi_rent_control.txt') #change input paths accordingly
input_path_sum = os.path.join(cwd,'raw data/summaries1_20_delhi_rent_control.txt')
output_path = os.path.join(cwd,'processed data/1_20_rent_summaries.csv')

with open(input_path_text, 'r') as file:
    inp = file.read()
with open(input_path_sum, 'r') as file:
    sums = file.read()

inps = inp.split('\n\n')

matches = re.findall(r'\[(\d+)\](.*?)\[/\1\]', sums, re.DOTALL)

result = {match[0]: match[1].strip() for match in matches}

# Print the results
inp_sum = list(result.values())

df = pd.DataFrame(columns=['original', 'summary'])

# Append data from the lists to the DataFrame
df['original'] = inps[1:21]
df['summary'] = inp_sum

# Display the DataFrame
df.to_csv(output_path, index=False)