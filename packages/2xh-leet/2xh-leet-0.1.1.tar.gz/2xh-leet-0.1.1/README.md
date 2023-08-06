# LEET

*Library of Eclectic Experiments by Tenchi*

Random modules that I made and use in several project and are too small to get their own package. A `util` library of sorts.

---

## Contents

<!-- MarkdownTOC autolink=true -->

- [Logging](#logging)
    - [Progress bars](#progress-bars)
    - [Images](#images)

<!-- /MarkdownTOC -->

## Logging

Module that provides a fancy-looking theme for Python loggers.

(TODO: Screenshot)

To enable, `import leet.logging` from anywhere (maybe the main `__init__.py` of your project). You will then have a global logger `log` function that you can use from anywhere:

```py
log.info("Hello")
log.warn("World")
```

### Progress bars

Also provides a progress bar (from [WoLpH/python-progressbar](https://github.com/WoLpH/python-progressbar)) that fits in the theme:

```py
from time import sleep
from leet.logging import ProgressBar

for i in ProgressBar(range(10)):
    sleep(1)
    log.info("Working on %d..." % i)
```

### Images

Also supports outputing images via [imgcat](https://iterm2.com/utilities/imgcat) if using [iTerm2](https://iterm2.com/) (support for other tools pending):

```py
log.warn("Image is too big:", extras={"img": "path/to/image.png"})
```
