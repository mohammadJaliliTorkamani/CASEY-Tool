import random
from datetime import datetime
from enum import Enum

import constants
import llm
import utils
from dataset_noise_creator_pipeline import DatasetNoisePipeline

EXECUTION_DATE_TIME = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")


class CWE_EvaluationResultEnum(str, Enum):
    IDENTICAL = 0
    GT_SUBSET_OF_PR = 1
    PR_SUBSET_OF_GT = 2
    EMPTY_PR = 3
    NULL_PR = 4
    NOT_OVERLAPPED = 5
    OVERLAPPED = 6

    def __str__(self) -> str:
        return f"{self.name}"


class Severity_EvaluationResultEnum(str, Enum):
    IDENTICAL = 0
    DIFFERENT = 1
    NULL_PR = 2

    def __str__(self) -> str:
        return f"{self.name}"


class IsVulnerable_EvaluationResultEnum(str, Enum):
    IDENTICAL = 0
    DIFFERENT = 1
    NULL_PR = 2

    def __str__(self) -> str:
        return f"{self.name}"


class IsSecurityVulnerable_EvaluationResultEnum(str, Enum):
    IDENTICAL = 0
    DIFFERENT = 1
    NULL_PR = 2

    def __str__(self) -> str:
        return f"{self.name}"


def description_generation():
    print("Loading dataset...")
    dataset = load_dataset(constants.EVALUATION_DATASET_PATH)

    print("\nBaseline experiments")
    if constants.BASE_LINE:
        for model_obj in constants.LLM_NORMAL_MODEL:
            model_category, model_id = model_obj['category'], model_obj['id']

            if model_category not in constants.ALLOWED_MODELS:
                print("Skipping ", model_category, "...")
                continue

            print(f"\n@@@@@@@@@@@@ Baseline LLM: {model_category} @@@@@@@@@@@@")

            if 'file' in constants.ALLOWED_EXPERIMENTS_DG:
                dg_file_results = dg_experiment_file(dataset, None, model_id, model_category)
                dg_file_statistics = dg_compute_statistics(dg_file_results)
                utils.save(EXECUTION_DATE_TIME, None, model_category, 'file',
                           dg_file_statistics, dg=True)
                print("************************")

            if 'method' in constants.ALLOWED_EXPERIMENTS_DG:
                dg_method_results = dg_experiment_method(dataset, None, model_id, model_category)
                dg_method_statistics = dg_compute_statistics(dg_method_results)
                utils.save(EXECUTION_DATE_TIME, None, model_category, 'method',
                           dg_method_statistics, dg=True)
                print("************************")

            if 'hunk' in constants.ALLOWED_EXPERIMENTS_DG:
                dg_hunk_results = dg_experiment_hunk(dataset, None, model_id, model_category)

                dg_hunk_statistics = dg_compute_statistics(dg_hunk_results)
                utils.save(EXECUTION_DATE_TIME, None, model_category, 'hunk',
                           dg_hunk_statistics, dg=True)
                print("************************")

        print("===========================")

    else:
        print("\nFine-tuning experiments")
        print("GPT4 fine-tuned model experiments")
        for model_obj in constants.DG_GPT4_FINE_TUNED_MODELS:
            model_category, model_fine_tune_type, model_id = model_obj['category'], model_obj['fine_tune_type'], \
                model_obj['id']

            if model_category not in constants.ALLOWED_MODELS:
                print("Skipping ", model_category, "|", model_fine_tune_type, "...")
                continue

            print(f"\n@@@@@@@@@@@@ GPT-4 Fine-tuned LLM: {model_category} @@@@@@@@@@@@")

            if 'file' in constants.ALLOWED_EXPERIMENTS_DG and model_fine_tune_type == 'file-level':
                dg_file_results = dg_experiment_file(dataset, model_fine_tune_type, model_id,
                                                     model_category)
                dg_file_statistics = dg_compute_statistics(dg_file_results)
                utils.save(EXECUTION_DATE_TIME, model_fine_tune_type, model_category, 'file',
                           dg_file_statistics, dg=True)
                print("************************")

            if 'method' in constants.ALLOWED_EXPERIMENTS_DG and model_fine_tune_type == 'method-level':
                dg_method_results = dg_experiment_method(dataset, model_fine_tune_type, model_id,
                                                         model_category)
                dg_method_statistics = dg_compute_statistics(dg_method_results)
                utils.save(EXECUTION_DATE_TIME, model_fine_tune_type, model_category, 'method',
                           dg_method_statistics, dg=True)
                print("************************")

            if 'hunk' in constants.ALLOWED_EXPERIMENTS_DG and model_fine_tune_type == 'hunk-level':
                dg_hunk_results = dg_experiment_hunk(dataset, model_fine_tune_type, model_id,
                                                     model_category)
                dg_hunk_statistics = dg_compute_statistics(dg_hunk_results)
                utils.save(EXECUTION_DATE_TIME, model_fine_tune_type, model_category, 'hunk',
                           dg_hunk_statistics, dg=True)
                print("************************")

        print("LLAMA-3 fine-tuned model experiments")
        for model_obj in constants.DG_LLAMA3_FINE_TUNED_MODELS:
            model_category, model_fine_tune_type, model_id = model_obj['category'], model_obj['fine_tune_type'], \
                model_obj['id']

            if model_category not in constants.ALLOWED_MODELS:
                print("Skipping ", model_category, "|", model_fine_tune_type, "...")
                continue

            print(f"\n@@@@@@@@@@@@ LLAMA-3 Fine-tuned LLM: {model_category} @@@@@@@@@@@@")
            if 'file' in constants.ALLOWED_EXPERIMENTS_DG and model_fine_tune_type == 'file-level':
                dg_file_results = dg_experiment_file(dataset, model_fine_tune_type, model_id,
                                                     model_category)
                dg_file_statistics = dg_compute_statistics(dg_file_results)
                utils.save(EXECUTION_DATE_TIME, model_fine_tune_type, model_category, 'file',
                           dg_file_statistics, dg=True)
                print("************************")

            if 'method' in constants.ALLOWED_EXPERIMENTS_DG and model_fine_tune_type == 'method-level':
                dg_method_results = dg_experiment_method(dataset, model_fine_tune_type, model_id,
                                                         model_category)
                dg_method_statistics = dg_compute_statistics(dg_method_results)
                utils.save(EXECUTION_DATE_TIME, model_fine_tune_type, model_category, 'method',
                           dg_method_statistics, dg=True)
                print("************************")

            if 'hunk' in constants.ALLOWED_EXPERIMENTS_DG and model_fine_tune_type == 'hunk-level':
                dg_hunk_results = dg_experiment_hunk(dataset, model_fine_tune_type, model_id,
                                                     model_category)
                dg_hunk_statistics = dg_compute_statistics(dg_hunk_results)
                utils.save(EXECUTION_DATE_TIME, model_fine_tune_type, model_category, 'hunk',
                           dg_hunk_statistics, dg=True)
                print("************************")


