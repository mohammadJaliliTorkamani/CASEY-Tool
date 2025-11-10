OPENAI_API_KEY = 'API KEY COMES HERE'
LLM_TEMPERATURE = 1
LLM_TOP_P = 1
LLM_PRESENCE_PENALTY = 0
LLM_FREQUENCY_PENALTY = 0
LLM_TRIAL_GAP_SECONDS = 3
LLM_NORMAL_MODEL = [{'category': 'gpt4', 'id': 'gpt-4o-mini'},
                    {'category': 'llama3', 'id': 'API END POINT COMES HERE'}]
GPT4_FINE_TUNED_MODELS = [{'fine_tune_type': 'description-level', 'category': 'gpt4',
                           'id': 'MODEL ID COMES HERE'},
                          {'fine_tune_type': 'description-file-level', 'category': 'gpt4',
                           'id': 'MODEL ID COMES HERE'},
                          {'fine_tune_type': 'description-method-level', 'category': 'gpt4',
                           'id': 'MODEL ID COMES HERE'},
                          {'fine_tune_type': 'description-hunk-level', 'category': 'gpt4',
                           'id': 'MODEL ID COMES HERE'}, ]
LLAMA3_FINE_TUNED_MODELS = [
    {'fine_tune_type': 'description-level', 'category': 'llama3', 'id': 'API END POINT COMES HERE'},
    {'fine_tune_type': 'description-file-level', 'category': 'llama3', 'id': 'API END POINT COMES HERE'},
    {'fine_tune_type': 'description-method-level', 'category': 'llama3', 'id': 'API END POINT COMES HERE'},
    {'fine_tune_type': 'description-hunk-level', 'category': 'llama3',
     'id': 'API END POINT COMES HERE'}, ]

DG_GPT4_FINE_TUNED_MODELS = [{'fine_tune_type': 'file-level', 'category': 'gpt4', 'id': 'MODEL ID COMES HERE'},
                             {'fine_tune_type': 'method-level', 'category': 'gpt4', 'id': 'MODEL ID COMES HERE'},
                             {'fine_tune_type': 'hunk-level', 'category': 'gpt4', 'id': 'MODEL ID COMES HERE'}, ]
DG_LLAMA3_FINE_TUNED_MODELS = [{'fine_tune_type': 'file-level', 'category': 'llama3',
                                'id': 'API END POINT COMES HERE'},
                               {'fine_tune_type': 'method-level', 'category': 'llama3',
                                'id': 'API END POINT COMES HERE'},
                               {'fine_tune_type': 'hunk-level', 'category': 'llama3',
                                'id': 'API END POINT COMES HERE'}, ]

LLM_SYSTEM_FIELD_FOR_VULNERABILITY_DETECTION_USING_BUG_DESCRIPTION = """You are an expert in assessing the severity of software vulnerabilities based on natural language descriptions.

Instructions:
1. Input:
   - Vulnerability description: You will receive a description of a potential software vulnerability.

2. Output:
   - Generate a JSON object with the following structure:
     {
       "is_vulnerable": boolean, // Indicates whether any software vulnerability is present. (If none, set to false)
       "is_security_vulnerable": boolean, // Indicates whether the vulnerability is a security vulnerability. (If none, set to false)
       "cwe": list of strings, // A list of Common Weakness Enumeration (CWE) IDs relevant to the described vulnerability. (If none, return an empty list [])
       "severity": string, // One of: "LOW", "MEDIUM", "HIGH", "CRITICAL", representing the CVSS severity level according to CVSS v%s. (If no vulnerability found, set to null)
       "cvss_score": float // CVSS score according to CVSS v%s. (If no vulnerability found, set to null)
     }

Additional Notes:
- If a security vulnerability is identified (e.g., CVE-type vulnerability based on predicted CWE IDs), determine and return the severity label and cvss score according to CVSS version %s.

Example Output:
If a security vulnerability is identified:
{
  "is_vulnerable": true,
  "is_security_vulnerable": true,
  "cwe": ["CWE-12", "CWE-77"],
  "severity": "HIGH",
  "cvss_score": 7.5
}

Important:
- The output must strictly conform to the specified JSON format.
- Do not include any explanations, additional fields, or text before or after the JSON output.
"""

LLM_USER_FIELD_FOR_VULNERABILITY_DETECTION_USING_BUG_DESCRIPTION = "Vulnerability description: %s"

