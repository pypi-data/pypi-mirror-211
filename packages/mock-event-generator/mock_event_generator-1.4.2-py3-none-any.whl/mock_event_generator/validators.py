"""Classes for G-event and S-event validation."""

from __future__ import annotations

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt  # type: ignore[import]
from matplotlib import colormaps

from .cache import GEventCacheEntry, SEventCacheEntry
from .exceptions import MEGValidationFailed
from .gracedbs import GraceDBWithContext

logger = logging.getLogger(__name__)

FILES_CHECKLIST = [
    'bayestar.multiorder.fits',
    'bayestar.fits.gz',
    'bayestar.png',
    'bayestar.html',
    '{}.p_astro.json',
    '{}.p_astro.png',
    'em_bright.json',
    'em_bright.png',
]

LABELS_CHECKLIST = ['EMBRIGHT_READY', 'GCN_PRELIM_SENT', 'PASTRO_READY', 'SKYMAP_READY']

ADV_LABELS = ['ADVNO', 'ADVOK']


class SEventValidator(SEventCacheEntry):
    """Class used to validate a cached S-event."""

    datetime_format = '%Y-%m-%d %H:%M:%S %Z'
    cmap = colormaps['tab10']
    data_template = {'found': False, 'time': 'never', 'latency': 9999.0}

    @classmethod
    def from_sevent_id(
        cls,
        sevent_id: str,
        source: GraceDBWithContext,
        disabled: bool,
        cache_path: Path,
    ) -> SEventValidator:
        """Init from S-event id.

        Fetches S-event and returns a validator instance.

        Parameters:
            sevent_id: The S-event GraceDB identifier.
            source: The GraceDB instance name from which events are downloaded,
                such as `production` or `playground`.
            disabled: If true, bypass the cache and always download the event
                data files.
            cache_path: The top-level path of the cache.
        """
        SEventCacheEntry.from_id(sevent_id, source, disabled, cache_path)

        return SEventValidator(cache_path / sevent_id)

    @classmethod
    def from_gevent_id(
        cls,
        gevent_id: str,
        source: GraceDBWithContext,
        disabled: bool,
        cache_path: Path,
    ) -> SEventValidator:
        """Init from G-event id.

        Fetches G-event info, queries for S-events in the corresponding
        search and returns a validator instance for the S-event associated to
        the input G-event.

        Parameters:
            gevent_id: The G-event GraceDB identifier.
            source: The GraceDB instance name from which events are downloaded,
                such as `production` or `playground`.
            disabled: If true, bypass the cache and always download the event
                data files.
            cache_path: The top-level path of the cache.

        Raises:
            RuntimeError: When the input G-event does not have ans associated
                S-event.
        """
        gevent_data = GEventCacheEntry.from_id(
            gevent_id, source, disabled, cache_path
        ).get_description()

        sevents = list(source.superevents(gevent_data.search))
        try:
            sevent_found, si = False, 0
            while not sevent_found:
                sevent_id = sevents[si]['superevent_id']
                sevent_found = gevent_id in sevents[si]['gw_events']
                si += 1

        except IndexError:
            raise RuntimeError(f'No superevent found for event {gevent_id}')

        return SEventValidator.from_sevent_id(sevent_id, source, disabled, cache_path)

    def validate(self, save_plot_to: Path | None) -> None:
        """Superevent validation method.

        Get S-event description, recover labels and file info,
        validate and produce a plot.

        Raises:
            RuntimeError: When the validation fails.
        """
        self.sevent_data = self.get_description().sevent_data
        self.sevent_id = self.sevent_data['sevent']['superevent_id']
        self.sub_time = datetime.strptime(
            self.sevent_data['sevent']['created'], self.datetime_format
        )
        self.pipeline = self.sevent_data['sevent']['preferred_event_data']['pipeline']
        logger.info(f'Validating {self.sevent_id} submitted {str(self.sub_time)}')

        self.labels_dict = self._get_labels()
        labels_ok = self._validate_labels()
        adv_ok = self._validate_advocate()
        self.files_dict = self._get_files()
        files_ok = self._validate_files()

        if not save_plot_to:
            save_plot_to = self.path
        self._save_data(save_plot_to)
        self._plot(save_plot_to)

        if not all([labels_ok, adv_ok, files_ok]):
            err_str = f'Validation failed for S-event {self.sevent_id}\n'
            if not labels_ok:
                err_str += 'Missing labels:'
                for key in LABELS_CHECKLIST:
                    if not self.labels_dict[key]['found']:
                        err_str += f' {key}'
                err_str += '\n'
            if not adv_ok:
                err_str += 'Missing ADV label (either ADVOK / ADVNO).\n'
            if not files_ok:
                err_str += 'Missing files:'
                for key in self.files_dict:
                    if not self.files_dict[key]['found']:
                        err_str += f' {key}'

            raise MEGValidationFailed(err_str)

    def _get_labels(self) -> dict[str, Any]:
        """Load labels info into a dictionary."""
        logs = self.sevent_data['labels']
        labels_dict = {
            key: self.data_template.copy() for key in LABELS_CHECKLIST + ADV_LABELS
        }
        for row in logs:
            labelname = row['name']
            log_time = datetime.strptime(row['created'], self.datetime_format)
            logger.info(f'Label {labelname} created {str(log_time)}')
            if labelname in LABELS_CHECKLIST + ADV_LABELS:
                labels_dict[labelname]['found'] = True
                labels_dict[labelname]['time'] = str(log_time)
                labels_dict[labelname]['latency'] = (
                    log_time - self.sub_time
                ).total_seconds()

        return labels_dict

    def _get_files(self) -> dict[str, Any]:
        """Load files info into a dictionary."""
        logs = self.sevent_data['logs']['log']
        files_dict = {
            key.format(self.pipeline): self.data_template.copy()
            for key in FILES_CHECKLIST
        }
        for row in logs:
            filename = row['filename']
            log_time = datetime.strptime(row['created'], self.datetime_format)
            if filename:
                logger.info(f'File {filename} created {str(log_time)}')
            if filename in files_dict:
                files_dict[filename]['found'] = True
                files_dict[filename]['time'] = str(log_time)
                files_dict[filename]['latency'] = (
                    log_time - self.sub_time
                ).total_seconds()

        return files_dict

    def _validate_labels(self) -> bool:
        """Returns True if all labels are found."""
        labels_created = [self.labels_dict[key]['found'] for key in LABELS_CHECKLIST]

        return all(labels_created)

    def _validate_advocate(self) -> bool:
        """Returns True if any advocate label (either ADVOK or ADVNO) is found."""
        adv_created = [self.labels_dict[key]['found'] for key in ADV_LABELS]

        return any(adv_created)

    def _validate_files(self) -> bool:
        """Returns True if all filenames are found."""
        files_created = [self.files_dict[key]['found'] for key in self.files_dict]

        return all(files_created)

    def _save_data(self, outdir: Path) -> None:
        """Saves latency data to json files..

        Parameters:
            outdir: Output directory.
        """
        data_dict = {
            'sub_time': str(self.sub_time),
            'labels': self.labels_dict,
            'files': self.files_dict,
        }
        filename = outdir / ('%s_latency_data.json' % str(self.sevent_id))
        with open(filename, 'w') as stream:
            json.dump(data_dict, stream, indent=4)
        logger.info(f'Data saved to {str(filename)}')

    def _plot(self, outdir: Path) -> None:
        """Plots timeline of label and filename creation.

        Parameters:
            outdir: Output directory.
        """
        self._init_figure()
        self._add_entries_to_plot(self.axes[0], self.labels_dict)
        self._add_entries_to_plot(self.axes[1], self.files_dict)

        x_span = self.axes[1].get_xlim()[1] - self.axes[1].get_xlim()[0]
        self.axes[1].set_xlim(
            self.axes[1].get_xlim()[0], self.axes[1].get_xlim()[1] + 0.2 * x_span
        )
        textstr = ''
        for key in ['superevent_id', 'category', 'submitter', 'created', 't_0']:
            textstr += '{}: {}\n'.format(key, self.sevent_data['sevent'][key])
        self.axes[1].text(
            0.01,
            0.05,
            textstr[:-2],
            fontsize=10,
            transform=self.axes[1].transAxes,
            va='bottom',
            ha='left',
            bbox={'boxstyle': 'round', 'facecolor': 'white', 'alpha': 0.6},
        )

        plt.tight_layout()
        plt.subplots_adjust(hspace=0)

        filename = outdir / ('%s_latency_plot.png' % str(self.sevent_id))
        plt.savefig(filename)
        logger.info(f'Plot saved to {str(filename)}')

    def _init_figure(self) -> None:
        """Init matplotlib objects."""
        plt.rc('font', size=10)
        self.fig = plt.figure(figsize=(10, 5))
        self.axes = []

        self.axes.append(self.fig.add_subplot(2, 1, 1))
        self.axes[0].grid(ls='--')
        self.axes[0].set_ylim(0, 1)
        self.axes[0].tick_params(
            axis='both', labelbottom=False, left=False, labelleft=False
        )

        self.axes.append(
            self.fig.add_subplot(2, 1, 2, sharex=self.axes[0], sharey=self.axes[0])
        )
        self.axes[1].grid(ls='--')
        self.axes[1].tick_params(axis='both', left=False, labelleft=False)
        self.axes[1].set_xlabel(r'Seconds since t$_0$')

    def _add_entries_to_plot(self, ax: plt.Axes, entries: dict[str, Any]) -> None:
        """Adds entries to a plot.

        Parameters:
            ax: instance of matplotlib Axes
            entries: dict as returned by self._get_labels() or self._get_files()
        """
        i = 0
        for key, item in entries.items():
            y_loc = i / len(entries.keys()) * 0.9 + 0.05
            if item['found']:
                ax.axvline(item['latency'], ls='-', color=self.cmap(y_loc))
                ax.plot(
                    [item['latency'], item['latency'] + 15],
                    [y_loc, y_loc],
                    color=self.cmap(y_loc),
                )
                ax.text(
                    item['latency'] + 17,
                    y_loc,
                    key,
                    color=self.cmap(y_loc),
                    va='center',
                )
            i += 1
