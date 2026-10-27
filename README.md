# album-check

Checks whether a folder of mastered tracks sits together as an album.

Per track: integrated loudness (LUFS), true peak (dBTP), duration. Later: spectral tilt, loudness range, and my own ITU-R BS.1770 loudness implementation verified against pyloudnorm.

Album view: one chart, every track against the −12 to −15 LUFS band, median line, outliers flagged.

Written by Nathan Lin for mastering my own album. Python 3.14.

## Run

```
python album_check.py <folder-of-wav-or-flac>
```

Charts and tables land in `output/` (ignored by git). Audio is never committed.

## Status

- [ ] v0: load, LUFS (pyloudnorm), true peak (4x oversampled), album chart
- [ ] v1: spectral tilt, LRA, own BS.1770 vs pyloudnorm verification

## Notes

Design notes live in my vault: `output/college/album-checker-brief.md`.
