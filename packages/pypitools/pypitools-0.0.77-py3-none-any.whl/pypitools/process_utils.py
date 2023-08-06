import subprocess
import sys
import os
from typing import List, Tuple

from pypitools.utils import get_logger
from pypitools.configs import ConfigOutput

PYTHONWARNINGS = "PYTHONWARNINGS"


def check_call_collect(args: List[str]) -> Tuple[str, str]:
    """
    Run a process and check that it returns an OK return code
    Gather any output and return it to the caller.
    If the process returns an error then print the output and
    the errors.
    :param args:
    """
    logger = get_logger()
    logger.debug("running %s", args)
    if ConfigOutput.verbose:
        print(f"running [{args}]..")
    if ConfigOutput.suppress_warnings:
        before = os.environ.get(PYTHONWARNINGS)
        os.environ[PYTHONWARNINGS] = "ignore"
    with subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as process:
        (res_stdout, res_stderr) = process.communicate()
        if process.returncode:
            print(res_stdout.decode(), end="", file=sys.stdout)
            print(res_stderr.decode(), end="", file=sys.stderr)
            raise ValueError(
                f"exit code from [{' '.join(args)}] was [{process.returncode}]"
            )
        if ConfigOutput.suppress_warnings:
            if before is None:
                del os.environ[PYTHONWARNINGS]
            else:
                os.environ[PYTHONWARNINGS] = before
        return res_stdout.decode(), res_stderr.decode()
