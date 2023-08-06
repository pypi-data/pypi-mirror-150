import builtins
import logging

import progressbar
from PIL import ImageColor
from sty import fg

from .imgcat import imgcat

progressbar.streams.wrap_stderr()

# TODO: Implement word wrapping

# Set to True to have the module name column dynamically resize as it grows
# TODO: Set option via different import
DYNAMIC_WIDTH = False

# Colors taken from https://lospec.com/palette-list/blk-neo
colors = [
    fg(*ImageColor.getrgb(c))
    for c in
    [
        "#909EDD", "#C1D9F2", "#FFCCD0", "#F29FAA", "#E54286", "#FF6EAF",
        "#FFA5D5", "#8CFF9B", "#42BC7F", "#3E83D1", "#50B9EB", "#8CDAFF",
        "#B483EF", "#854CBF", "#FFE091", "#FFAA6E", "#78FAE6", "#27D3CB",
    ]
]

logger = logging.getLogger("Rack")
logger.setLevel(logging.DEBUG)

current_width = 10 if DYNAMIC_WIDTH else 30
max_width = 30
first_log = True


class LoggingFilter(logging.Filter):
    def filter(self, record):
        global current_width, first_log

        name = "%s.%s" % (record.module, record.funcName)
        lineno = len(str(record.lineno))

        lines = record.msg.split("\n")
        new_lines = [lines[0]]

        if len(name) + 1 + lineno > current_width and current_width < max_width:
            gap = current_width
            current_width = min(len(name) + 1 + lineno, max_width)
            gap = current_width - gap
            if not first_log:
                new_lines.append(
                    " " * 8 + " │ "
                    + " " * 7 + " │ "
                    + " " * (current_width - gap)
                    + f" └{'─' * (gap - 1)}┐ "
                )
            else:
                first_log = False

        max_len = current_width - 1 - lineno
        if len(name) > max_len:
            name = name[:max_len - 1] + "…"

        quick_checksum = sum(bytearray(name.encode("utf-8")))
        color = colors[quick_checksum % len(colors)]

        just = current_width - len(name + ":" + str(record.lineno))
        record.fullname = f"{color}{name}:{record.lineno}{fg.rs}" + " " * just

        indent = " " * 8 + " │ " + " " * 7 + " │ " + " " * current_width + " │ "
        for line in lines[1:]:
            new_lines.append(indent + line)

        if hasattr(record, "img"):
            height_chars = 5
            if hasattr(record, "img_height"):
                height_chars = record.img_height
            img = imgcat(record.img, height_chars=height_chars)
            if img:
                go_up = f"\033[{height_chars}A"
                new_lines.append(indent)
                new_lines.append(indent + img + go_up)
                new_lines.extend([indent] * height_chars)

        record.msg = "\n".join(new_lines)

        return True


logger.addFilter(LoggingFilter())

formatter = logging.Formatter(
    "{asctime:8} │ {levelname} │ {fullname} │ {message}",
    # datefmt="%Y-%m-%d %H:%M:%S",
    datefmt="%H:%M:%S",
    style="{"
)


def ProgressBar(*args, **kwargs):
    progress = progressbar.ProgressBar(
        widgets=[
            progressbar.CurrentTime(format="%(current_time)s"),
            " │    %    │                                │"
            " ", progressbar.SimpleProgress(),
            " ", progressbar.Percentage(format="(%(percentage)d%%)"),
            " ", progressbar.Bar(left=" ", right=" ", marker="▓", fill="░"),
            " ", progressbar.Timer(),
            " ", progressbar.AdaptiveETA(),
        ],
        redirect_stdout=True,
    )
    return progress(*args, **kwargs)


handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
handler.setFormatter(formatter)

logging.addLevelName(logging.DEBUG,              " debug "        )  # noqa
logging.addLevelName(logging.INFO,               "  inf  "        )  # noqa
logging.addLevelName(logging.WARNING,  fg(208) + "warning" + fg.rs)
logging.addLevelName(logging.ERROR,    fg(196) + " error " + fg.rs)
logging.addLevelName(logging.CRITICAL, fg(196) + " fatal " + fg.rs)
logger.addHandler(handler)

# TODO: Have a separate import that doesn't touch builtins and gives a logger
builtins.log = logger  # type: ignore