def load_dataset(evaluation_path):
    return utils.load_json_file(evaluation_path)


def compute_statistics(results):
    print("Computing statistics...")
    number_of_null_is_vulnerable_prediction = 0
    number_of_correct_is_vulnerable_prediction = 0
    number_of_incorrect_is_vulnerable_prediction = 0

    number_of_null_is_security_vulnerable_prediction = 0
    number_of_correct_is_security_vulnerable_prediction = 0
    number_of_incorrect_is_security_vulnerable_prediction = 0

    number_of_null_cwe_prediction = 0
    number_of_empty_cwe_prediction = 0
    number_of_identical_cwe_prediction = 0
    number_of_gt_subset_equal_pr_cwe_prediction = 0
    number_of_pr_subset_equal_gt_cwe_prediction = 0
    number_of_overlapped_cwe_prediction = 0
    number_of_not_overlapped_cwe_prediction = 0

    number_of_severity_null_prediction = 0
    number_of_severity_correct_prediction = 0
    number_of_severity_incorrect_prediction = 0

    number_of_cvss_score_null_prediction = 0
    number_of_cvss_score_proximity_prediction = {r: 0 for r in constants.ANALYSIS_RADIUS}

    number_of_identical_is_vulnerable_identical_is_security_vulnerable_identical_cwe_correct_severity_in_range_cvss_prediction = {
        r: 0 for r in constants.ANALYSIS_RADIUS}
    number_of_identical_is_vulnerable_identical_is_security_vulnerable_pr_subset_equal_gt_cwe_correct_severity_in_range_cvss_prediction = {
        r: 0 for r in constants.ANALYSIS_RADIUS}

    number_of_identical_is_vulnerable_identical_is_security_vulnerable_gt_subset_equal_pr_cwe_correct_severity_in_range_cvss_prediction = {
        r: 0 for r in constants.ANALYSIS_RADIUS}

    for result in results:
        if result['is_vulnerable_comparison'] == str(IsVulnerable_EvaluationResultEnum.NULL_PR):
            number_of_null_is_vulnerable_prediction += 1
        elif result['is_vulnerable_comparison'] == str(IsVulnerable_EvaluationResultEnum.IDENTICAL):
            number_of_correct_is_vulnerable_prediction += 1
        elif result['is_vulnerable_comparison'] == str(IsVulnerable_EvaluationResultEnum.DIFFERENT):
            number_of_incorrect_is_vulnerable_prediction += 1

        if result['is_security_vulnerable_comparison'] == str(IsSecurityVulnerable_EvaluationResultEnum.NULL_PR):
            number_of_null_is_security_vulnerable_prediction += 1
        elif result['is_security_vulnerable_comparison'] == str(IsSecurityVulnerable_EvaluationResultEnum.IDENTICAL):
            number_of_correct_is_security_vulnerable_prediction += 1
        elif result['is_security_vulnerable_comparison'] == str(IsSecurityVulnerable_EvaluationResultEnum.DIFFERENT):
            number_of_incorrect_is_security_vulnerable_prediction += 1

        if result['cwe_comparison'] == str(CWE_EvaluationResultEnum.NULL_PR):
            number_of_null_cwe_prediction += 1
        elif result['cwe_comparison'] == str(CWE_EvaluationResultEnum.EMPTY_PR):
            number_of_empty_cwe_prediction += 1
        elif result['cwe_comparison'] == str(CWE_EvaluationResultEnum.IDENTICAL):
            number_of_identical_cwe_prediction += 1
            number_of_pr_subset_equal_gt_cwe_prediction += 1
            number_of_gt_subset_equal_pr_cwe_prediction += 1
        elif result['cwe_comparison'] == str(CWE_EvaluationResultEnum.OVERLAPPED):
            number_of_overlapped_cwe_prediction += 1
        elif result['cwe_comparison'] == str(CWE_EvaluationResultEnum.NOT_OVERLAPPED):
            number_of_not_overlapped_cwe_prediction += 1
        elif result['cwe_comparison'] == str(CWE_EvaluationResultEnum.PR_SUBSET_OF_GT):
            number_of_pr_subset_equal_gt_cwe_prediction += 1
        elif result['cwe_comparison'] == str(CWE_EvaluationResultEnum.GT_SUBSET_OF_PR):
            number_of_gt_subset_equal_pr_cwe_prediction += 1

        if result['severity_comparison'] == str(Severity_EvaluationResultEnum.NULL_PR):
            number_of_severity_null_prediction += 1
        elif result['severity_comparison'] == str(Severity_EvaluationResultEnum.IDENTICAL):
            number_of_severity_correct_prediction += 1
        elif result['severity_comparison'] == str(Severity_EvaluationResultEnum.DIFFERENT):
            number_of_severity_incorrect_prediction += 1

        if result['cvss_score_comparison'][0] == None:
            number_of_cvss_score_null_prediction += 1
        else:
            if result['cvss_score_comparison'][0]:
                number_of_cvss_score_proximity_prediction[result['cvss_score_comparison'][1]] += 1

        if (result['is_vulnerable_comparison'] == str(IsVulnerable_EvaluationResultEnum.IDENTICAL) and
                result['is_security_vulnerable_comparison'] == str(
                    IsSecurityVulnerable_EvaluationResultEnum.IDENTICAL) and
                result['cwe_comparison'] == str(CWE_EvaluationResultEnum.IDENTICAL) and
                result['cvss_score_comparison'][0]):
            number_of_identical_is_vulnerable_identical_is_security_vulnerable_identical_cwe_correct_severity_in_range_cvss_prediction[
                result['cvss_score_comparison'][1]] += 1

        if (result['is_vulnerable_comparison'] == str(IsVulnerable_EvaluationResultEnum.IDENTICAL) and
                result['is_security_vulnerable_comparison'] == str(
                    IsSecurityVulnerable_EvaluationResultEnum.IDENTICAL) and
                (result['cwe_comparison'] == str(CWE_EvaluationResultEnum.IDENTICAL) or result[
                    'cwe_comparison'] == str(CWE_EvaluationResultEnum.PR_SUBSET_OF_GT)) and
                result['cvss_score_comparison'][0]):
            number_of_identical_is_vulnerable_identical_is_security_vulnerable_pr_subset_equal_gt_cwe_correct_severity_in_range_cvss_prediction[
                result['cvss_score_comparison'][1]] += 1

        if (result['is_vulnerable_comparison'] == str(IsVulnerable_EvaluationResultEnum.IDENTICAL) and
                result['is_security_vulnerable_comparison'] == str(
                    IsSecurityVulnerable_EvaluationResultEnum.IDENTICAL) and
                (result['cwe_comparison'] == str(CWE_EvaluationResultEnum.IDENTICAL) or result[
                    'cwe_comparison'] == str(CWE_EvaluationResultEnum.GT_SUBSET_OF_PR)) and
                result['cvss_score_comparison'][0]):
            number_of_identical_is_vulnerable_identical_is_security_vulnerable_gt_subset_equal_pr_cwe_correct_severity_in_range_cvss_prediction[
                result['cvss_score_comparison'][1]] += 1

    return {
        'size': len(results),
        'date_time': EXECUTION_DATE_TIME,
        'number_of_null_is_vulnerable_prediction': number_of_null_is_vulnerable_prediction,
        'number_of_correct_is_vulnerable_prediction': number_of_correct_is_vulnerable_prediction,
        'number_of_incorrect_is_vulnerable_prediction': number_of_incorrect_is_vulnerable_prediction,

        'number_of_null_is_security_vulnerable_prediction': number_of_null_is_security_vulnerable_prediction,
        'number_of_correct_is_security_vulnerable_prediction': number_of_correct_is_security_vulnerable_prediction,
        'number_of_incorrect_is_security_vulnerable_prediction': number_of_incorrect_is_security_vulnerable_prediction,

        'number_of_null_cwe_prediction': number_of_null_cwe_prediction,
        'number_of_empty_cwe_prediction': number_of_empty_cwe_prediction,
        'number_of_identical_cwe_prediction': number_of_identical_cwe_prediction,
        'number_of_gt_subset_equal_pr_cwe_prediction': number_of_gt_subset_equal_pr_cwe_prediction,
        'number_of_pr_subset_equal_gt_cwe_prediction': number_of_pr_subset_equal_gt_cwe_prediction,
        'number_of_overlapped_cwe_prediction': number_of_overlapped_cwe_prediction,
        'number_of_not_overlapped_cwe_prediction': number_of_not_overlapped_cwe_prediction,

        'number_of_severity_null_prediction': number_of_severity_null_prediction,
        'number_of_severity_correct_prediction': number_of_severity_correct_prediction,
        'number_of_severity_incorrect_prediction': number_of_severity_incorrect_prediction,

        'number_of_cvss_score_null_prediction': number_of_cvss_score_null_prediction,
        'number_of_cvss_score_proximity_prediction': number_of_cvss_score_proximity_prediction,

        'number_of_identical_is_vulnerable_identical_is_security_vulnerable_identical_cwe_correct_severity_in_range_cvss_prediction': number_of_identical_is_vulnerable_identical_is_security_vulnerable_identical_cwe_correct_severity_in_range_cvss_prediction,
        'number_of_identical_is_vulnerable_identical_is_security_vulnerable_pr_subset_equal_gt_cwe_correct_severity_in_range_cvss_prediction': number_of_identical_is_vulnerable_identical_is_security_vulnerable_pr_subset_equal_gt_cwe_correct_severity_in_range_cvss_prediction,
        'number_of_identical_is_vulnerable_identical_is_security_vulnerable_gt_subset_equal_pr_cwe_correct_severity_in_range_cvss_prediction': number_of_identical_is_vulnerable_identical_is_security_vulnerable_gt_subset_equal_pr_cwe_correct_severity_in_range_cvss_prediction,

    }


