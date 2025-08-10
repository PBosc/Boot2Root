import os
import re

folder_path = 'ft_fun'
files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.pcap')]

# List to hold file contents and their order
file_contents_with_order = []

for file in files:
    with open(file, 'r') as f:
        lines = f.readlines()
        
        # Extract order number from the last line
        last_line = lines[-1].strip()
        match = re.search(r"//file(\d+)", last_line)
        
        if match:
            order = int(match.group(1))
            content = ''.join(lines[:-1])  # Exclude the last line
            file_contents_with_order.append((content, order))

# Sort by order number and print each file's content
for content, _ in sorted(file_contents_with_order, key=lambda x: x[1]):
    print(content)
