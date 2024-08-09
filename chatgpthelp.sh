#!/bin/bash

# Check if the input file is provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 [input_file]"
    exit 1
fi

# Check if the provided file exists
input_file="$1"
if [ ! -f "$input_file" ]; then
    echo "File not found: $input_file"
    exit 1
fi

# Read the contents of the input file
error_output=$(cat "$input_file")

# Create or empty the output file
output_file="output.txt"
echo -e "my error output '$error_output'\n" > "$output_file"

# Find all Python files in the current directory and subdirectories excluding "venv"
find . -name "*.py" ! -path "*/venv/*" | while read -r file; do
    if [ -f "$file" ]; then
        # Write the file name and its source code to the output file
        echo "this python file $file" >> "$output_file"
        cat "$file" >> "$output_file"
        echo -e "\n" >> "$output_file"  # Add a newline for better readability
    fi
done

# Open the output file
xdg-open "$output_file"

