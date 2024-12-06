
import pytest

from etl.utils.blenders import set_suffixes


def test_default_suffixes():
    """
    Test that default suffixes are returned when no config is provided
    """
    config = {}
    result = set_suffixes(config)
    assert result == ("_x", "_y")

def test_custom_valid_suffixes():
    """
    Test that custom suffixes with exactly 2 elements are correctly returned
    """
    config = {'suffixes': ('a', 'b')}
    result = set_suffixes(config)
    assert result == ('a', 'b')


def test_single_suffix_raises_error():
    """
    Test that providing a single suffix raises a ValueError
    """
    config = {'suffixes': ('single',)}
    with pytest.raises(ValueError):
        set_suffixes(config)

def test_zero_suffixes_raises_error():
    """
    Test that providing no suffixes raises a ValueError
    """
    config = {'suffixes': ()}
    with pytest.raises(ValueError):
        set_suffixes(config)

def test_three_or_more_suffixes_raises_error():
    """
    Test that providing more than 2 suffixes raises a ValueError
    """
    config = {'suffixes': ('a', 'b', 'c')}
    with pytest.raises(ValueError):
        set_suffixes(config)
