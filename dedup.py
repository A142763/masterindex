import pandas as pd

# Read the text file into a DataFrame J:\PDF Library\filedb.txt
df = pd.read_csv('J:/PDF Library/filedb.txt', sep='\t', header=None, encoding='utf-8', names=['ufn', 'hash'])

# Sort the DataFrame by 'hash' column
df.sort_values(by='hash', inplace=True)

# Identify duplicates based on 'hash' column
df['dup'] = df.duplicated(subset='hash', keep=False).astype(int)

# Create a new DataFrame 'dups' with only duplicate records
dups = df[df['dup'] == 1]

# Output the 'dups' DataFrame as a file with tab-separated values, do not include the 3rd column (dup)
dups.to_csv('J:/PDF Library/dups.txt', sep='\t', header=False, index=False, columns=['ufn', 'hash'])
