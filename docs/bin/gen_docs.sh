#!/bin/bash

# Check if output file is provided as argument
if [ $# -eq 0 ]; then
    echo "Usage: $0 <output_file>"
    echo "Example: $0 combined_docs.md"
    exit 1
fi

OUTPUT_FILE="$1"

# Clear the output file
> "$OUTPUT_FILE"

# Concatenate all markdown files in docs folder (sorted by name)
for md_file in ../*.md; do
    if [ -f "$md_file" ]; then
        echo "Adding $md_file..."
        cat "$md_file" >> "$OUTPUT_FILE"
        echo -e "\n" >> "$OUTPUT_FILE"  # Add newline between files
    fi
done

# Add the generated annotation docs
echo "Adding generated annotation docs..."
python gen_annotation_docs.py >> "$OUTPUT_FILE"

echo "Combined documentation written to $OUTPUT_FILE"