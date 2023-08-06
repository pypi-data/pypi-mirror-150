from dataclasses import dataclass
from typing import Any, List, Tuple


@dataclass
class failed_test:
    """Class that represents a failed test case"""
    msg: str = ""
    want: Any = None
    got: Any = None


@dataclass
class failed_partid:
    """Class that represents a failed test case"""
    test_name: str
    failed_tests: List[failed_test]
    num_tests: int


def compute_grading_score(failed_cases: List[failed_test], num_cases: int) -> Tuple[float, str]:
    """Computes the score based on the number of failed and total cases.
    Args:
        failed_cases (List): Failed cases.
        num_cases (int): Total number of cases.
    Returns:
        Tuple[float, str]: The grade and feedback message.
    """

    score = 1.0 - len(failed_cases) / num_cases
    feedback_msg = "All tests passed! Congratulations!"

    if failed_cases:
        feedback_msg = ""
        for failed_case in failed_cases:
            feedback_msg += f"Failed test case: {failed_case.msg}.\nExpected:\n{failed_case.want},\nbut got:\n{failed_case.got}.\n\n"
        return round(score, 2), feedback_msg

    return score, feedback_msg



def compute_grading_score_multi_partid(failed_cases: List[failed_partid]) -> Tuple[float, str]:
    """Computes the score based on the number of failed and total cases.
    Args:
        failed_partid (List): Failed cases for every part.
    Returns:
        Tuple[float, str]: The grade and feedback message.
    """
    scores = []
    msgs = []

    for f in failed_cases:
        feedback_msg = f"All tests passed for {f.test_name}!\n"
        score = 1.0 - len(f.failed_tests) / f.num_tests
        score = round(score, 2)
        scores.append(score)

        if f.failed_tests:
            feedback_msg = f"Details of failed tests for {f.test_name}\n\n"
            for failed_case in f.failed_tests:
                feedback_msg += f"Failed test case: {failed_case.msg}.\nExpected:\n{failed_case.want},\nbut got:\n{failed_case.got}.\n\n"
        msgs.append(feedback_msg)

    final_score = sum(scores)/len(scores)
    final_score = round(final_score, 2)
    final_msg = "\n".join(msgs)

    return final_score, final_msg


def object_to_grade(origin_module, attr_name):
    """Used as a parameterized decorator to get an attribute from a module.

    Args:
        origin_module (ModuleType): A module.
        attr_name (str): Name of the attribute to extract from the module.
    """
    def middle(func):
        def wrapper():
            val = getattr(origin_module, attr_name, None)
            return func(val)
        return wrapper
    return middle