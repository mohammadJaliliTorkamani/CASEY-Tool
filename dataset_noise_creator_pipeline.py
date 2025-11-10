import json
import os
import random

from noise_dead_code import DeadCodeInserter
from noise_dummy_var import DummyVarInserter
from noise_function_rename import FunctionRenamer
from noise_new_line import NoiseNewLine


class DatasetNoisePipeline:
    def __init__(self, sample_dataset_path: str, ref_dataset_path: str, output_dir: str = "./output"):
        self.sample_dataset_path = sample_dataset_path
        self.ref_dataset_path = ref_dataset_path
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

        self.NOISE_FUNCTIONS = {
            "noise_new-line": self.noise_new_line,
            "noise_comment": self.noise_comment,
            "noise_function-rename": self.noise_function_rename,
            "noise5_add-dummy_var": self.noise_add_dummy_var,
            "noise6_dead-code-insertion": self.noise_dead_code_insertion,
        }

    # ---------------- Noise functions ----------------
    def noise_new_line(self, methods, ext):
        return NoiseNewLine(ext).apply(methods)

    def noise_comment(self, methods, ext):
        noisy_methods = []
        comment_styles = {
            ".py": "#", ".rb": "#", ".c": "//", ".cpp": "//", ".java": "//",
            ".js": "//", ".ts": "//", ".go": "//", ".php": "//",
        }
        comment_token = comment_styles.get(ext, "#")
        for method in methods:
            lines = method.split("\n")
            if not lines:
                noisy_methods.append(method)
                continue
            line_index = random.randint(0, len(lines) - 1)
            lines[line_index] = lines[line_index] + f"  {comment_token} This method is vulnerable"
            noisy_methods.append("\n".join(lines))
        return noisy_methods

    def noise_function_rename(self, methods, ext):
        renamer = FunctionRenamer(ext)
        return [renamer.rename_functions(m) for m in methods]

    def noise_add_dummy_var(self, methods, ext):
        return DummyVarInserter(ext).insert_dummy_var(methods)

    def noise_dead_code_insertion(self, methods, ext):
        return DeadCodeInserter(ext).insert_dead_code(methods)

    # ---------------- Core pipeline ----------------
    def create_noisy_dataset(self):
        with open(self.sample_dataset_path, "r", encoding="utf-8") as f:
            records = json.load(f)

        output_records = []
        for record in records:
            new_entry = {"id": record.get("id")}
            ext = "." + record.get("lang").split(".")[1]
            base_methods = record.get("vulnerability", {}).get("method_level", [])[:]

            new_entry["0_noise"] = base_methods

            for i in range(1, 6):
                noisy_methods = base_methods[:]
                applied_noises = random.sample(list(self.NOISE_FUNCTIONS.keys()), i)

                # Apply them in order
                for noise in applied_noises:
                    noisy_methods = self.NOISE_FUNCTIONS[noise](noisy_methods, ext)

                new_entry[f"{i}_noises"] = {
                    "noises": applied_noises[:],
                    "noisy_code": noisy_methods
                }

            output_records.append(new_entry)

        noisy_dataset_path = os.path.join(self.output_dir, "noisy_dataset.json")
        with open(noisy_dataset_path, "w", encoding="utf-8") as f:
            json.dump(output_records, f, ensure_ascii=False, indent=4)

        return noisy_dataset_path

    def create_evaluation_datasets(self, noisy_dataset_path: str):
        with open(noisy_dataset_path, "r") as f:
            noisy_dataset = json.load(f)

        with open(self.ref_dataset_path, "r") as f:
            ref_dataset = json.load(f)

        ref_lookup = {item["id"]: item for item in ref_dataset}
        output_files = []

        for noise_level in range(0, 6):
            output_data = []
            noise_key = f"{noise_level}_noise" if noise_level == 0 else f"{noise_level}_noises"

            for noisy_item in noisy_dataset:
                noisy_id = noisy_item["id"]
                noise_value = noisy_item.get(noise_key) if noise_level == 0 else noisy_item.get(noise_key).get(
                    "noisy_code")

                ref_item = ref_lookup.get(noisy_id)
                if not ref_item:
                    continue

                output_item = {
                    "id": ref_item["id"],
                    "cve": ref_item.get("cve"),
                    "description": ref_item.get("description"),
                    "cwe": ref_item.get("cwe"),
                    "severity": ref_item.get("severity"),
                    "cvss_score": ref_item.get("cvss_score"),
                    "cvss_version": ref_item.get("cvss_version"),
                    "vulnerability": {
                        "file_level": ref_item["vulnerability"].get("file_level"),
                        "hunk_level": ref_item["vulnerability"].get("hunk_level"),
                        "method_level": noise_value
                    }
                }
                output_data.append(output_item)

            output_filename = os.path.join(self.output_dir, f"{noise_level}_noises_evaluation_dataset.json")
            with open(output_filename, "w") as f:
                json.dump(output_data, f, indent=2)

            output_files.append((noise_level, output_filename))

        return output_files

    def run(self):
        noisy_dataset_path = self.create_noisy_dataset()
        evaluation_files = self.create_evaluation_datasets(noisy_dataset_path)
        return evaluation_files
