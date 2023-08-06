from sonusai.mixture.apply_augmentation import apply_augmentation
from sonusai.mixture.class_count import get_class_count
from sonusai.mixture.generate_truth import generate_truth
from sonusai.mixture.get_class_weights_threshold import get_class_weights_threshold


def process_target(record: dict, mixdb: dict, raw_target_audio: list) -> dict:
    """Apply augmentation and update target metadata."""
    file_index = record['target_file_index']
    augmentation_index = record['target_augmentation_index']
    augmentation = mixdb['target_augmentations'][augmentation_index]

    audio = apply_augmentation(audio_in=raw_target_audio[file_index],
                               augmentation=augmentation,
                               length_common_denominator=mixdb['feature_step_samples'])

    # target_gain is used to back out the gain augmentation in order to return the target audio
    # to its normalized level when calculating truth.
    if 'gain' in augmentation:
        record['target_gain'] = 10 ** (augmentation['gain'] / 20)
    else:
        record['target_gain'] = 1

    record['samples'] = len(audio)

    truth_index = [sub['index'] for sub in
                   mixdb['targets'][file_index]['truth_settings']]

    truth = generate_truth(mixdb=mixdb,
                           record=record,
                           target=audio)

    class_weights_threshold = get_class_weights_threshold(mixdb)

    record['class_count'] = get_class_count(truth_index=truth_index,
                                            truth=truth,
                                            class_weights_threshold=class_weights_threshold)

    return record
