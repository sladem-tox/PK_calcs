# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "marimo",
#     "matplotlib",
#     "numpy",
#     "scipy",
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
    from scipy import integrate

    return integrate, mo, np, plt


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Single IV Dose Plasma-time Curve
    `Page by Dr Slade Matthews, The University of Sydney, 2023`
    · converted to marimo from the [original Colab notebook](https://github.com/sladem-tox/PK_calcs/blob/main/PlasmaTime_SingleIV.ipynb)

    Follows the formula:

    $$C = C_0 \cdot e^{-kt}$$

    The initial drug plasma concentration for an IV dose is given by:

    $$C_0 = \frac{dose}{Vd}$$

    The formula for the constant "k" is given by:

    $$k = \frac{Cl}{Vd}$$

    ---
    Use the sliders below to choose your own values for dose, clearance, and volume of distribution and observe the effects on the plasma-time curve.
    """)
    return


@app.cell
def _(mo):
    # Drug parameters: dose (mg), Cl = clearance (L/h), Vd = volume of distribution (L)
    dose_slider = mo.ui.slider(10, 500, step=10, value=100, label="Dose (mg)", show_value=True)
    cl_slider = mo.ui.slider(1, 100, step=1, value=20, label="Cl (L/h)", show_value=True)
    vd_slider = mo.ui.slider(10, 500, step=10, value=200, label="Vd (L)", show_value=True)
    mo.vstack([dose_slider, cl_slider, vd_slider])
    return cl_slider, dose_slider, vd_slider


@app.cell
def _(cl_slider, dose_slider, vd_slider):
    dose = dose_slider.value
    Cl = cl_slider.value
    Vd = vd_slider.value

    # Initial concentration is dose over volume of distribution
    ystart = dose / Vd
    # The elimination rate constant is Cl over Vd
    k = Cl / Vd
    return Cl, Vd, dose, k, ystart


@app.cell
def _(k, np, plt, ystart):
    _t = np.linspace(0, 24, 100)
    _y = ystart * np.exp(-k * _t)

    plt.figure(figsize=(10, 5))
    plt.plot(_t, _y)
    plt.xlabel("Time (h)")
    plt.ylabel("Plasma Concentration (mg/L)")
    plt.gca()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The AUC can be calculated using the relationship:

    $$AUC = \frac{Dose}{Cl}$$
    """)
    return


@app.cell
def _(Cl, dose, mo):
    AUC = dose / Cl
    mo.md(f"The AUC is **{AUC:g}**")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We can also determine the AUC by integrating the plasma-time curve as this is how it would be determined experimentally. Here we use trapezoidal integration with a set of x y coordinates determined using the formula for the IV plasma-time curve.
    """)
    return


@app.cell
def _(integrate, k, mo, np, ystart):
    def f1(t):
        return ystart * np.exp(-k * t)

    # linspace returns an evenly spaced set of 1000 values from 0 to 24, as used in the plot above
    _t = np.linspace(0, 24, 1000)
    # Run f1 on every time value to get the y coordinates
    y1 = f1(_t)
    # Trapezoidal integration adds up the trapezoids built from the x and y coordinates
    I1 = integrate.trapezoid(y1, _t)
    mo.md(f"The AUC from integration is **{I1:.4f}**")
    return (f1,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## The AUC from integration is not the same as Dose/Cl. Why?
    """)
    return


@app.cell
def _(f1, integrate, np):
    # The trapezoidal rule can't go up to infinity because we can't keep making boxes for ever!
    # scipy has an integral function that can reach infinity.
    I = integrate.quad(f1, 0, np.inf)
    I
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The quad integral (above) returns the integral and an error estimate. Pretty small error and very close to exactly Dose/Cl!
    """)
    return


@app.cell
def _(mo):
    time_slider = mo.ui.slider(0, 48, step=0.5, value=20, label="Time t (h)", show_value=True)
    time_slider
    return (time_slider,)


@app.cell
def _(f1, mo, time_slider):
    # You can plug any time value "t" into the equation to find the corresponding concentration value
    conc = f1(time_slider.value)
    mo.md(f"The plasma concentration at time t = {time_slider.value} h is **{conc:.2f} mg/L**")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The formula for half-life is given by:

    $$t_{\frac{1}{2}} = 0.693 \cdot \frac{Vd}{Cl}$$
    """)
    return


@app.cell
def _(Cl, Vd, mo):
    halflife = 0.693 * (Vd / Cl)
    mo.md(f"The half-life for the drug is **{halflife:.2f} hours**.")
    return (halflife,)


@app.cell
def _(halflife, mo, ystart):
    # Calculate how many half-lives have passed at some timepoint and determine the plasma concentration remaining.
    timepoint = 24
    num_hfl = timepoint / halflife
    remain = ystart / 2**num_hfl
    mo.md(f"At {timepoint:.1f} hours there will be **{remain:.3f} mg/L** remaining in the plasma")
    return


@app.cell
def _():
    # Simple example of why 2 to the power of how many half-lives determines the fraction remaining.
    # Convince yourself that 2 to the power of "how many half-lives" gives the fraction remaining.
    # 50 div 2 is 25 (2^1)
    # 25 div 2 is 12.5 (2^2)
    # 12.5 div 2 is 6.25 (2^3)
    Czero = 50
    Czero / 2**3
    return


if __name__ == "__main__":
    app.run()
