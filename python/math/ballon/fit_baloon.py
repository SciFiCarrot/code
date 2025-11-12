# fit_balloon.py
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from lmfit import Model, Parameters, report_fit

df = pd.read_csv("Ballon_data_opg6.csv")
x = df.iloc[:, 0].to_numpy(float)
y = df.iloc[:, 1].to_numpy(float)


def model(x, a, b, c, d):
    return a * (x - b) / (x**3 - c) + d


g = Model(model)
p = Parameters()
p.add("a", value=1e8)
p.add("b", value=0.0)
# keep c outside data x^3 to avoid singularity; set loose but sane bounds
x3 = x**3
p.add(
    "c",
    value=float(x3.min()) - 1e8,
    min=float(x3.min()) - 1e12,
    max=float(x3.min()) - 1e3,
)
p.add("d", value=float(np.median(y)))

fit = g.fit(y, params=p, x=x, method="leastsq")
report_fit(fit)

# R^2
yhat = fit.eval(x=x)
ss_res = np.sum((y - yhat) ** 2)
ss_tot = np.sum((y - y.mean()) ** 2)
r2 = 1 - ss_res / ss_tot

# Residuals
resid = y - yhat

# Bootstrap parameter CIs (quick-and-dirty)
rng = np.random.default_rng(0)
boots = []
for _ in range(500):
    idx = rng.integers(0, len(x), len(x))
    f2 = g.fit(y[idx], params=fit.params.copy(), x=x[idx], method="leastsq")
    boots.append([f2.params[n].value for n in ["a", "b", "c", "d"]])
boots = np.array(boots)
ci_low = np.percentile(boots, 2.5, axis=0)
ci_hi = np.percentile(boots, 97.5, axis=0)

print("\nParams:")
for name, val in fit.params.items():
    i = ["a", "b", "c", "d"].index(name)
    print(f"{name} = {val.value:.6g}  [{ci_low[i]:.6g}, {ci_hi[i]:.6g}]")
print(f"R^2 = {r2:.6f}")

# Plots
xx = np.linspace(x.min(), x.max(), 1000)
mask = np.abs(xx**3 - fit.params["c"].value) > 1e-9
xx = xx[mask]
yy = fit.eval(x=xx)

plt.figure()
plt.scatter(x, y, s=12, label="data")
plt.plot(xx, yy, label="fit")
plt.xlabel(df.columns[0])
plt.ylabel(df.columns[1])
plt.legend()
plt.tight_layout()
plt.savefig("fit.png", dpi=160)

plt.figure()
plt.scatter(x, resid, s=12)
plt.axhline(0, ls="--")
plt.xlabel("x")
plt.ylabel("residual")
plt.tight_layout()
plt.savefig("residuals.png", dpi=160)

pd.DataFrame(
    {
        "param": ["a", "b", "c", "d"],
        "value": [fit.params[n].value for n in ["a", "b", "c", "d"]],
        "ci_low": ci_low,
        "ci_high": ci_hi,
    }
).to_csv("params.csv", index=False)