def dg_compute_statistics(results):
    print(
        "Computing statistics...")
    ##

    ##
    return {
        'size': len(results),
        'date_time': EXECUTION_DATE_TIME
    }


def process_llm_output(raw_llm_output):
    try:
        return json.loads(raw_llm_output)
    except Exception as e:
        print(e)
        return raw_llm_output


def _evaluate(processed_llm_output, record, record_gt_cwe: set, record_gt_severity, record_gt_cvss_score):
    is_vulnerable_comparison = None
    is_security_vulnerable_comparison = None
    CWE_comparison = None
    severity_comparison = None
    cvss_score_comparison = (None, None)

    ##           IS_VULNERABLE          ##
    if processed_llm_output['is_vulnerable'] == None or str(processed_llm_output['is_vulnerable']).lower() == 'null':
        is_vulnerable_comparison = IsVulnerable_EvaluationResultEnum.NULL_PR
    else:
        predicted_is_vulnerable = True if str(processed_llm_output['is_vulnerable']).lower() == 'true' else False

        if predicted_is_vulnerable:  # because all ground truth instances are vulnerable
            is_vulnerable_comparison = IsVulnerable_EvaluationResultEnum.IDENTICAL
        else:
            is_vulnerable_comparison = IsVulnerable_EvaluationResultEnum.DIFFERENT

        ##           IS_SECURITY_VULNERABLE          ##
    if processed_llm_output['is_security_vulnerable'] == None or str(
            processed_llm_output['is_security_vulnerable']).lower() == 'null':
        is_security_vulnerable_comparison = IsSecurityVulnerable_EvaluationResultEnum.NULL_PR
    else:
        predicted_is_security_vulnerable = True if str(
            processed_llm_output['is_security_vulnerable']).lower() == 'true' else False

        if predicted_is_security_vulnerable:  # because all ground truth instances are vulnerable
            is_security_vulnerable_comparison = IsSecurityVulnerable_EvaluationResultEnum.IDENTICAL
        else:
            is_security_vulnerable_comparison = IsSecurityVulnerable_EvaluationResultEnum.DIFFERENT

    ##           CWE           ##

    if processed_llm_output['cwe'] == None or str(processed_llm_output['cwe']).lower() == 'null':
        CWE_comparison = CWE_EvaluationResultEnum.NULL_PR
    else:
        predicted_cwe = set(processed_llm_output['cwe'])

        if len(predicted_cwe) == 0:
            CWE_comparison = CWE_EvaluationResultEnum.EMPTY_PR
        elif predicted_cwe == record_gt_cwe:
            CWE_comparison = CWE_EvaluationResultEnum.IDENTICAL
        elif record_gt_cwe.issubset(predicted_cwe):
            CWE_comparison = CWE_EvaluationResultEnum.GT_SUBSET_OF_PR  # this does not include equal
        elif predicted_cwe.issubset(record_gt_cwe):
            CWE_comparison = CWE_EvaluationResultEnum.PR_SUBSET_OF_GT  # this does not include equal
        elif predicted_cwe.isdisjoint(record_gt_cwe):
            CWE_comparison = CWE_EvaluationResultEnum.NOT_OVERLAPPED
        else:
            CWE_comparison = CWE_EvaluationResultEnum.OVERLAPPED  # this does not include equal

    ##           SEVERITY           ##
    if processed_llm_output['severity'] == None or str(processed_llm_output['severity']).lower() == 'null':
        severity_comparison = Severity_EvaluationResultEnum.NULL_PR
    else:
        predicted_severity = str(processed_llm_output['severity']).lower()

        if predicted_severity == record_gt_severity.lower():
            severity_comparison = Severity_EvaluationResultEnum.IDENTICAL
        else:
            severity_comparison = Severity_EvaluationResultEnum.DIFFERENT

    ##          CVSS SCORE       ##
    if processed_llm_output['cvss_score'] == None or str(processed_llm_output['cvss_score']).lower() == 'null':
        cvss_score_comparison = (None, None)
    else:
        predicted_cvss_score = float(processed_llm_output['cvss_score'])

        cvss_score_comparison = (False, None)
        for radius in sorted(constants.ANALYSIS_RADIUS):
            radius_range = (predicted_cvss_score - radius, predicted_cvss_score + radius)
            in_range = radius_range[0] <= record_gt_cvss_score <= radius_range[1]

            if in_range:
                cvss_score_comparison = (True, radius)
                break

    ######

    return {
        'llm_output': processed_llm_output,
        'gt': record,

        'is_vulnerable_comparison': str(is_vulnerable_comparison),
        'is_security_vulnerable_comparison': str(is_security_vulnerable_comparison),
        'cwe_comparison': str(CWE_comparison),
        'severity_comparison': str(severity_comparison),
        'cvss_score_comparison': [cvss_score_comparison[0], cvss_score_comparison[1]],
    }


