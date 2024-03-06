from helpers import *
import anthropic
import os

anthropic_api_key = os.environ['anthropic_api_key']

client = anthropic.Anthropic(api_key=anthropic_api_key)


def get_response(message: str):
    retry_count = 0
    while True:
        try:
            response = client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=4096,
                temperature=0.9,
                messages=[{
                    "role": "user",
                    "content": [{
                        "type": "text",
                        "text": message
                    }]
                }])
            return response.content[0].text
        except IndexError as e:
            retry_count += 1
            if retry_count > 5:
                raise ValueError(e)


enriched_data = dict()
if os.path.isfile("data/finqa_data_enriched_anthropic.json"):
    with open("data/finqa_data_enriched_anthropic.json", encoding="utf-8") as f_in:
        with open("data/finqa_data_enriched_anthropic_backup.json", "w", encoding="utf-8") as f_out:
            for line in f_in:
                data = from_json(line)
                enriched_data[create_instance_key(data)] = data
                f_out.write(to_json(data) + "\n")

line_count = 0
with open("data/finqa_data.json", encoding="utf-8") as f_in:
    with open("data/finqa_data_enriched_anthropic.json", "w", encoding="utf-8") as f_out:
        for line in f_in:
            data = from_json(line)
            key = create_instance_key(data)
            print(f"{line_count} {key}")
            line_count += 1
            if key in enriched_data:
                f_out.write(to_json(enriched_data[key]) + "\n")
                f_out.flush()
                continue
            body = create_message_body(data)
            data["response"] = get_response(body)
            f_out.write(to_json(data) + "\n")
            f_out.flush()

if os.path.isfile("data/finqa_data_enriched_anthropic_backup.json"):
    os.remove("data/finqa_data_enriched_anthropic_backup.json")
