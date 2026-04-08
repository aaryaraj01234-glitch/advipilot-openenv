def grade(output, expected):
    if isinstance(expected, list):
        return sum([1 for i in expected if i in output]) / len(expected)
    return 1 if expected in str(output) else 0