# World news, Wednesday 18 November 2026, in one image

Entry for the make.fun bounty [Sum up 18 November's world news in one image](https://make.fun/bounty/news-image-20261118).

- `build.py` draws `entry.png` (1024x1024): a dated masthead, 9 illustrated lead-story cards and 35 briefs across 7 regions, 44 stories in all.
- `main.py` copies `entry.png` to `/output/entry.png` (or `$MAKEFUN_OUTPUT_DIR`). Python 3.13 standard library only, no network.
- `SOURCES.md` lists the dated source for every story.

Run: `MAKEFUN_OUTPUT_DIR=out python main.py`

License: MIT.
