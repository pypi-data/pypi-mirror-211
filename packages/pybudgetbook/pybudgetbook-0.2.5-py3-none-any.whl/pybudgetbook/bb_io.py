"""Manages folder structure of data folder and IO of data"""
from pathlib import Path
import os
import logging
import json
import pandas as pd
import h5py
import warnings
import shutil

from .configs import config
from .configs import constants
from . import __version__ as bbvers, name as bbname


logger = logging.getLogger(__package__)


def _findFilesExt(directory, ext):
    """Finds all files that have the extension(s) sepcified

    Walks through all folders and sub-folders and generates an iterator
    containing all files that match the extension. If a list is needed, use
    list(findFilesExt())

    Parameters
    ----------
    directory: `str`, `Path`
        Super directory to search for files
    ext: `list`, `str`
        List of string patterns that files have to match or a single string

    Returns
    -------
    (root, basename, filename): `generator` for `tuple`
        Generator for the tuple containing the root folder of the file,
        the basename (just the filename), and the filename as a full, absolute,
        path.
    """
    if not Path(directory).is_dir():
        logger.warning('Search directory does not exist')

    if isinstance(ext, str):
        ext = [ext]

    for root, _, files in os.walk(directory):
        for basename in files:
            if os.path.splitext(basename)[1] in ext:
                filename = os.path.join(root, basename)
                yield Path(root), basename, Path(filename)


def _unique_file_name(path):
    """
    Generates a unique file name adding numbers until a free name is found.

    Parameters
    ----------
    path : `Path`
        Inital file name to try

    Returns
    -------
    `Path`
        File name of a non-existing file.
    """
    if not path.exists():
        return path

    name, ext = os.path.splitext(path.name)
    i = 1
    while True:
        new_name = f"{name}_{i}{ext}"
        new_path = path.with_name(new_name)
        if not new_path.exists():
            return new_path
        i += 1


def _load_user_match_data(lang):
    """Loads user only match data for given language `lang`"""
    user_data = Path(config.options['data_folder']) / f'item_groups_{lang:s}.json'

    if not user_data.is_file():
        error = (f'No matching data for {lang:s} in user folder, please '
                 'create template to enable feedback of data.')
        logger.error(error)
        raise FileNotFoundError(error)

    else:
        with open(user_data, encoding='utf-8') as udd:
            result = json.load(udd)

    return result, user_data


def _load_basic_match_data(lang):
    """Loads package only match data for given language `lang`"""
    basic_data = Path(__file__).parent / 'group_templates' / f'item_groups_{lang:s}.json'

    if not basic_data.is_file():
        error = (f'No matching data for {lang:s} delivered with package, please '
                 'create PR if needed.')
        logger.error(error)
        raise FileNotFoundError(error)

    else:
        with open(basic_data, encoding='utf-8') as bdd:
            result = json.load(bdd)

    return result, basic_data


def _save_user_match_data(data, target):
    """
    Small wrapper aroung `json.dump()` to save user match data in the correct
    file.
    """
    if not target.is_file():
        logger.info('No matching data for in user folder, new file '
                    'will be created.')

    with open(target, 'w', encoding='utf-8') as udd:
        json.dump(data, udd, indent=4, ensure_ascii=False)


def load_negative_match_data(lang):
    """
    Loads negative group match data for a given language `lang`. This data is
    used to clean up matcher feedback with some very common words.
    """
    neg_data = Path(config.options['data_folder']) / f'negative_match_{lang:s}.json'

    if not neg_data.is_file():
        error = (f'No negative match data found for {lang:s}, please check '
                 'data folder or recopy templates')
        logger.error(error)
        raise FileNotFoundError(error)

    else:
        with open(neg_data, encoding='utf-8') as ndd:
            result = json.load(ndd)['neg_match_data']

    return result


def load_group_match_data(lang):
    """
    Load and merge match data from different locations for a given language.
    Currently, a package wide location and a user specific (that is data folder
    specific) location are implemented.

    Parameters
    ----------
    lang : `str`
        The language setting to use for loading.

    Returns
    -------
    result : `dict`
        Concatenated match data from user and package space.
    """
    basic_data = Path(__file__).parent / 'group_templates' / f'item_groups_{lang:s}.json'
    user_data = Path(config.options['data_folder']) / f'item_groups_{lang:s}.json'

    if not basic_data.is_file() and not user_data.is_file():
        error = ('Neither basic package matching data nor user matching data '
                 f'found for language {lang:s}')
        logger.error(error)
        raise FileNotFoundError(error)

    if not basic_data.is_file():
        logger.warning(f'No matching data for {lang:s} included with package')
        with open(user_data, encoding='utf-8') as udd:
            result = json.load(udd)

    elif not user_data.is_file():
        logger.warning(f'No matching data for {lang:s} in user folder')
        with open(basic_data, encoding='utf-8') as bdd:
            result = json.load(bdd)

    else:
        with open(basic_data, encoding='utf-8') as bdd:
            bd = json.load(bdd)

        with open(user_data, encoding='utf-8') as udd:
            ud = json.load(udd)

        result = dict()
        for key in ud.keys():
            if key in bd:
                result[key] = list(set(ud[key].copy()).union(set(bd[key].copy())))
            else:
                result[key] = ud[key].copy()
        for key in bd:
            if key not in result:
                result[key] = bd[key].copy()

    return result


