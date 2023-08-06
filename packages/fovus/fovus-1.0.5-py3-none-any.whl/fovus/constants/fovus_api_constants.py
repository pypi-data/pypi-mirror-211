# API
from fovus.config.config import DOMAIN_NAME
from fovus.constants.cli_constants import MAX_VCPU, MIN_VCPU

COGNITO_REGION = "us-east-1"
TIMEOUT_SECONDS = 10

# API
JOB = "job"
FILE = "file"
SOFTWARE = "software"
BENCHMARK = "benchmark"
__APIS = {
    JOB: DOMAIN_NAME + "/job",
    FILE: DOMAIN_NAME + "/file",
    SOFTWARE: DOMAIN_NAME + "/software",
    BENCHMARK: DOMAIN_NAME + "/benchmark",
}

CREATE_JOB = "CREATE_JOB"
GET_JOB_INFO = "GET_JOB_STATUS"

GET_FILE_DOWNLOAD_TOKEN = "GET_FILE_DOWNLOAD_TOKEN"  # nosec
GET_FILE_UPLOAD_TOKEN = "GET_FILE_UPLOAD_TOKEN"  # nosec

LIST_SOFTWARE = "LIST_SOFTWARE"

LIST_BENCHMARK_PROFILE = "LIST_BENCHMARK_PROFILE"

APIS = {
    JOB: {CREATE_JOB: __APIS[JOB] + "/create-job", GET_JOB_INFO: __APIS[JOB] + "/get-job-info"},
    FILE: {
        GET_FILE_DOWNLOAD_TOKEN: __APIS[FILE] + "/get-file-download-token",
        GET_FILE_UPLOAD_TOKEN: __APIS[FILE] + "/get-file-upload-token",
    },
    SOFTWARE: {
        LIST_SOFTWARE: __APIS[SOFTWARE] + "/list-software",
    },
    BENCHMARK: {LIST_BENCHMARK_PROFILE: __APIS[BENCHMARK] + "/list-benchmark-profile"},
}

# Benchmarking
BOUNDS_TO_SCALE = (MIN_VCPU, MAX_VCPU)
BOUND_VALUE_CORRECTION_PRINT_ORDER = ("minvCpu", "maxvCpu", "minvCpuMemGiB", "minGpu", "maxGpu", "minGpuMemGiB")

# Payload
AUTHORIZATION_HEADER = "Authorization"
CONTAINERIZED = "containerized"
ENVIRONMENT = "environment"
LICENSE_COUNT_PER_TASK = "licenseCountPerTask"
LICENSE_FEATURE = "licenseFeature"
MONOLITHIC_LIST = "monolithicList"
PAYLOAD_CONSTRAINTS = "constraints"
PAYLOAD_JOB_CONSTRAINTS = "jobConstraints"
PAYLOAD_JOB_NAME = "jobName"
PAYLOAD_TASK_CONSTRAINTS = "taskConstraints"
PAYLOAD_TIME_COST_PRIORITY_RATIO = "timeToCostPriorityRatio"
PAYLOAD_TIMESTAMP = "timestamp"
PAYLOAD_WORKSPACE_ID = "workspaceId"
SOFTWARE_NAME = "softwareName"
SOFTWARE_VERSION = "softwareVersion"
STATUS_CODE = "statusCode"
VENDOR_NAME = "vendorName"

# Response
BODY = "body"
BP_HYPERTHREADING = "bpHyperthreading"
ERROR_MESSAGE = "errorMessage"
JOB_STATUS = "jobStatus"
SOFTWARE_MAP = "softwareMap"
SOFTWARE_VERSIONS = "softwareVersions"
