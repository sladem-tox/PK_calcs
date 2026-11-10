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
    # Multiple Oral Dosing Plasma-time Curve
    `Page by Dr Slade Matthews, The University of Sydney, 2023`
    · converted to marimo from the [original Colab notebook](https://github.com/sladem-tox/PK_calcs/blob/main/MultipleOralDose.ipynb)

    The plasma concentration at any time following multiple dosing can be determined with the following formula * :

    $$C_p = \frac{F \cdot Dose \cdot k_a}{Vd(k-k_a)} \cdot \Big[ \Big( \frac{1-e^{-nk_a \tau}}{1-e^{-k_a\tau}} \Big)e^{-k_at} - \Big(\frac{1-e^{-nk\tau}}{1-e^{-k\tau}} \Big)e^{-kt} \Big]$$

    Where n = number of doses, τ = dose interval, F = fraction absorbed, Vd is volume of distribution, t = time after administration of n doses, ka is the absorption rate constant, k is the elimination rate constant.

    *Appears as equation 8.34 in Shargel, & Yu, A. B. C. (2016). Applied biopharmaceutics & pharmacokinetics (7th edition.). McGraw Hill Education.*

    ---
    Below we require values for dose, Cl, Vd, F, and ka.
    This simple model does not account for salting effects, metabolism, etc.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Example from textbook

    Cp at 4 hours after the seventh dose may be calculated using Equation 8.34, letting n = 7, t = 4, τ = 8, and making the appropriate substitutions. Where Bioavailability = 0.75, Dose = 250, ka = 0.9h^-1, Vd =1.5, ke =0.07.

    ![image.png](data:image/png;base64,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)

    Cp = 2.86 mg/L
    """)
    return


@app.cell
def _(np):
    def cp_multiple(t, n, dose, tau, F, ka, k, Vd):
        """Equation 8.34: plasma concentration t hours after the nth dose."""
        return (F * dose * ka) / (Vd * (k - ka)) * (
            ((1 - np.exp(-n * ka * tau)) / (1 - np.exp(-ka * tau))) * np.exp(-ka * t)
            - ((1 - np.exp(-n * k * tau)) / (1 - np.exp(-k * tau))) * np.exp(-k * t)
        )

    return (cp_multiple,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    So here we check that we can get the same value as the textbook with our python script...
    """)
    return


@app.cell
def _(cp_multiple):
    # Textbook parameters: 4 hours after the 7th dose
    textbook = dict(
        dose=250,
        tau=8,  # dosing interval is called tau
        F=0.75,
        ka=0.9,
        k=0.07,
        Vd=121.5,  # 1.5 L/kg * 81 kg
    )
    round(float(cp_multiple(4, 7, **textbook)), 2)
    return (textbook,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    So the plasma concentration following each dose must be calculated separately and then added together using superposition of the curves to get the whole plasma-time curve for multiple dosing.

    The variable t (dosetime below) becomes time since the nth dose being modelled. So for the first dose time is simply t but for the 3rd dose, t = (time - (2*τ)).

    OK. So now we try to map the whole of dose 7...
    """)
    return


@app.cell
def _(cp_multiple, np, plt, textbook):
    _time = np.linspace(0, 24, 100)
    plt.figure(figsize=(10, 5))
    plt.plot(_time, cp_multiple(_time, 7, **textbook))
    plt.xlabel("Time (h)")
    plt.ylabel("Plasma Concentration (mg/L)")
    plt.gca()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Finally we generate a plot of multiple dosing where we can choose the dosing interval τ and how long we observe (168 hours in a week).
    """)
    return


@app.cell
def _(mo):
    dose_slider = mo.ui.slider(10, 1000, step=10, value=250, label="Dose (mg)", show_value=True)
    tau_slider = mo.ui.slider(1, 48, step=1, value=24, label="τ dosing interval (h)", show_value=True)
    duration_slider = mo.ui.slider(24, 336, step=24, value=168, label="Observe for (h)", show_value=True)
    f_slider = mo.ui.slider(0.05, 1.0, step=0.05, value=0.75, label="F", show_value=True)
    ka_slider = mo.ui.slider(0.05, 3.0, step=0.05, value=0.9, label="ka (h⁻¹)", show_value=True)
    k_slider = mo.ui.slider(0.01, 0.5, step=0.01, value=0.07, label="k (h⁻¹)", show_value=True)
    vd_slider = mo.ui.slider(10, 500, step=0.5, value=121.5, label="Vd (L)", show_value=True)
    mo.vstack([dose_slider, tau_slider, duration_slider, f_slider, ka_slider, k_slider, vd_slider])
    return (
        dose_slider,
        duration_slider,
        f_slider,
        k_slider,
        ka_slider,
        tau_slider,
        vd_slider,
    )


@app.cell
def _(
    cp_multiple,
    dose_slider,
    duration_slider,
    f_slider,
    k_slider,
    ka_slider,
    mo,
    np,
    plt,
    tau_slider,
    vd_slider,
):
    k = k_slider.value
    ka = ka_slider.value
    Vd = vd_slider.value
    tau = tau_slider.value
    mo.stop(abs(k - ka) < 1e-9, mo.md("**ka must differ from k** — the formula divides by (k − ka)."))

    _time = np.linspace(0, duration_slider.value, num=1000)
    # The dose number (m_array) is time/tau as an integer plus one (to correct for the initial zero),
    # and dosetime is time since the last dose, so it starts from zero after each dose.
    _n_array = np.int_(_time / tau)
    _dosetime = _time - _n_array * tau
    _m_array = _n_array + 1
    _y = cp_multiple(_dosetime, _m_array, dose_slider.value, tau, f_slider.value, ka, k, Vd)

    plt.figure(figsize=(10, 5))
    plt.plot(_time, _y)
    plt.xlabel("Time (hours)")
    plt.ylabel("Plasma Concentration (mg/L)")
    plt.title("Plasma Concentration for multiple oral doses")
    plt.grid(True)
    plt.gca()
    return Vd, k


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    It takes about five half-lives to reach steady-state (see below). With the default values the top and bottom of the curves even out after about the 50 hour timepoint.
    """)
    return


@app.cell
def _(Vd, k, mo):
    Cl = k * Vd
    halflife = 0.693 * (Vd / Cl)
    time2steady = 5 * halflife
    mo.md(f"It will take approximately **{time2steady:.2f} hours** to reach steady-state.")
    return


if __name__ == "__main__":
    app.run()