def _dg_evaluate(processed_llm_output, record, record_gt_description):
    description_comparison = None

    # do some comparison with record_gt_description
    return {
        'llm_output': processed_llm_output,
        'gt': record,
        'description_comparison': description_comparison
    }


def evaluate(processed_llm_output, record, record_gt_cwe: set, record_gt_severity, record_gt_cvss_score):
    if (isinstance(processed_llm_output, dict) and
            'is_vulnerable' in processed_llm_output and
            'is_security_vulnerable' in processed_llm_output and
            'cwe' in processed_llm_output and
            'severity' in processed_llm_output and
            'cvss_score' in processed_llm_output
    ):
        return _evaluate(processed_llm_output, record, record_gt_cwe, record_gt_severity, record_gt_cvss_score)

    elif isinstance(processed_llm_output, str):
        return {
            'llm_output': processed_llm_output,
            'gt': record,

            'is_vulnerable_comparison': str(IsVulnerable_EvaluationResultEnum.NULL_PR),
            'is_security_vulnerable_comparison': str(IsSecurityVulnerable_EvaluationResultEnum.NULL_PR),
            'cwe_comparison': str(CWE_EvaluationResultEnum.NULL_PR),
            'severity_comparison': str(Severity_EvaluationResultEnum.NULL_PR),
            'cvss_score_comparison': [None, None],

        }
    else:
        print("New processed llm output type detected that is not supported by the tool! it is: ", processed_llm_output,
              "and type is:", type(processed_llm_output))
        return {
            'llm_output': processed_llm_output,
            'gt': record,

            'is_vulnerable_comparison': str(IsVulnerable_EvaluationResultEnum.NULL_PR),
            'is_security_vulnerable_comparison': str(IsSecurityVulnerable_EvaluationResultEnum.NULL_PR),
            'cwe_comparison': str(CWE_EvaluationResultEnum.NULL_PR),
            'severity_comparison': str(Severity_EvaluationResultEnum.NULL_PR),
            'cvss_score_comparison': [None, None],

        }


