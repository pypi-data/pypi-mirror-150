from typing import List
from typing import Union

import numpy as np

from sonusai.mixture import get_file_frame_segments


def get_mixid_data(mixdb: dict,
                   mixid: Union[str, List[int]],
                   truth_f: np.ndarray,
                   predict: np.ndarray) -> (np.ndarray, np.ndarray):
    """Collect per-feature data of specified mixids from mixdb where inputs are:
       truth_f:   truth data matching mixdb (size #feature_frames x num_classes)
       predict:   prediction or segsnr data size #feature_frames x ndim (ndim > 1)

    Returns:
        ytrue:    np.array combined truth from mixids
        ypred:    np.array combined data from mixids
    """
    num_classes = truth_f.shape[1]
    # same as num_class for prediction data, but use for segsnr too
    dnum = predict.shape[1]

    file_frame_segments = get_file_frame_segments(mixdb, mixid)
    total_frames = sum([file_frame_segments[m].length for m in file_frame_segments])
    ytrue = np.empty((total_frames, num_classes), dtype=np.single)
    ypred = np.empty((total_frames, dnum), dtype=np.single)
    start = 0
    for m in file_frame_segments:
        length = file_frame_segments[m].length
        ytrue[start:start + length] = truth_f[file_frame_segments[m].get_slice()]
        ypred[start:start + length] = predict[file_frame_segments[m].get_slice()]
        start += length

    return ytrue, ypred
