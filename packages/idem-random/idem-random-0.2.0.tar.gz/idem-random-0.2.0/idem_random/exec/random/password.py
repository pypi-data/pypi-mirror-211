import random
from typing import List


async def generate_random_string(hub, length: int, **params):
    """
    generate random string
    """

    ret = dict(comment=[], ret="", result=True)

    num_chars = "0123456789"
    lower_chars = "abcdefghijklmnopqrstuvwxyz"
    upper_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    special_chars = "!@#$%&*()-_=+[]{}<>:?"
    if params.get("override_special", None):
        special_chars = params.get("override_special")

    chars = ""
    if params.get("upper", True):
        chars = chars + upper_chars

    if params.get("lower", True):
        chars = chars + lower_chars

    if params.get("numeric", True):
        chars = chars + num_chars

    if params.get("special", True):
        chars = chars + special_chars

    min_mapping = {
        "num_chars": params.get("min_numeric", 0),
        "lower_chars": params.get("min_lower", 0),
        "upper_chars": params.get("min_upper", 0),
        "special_chars": params.get("min_special", 0),
    }

    result = []

    for k, v in min_mapping.items():
        if k == "num_chars":
            result.extend(generate_random_bytes(num_chars, v))
        elif k == "lower_chars":
            result.extend(generate_random_bytes(lower_chars, v))
        elif k == "upper_chars":
            result.extend(generate_random_bytes(upper_chars, v))
        elif k == "special_chars":
            result.extend(generate_random_bytes(special_chars, v))

    try:
        result.extend(generate_random_bytes(chars, length - len(result)))
    except Exception as e:
        ret["comment"].append(str(e))
        ret["result"] = False
        return result

    resultant_string = "".join(result)
    ret["comment"].append("Successfully generated password")
    ret["ret"] = resultant_string
    return ret


def generate_random_bytes(chars: str, length: int) -> List:
    random_bytes = [None] * length
    limit = len(chars)
    for i in range(length):
        idx = random.randint(0, limit - 1)
        random_bytes[i] = chars[idx]

    return random_bytes