def dg_evaluate(processed_llm_output, record, record_gt_description):
    if (isinstance(processed_llm_output, dict) and
            'description' in processed_llm_output
    ):
        return _dg_evaluate(processed_llm_output, record, record_gt_description)

    elif isinstance(processed_llm_output, str):
        return {
            'llm_output': processed_llm_output,
            'gt': record,
            'description_comparison': None
        }
    else:
        raise Exception("New processed llm output type detected that is not supported by the tool!")


def experiment_description(dataset, number_of_noises, fine_tune_type, model_id, model_category):
    input_type = 'description'.replace(' ', '_')
    print("Running experiments of '", input_type, "'...")

    results = []
    llm_obj = llm.LLM()
    for idx, record in enumerate(dataset):
        print(f'record {idx + 1} / {len(dataset)}')

        record_desc = record['description']

        record_gt_cvss_version = float(record['cvss_version'])
        raw_llm_output = llm_obj.inference_with_description(record_desc, record_gt_cvss_version, model_category,
                                                            model_id)
        processed_llm_output = process_llm_output(raw_llm_output)

        record_gt_cwe = set(record['cwe'])
        record_gt_severity = str(record['severity'])
        record_gt_cvss_score = float(record['cvss_score'])

        result = evaluate(processed_llm_output, record, record_gt_cwe, record_gt_severity, record_gt_cvss_score)

        utils.save_result(EXECUTION_DATE_TIME, number_of_noises, fine_tune_type, model_category, input_type, idx,
                          result)

        results.append(result)

    return results


def experiment_description_and_file(dataset, number_of_noises, fine_tune_type, model_id, model_category):
    input_type = 'description and file'.replace(' ', '_')
    print("Running experiments of '", input_type, "'...")

    results = []
    llm_obj = llm.LLM()
    for idx, record in enumerate(dataset):
        print(f'record {idx + 1} / {len(dataset)}')

        record_desc = record['description']
        record_files = record['vulnerability']['file_level']

        record_gt_cvss_version = float(record['cvss_version'])
        raw_llm_output = llm_obj.inference_with_description_and_file(record_desc, record_gt_cvss_version, record_files,
                                                                     model_category,
                                                                     model_id)
        processed_llm_output = process_llm_output(raw_llm_output)

        record_gt_cwe = set(record['cwe'])
        record_gt_severity = str(record['severity'])
        record_gt_cvss_score = float(record['cvss_score'])

        result = evaluate(processed_llm_output, record, record_gt_cwe, record_gt_severity, record_gt_cvss_score)

        utils.save_result(EXECUTION_DATE_TIME, number_of_noises, fine_tune_type, model_category, input_type, idx,
                          result)

        results.append(result)

    return results


