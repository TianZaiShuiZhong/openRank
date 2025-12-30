import pandas as pd
import numpy as np


def load_and_compute_trend(file_path, window=3):
    """加载 CSV 并计算活跃度时序、移动平均、线性趋势、趋势分类与异常点。

    返回字段：metric, slope, trend (increasing/decreasing/stable),
    percent_change, anomalies, latest, series
    """
    df = pd.read_csv(file_path, parse_dates=['date'])
    if df.empty:
        return {'error': 'no data'}
    df = df.sort_values('date').reset_index(drop=True)
    # 使用 stars 作为活跃度度量示例
    df['days'] = (df['date'] - df['date'].min()).dt.days
    df['ma'] = df['stars'].rolling(window, min_periods=1).mean()

    x = df['days'].values
    y = df['stars'].values
    slope = 0.0
    if len(x) >= 2 and np.ptp(x) > 0:
        coef = np.polyfit(x, y, 1)
        slope = float(coef[0])

    # 最近一段的相对变化（相对于最早值或窗口平均）
    percent_change = None
    if len(y) >= 2 and y[0] != 0:
        percent_change = float((y[-1] - y[0]) / max(1, y[0]))

    # 简单趋势分类
    TREND_SLOPE_THRESH = max(0.1, max(1e-6, abs(y.mean()) * 0.001))
    if slope > TREND_SLOPE_THRESH:
        trend = 'increasing'
    elif slope < -TREND_SLOPE_THRESH:
        trend = 'decreasing'
    else:
        trend = 'stable'

    # 异常检测：差分的 z-score
    diffs = np.diff(y)
    anomalies = []
    if len(diffs) > 0:
        mu = diffs.mean()
        sigma = diffs.std(ddof=0)
        if sigma == 0:
            z = np.zeros_like(diffs)
        else:
            z = (diffs - mu) / sigma
        for i, zval in enumerate(z, start=1):
            if abs(zval) > 2.0:
                anomalies.append({
                    'date': df.loc[i, 'date'].strftime('%Y-%m-%d'),
                    'stars': int(df.loc[i, 'stars']),
                    'diff': int(diffs[i-1]),
                    'zscore': float(zval)
                })

    latest_row = df.iloc[-1]
    latest = {
        'date': latest_row['date'].strftime('%Y-%m-%d'),
        'stars': int(latest_row['stars']),
        'forks': int(latest_row.get('forks', 0)),
        'contributors': int(latest_row.get('contributors', 0))
    }

    series = []
    for _, row in df.iterrows():
        series.append({
            'date': row['date'].strftime('%Y-%m-%d'),
            'stars': int(row['stars']),
            'ma': float(row['ma'])
        })

    return {
        'metric': 'stars',
        'slope': slope,
        'trend': trend,
        'percent_change': percent_change,
        'anomalies': anomalies,
        'latest': latest,
        'series': series
    }
