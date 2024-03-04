from helpers import from_json_file, glob_files, to_json
import re

data_files = glob_files("data/original/*.json")
with open("data/finqa_data.json", "w", encoding="utf-8") as f_out:
    for data_file in data_files:
        instances = from_json_file(data_file)
        for instance in instances:
            pre_text = instance["pre_text"]
            post_text = instance["post_text"]
            table = instance["table_ori"]
            qa_pairs = []
            for key in list(sorted(list(instance.keys()))):
                match = re.search(r"^qa_?(\d+)?$", key)
                if match is not None:
                    q_num = match.group(1)
                    if q_num is not None:
                        if int(q_num) > 9:
                            raise ValueError("Sort broken")
                    qa_pairs.append({
                        "question": instance[key]["question"],
                        "answer": instance[key]["answer"]
                    })
            f_out.write(to_json({
                "pre_text": " ".join(pre_text),
                "table": "\n".join(["\t".join(row) for row in table]),
                "post_text": " ".join(post_text),
                "qa_pairs": qa_pairs,
            }) + "\n")
