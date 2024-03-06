# Import all functions from the helpers module
# Import the os module to access environment variables
import os
# Import the anthropic module to use its functionalities
import anthropic
from helpers import *

# Retrieve the Anthropic API key from environment variables
anthropic_api_key = os.environ['anthropic_api_key']

# Initialize the Anthropic API client with the retrieved API key
client = anthropic.Anthropic(api_key=anthropic_api_key)


def get_response(message: str):
    """
    Get a response from the Anthropic API given a user message.

    Args:
        message (str): The user message for which a response is requested.

    Returns:
        str: The generated response from the Anthropic API.

    Raises:
        ValueError: If the maximum number of retries is exceeded due to empty response content.
    """
    # Initialize the retry count to track the number of retries
    retry_count = 0
    while True:
        try:
            # Send the message to the Anthropic API to get a response
            response = client.messages.create(
                model="claude-3-opus-20240229",  # Specify the model to use for generating the response
                max_tokens=4096,  # Set the maximum number of tokens (words) in the generated response
                temperature=0.9,  # Set the randomness of the response generation
                messages=[{
                    "role": "user",
                    "content": [{
                        "type": "text",
                        "text": message  # Pass the user's message to the model
                    }]
                }])
            # Extract and return the generated response from the API response
            return response.content[0].text
        # Catch IndexError raised when the response content is empty
        except IndexError as e:
            # Increment the retry count
            retry_count += 1
            # Check if the maximum retry count has been exceeded
            if retry_count > 5:
                # Raise a ValueError with the original exception if retries exceed the limit
                raise ValueError(e)


# This mechanism ensures safe and robust resumption of the enrichment process
# over the Anthropic API in case of network interruptions or failures due to token rate limits,
# which Anthropic enforces in a strict manner.
enriched_data = dict()
# Check if the enriched data file exists
if os.path.isfile("data/finqa_data_enriched_anthropic.json"):
    # If the file exists, open it for reading
    with open("data/finqa_data_enriched_anthropic.json", encoding="utf-8") as f_in:
        # Open a new file for writing as a backup
        with open("data/finqa_data_enriched_anthropic_backup.json", "w", encoding="utf-8") as f_out:
            # Iterate over each line in the input file
            for line in f_in:
                # Parse JSON data from the current line
                data = from_json(line)
                # Create a key for the current data instance
                instance_key = create_instance_key(data)
                # Add the parsed data to the enriched data dictionary
                enriched_data[instance_key] = data
                # Write the parsed data back to the backup file
                f_out.write(to_json(data) + "\n")

# Initialize line count for tracking progress
line_count = 0
with open("data/finqa_data.json", encoding="utf-8") as f_in:
    with open("data/finqa_data_enriched_anthropic.json", "w", encoding="utf-8") as f_out:
        # Iterate over each line in the input file
        for line in f_in:
            # Parse JSON data from the current line
            data = from_json(line)
            # Create a unique key for the current data instance
            key = create_instance_key(data)
            # Print progress information
            print(f"{line_count} {key}")
            # Increment line count
            line_count += 1
            # Check if the current data instance is already enriched
            if key in enriched_data:
                # If enriched, write the enriched data to the output file
                f_out.write(to_json(enriched_data[key]) + "\n")
                # Flush the buffer to ensure data is written immediately
                f_out.flush()
                # Move to the next iteration
                continue
            # If not enriched, create a message body for the current data
            body = create_message_body(data)
            # Get a response from the Anthropic API based on the message body
            data["response"] = get_response(body)
            # Write the enriched data to the output file
            f_out.write(to_json(data) + "\n")
            # Flush the buffer to ensure data is written immediately
            f_out.flush()

# Check if the backup file exists
if os.path.isfile("data/finqa_data_enriched_anthropic_backup.json"):
    # If it exists, remove the backup file
    os.remove("data/finqa_data_enriched_anthropic_backup.json")
