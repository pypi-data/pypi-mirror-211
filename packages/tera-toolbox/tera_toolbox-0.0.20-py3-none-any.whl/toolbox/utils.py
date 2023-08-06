import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from . import stats


def extract_values_from_key(list_of_dicts, key):
    return [d[key] for d in list_of_dicts if key in d]


def count_days(start_date, end_date, business=True, holidays=[]):

    date_range = pd.date_range(start_date, end_date, freq="D")

    if business:
        holidays = pd.to_datetime(holidays)
        weekdays = np.isin(date_range.weekday, [5, 6], invert=True)
        non_holidays = np.isin(date_range, holidays, invert=True)
        valid_days = np.logical_and(weekdays, non_holidays).sum()
    else:
        valid_days = len(date_range)

    return valid_days - 1


def add_days(
    start_date,
    num_days=0,
    num_months=0,
    num_years=0,
    business=True,
    holidays=[],
):
    date_format = "%Y-%m-%d"
    start_date = datetime.strptime(start_date, date_format)

    holidays = [datetime.strptime(h, date_format) for h in holidays]

    new_date = start_date + relativedelta(
        days=num_days, months=num_months, years=num_years
    )

    if business:
        while new_date.weekday() in (5, 6) or new_date in holidays:
            new_date += timedelta(days=1)

    return new_date.strftime(date_format)


def random_bool(p, N):
    return np.random.choice(a=[True, False], size=(N,), p=[p, 1 - p])