def dg_experiment_file(dataset, fine_tune_type, model_id, model_category):
    input_type = 'file'.replace(' ', '_')
    print("Running experiments of '", input_type, "'...")

    results = []
    llm_obj = llm.LLM()
    for idx, record in enumerate(dataset):
        print(f'record {idx + 1} / {len(dataset)}')

        record_files = record['vulnerability']['file_level']
        record_cwes = record['cwe']

        record_gt_cvss_version = float(record['cvss_version'])
        raw_llm_output = llm_obj.dg_inference_with_file(record_gt_cvss_version, record_files, record_cwes,
                                                        model_category,
                                                        model_id)
        processed_llm_output = process_llm_output(raw_llm_output)

        record_gt_description = record['description']

        result = dg_evaluate(processed_llm_output, record, record_gt_description)

        utils.save_result(EXECUTION_DATE_TIME, fine_tune_type, model_category, input_type, idx, result, dg=True)

        results.append(result)

    return results


def dg_experiment_method(dataset, fine_tune_type, model_id, model_category):
    input_type = 'method'.replace(' ', '_')
    print("Running experiments of '", input_type, "'...")

    results = []
    llm_obj = llm.LLM()
    for idx, record in enumerate(dataset):
        print(f'record {idx + 1} / {len(dataset)}')

        record_methods = record['vulnerability']['method_level']
        record_cwes = record['cwe']

        record_gt_cvss_version = float(record['cvss_version'])
        raw_llm_output = llm_obj.dg_inference_with_method(record_gt_cvss_version, record_methods, record_cwes,
                                                          model_category,
                                                          model_id)
        processed_llm_output = process_llm_output(raw_llm_output)

        record_gt_description = record['description']

        result = dg_evaluate(processed_llm_output, record, record_gt_description)

        utils.save_result(EXECUTION_DATE_TIME, fine_tune_type, model_category, input_type, idx, result, dg=True)

        results.append(result)

    return results


def dg_experiment_hunk(dataset, fine_tune_type, model_id, model_category):
    input_type = 'hunk'.replace(' ', '_')
    print("Running experiments of '", input_type, "'...")

    results = []
    llm_obj = llm.LLM()
    for idx, record in enumerate(dataset):
        print(f'record {idx + 1} / {len(dataset)}')

        record_hunks = record['vulnerability']['hunk_level']
        record_cwes = record['cwe']

        record_gt_cvss_version = float(record['cvss_version'])
        raw_llm_output = llm_obj.dg_inference_with_hunk(record_gt_cvss_version, record_hunks, record_cwes,
                                                        model_category,
                                                        model_id)
        processed_llm_output = process_llm_output(raw_llm_output)

        record_gt_description = record['description']

        result = dg_evaluate(processed_llm_output, record, record_gt_description)

        utils.save_result(EXECUTION_DATE_TIME, fine_tune_type, model_category, input_type, idx, result, dg=True)

        results.append(result)

    return results


def experiment_description_and_method(dataset, number_of_noises, fine_tune_type, model_id, model_category):
    input_type = 'description and method'.replace(' ', '_')
    print("Running experiments of '", input_type, "'...")

    results = []
    llm_obj = llm.LLM()
    for idx, record in enumerate(dataset):
        print(f'record {idx + 1} / {len(dataset)}')

        record_desc = record['description']
        record_methods = record['vulnerability']['method_level']

        record_gt_cvss_version = float(record['cvss_version'])
        raw_llm_output = llm_obj.inference_with_description_and_method(record_desc, record_gt_cvss_version,
                                                                       record_methods, model_category,
                                                                       model_id)
        processed_llm_output = process_llm_output(raw_llm_output)

        record_gt_cwe = set(record['cwe'])
        record_gt_severity = str(record['severity'])
        record_gt_cvss_score = float(record['cvss_score'])

        result = evaluate(processed_llm_output, record, record_gt_cwe, record_gt_severity, record_gt_cvss_score)

        utils.save_result(EXECUTION_DATE_TIME, number_of_noises, fine_tune_type, model_category, input_type, idx,
                          result)

        results.append(result)

    return results


def experiment_description_and_hunk(dataset, number_of_noises, fine_tune_type, model_id, model_category):
    input_type = 'description and hunk'.replace(' ', '_')
    print("Running experiments of '", input_type, "'...")

    results = []
    llm_obj = llm.LLM()
    for idx, record in enumerate(dataset):
        print(f'record {idx + 1} / {len(dataset)}')

        record_desc = record['description']
        record_hunks = record['vulnerability']['hunk_level']

        record_gt_cvss_version = float(record['cvss_version'])
        raw_llm_output = llm_obj.inference_with_description_and_hunk(record_desc, record_gt_cvss_version, record_hunks,
                                                                     model_category,
                                                                     model_id)
        processed_llm_output = process_llm_output(raw_llm_output)

        record_gt_cwe = set(record['cwe'])
        record_gt_severity = str(record['severity'])
        record_gt_cvss_score = float(record['cvss_score'])

        result = evaluate(processed_llm_output, record, record_gt_cwe, record_gt_severity, record_gt_cvss_score)

        utils.save_result(EXECUTION_DATE_TIME, number_of_noises, fine_tune_type, model_category, input_type, idx,
                          result)

        results.append(result)

    return results


