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
    # IV infusion Plasma-time curves
    `Page by Dr Slade Matthews, The University of Sydney, 2023`
    · converted to marimo from the [original Colab notebook](https://github.com/sladem-tox/PK_calcs/blob/main/Infusion_curves.ipynb)

    Concentration during infusion is given by:

    $$C_t = \frac{R}{Cl} \cdot (1-e^{-k_e t})$$

    Where C is drug concentration in plasma at time t, R = infusion rate, Cl = clearance, k_e = elimination rate constant, t = time

    Note that the above equation is derived by integrating the differential equation for drug infusion that combines the constant rate of infusion (zero-order) with the first-order process of elimination.

    $$\frac{dD_b}{dt} = R - k_e D_b$$

    where R is the infusion rate constant (zero order), D_b is the amount of drug in the body, and k_e is the elimination rate constant (first order).

    Also note the relationship between rate of drug infusion, clearance and steady-state drug concentration:

    $$C_{ss} = \frac{R}{Cl}$$

    ---
    Use the sliders below to change R (infusion rate) or Cl (clearance) and note the effects on the steady-state drug plasma concentration achieved.
    """)
    return


@app.cell
def _(mo):
    # R = infusion rate (mg/h), Cl = clearance (L/h), Vd = volume of distribution (L)
    r_slider = mo.ui.slider(1, 50, step=1, value=10, label="R (mg/h)", show_value=True)
    cl_sliders = mo.ui.array(
        [
            mo.ui.slider(5, 150, step=5, value=_v, label=f"Cl curve {_i + 1} (L/h)", show_value=True)
            for _i, _v in enumerate([40, 60, 80])
        ]
    )
    vd_slider = mo.ui.slider(20, 500, step=10, value=200, label="Vd (L)", show_value=True)
    mo.vstack([r_slider, *cl_sliders, vd_slider])
    return cl_sliders, r_slider, vd_slider


@app.cell
def _(cl_sliders, np, plt, r_slider, vd_slider):
    R = r_slider.value
    Vd = vd_slider.value
    clearances = cl_sliders.value

    t = np.linspace(0, 24, 100)
    plt.figure(figsize=(10, 5))
    for _Cl in clearances:
        # The elimination rate constant is Cl over Vd
        _k = _Cl / Vd
        plt.plot(t, R / _Cl * (1 - np.exp(-_k * t)), label=f"Clearance {_Cl} L/h")
    plt.xlabel("Time (h)")
    plt.ylabel("Plasma Concentration (mg/L)")
    plt.legend()
    plt.gca()
    return Vd, clearances


@app.cell
def _(Vd, clearances, mo):
    _lines = []
    for _Cl in clearances:
        _halflife = 0.693 * (Vd / _Cl)
        _ttss = 5 * _halflife
        _lines.append(f"- It will take **{_ttss:.2f} hours** to reach steady state if clearance is {_Cl:.0f} L/h")
    mo.md("\n".join(_lines))
    return


if __name__ == "__main__":
    app.run()
