
import os
import sys
import logging
import functools
import json
import concurrent.futures
from datetime import datetime
import argparse
import csv
import warnings
import numpy as np
import librosa

from koogu.data import FilenameExtensions, AssetsExtraNames
from koogu.data.raw import Process, Settings
from koogu.utils import instantiate_logging
from koogu.utils.detections import SelectionTableReader, LabelHelper
from koogu.utils.terminal import ArgparseConverters
from koogu.utils.config import Config, ConfigError, datasection2dict, log_config
from koogu.utils.filesystem import restrict_classes_with_whitelist_file, \
    AudioFileList, get_valid_audio_annot_entries, recursive_listing

_program_name = 'prepare_data'


def from_selection_table_map(audio_settings, audio_seltab_list,
                             audio_root, seltab_root, output_root,
                             label_column_name=None,
                             desired_labels=None,
                             remap_labels_dict=None,
                             negative_class_label=None,
                             **kwargs):
    """
    Pre-process training data using info contained in ``audio_seltab_list``.

    :param audio_settings: A dictionary specifying the parameters for processing
        audio from files.
    :param audio_seltab_list: A list containing pairs (tuples or sub-lists) of
        relative paths to audio files and the corresponding annotation
        (selection table) files. Alternatively, you could also specify (path to)
        a 2-column csv file containing these pairs of entries (in the same
        order). Only use the csv option if the paths are simple (i.e., the
        filenames do not contain commas or other special characters).
    :param audio_root: The full paths of audio files listed in
        ``audio_seltab_list`` are resolved using this as the base directory.
    :param seltab_root: The full paths of annotations files listed in
        ``audio_seltab_list`` are resolved using this as the base directory.
    :param output_root: "Prepared" data will be written to this directory.
    :param label_column_name: A string identifying the header of the column in
        the selection table file(s) from which class labels are to be extracted.
        If None (default), will look for a column with the header "Tags".
    :param desired_labels: The target set of class labels. If not None, must be
        a list of class labels. Any selections (read from the selection tables)
        having labels that are not in this list will be discarded. This list
        will be used to populate classes_list.json that will define the classes
        for the project. If None, then the list of classes will be populated
        with the annotation labels read from all selection tables.
    :param remap_labels_dict: If not None, must be a Python dictionary
        describing mapping of class labels. For details, see similarly named
        parameter to the constructor of
        :class:`koogu.utils.detections.LabelHelper`.

        .. note:: If ``desired_labels`` is not None, mappings for which targets
           are not listed in ``desired_labels`` will be ignored.

    :param negative_class_label: A string (e.g. 'Other', 'Noise') which will be
        used as a label to identify the negative class clips (those that did not
        match any annotations). If None (default), saving of negative class
        clips will be disabled.

    Other parameters specific to
    :func:`koogu.utils.detections.assess_annotations_and_clips_match`
    can also be specified, and will be passed as-is to the function.

    :return: A dictionary whose keys are annotation tags (either discovered from
        the set of annotations, or same as ``desired_labels`` if not None) and
        the values are the number of clips produced for the corresponding class.
    """

    logger = logging.getLogger(__name__)

    # Discard invalid entries, if any
    v_audio_seltab_list = get_valid_audio_annot_entries(
            audio_seltab_list, audio_root, seltab_root, logger=logger)
    if len(v_audio_seltab_list) == 0:
        print('Nothing to process')
        return {}

    classes_n_counts = annot_classes_and_counts(
        seltab_root,
        [e[-1] for e in v_audio_seltab_list],
        label_column_name or "Tags",
        **({'num_threads': kwargs['num_threads']} if 'num_threads' in kwargs
           else {})
    )

    logger.info('  {:<55s} - {:>5s}'.format('Class', 'Annotations'))
    logger.info('  {:<55s}   {:>5s}'.format('-----', '-----------'))
    for class_name in sorted(classes_n_counts.keys()):
        logger.info('  {:<55s} - {:>5d}'.format(class_name,
                                                classes_n_counts[class_name]))

    ig_kwargs = {}      # Undocumented settings
    if negative_class_label is not None:
        if 'ignore_zero_annot_files' in kwargs:
            ig_kwargs['ignore_zero_annot_files'] = \
                kwargs.pop('ignore_zero_annot_files')
        if 'filetypes' in kwargs:
            ig_kwargs['filetypes'] = kwargs.pop('filetypes')
    input_generator = AudioFileList.from_annotations(
        v_audio_seltab_list,
        audio_root, seltab_root,
        label_column_name or "Tags",
        show_progress=kwargs.pop('show_progress', False),
        **ig_kwargs)

    # Re-map parameter names and add defaults for any missing ones
    if 'positive_overlap_threshold' in kwargs:
        if 'min_annot_overlap_fraction' in kwargs:
            kwargs.pop('positive_overlap_threshold')
            warnings.showwarning(
                'Parameter \'positive_overlap_threshold\' is deprecated and ' +
                'will be removed in the future. Ignoring the parameter since ' +
                '\'min_annot_overlap_fraction\' is also specified.',
                DeprecationWarning, 'prepare_data.py', '')
        else:
            kwargs['min_annot_overlap_fraction'] = \
                np.float16(kwargs.pop('positive_overlap_threshold'))
            warnings.showwarning(
                'Parameter \'positive_overlap_threshold\' is deprecated and ' +
                'will be removed in the future. Use ' +
                '\'min_annot_overlap_fraction\' instead.',
                DeprecationWarning, 'prepare_data.py', '')
    if 'negative_overlap_threshold' in kwargs:
        if 'max_nonmatch_overlap_fraction' in kwargs:
            kwargs.pop('negative_overlap_threshold')
            warnings.showwarning(
                'Parameter \'negative_overlap_threshold\' is deprecated and ' +
                'will be removed in the future. Ignoring the parameter since ' +
                '\'max_nonmatch_overlap_fraction\' is also specified.',
                DeprecationWarning, 'prepare_data.py', '')
        else:
            kwargs['max_nonmatch_overlap_fraction'] = \
                np.float16(kwargs.pop('negative_overlap_threshold'))
            warnings.showwarning(
                'Parameter \'negative_overlap_threshold\' is deprecated and ' +
                'will be removed in the future. Use ' +
                '\'max_nonmatch_overlap_fraction\' instead.',
                DeprecationWarning, 'prepare_data.py', '')

    return _batch_process(
        audio_settings,
        [lbl for lbl in classes_n_counts.keys()],
        input_generator,
        audio_root, output_root,
        desired_labels=desired_labels,
        remap_labels_dict=remap_labels_dict,
        negative_class_label=negative_class_label,
        **kwargs)


