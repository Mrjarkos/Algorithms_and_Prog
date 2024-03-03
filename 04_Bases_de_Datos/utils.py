def common_keys(dict1, dict2) -> list:
    # Get the intersection of keys from both dictionaries
    common_keys_set = set(dict1.keys()) & set(dict2.keys())
    return list(common_keys_set)