def execute_vulnerability_assessment(dataset, number_of_noises=-1):
    print("\nBaseline experiments")
    if constants.BASE_LINE:
        for model_obj in constants.LLM_NORMAL_MODEL:
            model_category, model_id = model_obj['category'], model_obj['id']

            if model_category not in constants.ALLOWED_MODELS:
                print("Skipping ", model_category, "...")
                continue

            print(f"\n@@@@@@@@@@@@ Baseline LLM: {model_category} @@@@@@@@@@@@")

            if 'description' in constants.ALLOWED_EXPERIMENTS:
                desc_results = experiment_description(dataset, number_of_noises, None, model_id, model_category)
                desc_statistics = compute_statistics(desc_results)
                utils.save(EXECUTION_DATE_TIME, number_of_noises, None, model_category, 'description', desc_statistics)
                print("************************")

            if 'description and file' in constants.ALLOWED_EXPERIMENTS:
                desc_and_file_results = experiment_description_and_file(dataset, number_of_noises, None, model_id,
                                                                        model_category)
                desc_and_file_statistics = compute_statistics(desc_and_file_results)
                utils.save(EXECUTION_DATE_TIME, number_of_noises, None, model_category, 'description and file',
                           desc_and_file_statistics)
                print("************************")

            if 'description and method' in constants.ALLOWED_EXPERIMENTS:
                desc_and_method_results = experiment_description_and_method(dataset, number_of_noises, None, model_id,
                                                                            model_category)
                desc_and_method_statistics = compute_statistics(desc_and_method_results)
                utils.save(EXECUTION_DATE_TIME, number_of_noises, None, model_category, 'description and method',
                           desc_and_method_statistics)
                print("************************")

            if 'description and hunk' in constants.ALLOWED_EXPERIMENTS:
                desc_and_hunk_results = experiment_description_and_hunk(dataset, number_of_noises, None, model_id,
                                                                        model_category)

                desc_and_hunk_statistics = compute_statistics(desc_and_hunk_results)
                utils.save(EXECUTION_DATE_TIME, number_of_noises, None, model_category, 'description and hunk',
                           desc_and_hunk_statistics)
                print("************************")

        print("===========================")

    else:
        print("\nFine-tuning experiments")
        print("GPT4 fine-tuned model experiments")
        for model_obj in constants.GPT4_FINE_TUNED_MODELS:
            model_category, model_fine_tune_type, model_id = model_obj['category'], model_obj['fine_tune_type'], \
                model_obj['id']

            if model_category not in constants.ALLOWED_MODELS:
                print("Skipping ", model_category, "|", model_fine_tune_type, "...")
                continue

            print(f"\n@@@@@@@@@@@@ GPT-4 Fine-tuned LLM: {model_category} @@@@@@@@@@@@")

            if 'description' in constants.ALLOWED_EXPERIMENTS and model_fine_tune_type == 'description-level':
                desc_results = experiment_description(dataset, number_of_noises, model_fine_tune_type, model_id,
                                                      model_category)
                desc_statistics = compute_statistics(desc_results)
                utils.save(EXECUTION_DATE_TIME, number_of_noises, model_fine_tune_type, model_category, 'description',
                           desc_statistics)
                print("************************")

            if 'description and file' in constants.ALLOWED_EXPERIMENTS and model_fine_tune_type == 'description-file-level':
                desc_and_file_results = experiment_description_and_file(dataset, number_of_noises, model_fine_tune_type,
                                                                        model_id,
                                                                        model_category)
                desc_and_file_statistics = compute_statistics(desc_and_file_results)
                utils.save(EXECUTION_DATE_TIME, number_of_noises, model_fine_tune_type, model_category,
                           'description and file',
                           desc_and_file_statistics)
                print("************************")

            if 'description and method' in constants.ALLOWED_EXPERIMENTS and model_fine_tune_type == 'description-method-level':
                desc_and_method_results = experiment_description_and_method(dataset, number_of_noises,
                                                                            model_fine_tune_type, model_id,
                                                                            model_category)
                desc_and_method_statistics = compute_statistics(desc_and_method_results)
                utils.save(EXECUTION_DATE_TIME, number_of_noises, model_fine_tune_type, model_category,
                           'description and method',
                           desc_and_method_statistics)
                print("************************")

            if 'description and hunk' in constants.ALLOWED_EXPERIMENTS and model_fine_tune_type == 'description-hunk-level':
                desc_and_hunk_results = experiment_description_and_hunk(dataset, number_of_noises, model_fine_tune_type,
                                                                        model_id,
                                                                        model_category)
                desc_and_hunk_statistics = compute_statistics(desc_and_hunk_results)
                utils.save(EXECUTION_DATE_TIME, number_of_noises, model_fine_tune_type, model_category,
                           'description and hunk',
                           desc_and_hunk_statistics)
                print("************************")

        print("LLAMA-3 fine-tuned model experiments")
        for model_obj in constants.LLAMA3_FINE_TUNED_MODELS:
            model_category, model_fine_tune_type, model_id = model_obj['category'], model_obj['fine_tune_type'], \
                model_obj['id']

            if model_category not in constants.ALLOWED_MODELS:
                print("Skipping ", model_category, "|", model_fine_tune_type, "...")
                continue

            print(f"\n@@@@@@@@@@@@ LLAMA-3 Fine-tuned LLM: {model_category} @@@@@@@@@@@@")

            if 'description' in constants.ALLOWED_EXPERIMENTS and model_fine_tune_type == 'description-level':
                desc_results = experiment_description(dataset, number_of_noises, model_fine_tune_type, model_id,
                                                      model_category)
                desc_statistics = compute_statistics(desc_results)
                utils.save(EXECUTION_DATE_TIME, number_of_noises, model_fine_tune_type, model_category, 'description',
                           desc_statistics)
                print("************************")

            if 'description and file' in constants.ALLOWED_EXPERIMENTS and model_fine_tune_type == 'description-file-level':
                desc_and_file_results = experiment_description_and_file(dataset, number_of_noises, model_fine_tune_type,
                                                                        model_id,
                                                                        model_category)
                desc_and_file_statistics = compute_statistics(desc_and_file_results)
                utils.save(EXECUTION_DATE_TIME, number_of_noises, model_fine_tune_type, model_category,
                           'description and file',
                           desc_and_file_statistics)
                print("************************")

            if 'description and method' in constants.ALLOWED_EXPERIMENTS and model_fine_tune_type == 'description-method-level':
                desc_and_method_results = experiment_description_and_method(dataset, number_of_noises,
                                                                            model_fine_tune_type, model_id,
                                                                            model_category)
                desc_and_method_statistics = compute_statistics(desc_and_method_results)
                utils.save(EXECUTION_DATE_TIME, number_of_noises, model_fine_tune_type, model_category,
                           'description and method',
                           desc_and_method_statistics)
                print("************************")

            if 'description and hunk' in constants.ALLOWED_EXPERIMENTS and model_fine_tune_type == 'description-hunk-level':
                desc_and_hunk_results = experiment_description_and_hunk(dataset, number_of_noises, model_fine_tune_type,
                                                                        model_id,
                                                                        model_category)
                desc_and_hunk_statistics = compute_statistics(desc_and_hunk_results)
                utils.save(EXECUTION_DATE_TIME, number_of_noises, model_fine_tune_type, model_category,
                           'description and hunk',
                           desc_and_hunk_statistics)
                print("************************")