def from_top_level_dirs(audio_settings, class_dirs,
                        audio_root, output_root,
                        remap_labels_dict=None,
                        **kwargs):
    """
    Pre-process training data available as audio files in ``class_dirs``.

    :param audio_settings: A dictionary specifying the parameters for processing
        audio from files.
    :param class_dirs: A list containing relative paths to class-specific
        directories containing audio files. Each directory's contents will be
        recursively searched for audio files.
    :param audio_root: The full paths of the class-specific directories listed
        in ``class_dirs`` are resolved using this as the base directory.
    :param output_root: "Prepared" data will be written to this directory.
    :param remap_labels_dict: If not None, must be a Python dictionary
        describing mapping of class labels. For details, see similarly named
        parameter to the constructor of
        :class:`koogu.utils.detections.LabelHelper`.
    :param filetypes: (optional) Restrict listing to files matching extensions
        specified in this parameter. Has defaults if unspecified.

    :return: A dictionary whose keys are annotation tags (discovered from the
        set of annotations) and the values are the number of clips produced for
        the corresponding class.
    """

    logger = logging.getLogger(__name__)

    file_types = kwargs.pop('filetypes', AudioFileList.default_audio_filetypes)

    logger.info('  {:<55s} - {:>5s}'.format('Class', 'Files'))
    logger.info('  {:<55s}   {:>5s}'.format('-----', '-----'))
    for class_name in class_dirs:
        count = 0
        for _ in recursive_listing(os.path.join(audio_root, class_name),
                                   file_types):
            count += 1
        logger.info('  {:<55s} - {:>5d}'.format(class_name, count))

    input_generator = AudioFileList.from_directories(
        audio_root, class_dirs, file_types,
        show_progress=kwargs.pop('show_progress', False))

    return _batch_process(
        audio_settings, class_dirs, input_generator,
        audio_root, output_root,
        remap_labels_dict=remap_labels_dict,
        **kwargs)


