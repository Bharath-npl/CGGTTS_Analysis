import math
import os
import sys
import warnings
from io import StringIO

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from CGGTTS_data_format import CGGTTS_data_format as show_data_format

warnings.filterwarnings('ignore')

st.set_page_config(
    page_title="BIPM CGGTTS Analyser v2",
    page_icon=":chart_with_upwards_trend:",
    layout="wide",
)

st.markdown(
    """<style>
    [data-testid="stMainBlockContainer"] {
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        padding-top: 1rem !important;
        max-width: 100% !important;
    }
    button[data-baseweb="tab"] p {
        font-weight: 700 !important;
        font-size: 15px !important;
    }
    </style>""",
    unsafe_allow_html=True,
)

GNSS_MAP = {
    'G': 'GPS', 'R': 'GLONASS', 'E': 'GALILEO',
    'C': 'BeiDou', 'J': 'QZSS', 'I': 'IRNSS',
}

_DEFAULTS: dict = {
    'cv_result': None,
    'cv_sv': None,
    'av_result': None,
    'cv_freq_warning': None,
}
for _k, _v in _DEFAULTS.items():
    if _k not in st.session_state:
        st.session_state[_k] = _v


# ── Pure / cacheable helpers ──────────────────────────────────────────────────

@st.cache_data(show_spinner=False)
def parse_cggtts_files(
    file_bytes_list: list[tuple[str, bytes]],
) -> tuple[pd.DataFrame, list[int], set, str | None, list[tuple[str, str]]]:
    records: list[dict] = []
    msgs: list[tuple[str, str]] = []
    gnss_type: str | None = None
    valid_names: list[str] = []
    rx_version = "unknown"
    rx_ref: str | None = None
    lab = "unknown"

    for filename, raw_bytes in file_bytes_list:
        content = raw_bytes.decode(errors='replace')
        lines = content.split('\n')

        if not (lines[0].startswith("CGGTTS") or lines[0].startswith("GGTTS")):
            msgs.append(("error", f"File format not supported: {filename}"))
            continue

        first_char = filename[0].upper() if filename else ''
        if first_char not in GNSS_MAP:
            msgs.append(("error", f"Cannot detect GNSS from filename: {filename}"))
            continue

        current_gnss = GNSS_MAP[first_char]
        if gnss_type is None:
            gnss_type = current_gnss
        elif gnss_type != current_gnss:
            msgs.append(("error", "Multiple GNSS types detected — upload files of one type only."))
            break

        frc_pos: int | None = None
        inside_header = True
        data_lines: list[str] = []
        prev_line = ""

        for line in lines:
            if "hhmmss  s  .1dg .1dg    .1ns" in line:
                p = prev_line.find('FRC')
                if p != -1:
                    frc_pos = p
                inside_header = False
                prev_line = line
                continue

            if line.startswith("CGGTTS") or line.startswith("GGTTS"):
                inside_header = True
                if "=" in line:
                    rx_version = line.split('=', 1)[1].strip()
                else:
                    msgs.append(("error", f"Missing '=' in version line in {filename}"))

            if line.startswith("REF=") or line.startswith("REF ="):
                rx_ref = line.split('=', 1)[1].strip()
            if line.startswith("LAB=") or line.startswith("LAB ="):
                lab = line.split('=', 1)[1].strip()

            if not inside_header and line.strip():
                data_lines.append(line)

            prev_line = line

        if rx_ref is None:
            msgs.append(("warning", f"No REF field in header of {filename}"))

        file_rows: list[dict] = []
        for line in data_lines:
            if len(line) < 10:
                continue
            try:
                sttime = line[13:19].strip()
                h, m, s = int(sttime[:2]), int(sttime[2:4]), int(sttime[4:6])
                frac = (h * 3600 + m * 60 + s) / 86400
                mjd = float(line[7:12].strip()) + frac
                frc = (
                    line[frc_pos:frc_pos + 3].strip()
                    if frc_pos is not None and len(line) > frc_pos + 2
                    else "L1C"
                )
                file_rows.append({
                    'SAT':     line[0:3].strip(),
                    'MJD':     mjd,
                    'ELV':     float(line[25:28].strip()),
                    'REFSV':   float(line[34:45].strip()),
                    'SRSV':    float(line[46:52].strip()),
                    'REFSYS':  float(line[53:64].strip()),
                    'FRC':     frc,
                    'REF':     rx_ref or '',
                    'Version': rx_version,
                    'LAB':     lab,
                })
            except (ValueError, IndexError):
                continue

        if not file_rows:
            msgs.append(("error", f"No valid data rows in {filename}"))
            continue

        records.extend(file_rows)
        valid_names.append(filename)

    if not records:
        return pd.DataFrame(), [], set(), gnss_type, msgs

    df = pd.DataFrame(records)
    df = df[df['SAT'].notna() & (df['SAT'] != '')].reset_index(drop=True)
    mjd_days = sorted({int(v) for v in df['MJD'] if not pd.isna(v)})
    frc_set = set(df['FRC'].dropna().unique())

    if valid_names:
        msgs.append(("success", f"Loaded: {', '.join(valid_names)}"))

    return df, mjd_days, frc_set, gnss_type, msgs


