# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "marimo",
#     "matplotlib",
#     "numpy",
# ]
# ///

import marimo

__generated_with = "0.23.6"
app = marimo.App()


@app.cell
def _():
    import marimo as mo
    import matplotlib.pyplot as plt
    import numpy as np

    return mo, np, plt


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Single Oral Dose Plasma-time Curve
    `Page by Dr Slade Matthews, The University of Sydney, 2023`
    · converted to marimo from the [original Colab notebook](https://github.com/sladem-tox/PK_calcs/blob/main/SingleOralDose.ipynb)

    Follows the formula:

    $$C = \frac{F \cdot Dose \cdot k_a}{Vd(k_a-k_e)} \cdot (e^{-k_e t} - e^{-k_a t})$$

    Here we are considering the situation where absorption is a first order process described by K_a. This is the most common model. Sometimes drug absorption is better described with a constant rate i.e. zero order absorption. We are not considering that situation here.
    For more on the clinical use of absorption rate see this excellent summary:

    *Holford, N. (2016). Absorption and Half-Life. Translational and Clinical Pharmacology, 24(4).*

    ---
    Below we require values for dose, Cl, Vd, F, and ka.
    This simple model does not account for salting effects, metabolism, etc.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    - Here we use the PK parameters from the single IV curve in this repo. For more on the estimation of oral PK parameters see: Gabrielsson 2006 (page 508).
    - Bioavailability would need to be determined experimentally: F = AUC<sub>oral</sub>/AUC<sub>iv</sub>.
    - k<sub>a</sub> is experimentally extrapolated by means of a method of residuals (feathering) where k<sub>a</sub> corresponds to the slope of the residual line. The default gives a nice shaped curve! You would need to consult published papers to find values of k<sub>a</sub> for your drug or determine it experimentally.
    """)
    return


@app.cell
def _(mo):
    dose_slider = mo.ui.slider(10, 1000, step=10, value=200, label="Dose (mg)", show_value=True)
    cl_slider = mo.ui.slider(1, 100, step=1, value=20, label="Cl (L/h)", show_value=True)
    vd_slider = mo.ui.slider(10, 500, step=10, value=200, label="Vd (L)", show_value=True)
    f_slider = mo.ui.slider(0.05, 1.0, step=0.05, value=0.8, label="F (bioavailability)", show_value=True)
    ka_slider = mo.ui.slider(0.05, 3.0, step=0.01, value=0.54, label="ka (h⁻¹)", show_value=True)
    mo.vstack([dose_slider, cl_slider, vd_slider, f_slider, ka_slider])
    return cl_slider, dose_slider, f_slider, ka_slider, vd_slider


@app.cell
def _(cl_slider, dose_slider, f_slider, ka_slider, vd_slider):
    dose = dose_slider.value
    Cl = cl_slider.value
    Vd = vd_slider.value
    F = f_slider.value
    ka = ka_slider.value
    # Assuming we have the data from the single IV curve we know Cl and Vd, so k can be estimated:
    # the elimination rate constant is simply Cl over Vd
    k = Cl / Vd
    kdif = ka - k
    return F, Vd, dose, k, ka, kdif


@app.cell
def _(k, mo, np):
    # Calculate half-life
    hl = -np.log(0.5) / k
    mo.md(f"The half-life for the drug is **{hl:.2f} hours**.")
    return


@app.cell
def _(F, Vd, dose, k, ka, kdif, mo, np, plt):
    mo.stop(abs(kdif) < 1e-9, mo.md("**ka must differ from k** — the formula divides by (ka − k)."))
    _t = np.linspace(0, 24, 100)
    _y = F * dose * ka / (Vd * kdif) * (np.exp(-k * _t) - np.exp(-ka * _t))
    plt.figure(figsize=(10, 5))
    plt.plot(_t, _y)
    plt.xlabel("Time (h)")
    plt.ylabel("Plasma Concentration (mg/L)")
    plt.gca()
    return


@app.cell
def _(F, Vd, dose, k, ka, kdif, np):
    # The oral disposition equation defined as a function so we can ask it about specific times.
    def oral(t):
        return F * dose * ka / (Vd * kdif) * (np.exp(-k * t) - np.exp(-ka * t))

    return (oral,)


@app.cell
def _(mo):
    time_slider = mo.ui.slider(0, 48, step=0.5, value=5, label="Time t (h)", show_value=True)
    time_slider
    return (time_slider,)


@app.cell
def _(mo, oral, time_slider):
    mo.md(
        f"The plasma concentration at t = {time_slider.value} h will be **{oral(time_slider.value):.2f} mg/L**"
    )
    return


if __name__ == "__main__":
    app.run()