def patrimonio_analysis(
    pl_inicial,
    ap,
    ex,
    months=1200,
    freq_ap=1,
    timing_ap=False,
    max_ap=999999999,
    max_ex=999999999,
    ap_till=720,
    ap_from=1,
    freq_ex=1,
    timing_ex=True,
    ex_till=1200,
    ex_from=1,
    juro_real=0.02,
    step_freq_ap=0,
    step_ap=0.0,
    step_freq_ex=0,
    step_ex=0.0,
    extra_ap=0,
    extra_prob_ap=0.0,
    extra_ex=0,
    extra_prob_ex=0.0,
    extra=[],
):
    extra = pd.DataFrame(np.array(extra), columns=["months", "aportes", "despesas"])
    df = pd.DataFrame(np.arange(1, months + 1, 1), columns=["months"])
    df["years"] = df["months"] / 12
    df["aportes"] = np.minimum(
        max_ap,
        (
            (df["months"] % freq_ap == 0)
            & (df["months"] <= ap_till)
            & (df["months"] >= ap_from)
        )
        * (ap * (1 + step_ap) ** (df["months"] // step_freq_ap)),
    ) + extra_ap * random_bool(extra_prob_ap, months)
    df["despesas"] = np.minimum(
        max_ex,
        (
            (df["months"] % freq_ex == 0)
            & (df["months"] <= ex_till)
            & (df["months"] >= ex_from)
        )
        * (ex * (1 + step_ex) ** (df["months"] // step_freq_ex)),
    ) + extra_ex * random_bool(extra_prob_ex, months)

    df["aportes"] = df["aportes"] + extra["aportes"]
    df["despesas"] = df["despesas"] + extra["despesas"]

    return calculate_patrimonio(df, pl_inicial, timing_ap, timing_ex, juro_real)


def calculate_patrimonio(df, pl_inicial, timing_ap, timing_ex, juro_real):
    juro_real = (1 + juro_real) ** (1 / 12) - 1
    result = []
    for i, r in df.iterrows():
        result.append(
            (
                (pl_inicial if i == 0 else result[i - 1])
                + (r["aportes"] if timing_ap else 0)
                - (r["despesas"] if timing_ex else 0)
            )
            * (1 + juro_real)
            + (r["aportes"] if not timing_ap else 0)
            - (r["despesas"] if not timing_ex else 0)
        )
    df["patrimonio"] = result

    return df

def sensitivity_analysis(data, function, var_x, var_y):
    # Initialize results list
    results = []

    # Iterate over all values in var_x and var_y
    for x in var_x['values']:
        for y in var_y['values']:
            # Update data dict
            data[var_x['key']] = x
            data[var_y['key']] = y

            # Call function with updated data as parameters
            result = function(**data)

            # Store x, y, and result in results list
            results.append((x, y, result))
            
    return results

def clean(data):
  """clean step to remove inconsistend data"""
  return data.copy().fillna(0).replace([np.inf, -np.inf, float('NaN')])

def to_quotes(returns, base=1e5):
  """converts returns series to quote prices"""
  return (1+ to_rolling_returns(returns))* base

def to_returns(prices):
  """simple arithmetic returns from a price series"""
  return prices.pct_change().dropna()

def to_rolling_returns(returns):
  """calculates rolling compounded returns"""
  return returns.add(1).cumprod() -1
  
def to_log_returns(returns, base='e'):
  """logarithm returns from a price series and base"""
  if base == '2':
    return np.log2(1+returns)
  elif base == '10':
    return np.log10(1+returns)
  else:
    return np.log(1+returns)

def rebase(prices, base=100):
  """rebase a series to a given initial base"""
  return prices / prices.iloc[0] * base

def to_excess_returns(returns, rf=0., periods=252):
    """Calculates excess returns"""
    if periods is not None:
        rf = np.power(1 + rf, 1./ periods)  -1.
    if isinstance(returns, pd.DataFrame):
        result = pd.DataFrame()
        for c in returns.columns:
            result[c] = returns[c] - rf
    else:
        result = returns - rf
    return result.dropna()

def match_volatility(returns, benchmark): 
  return (returns / returns.std()) * benchmark.std()
  
def group_returns(returns, groupby, compounded=True):
  """Summarize returns
  group_returns(df, df.index.year)
  group_returns(df, [df.index.year, df.index.month])
  """
  if compounded:
      return returns.groupby(groupby).apply(stats.total_return)
  return returns.groupby(groupby).sum()

def aggregate_returns(returns, period=None, compounded=True):
  """Aggregates returns based on date periods"""
  if period is None or 'day' in period:
    return returns
  index = returns.index

  if 'month' in period:
    return group_returns(returns, index.month, compounded=compounded)

  if 'quarter' in period:
    return group_returns(returns, index.quarter, compounded=compounded)

  if period == "Y" or any(x in period for x in ['year', 'eoy', 'yoy']):
    return group_returns(returns, index.year, compounded=compounded)

  if 'week' in period:
    return group_returns(returns, index.isocalendar().week, compounded=compounded)

  if 'eow' in period or period == "W":
    return group_returns(returns, [index.year, index.isocalendar().week],
                            compounded=compounded)

  if 'eom' in period or period == "M":
    return group_returns(returns, [index.year, index.month],
                            compounded=compounded)

  if 'eoq' in period or period == "Q":
    return group_returns(returns, [index.year, index.quarter],
                            compounded=compounded)

  if not isinstance(period, str):
    return group_returns(returns, period, compounded)

  return returns

def count_consecutive(data):
  """Counts consecutive data"""
  if isinstance(data, pd.DataFrame):
    results = pd.DataFrame()
    for c in data:
      results[c] = data[c] * (data[c].groupby((data[c] != data[c].shift(1)).cumsum()).cumcount() + 1)
    return results

  return data * (data.groupby((data != data.shift(1)).cumsum()).cumcount() + 1)

def to_drawdown_series(returns):
    """Convert returns series to drawdown series"""
    prices = to_quotes(returns, 1)
    prices = clean(prices)
    dd = prices / np.maximum.accumulate(prices) - 1.
    return dd.replace([np.inf, -np.inf, -0], 0)

def remove_outliers(returns, quantile=.95):
  """Returns series of returns without the outliers"""
  return returns[returns < returns.quantile(quantile)]

def exposure(returns):
  """Returns the market exposure time (returns != 0)"""

  return 100 * returns[(returns != 0)].count() / returns.count() / 100