def mjd_filter(df: pd.DataFrame, start: int, end: int) -> pd.DataFrame:
    df = df.copy()
    df['MJD'] = pd.to_numeric(df['MJD'], errors='coerce')
    if start == end:
        return df[(df['MJD'] > start - 1) & (df['MJD'] < start + 1)]
    return df[(df['MJD'] >= float(start)) & (df['MJD'] <= float(end + 1))]


def weighted_refsys_avg(df: pd.DataFrame, frequency: str) -> pd.DataFrame:
    sub = df[df['FRC'] == frequency].copy()
    if sub.empty:
        return pd.DataFrame()
    sub['sin2'] = np.sin(np.radians(sub['ELV'] / 10)) ** 2
    sub['sin2'] = sub.groupby('MJD')['sin2'].transform(lambda x: x / x.sum())
    sub['w_REFSYS'] = sub['REFSYS'] * sub['sin2'] * 0.1
    return (
        sub.groupby('MJD')['w_REFSYS'].sum()
        .reset_index()
        .rename(columns={'w_REFSYS': 'REFSYS'})
    )


def process_cv(
    df1: pd.DataFrame, df2: pd.DataFrame,
    mjd_times: list, svids: list, all_svids: list,
    elv_mask: float, outlier: float,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    d1 = df1[df1['ELV'] >= elv_mask * 10]
    d2 = df2[df2['ELV'] >= elv_mask * 10]
    use = all_svids if 'ALL' in svids else [s for s in svids if s not in ('ALL', 'NONE')]

    merged = pd.merge(
        d1[d1['MJD'].isin(mjd_times) & d1['SAT'].isin(use)],
        d2[d2['MJD'].isin(mjd_times) & d2['SAT'].isin(use)],
        on=['SAT', 'MJD'], suffixes=('_1', '_2'),
    )
    if merged.empty:
        return pd.DataFrame(), pd.DataFrame()

    merged['CV_diff'] = (merged['REFSYS_1'] - merged['REFSYS_2']) * 0.1
    mu, sigma = merged['CV_diff'].mean(), merged['CV_diff'].std()
    merged = merged[abs(merged['CV_diff'] - mu) <= outlier * sigma]

    result = merged.groupby('MJD')['CV_diff'].mean().reset_index()
    cv_sv = (
        merged.groupby('MJD')
        .apply(lambda g: pd.Series({
            'SAT_list': g['SAT'].tolist(),
            'CV_diff_list': g['CV_diff'].tolist(),
        }))
        .reset_index()
    )
    return result, cv_sv


def process_av(
    df1: pd.DataFrame, df2: pd.DataFrame,
    svids: list, all_svids: list, mjd_times: list,
    elv_mask: float, outlier: float,
) -> pd.DataFrame:
    d1 = df1[df1['ELV'] >= elv_mask * 10].copy()
    d2 = df2[df2['ELV'] >= elv_mask * 10].copy()
    use = all_svids if 'ALL' in svids else [s for s in svids if s not in ('ALL', 'NONE')]
    d1['sin2'] = np.sin(np.radians(d1['ELV'] * 0.1)) ** 2
    d2['sin2'] = np.sin(np.radians(d2['ELV'] * 0.1)) ** 2

    def _weighted(sub: pd.DataFrame, cond: pd.Series) -> float:
        w = sub.loc[cond, 'sin2']
        return (sub.loc[cond, 'REFSYS'] * (1 / w.sum()) * w).sum() * 0.1

    rows = []
    for t in mjd_times:
        s1 = d1[d1['MJD'] == t].copy()
        s2 = d2[d2['MJD'] == t].copy()
        if s1.empty or s2.empty:
            continue

        for s in (s1, s2):
            mu, sigma = s['REFSYS'].mean(), s['REFSYS'].std()
            keep = abs(s['REFSYS'] - mu) <= outlier * sigma
            s.drop(s.index[~keep.values], inplace=True)

        c1, c2 = s1['SAT'].isin(use), s2['SAT'].isin(use)
        if not c1.any() or not c2.any():
            continue

        ws1, ws2 = _weighted(s1, c1), _weighted(s2, c2)

        res1 = s1['REFSYS'] - ws1
        res2 = s2['REFSYS'] - ws2
        std1 = np.sqrt((res1 ** 2).mean())
        std2 = np.sqrt((res2 ** 2).mean())
        s1 = s1[abs(res1.values) <= outlier * std1]
        s2 = s2[abs(res2.values) <= outlier * std2]

        c1, c2 = s1['SAT'].isin(use), s2['SAT'].isin(use)
        if not c1.any() or not c2.any():
            continue

        ws1, ws2 = _weighted(s1, c1), _weighted(s2, c2)
        rows.append({'MJD_time': t, 'AV_diff': round(ws1 - ws2, 2)})

    return pd.DataFrame(rows, columns=['MJD_time', 'AV_diff']) if rows else pd.DataFrame()


def to_csv(header: str, df: pd.DataFrame) -> str:
    buf = StringIO()
    buf.write(header)
    out = df.copy()
    out.columns = ['#' + out.columns[0]] + list(out.columns[1:])
    out.to_csv(buf, sep='\t', index=False)
    return buf.getvalue()


def scatter_fig(x, y, title: str, std: float | None = None, ylabel="Time difference (ns)") -> go.Figure:
    x_arr = np.asarray(x, dtype=float)
    y_arr = np.asarray(y, dtype=float)
    mask = np.isfinite(x_arr) & np.isfinite(y_arr)
    x_arr, y_arr = x_arr[mask], y_arr[mask]

    mean_y = float(np.mean(y_arr))
    if std is None:
        std = float(np.std(y_arr, ddof=1))
    coeffs = np.polyfit(x_arr, y_arr, 1)
    slope  = coeffs[0]
    sort_i = np.argsort(x_arr)
    x_line = x_arr[sort_i]
    y_line = np.polyval(coeffs, x_line)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x_arr, y=y_arr, mode='markers',
        marker=dict(size=8), name='Data',
    ))
    fig.add_trace(go.Scatter(
        x=x_line, y=y_line, mode='lines',
        line=dict(color='red', width=2), name='Linear fit',
        showlegend=False,
    ))
    fig.add_annotation(
        xref='paper', yref='paper', x=1, y=1,
        text=(
            f"Mean:     {mean_y:.3f} ns<br>"
            f"Std Dev:  {std:.3f} ns<br>"
            f"Slope:    {slope:.4f} ns/day"
        ),
        showarrow=False, font=dict(size=14, color="black"),
        xanchor='right', yanchor='top',
        align='left',
        bgcolor='rgba(255,255,255,0.85)',
        bordercolor='rgba(100,100,100,0.4)',
        borderwidth=1,
        borderpad=6,
    )
    fig.update_layout(
        title=title, title_font=dict(size=18, color="black"),
        xaxis_title="MJD", yaxis_title=ylabel,
        xaxis=dict(tickformat=".2f", exponentformat='none', tickfont=dict(size=13)),
        yaxis=dict(tickmode='auto', nticks=10, tickfont=dict(size=13)),
        height=500,
    )
    return fig


