# AI Text Summarizer

**Skill Nexis | LLM Development | Week 1 – Mini Project 1**

A Python-based AI Text Summarizer built using a pretrained Hugging Face model (`sshleifer/distilbart-cnn-12-6`). It accepts text input and generates a concise summary based on the requested length. It also handles empty and excessively long input and includes factual-accuracy evaluation using five examples.

## Features

- **Text summarization:** Generates summaries from user-provided text.
- **Summary length control:** Supports:
  - Short – approximately 30 words
  - Medium – approximately 60 words
  - Long – approximately 100 words
  - Custom word count
- **Input handling:**
  - Rejects empty or whitespace-only input with a clear error.
  - Returns very short input unchanged.
  - Splits long input into chunks, summarizes each chunk, and combines the results.
  - Rejects input exceeding 20,000 words.
- **Factual evaluation:** Includes an automatic check for unsupported numbers and names, along with manual evaluation.
- **Web interface:** Flask-based interface with summary-length options, example texts, word counts, and a copy button.
- **Testing:** Includes tests that can run without downloading the model.

## Project Structure

```text
AI-Text-Summarizer/
├── summarizer/
│   ├── __init__.py
│   └── core.py
├── app.py
├── web.py
├── templates/
│   └── index.html
├── evaluate.py
├── data/
│   └── examples.json
├── notebooks/
│   └── AI_Text_Summarizer.ipynb
├── tests/
│   ├── __init__.py
│   ├── test_summarizer.py
│   └── test_web.py
├── docs/
│   ├── assignment1.md
│   └── model_and_prompts.md
├── results/
├── requirements.txt
├── README.md
└── LICENSE
```

## Technologies Used

- Python
- Hugging Face Transformers
- PyTorch
- Pandas
- Flask
- Jupyter Notebook / Google Colab

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/Keerthi-0571/AI-Text-Summarizer.git
cd AI-Text-Summarizer
```

### 2. Create and activate a virtual environment

For Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install the required packages

```bash
pip install -r requirements.txt
```

The first run downloads the pretrained model from Hugging Face.

## Usage

### 1. Command Line

Summarize a text file:

```bash
python app.py --file article.txt --length short
```

Summarize text directly:

```bash
python app.py --text "Your long text here..." --length 50
```

### 2. Python

```python
from summarizer import summarize

print(summarize(my_text, length="medium"))
```

### 3. Jupyter Notebook

Open `notebooks/AI_Text_Summarizer.ipynb` in Google Colab or Jupyter Notebook and run all cells.

## Web Application

Start the Flask web application:

```bash
python web.py
```

Open the following address in your browser:

`http://127.0.0.1:5000`

Paste your text, select the summary length, and click **Summarize**. The application displays the generated summary and word count.

Press `Ctrl + C` in the terminal to stop the server.

## Evaluation

The summarizer was tested using five sample passages covering different topics.

### Evaluation Results

| ID | Topic | Summary Words | Automatic Check | Manual Verdict |
|---|---|---:|---|---|
| 1 | Science | 26 | OK | Minor issue |
| 2 | Business | 19 | OK | Minor issue |
| 3 | Technology | 21 | OK | Minor issue |
| 4 | Health | 37 | OK | Minor issue |
| 5 | Education | 36 | OK | Minor issue |

### Evaluation Notes

1. **Science:** Important details about the causes of reef recovery and its vulnerability were omitted.
2. **Business:** Employee impact, cost savings, and financial details were omitted.
3. **Technology:** Performance details, device limitations, and future voice support were omitted.
4. **Health:** Campaign activities, funding, and mobile clinic details were omitted.
5. **Education:** Cost savings, teacher vacancies, and childcare concerns were omitted. The second sentence was incomplete.

The automatic check did not flag unsupported numbers or names in these five summaries. Manual review identified omissions and a sentence-quality issue.

The automatic check is a basic heuristic and does not guarantee factual accuracy.

## Test Results

The project was tested using Python's `unittest` framework.

**Command executed:**

```bash
python -m unittest discover -s tests -v
```

**Results:**

- Total tests: 19
- Passed: 19
- Failed: 0
- Errors: 0

**Status: All tests passed successfully.**

## Run Tests

Run the test suite using:

```bash
python -m unittest discover -s tests -v
```

## Model and Prompts

The project uses the pretrained `sshleifer/distilbart-cnn-12-6` model from Hugging Face Transformers for abstractive text summarization.

Additional information about the model and prompts is available in:

`docs/model_and_prompts.md`

## Limitations

- The model is primarily trained on news articles, so summarization quality may vary for other types of text.
- Abstractive summaries may omit important details or misrepresent facts.
- Automatic factual checks cannot identify every possible factual error.
- Manual review is recommended to verify the accuracy and completeness of summaries.

## Author

**K S Keerthi**

**Skill Nexis – Generative AI & LLM Development**