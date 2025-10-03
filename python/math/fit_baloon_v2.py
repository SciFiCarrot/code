# fit_models.py
from pathlib import Path
from typing import Callable, Dict, Tuple

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# ---------- Load data ----------
csv = "Ballon_data_opg6.csv"
df = pd.read_csv(csv)
x = df.iloc[:, 0].to_numpy(float)
y = df.iloc[:, 1].to_numpy(float)


# ---------- Utility ----------
def eval_metrics(y, yhat, k):
    n = len(y)
    ss_res = float(np.sum((y - yhat) ** 2))
    ss_tot = float(np.sum((y - y.mean()) ** 2))
    r2 = 1.0 - ss_res / ss_tot
    rmse = np.sqrt(ss_res / n)
    aic = n * np.log(ss_res / n) + 2 * k
    bic = n * np.log(ss_res / n) + k * np.log(n)
    return r2, rmse, aic, bic


def fit_curve(
    model: Callable, p0, bounds, name: str
) -> Tuple[np.ndarray, np.ndarray, dict]:
    try:
        from scipy.optimize import curve_fit

        popt, pcov = curve_fit(model, x, y, p0=p0, bounds=bounds, maxfev=200000)
    except Exception:
        # fallback: simple Nelder-Mead via minimize on MSE
        from scipy.optimize import minimize

        def mse(p):
            return np.mean((y - model(x, *p)) ** 2)

        res = minimize(
            mse,
            np.array(p0, float),
            method="Nelder-Mead",
            options=dict(maxiter=200000, xatol=1e-10, fatol=1e-10),
        )
        popt, pcov = res.x, None
    yhat = model(x, *popt)
    r2, rmse, aic, bic = eval_metrics(y, yhat, len(popt))
    # plots
    xx = np.linspace(x.min(), x.max(), 1000)
    yy = model(xx, *popt)
    plt.figure()
    plt.scatter(x, y, s=12, label="data")
    plt.plot(xx, yy, label=name)
    plt.xlabel(df.columns[0])
    plt.ylabel(df.columns[1])
    plt.legend()
    plt.tight_layout()
    Path("out").mkdir(exist_ok=True)
    plt.savefig(f"out/{name}_fit.png", dpi=180)
    plt.close()
    resid = y - yhat
    plt.figure()
    plt.scatter(x, resid, s=10)
    plt.axhline(0, ls="--")
    plt.xlabel(df.columns[0])
    plt.ylabel("residuals")
    plt.tight_layout()
    plt.savefig(f"out/{name}_resid.png", dpi=180)
    plt.close()
    return popt, pcov, dict(r2=r2, rmse=rmse, aic=aic, bic=bic)


# ---------- Existing models ----------
def rational_abcd(x, a, b, c, d):
    # y = a*(x-b)/(x**3 - c) + d
    den = x**3 - c
    den = np.where(den == 0, np.finfo(float).eps, den)
    return a * (x - b) / den + d


def biexp(x, A, k, B, m, d):
    return d + A * np.exp(-k * x) + B * np.exp(-m * x)


# ---------- Model registry ----------
MODELS: Dict[str, dict] = {
    "rational_abcd": {
        "fn": rational_abcd,
        "p0": [1e8, 0.0, (x**3).min() - 1e8, np.median(y)],
        "bounds": (
            [-1e12, -1e6, (x**3).min() - 1e16, y.min() - 1e6],
            [1e12, 1e6, (x**3).min() - 1e3, y.max() + 1e6],
        ),
        "params": ["a", "b", "c", "d"],
    },
    "biexp": {
        "fn": biexp,
        "p0": [
            y[0] - y[-1],
            0.01,
            (np.percentile(y, 20) - np.percentile(y, 80)),
            0.001,
            np.percentile(y, 80),
        ],
        "bounds": (
            [-np.inf, 1e-9, -np.inf, 1e-9, y.min() - 1e5],
            [np.inf, 1.0, np.inf, 1.0, y.max() + 1e5],
        ),
        "params": ["A", "k", "B", "m", "d"],
    },
}

# ---------- Run all and compare ----------
records = []
for name, spec in MODELS.items():
    popt, pcov, m = fit_curve(spec["fn"], spec["p0"], spec["bounds"], name)
    rec = {"model": name, **m}
    for key, val in zip(spec["params"], popt):
        rec[key] = val
    records.append(rec)

pd.DataFrame(records).sort_values("aic").to_csv("out/summary.csv", index=False)
print(pd.DataFrame(records).sort_values("aic"))