LLM_SYSTEM_FIELD_FOR_VULNERABILITY_DETECTION_USING_BUG_DESCRIPTION_AND_FILE = """You are an expert in assessing the severity of software vulnerabilities based on natural language description and vulnerable code files.

Instructions:
1. Input:
   - Vulnerability description: You will receive a description of a potential software vulnerability.
   - Vulnerable code files: 
        You will receive the code file(s) name and content containing the potential software vulnerability.

2. Output:
   - Generate a JSON object with the following structure:
     {
       "is_vulnerable": boolean, // Indicates whether any software vulnerability is present. (If none, set to false)
       "is_security_vulnerable": boolean, // Indicates whether the vulnerability is a security vulnerability. (If none, set to false)
       "cwe": list of strings, // A list of Common Weakness Enumeration (CWE) IDs relevant to the described vulnerability. (If none, return an empty list [])
       "severity": string, // One of: "LOW", "MEDIUM", "HIGH", "CRITICAL", representing the CVSS severity level according to CVSS v%s. (If no vulnerability found, set to null)
       "cvss_score": float // CVSS score according to CVSS v%s. (If no vulnerability found, set to null)
     }

Additional Notes:
- If a security vulnerability is identified (e.g., CVE-type vulnerability based on predicted CWE IDs), determine and return the severity label and cvss score according to CVSS version %s.

Example Output:
If a security vulnerability is identified:
{
  "is_vulnerable": true,
  "is_security_vulnerable": true,
  "cwe": ["CWE-12", "CWE-77"],
  "severity": "HIGH",
  "cvss_score": 7.5
}

Important:
- The output must strictly conform to the specified JSON format.
- Do not include any explanations, additional fields, or text before or after the JSON output.
"""
LLM_USER_FIELD_FOR_VULNERABILITY_DETECTION_USING_BUG_DESCRIPTION_AND_FILE = "Vulnerability description: %s\nVulnerable code files:\n%s"

LLM_SYSTEM_FIELD_FOR_DESCRIPTION_GENERATION_USING_FILE = """You are an expert in software vulnerability analysis and technical documentation. Your task is to generate a clear and technically accurate vulnerability description based on the provided vulnerable code file content and CWE ids.

Instructions:

1. Input:
   - Vulnerable code files: 
        File(s) content that contains one or more vulnerabilities.
   - CWE ids: 
        CWE id(s) that have been found within vulnerable code files.
        

2. Output:
   - Generate a JSON object with the following structure:
     {
       "description": string // A natural language explanation of the vulnerability.
     }

Requirements for the "description" field:
- Clearly explain what the vulnerability is.
- Describe how the issue occurs in the code (e.g., unsanitized input, improper access control, buffer overflow).
- Optionally include potential consequences if the vulnerability is exploited.
- Use formal and objective language suitable for security reports or advisories.
- If there are multiple vulnerabilities, describe them in separate sentences or paragraphs within the same description string.
- Do not include any line numbers unless explicitly present in the input.

Example Output:
{
  "description": "The function executes operating system commands using unsanitized user input, which allows an attacker to inject arbitrary commands. This could lead to unauthorized command execution on the host system."
}

Important:
- The output must be a strictly valid JSON object with a single key: `description`.
- Do not include any explanatory text, formatting, or metadata outside the JSON object.
"""
LLM_USER_FIELD_FOR_DESCRIPTION_GENERATION_USING_FILE = "Vulnerable code files:\n%s\nCWE ids: %s"

