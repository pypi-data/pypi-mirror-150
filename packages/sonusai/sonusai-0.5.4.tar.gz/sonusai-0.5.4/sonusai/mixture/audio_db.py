from os.path import exists
from os.path import expandvars
from typing import List

import numpy as np
from tqdm import tqdm

from sonusai import SonusAIError
from sonusai.mixture.apply_augmentation import apply_augmentation
from sonusai.mixture.read_audio import read_audio
from sonusai.utils import p_map

# NOTE: multiprocessing dictionary is required for run-time performance; using 'partial' is much slower.
MP_DICT = dict()


def build_noise_audio_db(mixdb: dict, show_progress: bool = False) -> List[dict]:
    """Build a list of noise audio data.

    Returns a list of dictionaries, each with the following keys:
        'file'            file index
        'augmentation'    augmentation index
        'audio'           audio samples
    """
    db = list()
    for file_index in tqdm(sorted(list(set([sub['noise_file_index'] for sub in mixdb['mixtures']]))),
                           desc='Read noise audio', disable=not show_progress):
        audio_in = read_audio(name=mixdb['noise_mix']['files'][file_index]['name'])
        for augmentation_index in sorted(list(set([sub['noise_augmentation_index'] for sub in mixdb['mixtures']]))):
            db.append({
                'file':         file_index,
                'augmentation': augmentation_index,
                'audio':        apply_augmentation(audio_in=audio_in,
                                                   augmentation=mixdb['noise_mix']['augmentations'][augmentation_index],
                                                   length_common_denominator=1)
            })
    return db


def get_noise_audio_from_db(db: List[dict], file_index: int, augmentation_index: int) -> np.ndarray:
    """Locate a record in a noise audio database using file and augmentation indices and return the audio samples."""
    for record in db:
        if record['file'] == file_index and record['augmentation'] == augmentation_index:
            return record['audio']

    raise SonusAIError(f'Could not find file_index {file_index} and augmentation_index '
                       f'{augmentation_index} in noise database')


def build_target_audio_db(mixdb: dict, show_progress: bool = False) -> list:
    """Build a list of target audio data.

    Returns a list of dictionaries, each with the following keys:
        'file'  file index
        'audio' audio samples
    """
    MP_DICT['mixdb'] = mixdb

    indices = sorted(list(set([sub['target_file_index'] for sub in mixdb['mixtures']])))
    progress = tqdm(total=len(indices), desc='Read target audio', disable=not show_progress)
    db = p_map(_read_target_audio, indices, progress=progress)
    return db


def _read_target_audio(file_index: int) -> dict:
    """Parallel target audio reader kernel."""
    mixdb = MP_DICT['mixdb']
    return {
        'file':  file_index,
        'audio': read_audio(name=mixdb['targets'][file_index]['name'])
    }


def get_target_audio_from_db(db: List[dict], file_index: int) -> np.ndarray:
    """Locate a record in a target audio database using file index and return the audio samples."""
    for record in db:
        if record['file'] == file_index:
            return record['audio']

    raise SonusAIError(f'Could not find file_index {file_index} in target database')


def check_audio_files_exist(mixdb: dict) -> None:
    """Walk through all the noise and target audio files in a mixture database ensuring that they exist."""
    for file_index in sorted(list(set(sub['noise_file_index'] for sub in mixdb['mixtures']))):
        file_name = expandvars(mixdb['noise_mix']['files'][file_index]['name'])
        if not exists(file_name):
            raise SonusAIError(f'Could not find {file_name}')

    for file_index in sorted(list(set(sub['target_file_index'] for sub in mixdb['mixtures']))):
        file_name = expandvars(mixdb['targets'][file_index]['name'])
        if not exists(file_name):
            raise SonusAIError(f'Could not find {file_name}')
