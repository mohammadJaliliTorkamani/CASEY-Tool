# Master's Thesis Project

Thesis Title: LLM-Assisted CWE Identification, Severity Assessment, and Vulnerability Description Generation

Degree: Master of Science in Computer Science

Student: Mohammad Jalili Torkamani

University: University of Nebraska–Lincoln (UNL)

December 2025

---

### Datasets:

* Evaluation (test set): https://drive.google.com/file/d/1KR0a9qFLbR6ogGGTJXbi7gmxDk4QJcB7/view?usp=share_link

* Fine-tuning (training set): https://drive.google.com/file/d/1E1ODpkfD3PFPP7oRPJy209AL5_3LF44H/view?usp=sharing

* Fine-tuning (validation set): https://drive.google.com/file/d/1A2jm2OKecj8Ca6ut35Jw1hXNYy6l66QS/view?usp=share_link

* Fine-tuning (Task 1 - GPT version): https://drive.google.com/drive/folders/1I_DDT6HJG8C2joPAh4iiK--Lfg2_xGsI?usp=sharing

* Fine-tuning (Tas 1 - LLaMA version): https://drive.google.com/drive/folders/1aDl_v2YcyQzmt2YqrYKwqNpK54RNEGdH?usp=sharing

* Fine-tuning (Task 2 - GPT version): https://drive.google.com/drive/folders/1HKWyEY7co3TQ3IB4FOE1tBn5h1hmtaY9?usp=sharing

* Fine-tuning (Task 2 - LLaMA version): https://drive.google.com/drive/folders/1uYhjCEVISEvfQSCv_A1q_-3snwFZJFBR?usp=sharing
---

## Requirements

CASEY tool runs on any operating system with Python 3.12 or later. However, it has been tested on macOS and Ubuntu 24.04 LTS. Using PyCharm as the IDE is recommended.


## How to run?

First, create a virtual environment:

    python -m venv .venv
    source .venv/bin/activate   # On Linux/Mac
    .\.venv\Scripts\activate    # On Windows

Thent, install dependencies within the created virtual environment:

    pip install -r requirements.txt
   
Then, configure CASEY flags in `constants.py`:

| Flag                                                       | Description |
|------------------------------------------------------------|-------------|
| `OPENAI_API_KEY`                                           | API key |
| `DEFAULT_SEVERITY_VERSION_FOR_CVSS`                        | Preferred CVSS version (Default: v3.1) |
| `EVALUATION_DATASET_PATH`                                  | Path to the evaluation dataset |
| `DATASET_SPLIT`                                            | Enable if dataset split is required |
| `VULNERABILITY_ASSESSMENT`                                 | Enable if Task 1 is intended |
| `BASE_LINE`                                                | Enable if baseline inference is required (set endpoints on `LLM_NORMAL_MODEL`) |
| `ALLOWED_MODELS`                                           | Set allowed models to be used by the tool |
| `ALLOWED_EXPERIMENTS`                                      | Set allowed prompt configurations used in Task 1 |
| `ALLOWED_EXPERIMENTS_DG`                                   | Set allowed prompt configurations used in Task 2 |
| `GPT4_FINE_TUNED_MODELS`                                   | CASEY GPT-assisted setup models per granularity level (Task 1) |
| `LLAMA3_FINE_TUNED_MODELS`                                 | CASEY LLaMA-assisted setup models per granularity level (Task 1) |
| `DG_GPT4_FINE_TUNED_MODELS`                                | CASEY GPT-assisted setup models per granularity level (Task 2) |
| `DG_LLAMA3_FINE_TUNED_MODELS`                              | CASEY LLaMA-assisted setup models per granularity level (Task 2) |
| `NOISE_CHECK_MANUAL_ANALYSIS_VULNERABILITY_DETECTION_MODE` | Enable for manual noise analysis random sampling mode |
| `SAMPLED_DATASET_FOR_NOISE_CHECK`                          | Noisy dataset file path to sample from |
| `NO_NOISY_DATASET_REGENERATION_IN_MANUAL_ANALYSIS`         | Enable to skip noise regeneration (requires `MANUAL_ANALYSIS_NOISY_DATASETS` to point to existing datasets) |

Finally, run the tool:

    python main.py