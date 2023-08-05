from typing import List


def get_class_balancing_samples(mixdb: dict) -> List[int]:
    """Determine the number of additional samples needed for each class in order for all classes to be represented
    evenly over all mixtures.

    If the truth mode is mutually exclusive, ignore the last class (i.e., set to zero).
    """
    import numpy as np

    class_count = mixdb['class_count']

    if mixdb['truth_mutex']:
        class_count = class_count[:-1]

    result = list(np.max(class_count) - class_count)

    if mixdb['truth_mutex']:
        result.append(0)

    return result


def get_unused_balancing_augmentations(mixdb: dict, target_file_index: int) -> List[int]:
    """Get a list of unused balancing augmentations for a given target file index."""
    balancing_augmentations = [item for item in range(len(mixdb['target_augmentations'])) if
                               item >= mixdb['first_balancing_augmentation_index']]
    used_balancing_augmentations = [sub['target_augmentation_index'] for sub in mixdb['mixtures'] if
                                    sub['target_file_index'] == target_file_index and
                                    sub['target_augmentation_index'] in balancing_augmentations]
    return [item for item in balancing_augmentations if
            item not in used_balancing_augmentations]
