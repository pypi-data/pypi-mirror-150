import copy

from open_serialzer.utils import dict_ops


def test_get_true_func():
    dict_1 = {
        "a1": {"a1": [1, 2, 3]},
        "b1": 2,
        "c1": 3,
    }
    dict_2 = {
        "a1": {"a1": [2, 3, 4]},
        "b1": 2,
        "c1": 4,
    }
    dict_gt_skip_duplicated = {
        "a1": {"a1": [1, 2, 3, 4]},
        "b1": 2,
        "c1": 4,
    }
    dict_gt_skip_extend = {
        "a1": {"a1": [1, 2, 3, 2, 3, 4]},
        "b1": 2,
        "c1": 4,
    }

    test_1 = copy.deepcopy(dict_1)
    dict_ops.merge_dict_recursively(test_1, dict_2, skip_duplicated_list=True)
    import pdb

    pdb.set_trace()
    assert test_1 == dict_gt_skip_duplicated

    test_2 = copy.deepcopy(dict_1)
    dict_ops.merge_dict_recursively(test_2, dict_2, skip_duplicated_list=False)
    assert test_2 == dict_gt_skip_extend
