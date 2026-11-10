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
    from scipy.integrate import solve_ivp

    return mo, np, plt, solve_ivp


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Two-Compartment Model for IV bolus
    `Page by Dr Slade Matthews, The University of Sydney, 2024`
    · converted to marimo from the [original Colab notebook](https://github.com/sladem-tox/PK_calcs/blob/main/2_CompartmentModel.ipynb)

    For the two compartment model there are **two differential equations** that describe the disposition of the drug:

    The first describes the change in concentration in the central compartment (C_1):

    $$\text{Equation 1:} \quad \frac{dC_1}{dt} = - (k_{10} + k_{12}) C_1 + k_{21} C_2 + \frac{D}{V_1} \delta(t)$$

    The second equation describes the change in concentration in the peripheral compartment (C_2):

    $$\text{Equation 2:} \quad \frac{dC_2}{dt} = k_{12} C_1 - k_{21} C_2$$
    """)
    return


@app.cell
def _(np, plt, solve_ivp):
    # Define the differential equations for the 2-compartment model
    def two_compartment_model(t, C, k10, k12, k21, D, V1):
        C1, C2 = C  # C1 is central compartment, C2 is peripheral compartment
        dC1_dt = -(k10 + k12) * C1 + k21 * C2 + (D / V1 if t == 0 else 0)  # Dose only at t=0
        dC2_dt = k12 * C1 - k21 * C2
        return [dC1_dt, dC2_dt]

    # Parameters
    _k10 = 0.1  # Elimination rate constant from central compartment
    _k12 = 0.05  # Transfer rate from central to peripheral compartment
    _k21 = 0.03  # Transfer rate from peripheral to central compartment
    _D = 100  # Dose (mg)
    _V1 = 10  # Volume of central compartment (L)

    # Initial conditions: No drug in the system at the start
    _initial_conditions = [0, 0]

    # Time span for the simulation
    _t_span = (0, 48)  # Simulate for 48 hours
    _t_eval = np.linspace(_t_span[0], _t_span[1], 500)  # Time points where solution is evaluated

    # Solve the differential equations
    _solution = solve_ivp(
        two_compartment_model,
        _t_span,
        _initial_conditions,
        args=(_k10, _k12, _k21, _D, _V1),
        t_eval=_t_eval,
    )

    plt.figure(figsize=(10, 6))
    plt.plot(_solution.t, _solution.y[0], label="Central Compartment (C1)", color="blue")
    plt.plot(_solution.t, _solution.y[1], label="Peripheral Compartment (C2)", color="orange")
    plt.xlabel("Time (hours)")
    plt.ylabel("Concentration (mg/L)")
    plt.title("2-Compartment Pharmacokinetic Model")
    plt.grid(True)
    plt.legend()
    plt.gca()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The concentrations C_1(t) and C_2(t) can be determined using the analytical solutions (via Laplace transforms) to the differential equations of the 2-compartment model:

    $$\text{Equation 2:} \quad C_1(t) = A e^{-\alpha t} + B e^{-\beta t}$$

    $$\text{Equation 3:} \quad C_2(t) = \frac{A \cdot k_{12}}{\alpha - k_{21}} e^{-\alpha t} + \frac{B \cdot k_{12}}{\beta - k_{21}} e^{-\beta t}$$

    Since we are usually most concerned with the concentration in the plasma, we primarily use the first equation, which solves for C_1.

    In the code below we just call this plasma concentration. But we need several parameters in order to plot the concentration-time curve for an IV bolus with 2 compartments. Namely, we need: **D**:dose (mg), **V1** (volume of distribution of the central compartment (L), **alpha** (rate constant alpha (hr^-1), **beta** (rate constant beta (hr^-1) and **k_21** (transfer rate constant from peripheral compartment back to central compartment hr^-1).

    The terms A, B, alpha, and beta are derived during the integration process and are functions of parameters: k12, k21, kel, dose, and V1.

    The macro-constants are based on the values of the micro-constants: kel (sometimes called k10), k12, k21.

    $$\alpha = \frac{(k_{el} + k_{12} + k_{21}) + \sqrt{(k_{el} + k_{12} + k_{21})^2 - 4 \cdot k_{el} \cdot k_{21}}}{2}$$

    and

    $$\beta = \frac{(k_{el} + k_{12} + k_{21}) - \sqrt{(k_{el} + k_{12} + k_{21})^2 - 4 \cdot k_{el} \cdot k_{21}}}{2}$$

    Since:

    $$\alpha + \beta = (k_{el} + k_{21} + k_{12})$$

    And:

    $$\alpha \cdot \beta = k_{el} \cdot k_{21}$$

    These formulae can be greatly simplified.

    The alpha term determines the speed of movement during the initial absorption phase while the beta parameter determines the speed of the elimination phase.

    The other two macro constants are A and B. These can be calculated once **alpha** and **beta** are calculated as above and also using **dose**, **V1** (volume of distribution in central compartment) and the microconstant **k_21**.

    $$A = \frac{D \cdot (\alpha - k_{21})}{V_1 \cdot (\alpha - \beta)}$$

    $$B = \frac{D \cdot (k_{21} - \beta)}{V_1 \cdot (\alpha - \beta)}$$

    The A and B macro-constants determine how high the plasma concentration gets during the initial phase and the elimination phase, respectively.

    # Determining A, B, α and β

    Although we are going from micro-constants to macro-constants here, in reality the macro-constants are regularly determined first because they can be read off the integrated plasma-time curve (Equation 3) by a process of feathering. This is where the plasma-time curve is plotted on semi-logarithmic plot which highlights the two underlying functions. On this plot the change in plasma concentration follows two distinct straight line functions.

    The steeper initial slope corresponds to α (distribution phase), and the shallower terminal slope corresponds to β (elimination phase).

    After determining α and β, the intercepts of these extrapolated lines can be used to calculate A and B.
    """)
    return


