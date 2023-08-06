import multiprocessing as mp
from typing import List

import numpy as np
from tqdm import tqdm

from sonusai import SonusAIError
from sonusai import logger
from sonusai.mixture.augmentation_rules import get_augmentations
from sonusai.mixture.class_count import compute_total_class_count
from sonusai.mixture.get_targets_for_truth_index import get_targets_for_truth_index
from sonusai.mixture.process_target import process_target
from sonusai.utils.p_tqdm import p_map

# NOTE: multiprocessing dictionary is required for run-time performance; using 'partial' is much slower.
MP_DICT = dict()


def balance_classes(mixdb: dict,
                    augmented_targets: List[dict],
                    class_balancing_augmentation: dict,
                    raw_target_audio: list) -> List[dict]:
    """Add target augmentations until the class count values are balanced."""
    if not class_balancing_augmentation:
        return augmented_targets

    first_cba_index = len(mixdb['target_augmentations'])

    MP_DICT['mixdb'] = mixdb
    MP_DICT['raw_target_audio'] = raw_target_audio

    for class_index, required_samples in enumerate(get_class_balancing_samples(mixdb, augmented_targets)):
        augmented_targets = _balance_class(mixdb=mixdb,
                                           augmented_targets=augmented_targets,
                                           class_balancing_augmentation=class_balancing_augmentation,
                                           first_cba_index=first_cba_index,
                                           class_index=class_index,
                                           required_samples=required_samples)

    return augmented_targets


def _balance_class(mixdb: dict,
                   augmented_targets: List[dict],
                   class_balancing_augmentation: dict,
                   first_cba_index: int,
                   class_index: int,
                   required_samples: int) -> List[dict]:
    """Add target augmentations for a single class until the required samples are satisfied."""
    if required_samples == 0:
        return augmented_targets

    class_label = mixdb['class_labels'][class_index]
    logger.info(f'Balancing "{class_label}" class')
    logger.info(f'  Need {required_samples} more active truth samples')

    # Get list of targets for this class
    target_indices = get_targets_for_truth_index(mixdb, class_index)
    if not target_indices:
        raise SonusAIError(f'Could not find single-class targets for class index {class_index}')

    num_cpus = mp.cpu_count()

    added_targets = 0
    while True:
        records = []
        while len(records) < num_cpus:
            for target_index in target_indices:
                augmentation_indices = get_unused_balancing_augmentations(mixdb=mixdb,
                                                                          augmented_targets=augmented_targets,
                                                                          first_cba_index=first_cba_index,
                                                                          target_file_index=target_index,
                                                                          rule=class_balancing_augmentation,
                                                                          amount=num_cpus)
                for augmentation_index in augmentation_indices:
                    records.append({
                        'target_file_index':         target_index,
                        'target_augmentation_index': augmentation_index,
                    })

        progress = tqdm(desc='balance ' + class_label, disable=True)
        records = p_map(_process_target, records, progress=progress)
        progress.close()

        for record in records:
            new_samples = np.sum(np.sum(record['class_count']))
            required_samples -= new_samples

            # If the current record will overshoot the required samples then add it only if
            # overshooting results in a sample count closer to the required than not overshooting.
            add_record = required_samples >= 0 or -required_samples < required_samples + new_samples

            if add_record:
                augmented_targets.append(record)
                added_targets += 1

            if required_samples <= 0:
                remove_unused_augmentations(mixdb=mixdb, records=augmented_targets)
                logger.info(f'  Added {added_targets} new augmentations')
                return augmented_targets


def _process_target(record: dict) -> dict:
    return process_target(record=record, mixdb=MP_DICT['mixdb'], raw_target_audio=MP_DICT['raw_target_audio'])


def get_class_balancing_samples(mixdb: dict, augmented_targets: List[dict]) -> List[int]:
    """Determine the number of additional active truth samples needed for each class in order for
    all classes to be represented evenly over all mixtures.

    If the truth mode is mutually exclusive, ignore the last class (i.e., set to zero).
    """
    class_count = compute_total_class_count(mixdb, augmented_targets)

    if mixdb['truth_mutex']:
        class_count = class_count[:-1]

    result = list(np.max(class_count) - class_count)

    if mixdb['truth_mutex']:
        result.append(0)

    return result


def get_unused_balancing_augmentations(mixdb: dict,
                                       augmented_targets: List[dict],
                                       first_cba_index: int,
                                       target_file_index: int,
                                       rule: dict,
                                       amount: int = 1) -> List[int]:
    """Get a list of unused balancing augmentations for a given target file index."""
    balancing_augmentations = [item for item in range(len(mixdb['target_augmentations'])) if
                               item >= first_cba_index]
    used_balancing_augmentations = [sub['target_augmentation_index'] for sub in augmented_targets if
                                    sub['target_file_index'] == target_file_index and
                                    sub['target_augmentation_index'] in balancing_augmentations]

    augmentation_indices = [item for item in balancing_augmentations if item not in used_balancing_augmentations]

    while len(augmentation_indices) < amount:
        new_augmentation = get_augmentations(rule)[0]
        mixdb['target_augmentations'].append(new_augmentation)
        augmentation_indices.append(len(mixdb['target_augmentations']) - 1)

    return augmentation_indices


def remove_unused_augmentations(mixdb: dict, records: List[dict]) -> None:
    """Remove any unused target augmentation rules from the end of the database."""
    max_used_augmentation = max([sub['target_augmentation_index'] for sub in records]) + 1
    mixdb['target_augmentations'] = mixdb['target_augmentations'][0:max_used_augmentation]