def create_noisy_datasets(sampled_dataset_path):
    if constants.NO_NOISY_DATASET_REGENERATION_IN_MANUAL_ANALYSIS:
        return [(idx, utils.load_json_file(path)) for idx, path in enumerate(constants.MANUAL_ANALYSIS_NOISY_DATASETS)]

    pipeline = DatasetNoisePipeline(
        sample_dataset_path=sampled_dataset_path,
        ref_dataset_path=constants.EVALUATION_DATASET_PATH,
        output_dir="./"
    )

    result_files = pipeline.run()
    return [(noise_level, utils.load_json_file(dataset_path)) for noise_level, dataset_path in result_files]


def vulnerability_assessment():
    print("Loading dataset...")

    if not constants.NOISE_CHECK_MANUAL_ANALYSIS_VULNERABILITY_DETECTION_MODE:
        dataset = load_dataset(constants.EVALUATION_DATASET_PATH)
        execute_vulnerability_assessment(dataset)
    else:
        datasets = create_noisy_datasets(constants.SAMPLED_DATASET_FOR_NOISE_CHECK)
        for (number_of_randomly_applied_noises, dataset) in datasets:
            print("Running for ", number_of_randomly_applied_noises)
            execute_vulnerability_assessment(dataset, number_of_randomly_applied_noises)


#####################################################################
def dataset_split(seed=42):
    # Load data
    with open("./dataset/" + constants.TOTAL_DATASET_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    if not data:
        return
    # Shuffle for random split
    random.seed(seed)
    random.shuffle(data)

    total_size = len(data)
    eval_size = int(total_size * constants.DATASET_SPLIT_RATIO['evaluation'])
    fine_tune_size = total_size - eval_size
    train_size = int(total_size * constants.DATASET_SPLIT_RATIO['fine-tuning']['training'])
    val_size = total_size - eval_size - train_size  # ensures all data is used

    # Split
    evaluation_data = data[:eval_size]
    training_data = data[eval_size:eval_size + train_size]
    validation_data = data[eval_size + train_size:]

    # Save splits
    with open(os.path.join("./dataset/", 'evaluation.json'), 'w', encoding='utf-8') as f:
        json.dump(evaluation_data, f, indent=2, ensure_ascii=False)

    with open(os.path.join("./dataset/", 'ft_training.json'), 'w', encoding='utf-8') as f:
        json.dump(training_data, f, indent=2, ensure_ascii=False)

    with open(os.path.join("./dataset/", 'ft_validation.json'), 'w', encoding='utf-8') as f:
        json.dump(validation_data, f, indent=2, ensure_ascii=False)

    print(
        f"Saved: {len(training_data)} training, {len(validation_data)} validation, {len(evaluation_data)} evaluation samples after shuffling.")


if __name__ == '__main__':
    if constants.DATASET_SPLIT:
        print("Mode: DATASET SPLIT")
        dataset_split()
    else:
        if constants.VULNERABILITY_ASSESSMENT:
            print("Mode: VULNERABILITY ASSESSMENT")
            vulnerability_assessment()
        else:
            print("Mode: DESCRIPTION GENERATION")
            description_generation()
