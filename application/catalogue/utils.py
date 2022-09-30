import re


def validate_sizes(sizes):
    """
    :param sizes: (string) for example 23-30
    :return: boolean
    """
    items = re.split("-", sizes)
    if len(items) != 2:
        return False
    for item in items:
        if not re.search(r"^\d{2}(\.\d)?$", item):
            return False
    if float(items[1]) <= float(items[0]):
        return False
    return True


def get_sizes_list_from_range(sizes: str):
    """
    Pass sizes in format, i.e. '22.5-26' and get list ['22.5', '23', '24', '25']
    :param sizes: (str)
    :return: (list)
    """
    float_min, float_max = [float(size) for size in sizes.split('-')]
    int_min, int_max = int(float_min), int(float_max)
    size_min = int(float_min) if int(float_min) == float_min else float_min
    size_max = int(float_max) if int(float_max) == float_max else float_max
    floats_range = [size_min, *range(int_min, int_max)[1:], size_max]
    return [str(size) for size in floats_range]

