import copy
import json
import logging
import sys
from typing import Any, Dict
from unittest import mock

import yt_dlp
from yt_dlp import utils as ydl_utils

__version__ = "0.0.4"

original_parse_options = yt_dlp.parse_options


def get_logger() -> logging.Logger:
    logger = logging.getLogger("log")
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        fmt = logging.Formatter("%(message)s")
        handler.setFormatter(fmt)
        handler.setLevel(logging.DEBUG)

        logger.addHandler(handler)

    return logger


class Popen(ydl_utils.Popen):
    @classmethod
    def run(cls, *args, timeout=None, **kwargs):  # type: ignore
        if args and "-progress" in args[0] and "ffmpeg" in args[0]:
            kwargs.pop("stdout", None)
        return super().run(*args, timeout=timeout, **kwargs)


class YtDlpProgress:
    def __init__(self) -> None:
        self.logger = get_logger()

        self.opts = {
            "logger": self.logger,
            "progress_hooks": [self._log_hook],
            "noprogress": True,
            "no_color": True,
            "prefer_ffmpeg": True,
            "postprocessor_args": ["-progress", "pipe:1"],
        }

    def _log_hook(self, data: Dict[str, Any]) -> None:
        size_done = data.get("downloaded_bytes", None)
        size_total = data.get("total_bytes_estimate", None)

        report = {
            "finished": data.get("status") == "finished",
            "done": "unk",
        }

        if size_done is not None and size_total is not None:
            report["downloaded"] = int(size_done)
            report["total"] = int(size_total)
            report["done"] = "%.2f%%" % (size_done * 100 / size_total)

        self.logger.info("progress %s", json.dumps(report))

    def _parse_options(self, argv=None):  # type: ignore
        parser, opts, urls, ydl_opts = original_parse_options(argv=argv)
        ydl_opts.update(self.opts)
        return parser, opts, urls, ydl_opts

    def execute(self) -> None:
        parse_options_mock = mock.patch("yt_dlp.parse_options", self._parse_options)
        popen_mock = mock.patch("yt_dlp.postprocessor.ffmpeg.Popen", Popen)

        with parse_options_mock, popen_mock:
            yt_dlp.main()


def main() -> None:
    YtDlpProgress().execute()