def _batch_process_wrapper(func):
    """
    Logs the running time of _batch_process() and its outputs, and saves classes
    list.
    """
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):

        logger = logging.getLogger(__name__)

        t_start = datetime.now()
        logger.info('Started at: {}'.format(t_start))

        final_classes, per_class_clip_counts = func(*args, **kwargs)

        t_end = datetime.now()
        logger.info('Finished at: {}'.format(t_end))
        logger.info('Processing time (hh:mm:ss.ms) {}'.format(t_end - t_start))

        logger.info('Results:')
        logger.info('  {:<55s} - {:>5s}'.format('Class', 'Clips'))
        logger.info('  {:<55s}   {:>5s}'.format('-----', '-----'))
        for class_name, clip_count in per_class_clip_counts.items():
            logger.info('  {:<55s} - {:>5d}'.format(class_name, clip_count))

        # Write out the list of class names
        json.dump(
            final_classes,
            open(os.path.join(args[4], AssetsExtraNames.classes_list), 'w'))

        return per_class_clip_counts

    return wrapper_timer


@_batch_process_wrapper
def _batch_process(audio_settings, class_list, input_generator,
                   audio_root, dest_root,
                   desired_labels=None,
                   remap_labels_dict=None,
                   negative_class_label=None,
                   **kwargs):
    # If not None, will mean that we'll be saving seltab negatives

    logger = logging.getLogger(__name__)

    # Warn about existing output directory
    if os.path.exists(dest_root) and os.path.isdir(dest_root):
        warnings.showwarning(
            f'Output directory {dest_root} already exists. Contents may get ' +
            'overwritten.', Warning, _program_name, '')

    if not os.path.exists(dest_root):
        os.makedirs(dest_root, exist_ok=True)

    audio_settings = Settings.Audio(**audio_settings)

    label_helper = LabelHelper(desired_labels if desired_labels else class_list,
                               remap_labels_dict=remap_labels_dict,
                               negative_class_label=negative_class_label,
                               fixed_labels=(desired_labels is not None),
                               assessment_mode=False)

    num_classes = len(label_helper.classes_list)
    per_class_clip_counts = {c: 0 for c in label_helper.classes_list}

    # List of desired and 'to be mapped' labels
    valid_classes = [lbl for lbl in label_helper.labels_to_indices.keys()]

    def handle_outcome(future_h, a_file, num_annots):
        # internal use utility function
        try:
            file_num_clips, file_per_class_clip_counts = future_h.result()
        except Exception as ho_exc:
            logger.error(
                'Processing file {:s} generated an exception: {:s}'.format(
                    repr(audio_file), repr(ho_exc)))
        else:
            if num_annots is not None:   # Seltabs were available
                if label_helper.negative_class_index is not None:
                    # Negative clips were written too
                    logger.info('{:s}: {:d} annotations. Wrote {:d} clips including {:d} non-target'.format(
                        a_file, num_annots, file_num_clips, file_per_class_clip_counts[label_helper.negative_class_index]))
                else:
                    logger.info('{:s}: {:d} annotations. Wrote {:d} clips'.format(
                        a_file, num_annots, file_num_clips))
            else:   # Top-level directories were processed
                logger.info('{:s}: Wrote {:d} clips'.format(a_file, file_num_clips))

            for c, ci in zip(label_helper.classes_list,
                             file_per_class_clip_counts):
                per_class_clip_counts[c] += ci

    file_min_dur = float(audio_settings.clip_length) / float(audio_settings.fs)     # Set to clip duration
    file_max_dur = kwargs.pop('max_file_duration', np.inf)

    num_workers = kwargs.pop('num_threads', os.cpu_count() or 1)
    futures_dict = {}
    # Keep up to 3 * num_workers in futures_dict so that in cases where there are very many files to process, the size
    # of futures_dict (and in turn the queuing mechanism in concurrent.futures) doesn't end up hindering memory use.
    # Continue adding more items as and when processing of previous items complete.
    with concurrent.futures.ProcessPoolExecutor(max_workers=num_workers) as executor:
        for audio_file, annots_times, annots_labels, annot_channels in input_generator:

            audio_file_fullpath = os.path.join(audio_root, audio_file)

            # If file is too short or too long, discard and continue to next
            file_dur = librosa.get_duration(filename=audio_file_fullpath)
            if not (file_min_dur < file_dur <= file_max_dur):
                logger.warning('%s: duration = %f s. Ignoring.',
                               repr(audio_file_fullpath), file_dur)
                continue

            # Derive destination paths. Create directories as necessary
            rel_path, filename = os.path.split(audio_file)
            target_filename = filename + FilenameExtensions.numpy
            target_dir = os.path.join(dest_root, rel_path)
            os.makedirs(target_dir, exist_ok=True)

            # Based on remap_labels_dict or desired_labels, some labels may
            # become invalid. Write out only the valid ones.
            if annots_times is None:     # invoked by from_top_level_dirs()
                if annots_labels not in valid_classes:
                    continue    # Not in desired classes. Skip.

            else:                        # invoked by from_selection_table_map()
                valid_annots_idxs = [
                    idx for idx, lbl in enumerate(annots_labels)
                    if lbl in valid_classes]

                annots_times = annots_times[valid_annots_idxs, :]
                annot_channels = annot_channels[valid_annots_idxs]
                annots_labels = [
                    annots_labels[idx] for idx in valid_annots_idxs]

            # Build dictionary of args for Process.audio2clips()
            a2c_kwargs = {**kwargs}     # copy remaining unpopped kwargs
            if annots_times is None:     # invoked by from_top_level_dirs()
                a2c_kwargs['annots_times'] = None
                a2c_kwargs['annots_class_idxs'] = \
                    label_helper.labels_to_indices[annots_labels]
                a2c_kwargs['annots_channels'] = None
            else:                        # invoked by from_selection_table_map()
                a2c_kwargs['annots_times'] = annots_times
                a2c_kwargs['annots_class_idxs'] = np.asarray([
                    label_helper.labels_to_indices[c] for c in annots_labels])
                a2c_kwargs['annots_channels'] = annot_channels
                if label_helper.negative_class_index is not None:
                    a2c_kwargs['negative_class_idx'] = \
                        label_helper.negative_class_index

            # If many items are already currently being processed, wait for and handle one finished result before adding
            # a new one to processing queue.
            if len(futures_dict) >= num_workers * 3:
                # Using a loop here only because it is safe. Will 'break' out after the first item anyways.
                del_future_h = None
                for future in concurrent.futures.as_completed(futures_dict):
                    handle_outcome(future, *futures_dict[future])

                    # Copy handle for deletion and get out
                    del_future_h = future
                    break

                # Deleting outside of the above loop, coz it may be unsafe to do so while in a generator
                if del_future_h is not None:
                    del futures_dict[del_future_h]

            # Now add to the processing queue
            futures_dict[executor.submit(Process.audio2clips,
                                         audio_settings,
                                         audio_file_fullpath,
                                         os.path.join(target_dir, target_filename),
                                         num_classes=num_classes,
                                         **a2c_kwargs)] = \
                (audio_file, None if annots_times is None else annots_times.shape[0])

        # Now wait for the trailing futures
        for future in concurrent.futures.as_completed(futures_dict):
            handle_outcome(future, *futures_dict[future])

    return label_helper.classes_list, per_class_clip_counts


