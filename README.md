# ConvFinQAInsights

ConvFinQAInsights is a repository aimed at providing insights into financial question answering (FinQA) models using conversational AI techniques. The repository contains code for data preprocessing, model evaluation, and performance analysis. Additionally, it includes a research document detailing the findings and implications of the analysis, along with instructions on replicating the experiments.

## Features

- **Data Preprocessing**: Efficient mechanisms for preprocessing financial data, including parsing, cleaning, and formatting.
- **Model Evaluation**: Evaluation scripts for assessing the performance of FinQA models against annotated datasets.
- **Performance Analysis**: Tools for analyzing model performance metrics and generating insightful visualizations.
- **Research Document**: A comprehensive research document summarizing key findings, implications, and recommendations based on the analysis.

## Getting Started

### Prerequisites

Before running the code, ensure you have the following dependencies installed:

- Python 3.x
- Required Python packages (install via `pip`): `anthropic`, `openai`, `requests`, `numpy`, `glob`, `hashlib`, `json`, `math`, `re`

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/ConvFinQAInsights.git
    cd ConvFinQAInsights
    ```

2. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```
Certainly! Below is the revised USAGE section focusing on the specific files and their execution order:

### Usage

1. **Data Parsing**:
   The first step is to parse the FinQA dataset using the script `01_parse_finqa_data.py`. This script combines the `train.json` and `dev.json` data files from the original dataset. This merging process ensures correct handling for subsequent analysis. Run the following command to execute the parsing script:
   ```bash
   python 01_parse_finqa_data.py
   ```

2. **Data Enrichment**:
   After parsing the dataset, enrich the FinQA data using Anthropic and OpenAI models. Two scripts handle this enrichment process:
   - `02_enrich_finqa_data_anthropic.py`: Enriches the dataset using Anthropic models.
   - `03_enrich_finqa_data_openai.py`: Enriches the dataset using OpenAI's GPT-4 model.
   These scripts can be run in parallel to expedite the enrichment process.
   ```bash
   python 02_enrich_finqa_data_anthropic.py
   python 03_enrich_finqa_data_openai.py
   ```

3. **Results Analysis**:
   Once the data enrichment is complete, analyze the results for accuracy using the script `04_plot_finqa_results.py`. This script plots the FinQA model performance metrics and generates insightful visualizations for analysis.
   ```bash
   python 04_plot_finqa_results.py
   ```

By following the numerical order (01, 02, 03, 04), you ensure a systematic and streamlined execution of the entire FinQA analysis pipeline, from data parsing to results analysis.

4. **Research Document**: Read the research document [Tomoro AI - Insights from the ConvFinQA Dataset.pdf](Tomoro%20AI%20-%20Insights%20from%20the%20ConvFinQA%20Dataset.pdf) for detailed insights, findings, and recommendations.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Special thanks to [Anthropic](https://anthropic.com/) and [OpenAI](https://openai.com/) for providing access to their AI models and APIs.