def map_gps_svids(svids: list[str]) -> list[str]:
    return ['G' + s if s.isdigit() and int(s) <= 63 else s for s in svids]


# ── Receiver section ──────────────────────────────────────────────────────────

def render_receiver(rx_id: int) -> None:
    ss = {
        'total':   f'df{rx_id}_total',
        'days':    f'mjd_days_{rx_id}',
        'frc':     f'unique_FRC{rx_id}',
        'ref':     f'REF{rx_id:02}',
        'lab':     f'LAB{rx_id}',
        'gnss':    f'GNSS{rx_id}',
        'sel_df':  f'sel_MJD_df_0{rx_id}',
        'sel_frc': f'sel_MJD_FRC_{rx_id:02}',
        'freq':    f'selected_frequency{rx_id}',
    }

    col_upload, col_controls = st.columns(2)

    # ── Left: uploader ────────────────────────────────────────────────────────
    with col_upload:
        with st.form(f"form_rx{rx_id}", clear_on_submit=True):
            files = st.file_uploader(
                f":file_folder: **Upload the CGGTTS files of receiver {rx_id}**",
                accept_multiple_files=True,
            )
            submitted = st.form_submit_button(f"**Submit{rx_id}**")

        if submitted and files:
            file_bytes = [(f.name, f.read()) for f in files]
            with st.spinner("Parsing files…"):
                df, mjd_days, frc_set, gnss_type, msgs = parse_cggtts_files(file_bytes)
            for level, text in msgs:
                getattr(st, level)(text)
            if not df.empty:
                st.session_state[ss['total']] = df
                st.session_state[ss['days']]  = mjd_days
                st.session_state[ss['frc']]   = frc_set
                st.session_state[ss['ref']]   = ', '.join(df['REF'].dropna().unique())
                st.session_state[ss['lab']]   = ' '.join(df['LAB'].dropna().unique())
                st.session_state[ss['gnss']]  = gnss_type or 'GPS'
                st.session_state.cv_result = None
                st.session_state.av_result = None

    # ── Right: MJD range + frequency (only once data is loaded) ───────────────
    filtered = None
    selected_freq = None
    with col_controls:
        if ss['total'] not in st.session_state:
            st.info("Upload and submit CGGTTS files to configure the MJD range and frequency.")
        else:
            mjd_days: list[int] = st.session_state[ss['days']]
            ctrl_a, ctrl_b = st.columns(2)
            with ctrl_a:
                start = st.selectbox("**Start MJD**", mjd_days, key=f'start_mjd_{rx_id:02}')
            with ctrl_b:
                end_opts = [d for d in mjd_days if d >= start]
                end = st.selectbox(
                    "**End MJD**", end_opts,
                    index=len(end_opts) - 1,
                    key=f'end_mjd_{rx_id:02}',
                )

            filtered = mjd_filter(st.session_state[ss['total']], start, end)
            st.session_state[ss['sel_df']] = filtered

            freqs = sorted(f for f in st.session_state.get(ss['frc'], []) if pd.notna(f))
            if not freqs:
                st.error("No valid frequencies in selected MJD range.")
            else:
                selected_freq = st.pills(
                    "**Select Frequency**", freqs, default=freqs[0], key=f'freq_pills_{rx_id}'
                )
                if selected_freq is None:
                    selected_freq = freqs[0]
                st.session_state[ss['freq']] = selected_freq

    # ── Below columns: chart + download ───────────────────────────────────────
    if filtered is None or selected_freq is None:
        return

    st.session_state[ss['sel_frc']] = filtered[filtered['FRC'] == selected_freq].copy()

    avg = weighted_refsys_avg(filtered, selected_freq)
    if avg.empty:
        st.error("No data for selected frequency in this MJD range.")
        return

    ref  = st.session_state.get(ss['ref'], '')
    gnss = st.session_state.get(ss['gnss'], '')
    lab  = st.session_state.get(ss['lab'], '')
    std  = avg['REFSYS'].std()

    fig = scatter_fig(
        avg['MJD'], avg['REFSYS'],
        title=(
            f"{ref} – {gnss} time at {lab} via {selected_freq}"
            "<br><sup>Each point = sum of satellite weighted REFSYS per epoch</sup>"
        ),
        std=std,
        ylabel="Weighted REFSYS (ns)",
    )
    st.plotly_chart(fig, use_container_width=True)

    out = avg.copy()
    out['MJD'] = out['MJD'].apply(lambda x: f"{x:.5f}")
    out['REFSYS'] = (out['REFSYS'] / 1e9).apply(lambda x: f"{x:.2e}")
    hdr = (
        f"# {ref} REFSYS data\n"
        f"# Start MJD: {math.floor(avg['MJD'].min())}\n"
        f"# End MJD: {math.ceil(avg['MJD'].max())}\n"
        f"# Frequency: {selected_freq}\n"
        f"# Lab: {lab}\n"
        f"# GNSS: {gnss}\n"
    )
    st.download_button(
        "Download Weighted REFSYS data",
        data=to_csv(hdr, out.rename(columns={'REFSYS': 'Weighted_Refsys(s)'})),
        file_name=f"Refsys_Rx{rx_id}.csv",
        mime='text/csv',
        key=f'dl_refsys_{rx_id}',
    )