def annot_classes_and_counts(seltab_root, annot_files, label_column_name,
                             **kwargs):
    """
    Query the list of annot_files to determine the unique labels present and
    their respective counts.
    Returns a dictionary mapping unique labels to respective counts.
    """

    logger = logging.getLogger(__name__)
    num_workers = kwargs['num_threads'] if 'num_threads' in kwargs else \
        max(1, os.cpu_count() - 1)

    filespec = [
        (label_column_name, str),
        ('Begin Time (s)', float),
        ('End Time (s)', float)]

    # Discard invalid entries, if any
    valid_entries_mask = [
        os.path.isfile(
            af if seltab_root is None else os.path.join(seltab_root, af))
        for af in annot_files
    ]

    if seltab_root is None:
        full_path = lambda x: x
    else:
        full_path = lambda x: os.path.join(seltab_root, x)

    futures_dict = dict()
    retval = dict()
    with concurrent.futures.ProcessPoolExecutor(max_workers=num_workers) as executor:
        for is_valid, annot_file in zip(valid_entries_mask, annot_files):
            if not is_valid:
                logger.error('File {:s} not found. Skipping entry...'.format(annot_file))
            else:
                futures_dict[executor.submit(_get_labels_counts_from_annot_file,
                                             full_path(annot_file), filespec)] = annot_file

        if len(futures_dict) == 0:
            logger.error('Nothing to process')
            return {}

        for future in concurrent.futures.as_completed(futures_dict):
            try:
                uniq_labels, label_counts = future.result()
            except Exception as ho_exc:
                logger.error('Reading file {:s} generated an exception: {:s}'.format(
                    repr(futures_dict[future]), repr(ho_exc)))
            else:
                for ul, lc in zip(uniq_labels, label_counts):
                    if ul in retval:
                        retval[ul] += lc
                    else:
                        retval[ul] = int(lc)

    return retval


