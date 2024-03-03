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
if os.path.isfile("data/qa_data_enriched.json"):
    with open("data/qa_data_enriched.json", encoding="utf-8") as f_in:
        with open("data/qa_data_enriched_backup.json", "w", encoding="utf-8") as f_out:
            for line in f_in:
                key = md5("\t".join([data["pre_text"], data["table"], data["post_text"]]))
                data = from_json(line)
                enriched_data[key] = data
                f_out.write(to_json(data) + "\n")

line_count = 0
with open("data/qa_data.json", encoding="utf-8") as f_in:
    with open("data/qa_data_enriched.json", "w", encoding="utf-8") as f_out:
        for line in f_in:
            data = from_json(line)
            key = md5("\t".join([data["pre_text"], data["table"], data["post_text"]]))
            print(f"{line_count} {key}")
            line_count += 1
            if key in enriched_data:
                f_out.write(to_json(enriched_data[key]) + "\n")
                f_out.flush()
                continue
            pre_text = re.sub(r"[\n\t\s]+", " ", data["pre_text"])
            table = re.sub(r"[\n\t\s]+", " ", data["table"])
            post_text = re.sub(r"[\n\t\s]+", " ", data["post_text"])
            qa_pairs = data["qa_pairs"]
            num_qa_pairs = len(qa_pairs)
            question_info = None
            question_header = None
            answer_info = None
            delimiter_info = None
            if num_qa_pairs == 1:
                question_info = "a question"
                question_header = "QUESTION:"
                answer_info = "answer"
                delimiter_info = ""
            elif num_qa_pairs == 2:
                question_info = "two questions"
                question_header = "QUESTIONS:"
                answer_info = "answers"
                delimiter_info = "tab delimited"
            else:
                raise ValueError(f"Unexpected number of qa_pairs")
            question_text = "\n".join([qa_pair["question"] for qa_pair in qa_pairs])
            data["openai_answers"] = get_response(
                f"Here is a document and {question_info} regarding the document. "
                f"Please respond with the numerical {answer_info} {delimiter_info}.\n\n"
                f"DOCUMENT: {pre_text}\n{table}\n{post_text}"
                f"{question_header}\n\n{question_text}")["choices"][0]["message"]["content"].strip()
            f_out.write(to_json(data) + "\n")
            f_out.flush()

if os.path.isfile("data/qa_data_enriched_backup.json"):
    os.remove("data/qa_data_enriched_backup.json")
