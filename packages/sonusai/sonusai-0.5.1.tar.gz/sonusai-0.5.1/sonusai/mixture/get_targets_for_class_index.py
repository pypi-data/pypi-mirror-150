def get_targets_for_class_index(mixdb: dict, class_index: int) -> list:
    target_indices = set()
    for target_index, target in enumerate(mixdb['targets']):
        for truth_setting in target['truth_settings']:
            for index in truth_setting['index']:
                if index == class_index + 1:
                    target_indices.add(target_index)
    return sorted(list(target_indices))
