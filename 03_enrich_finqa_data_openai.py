from helpers import *
import requests
import openai
import os

openai.organization = os.environ['openai_organization']
openai.api_key = os.environ['openai_api_key']


def make_post_request(request_url, headers, request_data):
    return requests.post(request_url,
                         data=json.dumps(request_data, ensure_ascii=True),
                         headers=headers)


def get_response(message: str):
    message = message[:15000]
    response = make_post_request("https://api.openai.com/v1/chat/completions", {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai.api_key}"
    }, {
        "model": "gpt-4",
        "messages": [{"role": "user", "content": f"{message}"}],
        "temperature": 0.9
    })
    return json.loads(response.content)


enriched_data = dict()
if os.path.isfile("data/finqa_data_enriched_openai.json"):
    with open("data/finqa_data_enriched_openai.json", encoding="utf-8") as f_in:
        with open("data/finqa_data_enriched_backup.json", "w", encoding="utf-8") as f_out:
            for line in f_in:
                data = from_json(line)
                enriched_data[create_instance_key(data)] = data
                f_out.write(to_json(data) + "\n")

line_count = 0
with open("data/finqa_data.json", encoding="utf-8") as f_in:
    with open("data/finqa_data_enriched_openai.json", "w", encoding="utf-8") as f_out:
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

if os.path.isfile("data/finqa_data_enriched_backup.json"):
    os.remove("data/finqa_data_enriched_backup.json")