# ── Common-View tab ───────────────────────────────────────────────────────────

def _render_cv() -> None:
    if 'df1_total' not in st.session_state or 'df2_total' not in st.session_state:
        st.info("Upload and submit CGGTTS files for **both** receivers first (Receiver 1 and Receiver 2 tabs).")
        return

    df1_base = st.session_state.get('sel_MJD_df_01', st.session_state['df1_total']).copy()
    df2_base = st.session_state.get('sel_MJD_df_02', st.session_state['df2_total']).copy()

    freqs1 = sorted(f for f in st.session_state.get('unique_FRC1', set()) if pd.notna(f))
    freqs2 = sorted(f for f in st.session_state.get('unique_FRC2', set()) if pd.notna(f))

    if not freqs1 or not freqs2:
        st.error("No frequency data available. Check that the receiver files loaded correctly.")
        return

    col_f1, col_f2, col_svid, col_elv, col_out = st.columns([1.7, 1.7, 2.6, 1.2, 1.2])
    with col_f1:
        freq1 = st.pills("**Freq – Rx1**", freqs1, default=freqs1[0], key='cv_freq1')
        if freq1 is None:
            freq1 = freqs1[0]
    with col_f2:
        freq2 = st.pills("**Freq – Rx2**", freqs2, default=freqs2[0], key='cv_freq2')
        if freq2 is None:
            freq2 = freqs2[0]

    df1 = df1_base[df1_base['FRC'] == freq1].copy()
    df2 = df2_base[df2_base['FRC'] == freq2].copy()

    if df1.empty or df2.empty:
        st.error("No data for the selected frequency in the loaded MJD range.")
        return

    if st.session_state.get('GNSS1') == 'GPS' == st.session_state.get('GNSS2'):
        df1['SAT'] = map_gps_svids(df1['SAT'].tolist())
        df2['SAT'] = map_gps_svids(df2['SAT'].tolist())

    all_svids     = sorted(set(df1['SAT'].unique()) | set(df2['SAT'].unique()))
    all_mjd_times = sorted(set(df1['MJD']) | set(df2['MJD']))

    if not all_svids:
        st.error("No satellite data from one or both receivers.")
        return

    with col_svid:
        selected_svids = st.multiselect(
            "**Satellites (PRN)**", ['ALL', 'NONE'] + all_svids, default=['ALL'], key='cv_svid_sel',
        )
    with col_elv:
        elevation_mask = st.number_input(
            '**Elev Mask (°)**', 0.0, 90.0, 15.0, 0.5, key='cv_elv',
        )
    with col_out:
        outlier_filter = st.number_input(
            '**Outlier (×σ)**', 0.5, 100.0, 1.5, 0.1, key='cv_out',
        )

    if st.button("Compute Common-View", key='cv_btn'):
        _cv_actual = [s for s in selected_svids if s not in ('ALL', 'NONE')]
        if 'NONE' in selected_svids and 'ALL' not in selected_svids and not _cv_actual:
            st.warning("No satellites selected. Choose at least one PRN or ALL to compute Common-View.")
            st.session_state.cv_result = None
            st.session_state.cv_sv = None
            st.session_state.cv_freq_warning = None
        elif st.session_state.get('GNSS1') != st.session_state.get('GNSS2'):
            st.error("Common-View cannot be processed: receivers are from different GNSS constellations.")
        else:
            with st.spinner("Computing Common-View…"):
                cv_result, cv_sv = process_cv(
                    df1, df2, all_mjd_times, selected_svids, all_svids,
                    elevation_mask, outlier_filter,
                )
            if cv_result.empty:
                st.error("No overlapping data. Check time periods, GNSS versions, or applied filters.")
                st.session_state.cv_result = None
                st.session_state.cv_sv = None
                st.session_state.cv_freq_warning = None
            else:
                st.session_state.cv_result = cv_result
                st.session_state.cv_sv = cv_sv
                st.session_state.cv_freq_warning = (
                    f"Caution: Comparing with different frequency codes: {freq1} vs {freq2}"
                    if freq1 != freq2 else None
                )

    if st.session_state.get('cv_freq_warning'):
        st.warning(st.session_state['cv_freq_warning'])

    lab1   = st.session_state.get('LAB1', 'Rx1')
    lab2   = st.session_state.get('LAB2', 'Rx2')
    gnss2  = st.session_state.get('GNSS2', '')

    cv_sv     = st.session_state.get('cv_sv')
    cv_result = st.session_state.get('cv_result')

    if cv_sv is not None and not cv_sv.empty:
        st.markdown("---")
        long_rows = [
            {'MJD': row['MJD'], 'SAT': sat, 'CV_diff': diff}
            for _, row in cv_sv.iterrows()
            for sat, diff in zip(row['SAT_list'], row['CV_diff_list'])
        ]
        long_df = pd.DataFrame(long_rows)

        x_sv  = long_df['MJD'].to_numpy(dtype=float)
        y_sv  = long_df['CV_diff'].to_numpy(dtype=float)
        fin   = np.isfinite(x_sv) & np.isfinite(y_sv)
        x_sv, y_sv = x_sv[fin], y_sv[fin]
        mean_sv   = float(np.mean(y_sv))
        std_sv    = float(np.std(y_sv, ddof=1))
        coeffs_sv = np.polyfit(x_sv, y_sv, 1)
        slope_sv  = coeffs_sv[0]
        sort_sv   = np.argsort(x_sv)
        x_line_sv = x_sv[sort_sv]
        y_line_sv = np.polyval(coeffs_sv, x_line_sv)

        fig = go.Figure()
        for sat in sorted(long_df['SAT'].unique()):
            sub = long_df[long_df['SAT'] == sat]
            fig.add_trace(go.Scatter(
                x=sub['MJD'], y=sub['CV_diff'],
                mode='markers', name=sat, marker=dict(size=8),
            ))
        fig.add_trace(go.Scatter(
            x=x_line_sv, y=y_line_sv, mode='lines',
            line=dict(color='black', width=2, dash='dash'),
            name='Linear fit', showlegend=False,
        ))
        fig.add_annotation(
            xref='paper', yref='paper', x=1, y=1,
            text=(
                f"Mean:     {mean_sv:.3f} ns<br>"
                f"Std Dev:  {std_sv:.3f} ns<br>"
                f"Slope:    {slope_sv:.4f} ns/day"
            ),
            showarrow=False, font=dict(size=14, color="black"),
            xanchor='right', yanchor='top',
            align='left',
            bgcolor='rgba(255,255,255,0.85)',
            bordercolor='rgba(100,100,100,0.4)',
            borderwidth=1,
            borderpad=6,
        )
        fig.update_layout(
            title=(
                f"{gnss2} CV per satellite: {lab1} ({freq1}) – {lab2} ({freq2})"
                "<br><sup>Each point = per-satellite REFSYS difference at each epoch</sup>"
            ),
            xaxis_title="MJD", yaxis_title="Time difference (ns)",
            xaxis=dict(tickformat=".2f", exponentformat='none', tickfont=dict(size=13)),
            yaxis=dict(tickmode='auto', nticks=10, tickfont=dict(size=13)),
            height=500,
        )
        st.plotly_chart(fig, use_container_width=True)

        min_x = math.floor(long_df['MJD'].min())
        max_x = math.ceil(long_df['MJD'].max()) - 1
        agg = (
            long_df.groupby('MJD')
            .agg(
                CV_SATs=('SAT', 'count'),
                PRNs=('SAT', lambda x: ','.join(x.astype(str))),
                Refsys_diff=('CV_diff', lambda x: ','.join((x / 1e9).apply(lambda v: f"{v:.2e}"))),
            )
            .reset_index()
        )
        agg['MJD'] = agg['MJD'].astype(float).apply(lambda x: f"{x:.5f}")
        hdr_sv = (
            f"# CV satellites: {lab1} – {lab2}\n"
            f"# Start MJD: {min_x}\n# End MJD: {max_x}\n"
            f"# Freq Rx1: {freq1} / Rx2: {freq2}\n"
            f"# Elevation mask: {elevation_mask} deg\n"
            f"# Outlier: {outlier_filter}× std dev\n"
            f"# Satellites: {', '.join(sorted(set(long_df['SAT'])))}\n"
        )
        st.download_button(
            "Download CV satellite data",
            data=to_csv(hdr_sv, agg),
            file_name="CV_satellite_data.csv",
            mime="text/csv",
            key='dl_cv_sat',
        )

        if cv_result is not None and not cv_result.empty:
            st.markdown("---")
            std = cv_result['CV_diff'].std()
            fig = scatter_fig(
                cv_result['MJD'], cv_result['CV_diff'],
                title=(
                    f"{gnss2} Common-View link: {lab1} ({freq1}) – {lab2} ({freq2})"
                    "<br><sup>Each point = mean REFSYS difference over common satellites per epoch</sup>"
                ),
                std=std,
            )
            st.plotly_chart(fig, use_container_width=True)

            out = cv_result.copy()
            out['MJD'] = out['MJD'].astype(float).apply(lambda x: f"{x:.5f}")
            out['CV_diff'] = (out['CV_diff'] / 1e9).apply(lambda x: f"{x:.2e}")
            hdr_cv = (
                f"# CV Time Transfer: {lab1} – {lab2}\n"
                f"# Start MJD: {min_x}\n# End MJD: {max_x}\n"
                f"# Freq Rx1: {freq1} / Rx2: {freq2}\n"
                f"# Elevation mask: {elevation_mask} deg\n"
                f"# Outlier: {outlier_filter}× std dev\n"
                f"# Satellites: {', '.join(sorted(set(long_df['SAT'])))}\n"
            )
            st.download_button(
                "Download CV data",
                data=to_csv(hdr_cv, out.rename(columns={'CV_diff': 'CV_difference(s)'})),
                file_name="Common_View_data.csv",
                mime="text/csv",
                key='dl_cv',
            )


