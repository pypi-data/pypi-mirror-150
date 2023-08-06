import subprocess
import sys
from typing import List, Tuple

from pypitools.utils import get_logger
from pypitools.configs import ConfigOutput


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
    with subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as process:
        (res_stdout, res_stderr) = process.communicate()
        if process.returncode:
            print(res_stdout.decode(), end="", file=sys.stdout)
            print(res_stderr.decode(), end="", file=sys.stderr)
            raise ValueError(
                f"exit code from [{' '.join(args)}] was [{process.returncode}]"
            )
        return res_stdout.decode(), res_stderr.decode()