LLM_SYSTEM_FIELD_FOR_VULNERABILITY_DETECTION_USING_BUG_DESCRIPTION_AND_METHOD = """You are an expert in assessing the severity of software vulnerabilities based on natural language description and vulnerable methods.

Instructions:
1. Input:
   - Vulnerability description: You will receive a description of a potential software vulnerability.
   - Vulnerable methods: 
        You will receive the method(s) containing the potential software vulnerability.

2. Output:
   - Generate a JSON object with the following structure:
     {
       "is_vulnerable": boolean, // Indicates whether any software vulnerability is present. (If none, set to false)
       "is_security_vulnerable": boolean, // Indicates whether the vulnerability is a security vulnerability. (If none, set to false)
       "cwe": list of strings, // A list of Common Weakness Enumeration (CWE) IDs relevant to the described vulnerability. (If none, return an empty list [])
       "severity": string, // One of: "LOW", "MEDIUM", "HIGH", "CRITICAL", representing the CVSS severity level according to CVSS v%s. (If no vulnerability found, set to null)
       "cvss_score": float // CVSS score according to CVSS v%s. (If no vulnerability found, set to null)
     }

Additional Notes:
- If a security vulnerability is identified (e.g., CVE-type vulnerability based on predicted CWE IDs), determine and return the severity label and cvss score according to CVSS version %s.

Example Output:
If a security vulnerability is identified:
{
  "is_vulnerable": true,
  "is_security_vulnerable": true,
  "cwe": ["CWE-12", "CWE-77"],
  "severity": "HIGH",
  "cvss_score": 7.5
}

Important:
- The output must strictly conform to the specified JSON format.
- Do not include any explanations, additional fields, or text before or after the JSON output.
"""
LLM_USER_FIELD_FOR_VULNERABILITY_DETECTION_USING_BUG_DESCRIPTION_AND_METHOD = "Vulnerability description: %s\nVulnerable methods:\n%s"

LLM_SYSTEM_FIELD_FOR_DESCRIPTION_GENERATION_USING_METHOD = """You are an expert in software vulnerability analysis and technical documentation. Your task is to generate a clear and technically accurate vulnerability description based on the provided vulnerable methods and CWE ids.

Instructions:

1. Input:
   - Vulnerable methods: 
        Methods that contains one or more vulnerabilities.
   - CWE ids: 
        CWE id(s) that have been found within vulnerable methods.

2. Output:
   - Generate a JSON object with the following structure:
     {
       "description": string // A natural language explanation of the vulnerability.
     }

Requirements for the "description" field:
- Clearly explain what the vulnerability is.
- Describe how the issue occurs in the code (e.g., unsanitized input, improper access control, buffer overflow).
- Optionally include potential consequences if the vulnerability is exploited.
- Use formal and objective language suitable for security reports or advisories.
- If there are multiple vulnerabilities, describe them in separate sentences or paragraphs within the same description string.
- Do not include any line numbers unless explicitly present in the input.

Example Output:
{
  "description": "The function executes operating system commands using unsanitized user input, which allows an attacker to inject arbitrary commands. This could lead to unauthorized command execution on the host system."
}

Important:
- The output must be a strictly valid JSON object with a single key: `description`.
- Do not include any explanatory text, formatting, or metadata outside the JSON object.
"""
LLM_USER_FIELD_FOR_DESCRIPTION_GENERATION_USING_METHOD = "Vulnerable methods:\n%s\nCWE ids: %s"

LLM_SYSTEM_FIELD_FOR_VULNERABILITY_DETECTION_USING_BUG_DESCRIPTION_AND_HUNK = """You are an expert in assessing the severity of software vulnerabilities based on natural language description and vulnerable code lines (hunks).

Instructions:
1. Input:
   - Vulnerability description: You will receive a description of a potential software vulnerability.
   - Vulnerable lines: 
        You will receive the lines containing the potential software vulnerability.

2. Output:
   - Generate a JSON object with the following structure:
     {
       "is_vulnerable": boolean, // Indicates whether any software vulnerability is present. (If none, set to false)
       "is_security_vulnerable": boolean, // Indicates whether the vulnerability is a security vulnerability. (If none, set to false)
       "cwe": list of strings, // A list of Common Weakness Enumeration (CWE) IDs relevant to the described vulnerability. (If none, return an empty list [])
       "severity": string, // One of: "LOW", "MEDIUM", "HIGH", "CRITICAL", representing the CVSS severity level according to CVSS v%s. (If no vulnerability found, set to null)
       "cvss_score": float // CVSS score according to CVSS v%s. (If no vulnerability found, set to null)
     }

Additional Notes:
- If a security vulnerability is identified (e.g., CVE-type vulnerability based on predicted CWE IDs), determine and return the severity label and cvss score according to CVSS version %s.

Example Output:
If a security vulnerability is identified:
{
  "is_vulnerable": true,
  "is_security_vulnerable": true,
  "cwe": ["CWE-12", "CWE-77"],
  "severity": "HIGH",
  "cvss_score": 7.5
}

Important:
- The output must strictly conform to the specified JSON format.
- Do not include any explanations, additional fields, or text before or after the JSON output.
"""
LLM_USER_FIELD_FOR_VULNERABILITY_DETECTION_USING_BUG_DESCRIPTION_AND_HUNK = "Vulnerability description:%s\nVulnerable lines:\n%s"