# ── All-in-View tab ───────────────────────────────────────────────────────────

def _render_av() -> None:
    if 'df1_total' not in st.session_state or 'df2_total' not in st.session_state:
        st.info("Upload and submit CGGTTS files for **both** receivers first (Receiver 1 and Receiver 2 tabs).")
        return

    df1_base = st.session_state.get('sel_MJD_df_01', st.session_state['df1_total']).copy()
    df2_base = st.session_state.get('sel_MJD_df_02', st.session_state['df2_total']).copy()

    freqs1 = sorted(f for f in st.session_state.get('unique_FRC1', set()) if pd.notna(f))
    freqs2 = sorted(f for f in st.session_state.get('unique_FRC2', set()) if pd.notna(f))

    if not freqs1 or not freqs2:
        st.error("No frequency data available. Check that the receiver files loaded correctly.")
        return

    col_f1, col_f2, col_svid, col_elv, col_out = st.columns([1.7, 1.7, 2.6, 1.2, 1.2])
    with col_f1:
        freq1 = st.pills("**Freq – Rx1**", freqs1, default=freqs1[0], key='av_freq1')
        if freq1 is None:
            freq1 = freqs1[0]
    with col_f2:
        freq2 = st.pills("**Freq – Rx2**", freqs2, default=freqs2[0], key='av_freq2')
        if freq2 is None:
            freq2 = freqs2[0]

    df1 = df1_base[df1_base['FRC'] == freq1].copy()
    df2 = df2_base[df2_base['FRC'] == freq2].copy()

    if df1.empty or df2.empty:
        st.error("No data for the selected frequency in the loaded MJD range.")
        return

    if st.session_state.get('GNSS1') == 'GPS' == st.session_state.get('GNSS2'):
        df1['SAT'] = map_gps_svids(df1['SAT'].tolist())
        df2['SAT'] = map_gps_svids(df2['SAT'].tolist())

    all_svids     = sorted(set(df1['SAT'].unique()) | set(df2['SAT'].unique()))
    all_mjd_times = sorted(set(df1['MJD']) | set(df2['MJD']))

    if not all_svids:
        st.error("No satellite data from one or both receivers.")
        return

    with col_svid:
        selected_svids = st.multiselect(
            "**Satellites (PRN)**", ['ALL', 'NONE'] + all_svids, default=['ALL'], key='av_svid_sel',
        )
    with col_elv:
        elevation_mask = st.number_input(
            '**Elev Mask (°)**', 0.0, 90.0, 15.0, 0.5, key='av_elv',
        )
    with col_out:
        outlier_filter = st.number_input(
            '**Outlier (×σ)**', 0.5, 100.0, 1.5, 0.1, key='av_out',
        )

    if st.button("Compute All-in-View", key='av_btn'):
        _av_actual = [s for s in selected_svids if s not in ('ALL', 'NONE')]
        if 'NONE' in selected_svids and 'ALL' not in selected_svids and not _av_actual:
            st.warning("No satellites selected. Choose at least one PRN or ALL to compute All-in-View.")
            st.session_state.av_result = None
        elif st.session_state.get('GNSS1') != st.session_state.get('GNSS2'):
            st.error("All-in-View cannot be processed: receivers are from different GNSS constellations.")
        else:
            common_mjd = sorted(set(df1['MJD']) & set(df2['MJD']))
            if not common_mjd:
                st.error("No common MJD epochs between the two receivers.")
            else:
                with st.spinner("Computing All-in-View…"):
                    av_result = process_av(
                        df1, df2, selected_svids, all_svids, all_mjd_times,
                        elevation_mask, outlier_filter,
                    )
                if av_result.empty:
                    st.error("No data remaining after applying filters.")
                    st.session_state.av_result = None
                else:
                    st.session_state.av_result = av_result

    av_result = st.session_state.get('av_result')
    ref1  = st.session_state.get('REF01', 'Rx1')
    ref2  = st.session_state.get('REF02', 'Rx2')
    gnss2 = st.session_state.get('GNSS2', '')

    if av_result is not None and not av_result.empty:
        st.markdown("---")
        std = av_result['AV_diff'].std()
        fig = scatter_fig(
            av_result['MJD_time'], av_result['AV_diff'],
            title=(
                f"{gnss2} All-in-View: {ref1} ({freq1}) – {ref2} ({freq2})"
                "<br><sup>Each point = difference of weighted average REFSYS of all satellites in view</sup>"
            ),
            std=std,
        )
        st.plotly_chart(fig, use_container_width=True)

        out = av_result.dropna(subset=['AV_diff']).copy()
        out['MJD_time'] = out['MJD_time'].astype(float).apply(lambda x: f"{x:.5f}")
        out['AV_diff'] = (out['AV_diff'] / 1e9).apply(lambda x: f"{x:.2e}")
        min_x = math.floor(float(av_result['MJD_time'].min()))
        max_x = math.ceil(float(av_result['MJD_time'].max())) - 1
        hdr_av = (
            f"# AV link: {ref1} – {ref2}\n"
            f"# Start MJD: {min_x}\n# End MJD: {max_x}\n"
            f"# Freq Rx1: {freq1} / Rx2: {freq2}\n"
            f"# Elevation mask: {elevation_mask} deg\n"
            f"# Outlier: {outlier_filter}× std dev\n"
            f"# Satellites: {', '.join(selected_svids)}\n"
        )
        st.download_button(
            "Download AV data",
            data=to_csv(
                hdr_av,
                out.rename(columns={'MJD_time': 'MJD', 'AV_diff': 'AV_difference(s)'}),
            ),
            file_name="All_in_View_data.csv",
            mime="text/csv",
            key='dl_av',
        )


# ── Sidebar ───────────────────────────────────────────────────────────────────
st.sidebar.image(
    "https://www.bipm.org/documents/20126/27072194/Logo+BIPM+blue.png"
    "/797bb4e6-8cfb-5d78-b480-e460ad5eeec2?t=1583920059345",
    width=200,
)
st.sidebar.write("")
st.sidebar.image("https://www.fusfoundation.org/images/IEEE-UFFC.jpg", width=200)
st.sidebar.header("Time & Frequency Capacity Building")
st.sidebar.markdown("---")
st.sidebar.markdown("**Contact: tf.cbkt@bipm.org**")
st.sidebar.markdown("**For more information visit:**")
st.sidebar.markdown("[**BIPM e-Learning Platform**](https://e-learning.bipm.org/)")

# ── Page layout ───────────────────────────────────────────────────────────────
st.title(":chart_with_upwards_trend: CGGTTS data analyser v2.0")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Receiver 1", "Receiver 2", "Common-View", "All-in-View", "Data Format",
])

with tab1:
    render_receiver(1)

with tab2:
    render_receiver(2)

with tab3:
    _render_cv()

with tab4:
    _render_av()

with tab5:
    show_data_format()
