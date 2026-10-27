"""Album loudness chart.

Written by Claude (AI), 2026-10-26, at Nathan's request. Not Nathan's code.
Everything that measures audio is in measure.py and is Nathan's.

Takes the list of track dicts from measure.scan_folder() and draws one bar per
track. Uses matplotlib's Figure directly (no pyplot) so the same figure can be
saved to a PNG now and embedded in a GUI later.
"""

import pathlib

import numpy
from matplotlib.figure import Figure

BAND_LOW = -15.0          # LUFS, bottom of the target band
BAND_HIGH = -12.0         # LUFS, top of the target band
OUTLIER_LU = 1.5          # flag a track this far from the album median
TRUE_PEAK_LIMIT = -0.9    # dBTP; flag above this. Tolerance, not the -1 spec:
                          # differences between meters are ~0.01 dB.
MIN_TRACKS_FOR_OUTLIERS = 3   # a median of 1-2 tracks says nothing

OK_COLOR = "#4a7fb5"
FLAG_COLOR = "#c0392b"


def flag_reasons(tracks):
    """For each track, a list of strings saying why it is flagged (empty = fine)."""
    lufs = [t["integrated_LUFS"] for t in tracks]
    median = float(numpy.median(lufs))
    judge_outliers = len(tracks) >= MIN_TRACKS_FOR_OUTLIERS
    reasons = []
    for t in tracks:
        r = []
        if judge_outliers and abs(t["integrated_LUFS"] - median) > OUTLIER_LU:
            r.append("loudness %+.1f LU from median" % (t["integrated_LUFS"] - median))
        if t["true_peak"] > TRUE_PEAK_LIMIT:
            r.append("true peak %.2f dBTP" % t["true_peak"])
        reasons.append(r)
    return reasons


def make_figure(tracks):
    """Return a matplotlib Figure for the album. Raises ValueError if no tracks."""
    if not tracks:
        raise ValueError("no tracks to chart")

    names = [pathlib.Path(t["name"]).stem for t in tracks]
    lufs = numpy.array([t["integrated_LUFS"] for t in tracks])
    median = float(numpy.median(lufs))
    reasons = flag_reasons(tracks)

    # Bars are drawn from the bottom of the axis up to the LUFS value,
    # because LUFS is negative and bars from 0 would hang downward.
    y_min = numpy.floor(min(lufs.min(), BAND_LOW)) - 1
    y_max = numpy.ceil(max(lufs.max(), BAND_HIGH)) + 1

    fig = Figure(figsize=(max(6, 0.9 * len(tracks) + 2), 5), dpi=120)
    ax = fig.add_subplot(111)

    ax.axhspan(BAND_LOW, BAND_HIGH, color="#2e8b57", alpha=0.15, label="target band (%d to %d LUFS)" % (BAND_LOW, BAND_HIGH))
    colors = [FLAG_COLOR if r else OK_COLOR for r in reasons]
    x = numpy.arange(len(tracks))
    bars = ax.bar(x, lufs - y_min, bottom=y_min, color=colors, width=0.6)
    ax.axhline(median, color="black", linestyle="--", linewidth=1, label="album median (%.1f LUFS)" % median)

    for bar, value in zip(bars, lufs):
        ax.text(bar.get_x() + bar.get_width() / 2, value + 0.1, "%.1f" % value,
                ha="center", va="bottom", fontsize=8)

    ax.set_ylim(y_min, y_max)
    ax.set_xticks(x)
    ax.set_xticklabels(names, rotation=35, ha="right", fontsize=8)
    ax.set_ylabel("integrated loudness (LUFS)")

    n_flagged = sum(1 for r in reasons if r)
    title = "Album loudness: %d tracks, %d flagged" % (len(tracks), n_flagged)
    if len(tracks) < MIN_TRACKS_FOR_OUTLIERS:
        title += " (loudness outliers need %d+ tracks)" % MIN_TRACKS_FOR_OUTLIERS
    ax.set_title(title, fontsize=10)

    handles, labels = ax.get_legend_handles_labels()
    from matplotlib.patches import Patch
    handles.append(Patch(color=FLAG_COLOR))
    labels.append("flagged (>%.1f LU from median or true peak >%.1f dBTP)" % (OUTLIER_LU, TRUE_PEAK_LIMIT))
    ax.legend(handles, labels, fontsize=7, loc="upper center",
              bbox_to_anchor=(0.5, -0.28), ncol=1, frameon=False)

    fig.subplots_adjust(bottom=0.38, left=0.15, right=0.97, top=0.92)
    return fig


def save_chart(tracks, out_path):
    """Draw and save the chart as a PNG. Returns the path."""
    out_path = pathlib.Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig = make_figure(tracks)
    fig.savefig(out_path)
    return out_path
