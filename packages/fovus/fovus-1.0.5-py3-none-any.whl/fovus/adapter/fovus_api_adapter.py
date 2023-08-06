import copy
import json
import os
from http import HTTPStatus

import requests

from fovus.adapter.aws_cognito_adapter import AwsCognitoAdapter, UserAttribute
from fovus.constants.benchmark_constants import (
    BENCHMARK_NAME,
    BOUNDS,
    COMPARISONS,
    COMPREHENSIONS,
    CORRECTABLE_COMPARISON,
)
from fovus.constants.cli_constants import (
    BENCHMARKING_PROFILE_NAME,
    COMPUTING_DEVICE,
    CPU,
    ENABLE_HYPERTHREADING,
    FOVUS_PROVIDED_CONFIGS,
    JOB_CONFIG_CONTAINERIZED_TEMPLATE,
    JOB_CONFIG_FILE_PATH,
    JOB_NAME,
    MAX_GPU,
    MIN_GPU,
    MIN_GPU_MEM_GIB,
    MONOLITHIC_OVERRIDE,
    PATH_TO_CONFIG_FILE_IN_REPO,
    TIMESTAMP,
    USER_ID,
    WORKSPACE_ID,
)
from fovus.constants.fovus_api_constants import (
    APIS,
    AUTHORIZATION_HEADER,
    BENCHMARK,
    BODY,
    BOUND_VALUE_CORRECTION_PRINT_ORDER,
    BP_HYPERTHREADING,
    CREATE_JOB,
    ENVIRONMENT,
    FILE,
    GET_FILE_DOWNLOAD_TOKEN,
    GET_FILE_UPLOAD_TOKEN,
    GET_JOB_INFO,
    JOB,
    JOB_STATUS,
    LICENSE_COUNT_PER_TASK,
    LICENSE_FEATURE,
    LIST_BENCHMARK_PROFILE,
    LIST_SOFTWARE,
    MONOLITHIC_LIST,
    PAYLOAD_CONSTRAINTS,
    PAYLOAD_JOB_CONSTRAINTS,
    PAYLOAD_JOB_NAME,
    PAYLOAD_TASK_CONSTRAINTS,
    PAYLOAD_TIMESTAMP,
    PAYLOAD_WORKSPACE_ID,
    SOFTWARE,
    SOFTWARE_MAP,
    SOFTWARE_NAME,
    SOFTWARE_VERSION,
    SOFTWARE_VERSIONS,
    TIMEOUT_SECONDS,
    VENDOR_NAME,
)
from fovus.constants.util_constants import UTF8
from fovus.exception.user_exception import UserException
from fovus.root_config import ROOT_DIR
from fovus.util.fovus_api_util import FovusApiUtil