def load_concatenad_data(work_dir=None):
    """
    Loads all data files from work dir and creates a concatenated dataset that
    checks that all mandatory columns are present.

    Parameters
    ----------
    work_dir : `Path`, optional
        Path to load the data from, by default None which chooses the data
        folder from the config.

    Returns
    -------
    `pd.DataFrame`
        Concatenated data from all datasets present in the folder.
    """
    if work_dir is None:
        data_files = Path(config.options['data_folder']) / 'data'
    else:
        data_files = Path(work_dir)

    data_files = list(_findFilesExt(data_files, '.hdf5'))
    n_files = len(data_files)

    conc_data = pd.DataFrame(columns=constants._MANDATORY_COLS)

    for _, _, file in data_files:
        this_dataset = load_with_metadata(file)
        conc_data = pd.concat((conc_data, this_dataset))

    return conc_data.sort_values('Date').reset_index(drop=True), n_files


def resort_data(data):
    """
    Ensures the correct column order and that all needed columns exists. Needed
    columns are defined in `constants`.
    """
    additional_cols = tuple(
        set(data.columns).difference(set(constants._MANDATORY_COLS)))
    data = data[list(constants._MANDATORY_COLS + additional_cols)]
    return data


def save_with_metadata(dataframe, target=None, img_path=None, unique_name=False,
                       move_on_save=False):
    """
    Saves a dataframe to hdf conserving possible attributes that are added to
    the dataframe. If img is specified, it will be moved to data folder (or
    copied)

    Parameters
    ----------
    dataframe : `pd.DataFrame`
        Data to save
    target : `Path`, optional
        Save target, by default None which creates a meaningful name from data
    img_path : `Path`, optional
        Image to copy / move and rename to the same name, by default None
    unique_name : `bool`, optional
        Generate a unique name to prevent override of existing files, by
        default False
    move_on_save : `bool`, optional
        Decides if the image is moved or copied, by default False
    """
    year = dataframe.loc[0, 'Date'].strftime('%Y')
    mon_day = dataframe.loc[0, 'Date'].strftime('%m_%d')
    if target is None:
        target = Path(config.options['data_folder']) / 'data' / year
        if not target.exists() or not target.is_dir():
            target.mkdir(parents=True, exist_ok=True)

        data_target = Path(target) / f'{mon_day:s}_{dataframe.loc[0, "Vendor"]:s}.hdf5'

    elif Path(target).is_dir():
        data_target = Path(target) / f'{mon_day:s}_{dataframe.loc[0, "Vendor"]:s}.hdf5'

    else:
        data_target = target

    if unique_name and data_target.exists():
        data_target = _unique_file_name(data_target)

    dataframe.attrs['version'] = bbvers
    dataframe.attrs['creator'] = bbname

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")

        dataframe.to_hdf(data_target, 'receipt', 'w', complevel=6, encoding='utf-8')

        with h5py.File(data_target, 'a') as hdfstore:
            # rec_grp = hdfstore['receipt']
            for name, val in dataframe.attrs.items():
                hdfstore.attrs.create(name, val)

    if img_path is not None:
        img_target = target / 'images' / data_target.with_suffix(img_path.suffix).name

        if not img_target.parent.exists() or not img_target.parent.is_dir():
            img_target.parent.mkdir(parents=True, exist_ok=True)

        if move_on_save:
            _ = shutil.move(img_path, img_target)
        else:
            _ = shutil.copy2(img_path, img_target)


def load_with_metadata(source):
    """
    Loads a pandas written h5 dataset and tries to retrieve any attributes that
    have been added to the dataset by the save function.

    Parameters
    ----------
    source : `Path`
        Location of file to load

    Returns
    -------
    `pd.DataFrame`
        Loaded data
    """
    receipt = pd.read_hdf(source, encoding='utf-8')
    with h5py.File(source) as hdfstore:
        att_dict = dict()
        for key, val in hdfstore.attrs.items():
            if not key.isupper():
                att_dict[key] = val

    receipt.attrs = att_dict

    return receipt
