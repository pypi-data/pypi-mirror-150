def spacer(string: str, max_length: int = 22) -> str:
    """
    Return a string full of whitespace that match the diff between the provided string len and the max_length parameter.

    :param string:
    :param max_length:
    :return:
    """
    if len(string) >= max_length:
        raise ValueError("Attribute max_length must be superior then string length")

    diff_len = max_length - len(string)

    res = ""
    for _ in range(diff_len):
        res += " "

    return res
