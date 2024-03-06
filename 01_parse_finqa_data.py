# Import necessary helper functions and the regular expression module
import re

from helpers import from_json_file, glob_files, to_json

# Glob pattern to match all JSON files in the 'data/original' directory
data_files = glob_files("data/original/*.json")

# Open a new JSON file for writing processed data
with open("data/finqa_data.json", "w", encoding="utf-8") as f_out:
    # Iterate over each data file found in the directory
    for data_file in data_files:
        # Load instances (data points) from the current JSON file
        instances = from_json_file(data_file)
        # Process each instance individually
        for instance in instances:
            # Extract pre-text, post-text, and table information from the instance
            pre_text = instance["pre_text"]
            post_text = instance["post_text"]
            table = instance["table_ori"]

            # Initialize a list to hold question-answer pairs
            qa_pairs = []

            # Iterate through keys in the instance, sorted numerically if applicable
            for key in list(sorted(list(instance.keys()))):
                # Use a regular expression to identify question-answer pair keys
                match = re.search(r"^qa_?(\d+)?$", key)

                # If a matching key is found
                if match is not None:
                    # Check for question number anomalies (e.g., greater than 9, indicating a sorting issue)
                    q_num = match.group(1)
                    if q_num is not None:
                        if int(q_num) > 9:
                            raise ValueError("Sort broken")

                    # Append the question-answer pair to the list
                    qa_pairs.append({
                        "question": instance[key]["question"],
                        "answer": instance[key]["answer"]
                    })

            # Write the processed instance to the output file as a JSON string, followed by a newline
            f_out.write(to_json({
                "pre_text": " ".join(pre_text),  # Combine pre-text strings
                "table": "\n".join(["\t".join(row) for row in table]),  # Format the table as a tab-delimited string
                "post_text": " ".join(post_text),  # Combine post-text strings
                "qa_pairs": qa_pairs,  # Include the processed question-answer pairs
            }) + "\n")
