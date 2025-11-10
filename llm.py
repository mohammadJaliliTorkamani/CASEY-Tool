import re

import openai
import requests
from openai.types.chat import ChatCompletion

import constants

openai.api_key = constants.OPENAI_API_KEY

import constants


class LLM:
    def __init__(self):
        pass

    def inference_with_gpt(self, model_id, user_field, system_field):
        msg = [{'role': 'system', 'content': system_field}, {'role': 'user', 'content': user_field}]
        response = openai.chat.completions.create(model=model_id,
                                                  temperature=constants.LLM_TEMPERATURE,
                                                  top_p=constants.LLM_TOP_P, stream=False,
                                                  presence_penalty=constants.LLM_PRESENCE_PENALTY,
                                                  frequency_penalty=constants.LLM_FREQUENCY_PENALTY,
                                                  messages=[{'role': 'system', 'content': system_field},
                                                            {'role': 'user', 'content': user_field}]
                                                  )
        return self.extract_message(response)

    def inference_with_llama(self, model_id, user_field, system_field):
        payload = {
            "system": system_field,
            "user": user_field
        }

        try:
            response = requests.post(model_id, json=payload)
            response.raise_for_status()
            json_req = response.json()
            if 'response' in json_req:
                res = response.json().get('response')
                return self.extract_msg(res)
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

    def extract_msg(self, res):
        if not res:
            return None

        # Remove code fences and leading "json"
        cleaned = re.sub(r"^```[a-zA-Z]*\n?", "", res, flags=re.IGNORECASE)
        cleaned = re.sub(r"```", "", cleaned)
        cleaned = cleaned.strip()

        if cleaned.lower().startswith("json"):
            cleaned = cleaned[4:].strip()

        # Extract first {...} block (handles nested braces correctly)
        start = cleaned.find("{")
        if start == -1:
            return res

        depth = 0
        for i, ch in enumerate(cleaned[start:], start=start):
            if ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    return cleaned[start:i + 1]

        return res

    def infer(self, model_category, model_id, user_field, system_field):
        if model_category == 'gpt4':
            return self.inference_with_gpt(model_id, user_field, system_field)
        elif model_category == 'llama3':
            return self.inference_with_llama(model_id, user_field, system_field)

    def inference_with_description(self, record_desc, cvss_version, model_category, model_id):
        system_field = constants.LLM_SYSTEM_FIELD_FOR_VULNERABILITY_DETECTION_USING_BUG_DESCRIPTION % (
            str(cvss_version), str(cvss_version), str(cvss_version))
        user_field = constants.LLM_USER_FIELD_FOR_VULNERABILITY_DETECTION_USING_BUG_DESCRIPTION % (record_desc)
        return self.infer(model_category, model_id, user_field, system_field)

    def inference_with_description_and_file(self, record_desc, cvss_version, record_files, model_category, model_id):
        def format_files(files, delimiter="-----------"):
            lines = []
            for file in files:
                lines.append(f'file name: "{file["name"]}"')
                lines.append(f'file content: "{file["content"]}"')
            blocks = ["\n".join(lines[i:i + 2]) for i in range(0, len(lines), 2)]
            return f"\n{delimiter}\n".join(blocks)

        system_field = constants.LLM_SYSTEM_FIELD_FOR_VULNERABILITY_DETECTION_USING_BUG_DESCRIPTION_AND_FILE % (
            str(cvss_version), str(cvss_version), str(cvss_version))
        user_field = constants.LLM_USER_FIELD_FOR_VULNERABILITY_DETECTION_USING_BUG_DESCRIPTION_AND_FILE % (
            record_desc,
            format_files(record_files))

        return self.infer(model_category, model_id, user_field, system_field)

    def inference_with_description_and_method(self, record_desc, cvss_version, record_methods, model_category,
                                              model_id):
        def join_methods(methods, delimiter="-----------"):
            return f"\n{delimiter}\n".join(methods)

        system_field = constants.LLM_SYSTEM_FIELD_FOR_VULNERABILITY_DETECTION_USING_BUG_DESCRIPTION_AND_METHOD % (
            str(cvss_version), str(cvss_version), str(cvss_version))
        user_field = constants.LLM_USER_FIELD_FOR_VULNERABILITY_DETECTION_USING_BUG_DESCRIPTION_AND_METHOD % (
            record_desc,
            join_methods(record_methods))

        return self.infer(model_category, model_id, user_field, system_field)

    def inference_with_description_and_hunk(self, record_desc, cvss_version, record_hunks, model_category, model_id):
        def join_lines(lines, delimiter="-----------"):
            return f"\n{delimiter}\n".join(hunk["content"] for hunk in lines)

        system_field = constants.LLM_SYSTEM_FIELD_FOR_VULNERABILITY_DETECTION_USING_BUG_DESCRIPTION_AND_HUNK % (
            str(cvss_version), str(cvss_version), str(cvss_version))
        user_field = constants.LLM_USER_FIELD_FOR_VULNERABILITY_DETECTION_USING_BUG_DESCRIPTION_AND_HUNK % (
            record_desc,
            join_lines(record_hunks))

        return self.infer(model_category, model_id, user_field, system_field)

    def dg_inference_with_file(self, cvss_version, record_files, record_cwes, model_category, model_id):
        def format_files(files, delimiter="-----------"):
            lines = []
            for file in files:
                lines.append(f'file name: "{file["name"]}"')
                lines.append(f'file content: "{file["content"]}"')
            blocks = ["\n".join(lines[i:i + 2]) for i in range(0, len(lines), 2)]
            return f"\n{delimiter}\n".join(blocks)

        def format_cwes(cwes):
            return str(cwes)

        system_field = constants.LLM_SYSTEM_FIELD_FOR_DESCRIPTION_GENERATION_USING_FILE
        user_field = constants.LLM_USER_FIELD_FOR_DESCRIPTION_GENERATION_USING_FILE % (
            format_files(record_files), format_cwes(record_cwes))

        return self.infer(model_category, model_id, user_field, system_field)

    def dg_inference_with_method(self, cvss_version, record_methods, record_cwes, model_category,
                                 model_id):
        def join_methods(methods, delimiter="-----------"):
            return f"\n{delimiter}\n".join(methods)

        def format_cwes(cwes):
            return str(cwes)

        system_field = constants.LLM_SYSTEM_FIELD_FOR_DESCRIPTION_GENERATION_USING_METHOD
        user_field = constants.LLM_USER_FIELD_FOR_DESCRIPTION_GENERATION_USING_METHOD % (
            join_methods(record_methods), format_cwes(record_cwes))

        return self.infer(model_category, model_id, user_field, system_field)

    def dg_inference_with_hunk(self, cvss_version, record_hunks, record_cwes, model_category, model_id):
        def join_lines(lines, delimiter="-----------"):
            return f"\n{delimiter}\n".join(hunk["content"] for hunk in lines)

        def format_cwes(cwes):
            return str(cwes)

        system_field = constants.LLM_SYSTEM_FIELD_FOR_DESCRIPTION_GENERATION_USING_HUNK
        user_field = constants.LLM_USER_FIELD_FOR_DESCRIPTION_GENERATION_USING_HUNK % (
            join_lines(record_hunks), format_cwes(record_cwes))

        return self.infer(model_category, model_id, user_field, system_field)

    def extract_message(self, response: ChatCompletion) -> str | None:
        try:
            return response.choices[0].message.content
        except Exception:
            return None