def _get_labels_counts_from_annot_file(annot_filepath, filespec):
    """Helper function for annot_classes_and_counts()"""
    labels = [entry[0]
              for entry in SelectionTableReader(annot_filepath, filespec)
              if all([e is not None for e in entry])]
    return np.unique(labels, return_counts=True)


def _instantiate_logging(args, audio_settings):
    # Create the logger
    logging.basicConfig(filename=args.log if args.log is not None else os.path.join(args.dst, _program_name + '.log'),
                        filemode='w', level=args.loglevel, format='[%(levelname).1s] %(funcName)s: %(message)s')

    logger = logging.getLogger(__name__)

    logger.info('Command-line arguments: {}'.format({k: v for k, v in vars(args).items() if v is not None}))
    logger.info('Audio settings: {}'.format(audio_settings))


# def _audio_settings_from_config(cfg_file):
#     """Load audio settings parameters from the config file and return a Settings.Audio instance"""
#
#     cfg = Config(cfg_file, 'DATA')
#
#     audio_settings = {
#         'clip_length': cfg.DATA.audio_clip_length,
#         'clip_advance': cfg.DATA.audio_clip_advance,
#         'desired_fs': cfg.DATA.audio_fs,
#         'filterspec': cfg.DATA.audio_filterspec
#     }
#
#     # Validate settings
#     _ = Settings.Audio(**audio_settings)    # Will throw, if failure. Will be caught by caller
#
#     return audio_settings


__all__ = ['from_selection_table_map', 'from_top_level_dirs']


