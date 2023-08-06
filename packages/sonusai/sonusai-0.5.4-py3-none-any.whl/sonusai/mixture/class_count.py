from typing import List
from typing import Union

import numpy as np

from sonusai import SonusAIError
from sonusai.mixture.get_mixtures_from_mixid import get_mixtures_from_mixid


def get_class_count(truth_index: List[List[int]],
                    truth: np.ndarray,
                    class_weights_threshold: List[float]) -> List[List[int]]:
    """Computes the number of samples for which each truth index is active for a given sample-based truth input."""
    class_count = [[] for _ in range(len(truth_index))]
    for n in range(len(truth_index)):
        class_count[n] = [0] * len(truth_index[n])
        for idx, cl in enumerate(truth_index[n]):
            truth_sum = int(np.sum(truth[:, cl - 1] >= class_weights_threshold[cl - 1]))
            class_count[n][idx] = truth_sum

    return class_count


def get_total_class_count(mixdb: dict, mixid: Union[str, List[int]] = ':') -> List[int]:
    """Sums the class counts for all mixtures."""
    mixtures = get_mixtures_from_mixid(mixdb, mixid)
    return compute_total_class_count(mixdb, mixtures)


def compute_total_class_count(mixdb: dict, records: List[dict]) -> List[int]:
    total_class_count = [0] * mixdb['num_classes']
    for record in records:
        truth_indices = [sub['index'] for sub in mixdb['targets'][record['target_file_index']]['truth_settings']]
        for n in range(len(truth_indices)):
            for idx, cl in enumerate(truth_indices[n]):
                total_class_count[cl - 1] += int(record['class_count'][n][idx])

    if mixdb['truth_mutex']:
        # Compute the class count for the 'other' class
        if total_class_count[-1] != 0:
            raise SonusAIError('Error: truth_mutex was set, but the class count for the last count was non-zero.')
        total_class_count[-1] = sum([sub['samples'] for sub in records]) - sum(total_class_count)

    return total_class_count