@app.cell
def _():
    # Provide micro-rate values
    # Here we use the values for Digoxin for a 70kg normal from Shargel.
    k_el = 0.18
    k_12 = 1.02
    k_21 = 0.15
    # Also provide dose and V1
    D = 3.6 * 70  # Dose in mg
    V1 = 0.78 * 70  # Volume of distribution in central compartment in L
    return D, V1, k_12, k_21, k_el


@app.cell
def _(k_12, k_21, k_el, mo, np):
    # Calculate alpha and beta given the values of the micro-constants.
    # Calculate sum (alpha + beta)
    sum_constants = k_el + k_12 + k_21
    alpha_beta = k_el * k_21
    # Calculate macroconstants alpha and beta
    alpha = (sum_constants + np.sqrt(sum_constants**2 - 4 * alpha_beta)) / 2
    beta = (sum_constants - np.sqrt(sum_constants**2 - 4 * alpha_beta)) / 2
    mo.md(f"Alpha (α): **{alpha:.4f}** hr⁻¹  \nBeta (β): **{beta:.4f}** hr⁻¹")
    return alpha, beta


@app.cell
def _(D, V1, alpha, beta, k_21, mo):
    # Calculate A and B given dose, V1 above, and having calculated alpha and beta.
    A = (D * (alpha - k_21)) / (V1 * (alpha - beta))
    B = (D * (k_21 - beta)) / (V1 * (alpha - beta))
    mo.md(f"A = **{A:.2f}**  \nB = **{B:.2f}**")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Possible values of A, B, alpha, beta that should give a good curve are set as the slider defaults below. Move them to see how each macro-constant shapes the curve.
    """)
    return


@app.cell
def _(mo):
    a_slider = mo.ui.slider(0, 50, step=0.5, value=20, label="A (mg/L)", show_value=True)
    b_slider = mo.ui.slider(0, 50, step=0.5, value=10, label="B (mg/L)", show_value=True)
    alpha_slider = mo.ui.slider(0.1, 10, step=0.1, value=4.1, label="α (hr⁻¹)", show_value=True)
    beta_slider = mo.ui.slider(0.01, 2, step=0.01, value=0.5, label="β (hr⁻¹)", show_value=True)
    mo.vstack([a_slider, b_slider, alpha_slider, beta_slider])
    return a_slider, alpha_slider, b_slider, beta_slider


@app.cell
def _(a_slider, alpha_slider, b_slider, beta_slider, np):
    curve_params = dict(
        A=a_slider.value,
        B=b_slider.value,
        alpha=alpha_slider.value,
        beta=beta_slider.value,
    )

    # Define the function C1(t)
    def C1(t, A, B, alpha, beta):
        return A * np.exp(-alpha * t) + B * np.exp(-beta * t)

    # Create a set of values for t and calculate C1(t) values
    t = np.linspace(0, 24, 200)
    C1_values = C1(t, **curve_params)
    return C1, C1_values, curve_params, t


@app.cell
def _(C1_values, plt, t):
    plt.figure(figsize=(10, 6))
    plt.plot(t, C1_values, label=r"$C(t) = A e^{-\alpha t} + B e^{-\beta t}$", color="blue", linewidth=2)
    plt.title("Concentration-time Curve for Two Compartment Model")
    plt.xlabel("Time (t)")
    plt.ylabel("Concentration (mg/L)")
    plt.grid(True)
    plt.axhline(0, color="black", linewidth=0.5)
    plt.axvline(0, color="black", linewidth=0.5)
    plt.legend()
    plt.tight_layout()
    plt.gca()
    return


@app.cell
def _(C1, curve_params):
    C1(0.1, **curve_params)
    return


@app.cell
def _(C1_values, D, V1, curve_params, mo, plt, t):
    # Now present the plot on a log-linear scale to show deviation from a straight line.
    plt.figure(figsize=(10, 6))
    plt.plot(t, C1_values, label=r"$C(t) = A e^{-\alpha t} + B e^{-\beta t}$", color="blue", linewidth=2)
    plt.yscale("log")
    plt.title("Concentration-time Curve for Two Compartment Model (log-linear)")
    plt.xlabel("Time (t)")
    plt.ylabel("Concentration (mg/L)")
    plt.grid(True)
    plt.axvline(0, color="black", linewidth=0.5)
    plt.legend()
    plt.tight_layout()
    _p = curve_params
    mo.vstack(
        [
            plt.gca(),
            mo.md(
                f"Curve parameters: Dose = {D:.2f}, V1 = {V1:.2f}, A = {_p['A']:.2f}, B = {_p['B']:.2f}, "
                f"alpha = {_p['alpha']:.2f}, beta = {_p['beta']:.2f}"
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    See also: https://www.youtube.com/watch?v=3ygsMD6DMFI&list=PLHZlPdW1nIJXUcE-igQhXuVpsahkgir18&index=9
    """)
    return


if __name__ == "__main__":
    app.run()
