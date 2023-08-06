import copy
import json
import logging
import sys
from typing import Any, Dict
from unittest import mock

import yt_dlp
from yt_dlp import utils as ydl_utils

__version__ = "0.0.3"

original_parse_options = yt_dlp.parse_options
original_popen = ydl_utils.Popen

YDL_OPTIONS: Dict[str, Any] = {
    "buffersize": 16 * 1024,
    "retries": 5,
    "fragment_retries": 5,
    "quiet": True,
    "noprogress": True,
    "no_color": True,
    "call_home": False,
    "ignoreerrors": False,
    "geo_bypass": True,
    "prefer_ffmpeg": True,
    "noplaylist": True,
}


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

        self.opts = copy.copy(YDL_OPTIONS)
        self.opts.update(
            {
                "logger": self.logger,
                "progress_hooks": [self._log_hook],
                "postprocessor_args": ["-progress", "pipe:1"],
            }
        )

    def _log_hook(self, data: Dict[str, Any]) -> None:
        size_done = data.get("downloaded_bytes", None)
        size_total = data.get("total_bytes", None)

        report = {
            "finished": data.get("status") == "finished",
            "done": "unk",
        }

        if size_done is not None and size_total is not None:
            report["downloaded"] = size_done
            report["total"] = size_total
            report["done"] = "%.2f%%" % (size_done * 100 / size_total)

        self.logger.info("progress %s", json.dumps(report))

    def _parse_options(self, argv=None):  # type: ignore
        v = original_parse_options(argv=argv)
        parser, opts, urls, ydl_opts = v
        opts.update_self = False
        ydl_opts.update(self.opts)
        return parser, opts, urls, ydl_opts

    def execute(self) -> None:
        parse_options_mock = mock.patch("yt_dlp.parse_options", self._parse_options)
        popen_mock = mock.patch("yt_dlp.postprocessor.ffmpeg.Popen", Popen)

        with parse_options_mock, popen_mock:
            yt_dlp.main()


def main() -> None:
    YtDlpProgress().execute()