LLM_SYSTEM_FIELD_FOR_DESCRIPTION_GENERATION_USING_HUNK = """You are an expert in software vulnerability analysis and technical documentation. Your task is to generate a clear and technically accurate vulnerability description based on the provided vulnerable lines (hunks) and CWE ids.

Instructions:

1. Input:
   - Vulnerable lines: 
        Lines that contains one or more vulnerabilities.
   - CWE ids: 
        CWE id(s) that have been found within vulnerable lines.

2. Output:
   - Generate a JSON object with the following structure:
     {
       "description": string // A natural language explanation of the vulnerability.
     }

Requirements for the "description" field:
- Clearly explain what the vulnerability is.
- Describe how the issue occurs in the code (e.g., unsanitized input, improper access control, buffer overflow).
- Optionally include potential consequences if the vulnerability is exploited.
- Use formal and objective language suitable for security reports or advisories.
- If there are multiple vulnerabilities, describe them in separate sentences or paragraphs within the same description string.
- Do not include any line numbers unless explicitly present in the input.

Example Output:
{
  "description": "The function executes operating system commands using unsanitized user input, which allows an attacker to inject arbitrary commands. This could lead to unauthorized command execution on the host system."
}

Important:
- The output must be a strictly valid JSON object with a single key: `description`.
- Do not include any explanatory text, formatting, or metadata outside the JSON object.
"""
LLM_USER_FIELD_FOR_DESCRIPTION_GENERATION_USING_HUNK = "Vulnerable lines:\n%s\nCWE ids: %s"

DEFAULT_SEVERITY_VERSION_FOR_CVSS = 'V3.1'

EVALUATION_DATASET_PATH = 'JSON PATH COMES HERE'

PYTHON_EXTRACTOR_SCRIPT_PATH = 'extractors/python_method_extractor.py'
JS_EXTRACTOR_SCRIPT_PATH = 'extractors/js_parser.py'
JAVA_EXTRACTOR_SCRIPT_PATH = 'extractors/java_parser.py'
PHP_EXTRACTOR_SCRIPT_PATH = 'extractors/php_parser.py'
TS_EXTRACTOR_SCRIPT_PATH = 'extractors/ts_parser.py'
C_EXTRACTOR_SCRIPT_PATH = 'extractors/c_parser.py'
CPP_EXTRACTOR_SCRIPT_PATH = 'extractors/cpp_parser.py'
GO_EXTRACTOR_SCRIPT_PATH = 'extractors/go_parser.py'
RB_EXTRACTOR_SCRIPT_PATH = 'extractors/ruby_parser.py'

ANALYSIS_RADIUS = [0, 0.5, 1, 1.5]

TOTAL_DATASET_PATH = "total_dataset.json"

###### Note: DG refers to description generation

DATASET_SPLIT = False

VULNERABILITY_ASSESSMENT = True
DESCRIPTION_GENERATION = not VULNERABILITY_ASSESSMENT

BASE_LINE = False

# ALLOWED_MODELS = ['gpt4', 'llama3']
ALLOWED_MODELS = ['llama3']
# ALLOWED_EXPERIMENTS = ['description', 'description and file', 'description and method',
#                        'description and hunk']  # useful for having only one running llama model at hand

ALLOWED_EXPERIMENTS = ['description and method']  # useful for having only one running llama model at hand

# ALLOWED_EXPERIMENTS_DG = ['file', 'method', 'hunk']  # useful for having only one running llama model at hand
ALLOWED_EXPERIMENTS_DG = ['hunk']  # useful for having only one running llama model at hand

DATASET_SPLIT_RATIO = {'evaluation': 0.1, 'fine-tuning': {'training': 0.8, 'validation': 0.1}}

NOISE_CHECK_MANUAL_ANALYSIS_VULNERABILITY_DETECTION_MODE = True
SAMPLED_DATASET_FOR_NOISE_CHECK = 'JSON PATH COMES HERE'

MANUAL_ANALYSIS_NOISY_DATASETS = ['JSON PATHS COME HERE']

NO_NOISY_DATASET_REGENERATION_IN_MANUAL_ANALYSIS = True