class FovusApiAdapter:
    def __init__(self, auth_type, auth_parameters, client_id):
        self.cognito_adapter = AwsCognitoAdapter()
        self.cognito_adapter.authenticate(auth_type, auth_parameters, client_id)

    def create_job(self, request):
        headers = self._get_api_authorization_header()
        response = requests.post(APIS[JOB][CREATE_JOB], json=request, headers=headers, timeout=TIMEOUT_SECONDS)
        FovusApiUtil.confirm_successful_response(response.json(), self.__class__.__name__)
        return response.json()

    def make_dynamic_changes_to_create_job_request(self, request):
        self._make_dynamic_changes_to_software(request)
        self._validate_benchmarking_profile(request)

    def _make_dynamic_changes_to_software(self, request):
        print("Validating software...")
        if MONOLITHIC_LIST not in request[ENVIRONMENT]:
            print("Request is for a containerized job. Filling missing/empty vendorName fields is not required.")
            return

        list_software_response = self.list_software()
        for i, monolithic_list_item in enumerate(copy.deepcopy(request[ENVIRONMENT][MONOLITHIC_LIST])):
            software_name = monolithic_list_item[SOFTWARE_NAME]
            software_version = monolithic_list_item[SOFTWARE_VERSION]
            software_vendor = monolithic_list_item[VENDOR_NAME]

            valid_software_names = []
            is_valid_software_name = False
            for valid_software_vendor in list_software_response[SOFTWARE_MAP]:
                if software_name in list_software_response[SOFTWARE_MAP][valid_software_vendor]:
                    is_valid_software_name = True
                    if (
                        software_version
                        in list_software_response[SOFTWARE_MAP][valid_software_vendor][software_name][SOFTWARE_VERSIONS]
                    ):
                        if valid_software_vendor != software_vendor:
                            print(
                                f"Replacing vendor name '{software_vendor}' with "
                                f"'{valid_software_vendor}' for monolithic list item {monolithic_list_item}."
                            )
                            request[ENVIRONMENT][MONOLITHIC_LIST][i][VENDOR_NAME] = valid_software_vendor
                        break  # Successful validation of current list item.
                    raise UserException(
                        HTTPStatus.BAD_REQUEST,
                        self.__class__.__name__,
                        f"Software version '{software_version}' for software name '{software_name}' is not valid. "
                        + "Valid software versions: "
                        + str(
                            list_software_response[SOFTWARE_MAP][valid_software_vendor][software_name][
                                SOFTWARE_VERSIONS
                            ]
                        ),
                    )
                valid_software_names.append(
                    {valid_software_vendor: list(list_software_response[SOFTWARE_MAP][valid_software_vendor].keys())}
                )
            if not is_valid_software_name:
                raise UserException(
                    HTTPStatus.BAD_REQUEST,
                    self.__class__.__name__,
                    f"Software name '{software_name}' is not valid. "
                    + "Valid software vendors and names (format: [{vendor: [name, ...]}, ...]): "
                    + str(valid_software_names),
                )

    def _validate_benchmarking_profile(self, request):  # pylint: disable=too-many-locals
        benchmarking_profile_name = request[PAYLOAD_CONSTRAINTS][PAYLOAD_JOB_CONSTRAINTS][BENCHMARKING_PROFILE_NAME]
        hyperthreading_enabled = request[PAYLOAD_CONSTRAINTS][PAYLOAD_JOB_CONSTRAINTS][ENABLE_HYPERTHREADING]
        print(
            f"Validating the benchmarking profile '{benchmarking_profile_name}' and "
            "updating values if necessary and possible..."
        )
        list_benchmark_profile_response = self.list_benchmarking_profile(request[PAYLOAD_WORKSPACE_ID])
        valid_benchmarking_profile_names = []
        for current_benchmarking_profile in list_benchmark_profile_response[  # pylint: disable=too-many-nested-blocks
            BODY
        ]:
            current_benchmarking_profile_name = current_benchmarking_profile[BENCHMARK_NAME]
            valid_benchmarking_profile_names.append(current_benchmarking_profile_name)
            if benchmarking_profile_name == current_benchmarking_profile_name:
                validations_config = FovusApiUtil.get_benchmark_validations_config(request)
                bound_scaler = FovusApiUtil.get_benchmark_bound_scaler(
                    hyperthreading_enabled,
                    current_benchmarking_profile[BP_HYPERTHREADING],
                )
                FovusApiUtil.print_benchmark_hyperthreading_info(hyperthreading_enabled)
                corrected_value_messages = {}
                for validation_type in validations_config:  # pylint: disable=consider-using-dict-items
                    for bound_to_validate in validations_config[validation_type][BOUNDS]:
                        current_value = request[PAYLOAD_CONSTRAINTS][PAYLOAD_TASK_CONSTRAINTS][bound_to_validate]
                        benchmarking_profile_bounds = FovusApiUtil.get_benchmark_profile_bounds(
                            current_benchmarking_profile, bound_to_validate, bound_scaler
                        )
                        for comparison, comprehension in zip(COMPARISONS, COMPREHENSIONS):
                            if comparison in validations_config[validation_type]:
                                benchmarking_profile_item_bound = validations_config[validation_type][comprehension](
                                    benchmarking_profile_bounds
                                )
                                if validations_config[validation_type][comparison](
                                    current_value, benchmarking_profile_item_bound
                                ):
                                    if comparison == CORRECTABLE_COMPARISON:
                                        corrected_value_messages[
                                            bound_to_validate
                                        ] = FovusApiUtil.get_corrected_value_message(
                                            validation_type,
                                            benchmarking_profile_name,
                                            bound_to_validate,
                                            benchmarking_profile_item_bound,
                                            hyperthreading_enabled,
                                            current_value,
                                        )
                                        request[PAYLOAD_CONSTRAINTS][PAYLOAD_TASK_CONSTRAINTS][
                                            bound_to_validate
                                        ] = benchmarking_profile_item_bound
                                    else:
                                        raise UserException(
                                            HTTPStatus.BAD_REQUEST,
                                            self.__class__.__name__,
                                            f"Invalid value of {current_value} for {bound_to_validate} with "
                                            f"benchmarking profile {benchmarking_profile_name}. "
                                            f"Allowed range: "
                                            f"[{min(benchmarking_profile_bounds)}, {max(benchmarking_profile_bounds)}]",
                                        )
                for bound_value_correction in BOUND_VALUE_CORRECTION_PRINT_ORDER:
                    if bound_value_correction in corrected_value_messages:
                        print(corrected_value_messages[bound_value_correction])
                return  # Successful validation.

        raise UserException(
            HTTPStatus.BAD_REQUEST,
            self.__class__.__name__,
            f"Invalid benchmarking profile: '{benchmarking_profile_name}'. "
            + f"Valid benchmarking profiles: {valid_benchmarking_profile_names}",
        )

    def get_file_download_token(self, request):
        headers = self._get_api_authorization_header()
        response = requests.post(
            APIS[FILE][GET_FILE_DOWNLOAD_TOKEN], json=request, headers=headers, timeout=TIMEOUT_SECONDS
        )
        FovusApiUtil.confirm_successful_response(response.json(), self.__class__.__name__)
        return response.json()

    def get_file_upload_token(self, request):
        headers = self._get_api_authorization_header()
        response = requests.post(
            APIS[FILE][GET_FILE_UPLOAD_TOKEN], json=request, headers=headers, timeout=TIMEOUT_SECONDS
        )
        FovusApiUtil.confirm_successful_response(response.json(), self.__class__.__name__)
        return response.json()

    def get_temporary_s3_upload_credentials(self, cli_dict):
        upload_credentials = self.get_file_upload_token(self.get_file_upload_download_token_request(cli_dict))
        FovusApiUtil.confirm_successful_response(upload_credentials, self.__class__.__name__)
        return FovusApiUtil.get_s3_info(upload_credentials[BODY])

    def get_temporary_s3_download_credentials(self, cli_dict):
        upload_credentials = self.get_file_download_token(self.get_file_upload_download_token_request(cli_dict))
        FovusApiUtil.confirm_successful_response(upload_credentials, self.__class__.__name__)
        return FovusApiUtil.get_s3_info(upload_credentials[BODY])

    def get_job_current_status(self, cli_dict, job_id):
        job_info = self.get_job_info(FovusApiAdapter.get_job_info_request(cli_dict, job_id))
        return job_info[BODY][JOB_STATUS]

    def get_job_info(self, request):
        headers = self._get_api_authorization_header()
        response = requests.post(APIS[JOB][GET_JOB_INFO], json=request, headers=headers, timeout=TIMEOUT_SECONDS)
        FovusApiUtil.confirm_successful_response(response.json(), self.__class__.__name__)
        return response.json()

    def list_software(self):
        headers = self._get_api_authorization_header()
        response = requests.get(APIS[SOFTWARE][LIST_SOFTWARE], headers=headers, timeout=TIMEOUT_SECONDS)
        FovusApiUtil.confirm_successful_response(response.json(), self.__class__.__name__)
        return response.json()

    def list_benchmarking_profile(self, workspace_id):
        headers = self._get_api_authorization_header()
        response = requests.get(
            APIS[BENCHMARK][LIST_BENCHMARK_PROFILE],
            params={"workspaceId": workspace_id},
            headers=headers,
            timeout=TIMEOUT_SECONDS,
        )
        FovusApiUtil.confirm_successful_response(response.json(), self.__class__.__name__)
        return response.json()

    def get_user_id(self):
        return self.cognito_adapter.get_user_attribute(UserAttribute.USER_ID)

    def _get_api_authorization_header(self):
        return {
            AUTHORIZATION_HEADER: self.cognito_adapter.get_id_token(),
        }

    @staticmethod
    def get_create_job_request(cli_dict):
        with open(os.path.expanduser(cli_dict[JOB_CONFIG_FILE_PATH]), encoding=UTF8) as job_config_file:
            create_job_request = json.load(job_config_file)
            FovusApiAdapter._add_create_job_request_remaining_fields(create_job_request, cli_dict)
            FovusApiAdapter._apply_cli_overrides_to_request(create_job_request, cli_dict)
            FovusApiAdapter._apply_computing_device_overrides(create_job_request)
            return create_job_request

    @staticmethod
    def _add_create_job_request_remaining_fields(create_job_request, cli_dict):
        create_job_request[PAYLOAD_TIMESTAMP] = cli_dict[TIMESTAMP]
        create_job_request[PAYLOAD_WORKSPACE_ID] = cli_dict[WORKSPACE_ID]
        if cli_dict.get(JOB_NAME):
            create_job_request[PAYLOAD_JOB_NAME] = cli_dict[JOB_NAME]
        else:
            create_job_request[PAYLOAD_JOB_NAME] = f"{create_job_request[PAYLOAD_TIMESTAMP]}-{cli_dict[USER_ID]}"

    @staticmethod
    def _apply_cli_overrides_to_request(create_job_request, cli_dict):
        print("Applying CLI overrides to create job request...")
        FovusApiAdapter._apply_single_field_overrides(create_job_request, cli_dict)
        FovusApiAdapter._apply_monolithic_list_overrides(create_job_request, cli_dict)

    @staticmethod
    def _apply_single_field_overrides(create_job_request, cli_dict):
        # The empty create job request is used to reference keys in the event that the provided config is not complete
        # and CLI arguments are being used to replace the remaining values.
        with open(
            os.path.join(
                ROOT_DIR, FOVUS_PROVIDED_CONFIGS[JOB_CONFIG_CONTAINERIZED_TEMPLATE][PATH_TO_CONFIG_FILE_IN_REPO]
            ),
            encoding=UTF8,
        ) as empty_job_config_file:
            empty_create_job_request = json.load(empty_job_config_file)
            del empty_create_job_request[ENVIRONMENT]

            for empty_sub_dict, create_job_request_sub_dict in FovusApiAdapter._get_deepest_sub_dict_pairs(
                empty_create_job_request, create_job_request
            ):
                FovusApiAdapter._apply_cli_overrides_to_sub_dict(create_job_request_sub_dict, empty_sub_dict, cli_dict)

    @staticmethod
    def _apply_monolithic_list_overrides(create_job_request, cli_dict):
        environment = create_job_request[ENVIRONMENT]
        if MONOLITHIC_LIST in environment:
            for monolithic in environment[MONOLITHIC_LIST]:
                for vendor_name, software_name, license_feature, new_license_count_per_task in cli_dict[
                    MONOLITHIC_OVERRIDE
                ]:
                    if (
                        monolithic[VENDOR_NAME] == vendor_name
                        and monolithic[SOFTWARE_NAME] == software_name
                        and monolithic[LICENSE_FEATURE] == license_feature
                    ):
                        print(
                            f"CLI override found for monolithic item with keys: {vendor_name}, {software_name}, and "
                            f"{license_feature}. Overriding default license count per task of "
                            f"{monolithic[LICENSE_COUNT_PER_TASK]} with {new_license_count_per_task}."
                        )
                        monolithic[LICENSE_COUNT_PER_TASK] = int(new_license_count_per_task)

    @staticmethod
    def _get_deepest_sub_dict_pairs(empty_create_job_request, create_job_request):
        sub_dict_pairs = []
        for key in empty_create_job_request.keys():
            if isinstance(empty_create_job_request[key], dict):
                if key not in create_job_request:
                    create_job_request[key] = {}
                sub_sub_dict_pairs = FovusApiAdapter._get_deepest_sub_dict_pairs(
                    empty_create_job_request[key], create_job_request[key]
                )
                if sub_sub_dict_pairs:
                    sub_dict_pairs.extend(sub_sub_dict_pairs)
                else:
                    sub_dict_pairs.append((empty_create_job_request[key], create_job_request[key]))
        return sub_dict_pairs

    @staticmethod
    def _apply_cli_overrides_to_sub_dict(sub_dict, empty_sub_dict, cli_dict):
        for sub_dict_parameter_key in empty_sub_dict.keys():
            cli_dict_value = cli_dict.get(sub_dict_parameter_key)
            if cli_dict[sub_dict_parameter_key] is not None:
                print(
                    f"CLI override found for key: {sub_dict_parameter_key}. Overriding default job config value of "
                    f"{sub_dict.get(sub_dict_parameter_key)} with {cli_dict[sub_dict_parameter_key]}."
                )
                if isinstance(cli_dict_value, str) and cli_dict_value.isdigit():
                    cli_dict_value = int(cli_dict_value)
                sub_dict[sub_dict_parameter_key] = cli_dict_value

    @staticmethod
    def _apply_computing_device_overrides(create_job_request):
        value_was_overridden = False
        computing_device = create_job_request[PAYLOAD_CONSTRAINTS][PAYLOAD_JOB_CONSTRAINTS][COMPUTING_DEVICE]
        print(f"Computing device is {computing_device}. Overriding related constraints if needed...")
        if computing_device == CPU:
            for field in [MIN_GPU, MAX_GPU, MIN_GPU_MEM_GIB]:
                current_field_value = create_job_request[PAYLOAD_CONSTRAINTS][PAYLOAD_TASK_CONSTRAINTS][field]
                if current_field_value != 0:
                    print(f"Overriding current {field} value of {current_field_value} with 0.")
                    value_was_overridden = True
                    create_job_request[PAYLOAD_CONSTRAINTS][PAYLOAD_TASK_CONSTRAINTS][field] = 0
        if not value_was_overridden:
            print("No overrides necessary.")

    @staticmethod
    def get_file_upload_download_token_request(cli_dict, duration_seconds=3600):
        return {"workspaceId": cli_dict["workspace_id"], "durationSeconds": duration_seconds}

    @staticmethod
    def get_job_info_request(cli_dict, job_id):
        return {"workspaceId": cli_dict["workspace_id"], "jobId": job_id}
