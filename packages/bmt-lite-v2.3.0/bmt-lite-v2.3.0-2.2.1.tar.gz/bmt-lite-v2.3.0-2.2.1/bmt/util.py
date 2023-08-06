"""Utilities."""
from functools import wraps
import re
from typing import Callable, List, Optional, TypeVar, Union

from .data import (
    all_classes, all_slots,
)


def pascal_to_snake(s: str, sep: str = "_") -> str:
    """Convert Pascal case to snake case.

    Assumes that
    a) all words are either all-lowercase or all-uppercase
    b) all 1-letter words are lowercase
    c) there are no adjacent 1-letter words
    d) there are no adjacent uppercase words

    Examples:
    PhenotypicFeature -> phenotypic_feature
    RNAProduct -> RNA_product
    FeedACamel -> feed_a_camel
    
    Optionally specify `sep` (default "_").
    """
    # add an underscore before each capital letter
    underscored = re.sub(
        r"(?<!^)(?=[A-Z])",
        sep,
        s,
    )
    # collapse any adjacent one-letter words
    collapsed = re.sub(
        r"(?<![a-zA-Z])[A-Z](?:_[A-Z](?=$|_))+",
        lambda match: match.group(0).replace("_", ""),
        underscored,
    )
    # lower-case any words containing only one uppercase letter
    lowercased = re.sub(
        r"(?<![A-Z])[A-Z](?![A-Z])",
        lambda match: match.group(0).lower(),
        collapsed,
    )
    return lowercased


def snake_to_pascal(s: str, sep: str = "_") -> str:
    """Convert snake case to Pascal case.

    This is the inverse of pascal_to_snake() when its assumptions
    are true.
    
    Optionally specify `sep` (default "_").
    """
    return re.sub(
        fr"(?:^|{sep})([a-zA-Z])",
        lambda match: match.group(1).upper(),
        s
    )


def guess_casing(s: str) -> str:
    """Guess snake case or Pascal case."""
    if "_" in s:
        return "snake"
    if any(c.isupper() for c in s):
        return "pascal"
    return "snake"


def normalize(s: str) -> str:
    """Normalize string input."""
    if s.startswith("biolink:"):
        s = s[8:]
    if "_" in s:
        # it's snake case
        return s.replace("_", " ")
    if " " in s:
        return s
    return pascal_to_snake(s, " ")


T = TypeVar("T")


def listify(func: Callable) -> Callable:
    """Expand function to take list of arguments."""
    @wraps(func)
    def wrapper(arg: Union[T, List[T]], **kwargs) -> Union[T, List[T]]:
        """Apply function to each element in list."""
        if isinstance(arg, list):
            return [
                func(el, **kwargs)
                for el in arg
            ]
        else:
            return func(arg, **kwargs)
    return wrapper


@listify
def format(s: str, case: Optional[str] = None, **kwargs) -> str:
    """Format space-case string as biolink CURIE."""
    if isinstance(case, str) and case.lower() == "pascal":
            return "biolink:" + snake_to_pascal(s, " ")
    elif isinstance(case, str) and case.lower() == "snake":
            return "biolink:" + s.replace(" ", "_")
    else:
        return "biolink:" + s


def with_formatting():
    """Add format conversions to method."""
    def decorator(func: Callable) -> Callable:
        """Generate decorator."""
        @wraps(func)
        def wrapper(self, s: str, *args, formatted=False, **kwargs):
            """Wrap in format conversions."""
            case = guess_casing(s)
            normalized = normalize(s)
            output: Union[str, List[str]] = func(self, normalized, *args, **kwargs)
            if formatted:
                if normalized in all_classes:
                    output = format(output, case="pascal")
                elif normalized in all_slots:
                    output = format(output, case="snake")
                else:
                    output = format(output, case=case)
            return output
        return wrapper
    return decorator
