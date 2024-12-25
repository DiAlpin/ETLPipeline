"""Blender utils functions."""


def set_suffixes(config):
    """
    Used for Merge Blender. Retrieve or validate suffixes
    from configuration.
    """

    default_suffixes = ("_x", "_y")
    suffixes = config.get('suffixes', default_suffixes)

    if len(suffixes) != 2:
        raise ValueError(
            f'Invalid suffixes len: {suffixes}. ' \
            + 'Len must be 2.'
            )

    return suffixes