if __name__ == '__main__':

    parser = argparse.ArgumentParser(prog=_program_name, allow_abbrev=False,
                                     description='Prepare audio data before their conversion to TFRecords.')
    parser.add_argument('cfg', metavar='<CONFIG FILE>',
                        help='Path to config file.')
    parser.add_argument('src', metavar='<AUDIO SOURCE>',
                        help='Path to either a single audio file or to a directory. When a directory, if selection ' +
                             'table info is also provided (using \'selmap\'), then this must be the root path from ' +
                             'which relative paths to audio files in the selection tables will be resolved. ' +
                             'Otherwise, this must be the root directory containing per-class top-level ' +
                             'subdirectories which in turn contain audio files.')
    parser.add_argument('dst', metavar='<DST DIRECTORY>',
                        help='Path to destination directory into which prepared data will be written.')
    parser.add_argument('--whitelist', metavar='FILE',
                        help='Path to text file containing names (one per line) of whitelisted classes.')
    arg_group_seltab = parser.add_argument_group('Selection tables',
                                                 'Control which sections of audio files are retained in the output, ' +
                                                 'with the use of Raven selection tables.')
    arg_group_seltab.add_argument('--selmap', metavar='CSVFILE',
                                  help='Path to csv file containing one-to-one mappings from audio files to selection' +
                                  ' table files. Audio filepaths must be relative to <AUDIO_SOURCE>. If selection ' +
                                  'table files are not absolute paths, use \'selroot\' to specify the root directory ' +
                                  'path.')
    arg_group_seltab.add_argument('--selroot', metavar='DIRECTORY',
                                  help='Path to the root directory containing selection table files. Note that, if ' +
                                  'this is specified, all selection table paths in \'selmap\' file be treated as ' +
                                  'relative paths.')
    arg_group_seltab.add_argument('--accept-thld', metavar='0-100', type=ArgparseConverters.valid_percent,
                                  default=90., dest='seltab_accept_thld',
                                  help='Clips from the source audio files are retained in the output only if the ' +
                                  'percentage of their temporal overlap with any annotation in a matched selection ' +
                                  'table is above this threshold value. Default: 90%%.')
    arg_group_seltab.add_argument('--save-reject-class', dest='save_reject_class', action='store_true',
                                  help='Enable saving of clips that do not match annotations as \'other\' class. ' +
                                       'Default: False.')
    arg_group_seltab.add_argument('--reject-thld', metavar='0-100', type=ArgparseConverters.valid_percent,
                                  default=0., dest='seltab_reject_thld',
                                  help='Clips from the source audio files are retained in the output \'other\' class ' +
                                       'only if the percentage of their temporal overlap with any annotation in a ' +
                                       'matched selection table is under this threshold value. Default: 0%%.')
    arg_group_prctrl = parser.add_argument_group('Process control')
    arg_group_prctrl.add_argument('--threads', metavar='NUM', type=ArgparseConverters.positive_integer,
                                  help='Number of threads to spawn for parallel execution (default: as many CPUs).')
    arg_group_logging = parser.add_argument_group('Logging')
    arg_group_logging.add_argument('--log', metavar='FILE',
                                   help='Path to file to which logs will be written out.')
    arg_group_logging.add_argument('--loglevel', choices=['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG'],
                                   default='INFO',
                                   help='Logging level.')
    arg_group_misc = parser.add_argument_group('Miscellaneous')
    arg_group_misc.add_argument('--filetypes', metavar='EXTN', nargs='+', default=AudioFileList.default_audio_filetypes,
                                help='Audio file types to restrict processing to. Option is ignored if processing ' +
                                     'selection tables or a single file. Can specify multiple types separated by ' +
                                     'whitespaces. By default, will include for processing all discovered files with ' +
                                     'the following extensions: ' + ', '.join(AudioFileList.default_audio_filetypes))
    arg_group_misc.add_argument('--maxdur', metavar='SECONDS', dest='max_file_duration', type=float,
                                help='Maximum duration of an audio file to consider it for processing. Larger files ' +
                                     'will be ignored. Default: no limit.')
    args = parser.parse_args()

    if not os.path.exists(args.src):
        print('Error: Invalid source specified', file=sys.stderr)
        exit(2)

    try:
        data_settings = datasection2dict(Config(args.cfg, 'DATA').DATA)
    except FileNotFoundError as exc:
        print('Error loading config file: {}'.format(exc.strerror), file=sys.stderr)
        exit(exc.errno)
    except ConfigError as exc:
        print('Error processing config file: {}'.format(str(exc)), file=sys.stderr)
        exit(1)
    except Exception as exc:
        print('Error processing config file: {}'.format(repr(exc)), file=sys.stderr)
        exit(1)

    if os.path.isfile(args.src):    # If src is an audio file by itself. Process and exit immediately.

        # Warn about ignoring whitelist and seltab info, if also provided
        if args.selmap is not None:
            warnings.showwarning('Processing a single file, will ignore \'selmap\'.', Warning, _program_name, '')
        if args.whitelist is not None:
            warnings.showwarning('Processing a single file, will ignore \'whitelist\'.', Warning, _program_name, '')

        num_clips, _ = Process.audio2clips(Settings.Audio(**data_settings['audio_settings']), args.src, args.dst)

        print('{:s}: {:d} clips'.format(os.path.split(args.src)[-1], num_clips[0]))

        exit(0)

    other_args = {'show_progress': False}
    if args.max_file_duration:
        other_args['max_file_duration'] = args.max_file_duration
    if args.threads:
        other_args['num_threads'] = args.threads

    instantiate_logging(args.log if args.log is not None else
                            os.path.join(args.dst, _program_name + '.log'),
                        args.loglevel, args)
    log_config(logging.getLogger(__name__), data_cfg={'audio_settings': data_settings['audio_settings']})

    exit_code = 0

    if args.selmap is not None:   # If selmap file is given, build a container with all relevant info

        with open(args.selmap, 'r', newline='') as f:
            seltab_filemap = [(entry[0], entry[1], entry[2])
                              for entry in csv.reader(f, delimiter=',', quoting=csv.QUOTE_NONE)
                              if len(entry) == 3]
        if len(seltab_filemap) == 0:
            print('No (valid) mappings found in {:s}'.format(args.selmap), file=sys.stderr)

        else:

            other_args['positive_overlap_threshold'] = args.seltab_accept_thld / 100
            if args.save_reject_class:
                other_args['negative_overlap_threshold'] = args.seltab_reject_thld / 100

            # Warn about ignoring whitelist, if also provided
            if args.whitelist is not None:
                warnings.showwarning('Will ignore \'whitelist\' because \'selmap\' is also provided.',
                                     Warning, _program_name, '')

            from_selection_table_map(data_settings['audio_settings'],
                                     audio_seltab_list=seltab_filemap,
                                     audio_root=args.src,
                                     seltab_root=args.selroot,
                                     output_root=args.dst,
                                     **other_args)

    else:
        # If seltab info wasn't available, build the list of classes from the combination of the dir listing of src and
        # classes whitelist.

        # List of classes (first level directory names)
        try:
            class_dirs = sorted([c for c in os.listdir(args.src) if os.path.isdir(os.path.join(args.src, c))])
        except FileNotFoundError as exc:
            print('Error reading source directory: {}'.format(exc.strerror), file=sys.stderr)
            exit_code = exc.errno
        else:

            if args.whitelist is not None:  # Apply whitelist
                class_dirs = restrict_classes_with_whitelist_file(class_dirs, args.whitelist)
                print('Application of whitelist from {:s} results in {:d} classes.'.format(
                    args.whitelist, len(class_dirs)))

            if len(class_dirs) == 0:
                print('No classes to process.')

            else:

                if args.filetypes:
                    other_args['filetypes'] = args.filetypes

                from_top_level_dirs(data_settings['audio_settings'], class_dirs, args.src, args.dst, **other_args)

    logging.shutdown()

    exit(exit_code)
