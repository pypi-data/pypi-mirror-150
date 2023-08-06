def find(tree, *keys, include_keys=False, fail_fast=True):
    # pylint: skip-file
    """
    Recursively search for a key in an iterable object

    Args:
        include_keys:
            if false
                return value of keys i.e. ['value1', 'value2', '...']
            if true
                return result as a dict i.e. {'key': 'value'}

        tree: (iterable object):
        keys: (tuple): list of keys
        fail_fast: (bool): Defaults to True
            if True
                A KeyError is raised
            if False
                 returns None

    Returns:
        value: (Any): Key value

    Raises: (KeyError): Key not found
    """

    def tree_traverse(_tree, _key):
        for k, v in _tree.items():
            if k == _key:
                return v
            elif isinstance(v, dict):
                found = tree_traverse(v, _key)
                if found is not None:
                    return found

    results = {} if include_keys else []
    not_found = list()

    for key in keys:
        found_value = tree_traverse(tree, key)

        if found_value is not None or not fail_fast:
            if include_keys:
                results[key] = found_value
            else:
                results.append(found_value)
        else:
            not_found.append(key)

    if fail_fast and not_found:
        raise KeyError('Keys \'{}\' not found'.format(', '.join(not_found)))

    if isinstance(results, list):
        results = tuple(results)

    return results
