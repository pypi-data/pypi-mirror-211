import os.path
from enum import Enum
from pingsafe_cli.version import build_type

CONFIG_FILE_NAME = "config.json"
TIME_FORMAT = "%Y-%m-%d %H:%M:%S.%f"
DEBUG_ENABLED = 0
BASELINE_FILE = ".baseline"
PACKAGE_NAME = "pingsafe_cli"
DEFAULT_TIMEOUT = (3.1, 5)
BINARY_LIST = ["bin_secret_detector"]
SENTRY_TAGS = ["org_id", "project_id"]

APP_URL = "https://app.pingsafe.com"
LOCAL_SERVER_URL = "http://localhost:8080"

MAIN_PIP_COMMAND = f"pip3 install --upgrade {PACKAGE_NAME}"
TEST_PIP_COMMAND = f"pip3 install -i https://test.pypi.org/simple/ --upgrade {PACKAGE_NAME}"

MAIN_PYPI_URL = f'https://pypi.org/pypi/{PACKAGE_NAME}/json'
TEST_PYPI_URL = f'https://test.pypi.org/pypi/{PACKAGE_NAME}/json'

PIP_COMMAND = MAIN_PIP_COMMAND if build_type == "pypi" else TEST_PIP_COMMAND
PYPI_URL = MAIN_PYPI_URL if build_type == "pypi" else TEST_PYPI_URL
BASE_URL = LOCAL_SERVER_URL if build_type == "local" else APP_URL

GET_PRE_SIGNED_URL = f"{BASE_URL}/apis/v1/cli/setup"
GET_CONFIG_DATA_URL = f"{BASE_URL}/apis/v1/cli/config"

DEFAULT_PINGSAFE_DIR = ".pingsafe"
PINGSAFE_LOCAL_CONFIG_PATH = os.path.join(DEFAULT_PINGSAFE_DIR, "local_config.json")


class MainSubParser(str, Enum):
    CODE = "code"
    CONFIG = "config"


class CodeTypeSubParser(str, Enum):
    IAC = "iac"
    SECRET = "secret"


class HttpMethod(str, Enum):
    GET = "GET"
    POST = "POST"


class IacProvider(str, Enum):
    ALL = "all"
    TERRAFORM = "terraform"
    TERRAFORM_PLAN = "terraform-plan"
    CLOUDFORMATION = "cloudformation"
    KUBERNETES = "kubernetes"
    HELM = "helm"


class IacConfigData(str, Enum):
    LAST_REFRESHED_AT = "last_refreshed_at"


class OutputFormat(str, Enum):
    JSON = "JSON"
    CSV = "CSV"


class MissingConfig(Exception):
    pass


class HttpConnectionError(Exception):
    pass


class RequestTimeout(Exception):
    pass


class MissingRequiredFlags(Exception):
    pass


class PlatformNotSupported(Exception):
    pass


class MissingDependencies(Exception):
    pass


class DownloadException(Exception):
    def __init__(self, message, url="", filename=""):
        super().__init__(message)
        self.url = url
        self.filename = filename


class LogColors(str, Enum):
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
