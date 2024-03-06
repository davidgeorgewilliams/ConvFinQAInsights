from collections import defaultdict
from helpers import *

# Define a dictionary to map model names to their respective data sources
sources = {
    "claude-3": "finqa_data_enriched_anthropic.json",
    "gpt-4": "finqa_data_enriched_openai.json"
}

# Initialize a nested defaultdict to store metrics for each model
metrics = defaultdict(lambda: defaultdict(float))

for source in sources:
    filename = sources[source]
    with open(f"data/{filename}", encoding="utf-8") as f_in:
        for line in f_in:
            data = from_json(line)
            qa_pairs = data["qa_pairs"]
            source_answers: List[Any] = list()
            source_response = data["response"]

            # Process source response to extract answers
            if len(qa_pairs) > 1:
                source_response = re.sub(r"\\\\n", " ", source_response)
                source_response = re.sub(r"\\t", " ", source_response)
                source_response = re.sub(r"\n", " ", source_response)
                source_answers.extend(re.findall(r"(\S+)", source_response,
                                                 re.DOTALL | re.IGNORECASE))
            else:
                source_answers.append(source_response)

            # Handle special cases where source response starts with specific text
            if source_response.startswith("The document"):
                source_answers.extend([None for _ in range(len(qa_pairs))])

            # Compare source answers with target answers and update metrics
            for i in range(len(qa_pairs)):
                source_answer = source_answers[i]
                target_answer = qa_pairs[i]['answer']

                # Convert yes/no answers to float if needed
                if is_yes_or_no_answer(qa_pairs[i]['answer']):
                    target_answer = str(yes_or_no_answer_to_float(qa_pairs[i]['answer']))
                if is_yes_or_no_answer(source_answers[i]):
                    source_answer = str(yes_or_no_answer_to_float(source_answers[i]))

                # If target answer is empty, use source answer
                if len(qa_pairs[i]['answer'].strip()) == 0:
                    target_answer = source_answer

                # Parse numerical values from answers
                target_value = parse_numerical_values(target_answer)[0]
                source_values = parse_numerical_values(source_answer)
                source_value = source_values[0] if len(source_values) else math.nan
                question = qa_pairs[i]['question']

                # Update metrics based on answer comparison
                if essentially_equals(target_value, source_value):
                    metrics[source]["correct"] += 1
                elif essentially_equals(abs(target_value), abs(source_value)):
                    metrics[source]["correct"] += 1
                elif essentially_equals(100 * abs(target_value), abs(source_value)):
                    metrics[source]["correct"] += 1
                elif essentially_equals(abs(target_value), 100 * abs(source_value)):
                    metrics[source]["correct"] += 1
                else:
                    metrics[source]["incorrect"] += 1

# Calculate and print the accuracy for each data source.
for source in sources:
    correct = metrics[source]["correct"]
    incorrect = metrics[source]["incorrect"]
    accuracy = correct / (correct + incorrect)
    print(f"Source {source}. Accuracy: {accuracy}.")
