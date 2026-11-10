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
    from scipy.integrate import odeint

    return mo, np, odeint, plt


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Zero-Order Elimination Plasma-time Curve
    `Page by Dr Slade Matthews, The University of Sydney, 2023`
    · converted to marimo from the [original Colab notebook](https://github.com/sladem-tox/PK_calcs/blob/main/ZeroOrderElimination.ipynb)

    Zero-order elimination can be described using an ordinary differential equation (ODE):

    $$\frac{dC}{dt} = -\frac{V_m \cdot C_p}{K_m + C_p}$$

    This behaviour is called Michaelis-Menten kinetics which was originally used to describe enzyme kinetics. The rate of enzymatic degradation of a substrate by an enzyme has some maximum, Vmax which along with Km (concentration at which rate = 1/2 Vmax) can be used to describe the dynamics of the enzyme reaction. Since enzymes and transporters important to drug disposition can be saturated the same formula can be useful in pharmacokinetics.

    This situation could arise with drugs such as alcohol where at most 10 grams can be eliminated from the body per hour (at Vmax). Another estimate (See **Holford, 1987**) describes the Vmax as 8.5 g/h/70kg which equates to a plasma elimination rate of 230 mg/L/h.  The Km for alcohol is around 0.01 % (g/100mL) so we are halfway to Vmax at this concentration. For calculation purposes we will use the value 80 mg/L (just below the 100 mg/L estimated in Burkett) as the Km as described in Holford 1987.

    Some other drugs such as phenytoin also display saturated elimination kinetics (see Chapter 9: Non-linear Pharmacokinetics *in* **Pharmacokinetics Made Easy** by Donald Burkett).

    *Holford, N., Clinical Pharmacokinetics of Ethanol. Clinical Pharmacokinetics, 1987. 13: p. 273-292.*

    ---

    Below we require values for C0, Vm, and Km.
    """)
    return


@app.cell
def _(mo):
    # Initial conditions for IV dosing. Conc at t=0, Vmax and Km
    c0_slider = mo.ui.slider(10, 1000, step=10, value=500, label="C0 (mg/L)", show_value=True)
    vm_slider = mo.ui.slider(10, 500, step=10, value=230, label="Vm (mg/L/h)", show_value=True)
    km_slider = mo.ui.slider(1, 500, step=1, value=80, label="Km (mg/L)", show_value=True)
    mo.vstack([c0_slider, vm_slider, km_slider])
    return c0_slider, km_slider, vm_slider


@app.cell
def _(c0_slider, km_slider, np, odeint, plt, vm_slider):
    # Define the Michaelis-Menten equation based here on a saturable elimination pathway.
    def decay_model(C, t, Vm, km):
        dCdt = -Vm * C / (km + C)
        return dCdt

    C0 = c0_slider.value  # Initial concentration (mg/L)
    Vm = vm_slider.value  # Maximum rate of decay (mg/L/h)
    km = km_slider.value  # C value at which decay is half Vm (mg/L)

    # Generate a series of timepoints with linspace.
    t = np.linspace(0, 10, 100)

    # Solve the ordinary differential equation (ODE) using scipy.
    # The ODE does not have a simple solution and must be integrated to find y values at time t.
    C = odeint(decay_model, C0, t, args=(Vm, km))

    plt.figure(figsize=(10, 5))
    plt.plot(t, C)
    plt.xlabel("Time (h)")
    plt.ylabel("Plasma Concentration (mg/L)")
    plt.title("Plasma-time Curve Showing Saturable Elimination Kinetics")
    plt.gca()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Why is it called ***zero order***?

    In chemistry the rate of a chemical process is often written as:

    $Rate = k \cdot [C]^n$

    where k = rate constant, [C] = concentration, and "n" is the **order of the reaction** with respect to concentration.

    In our first example we looked at single IV dose with the equation:

    $C_t = C_0 \cdot e^{-kt}$

    which was the analytical solution for the differential equation:

    $\frac{dC}{dt} = -kC$

    Here n = 1 and the rate depends linearly on concentration.

    When elimination is zero-order, n = 0.

    $\frac{dC}{dt} = -k$

    because n = 0 then $-kC^0 = -k$ and the rate is no longer proportional to concentration.

    This happens when the concentration is much higher than $K_m$.

    In Michaelis-Menten kinetics:

    $$\frac{dC}{dt} = -\frac{V_m \cdot C_p}{K_m + C_p}$$

    At low concentrations C << $K_m$, so

    $$v \text{ (reaction velocity)} \approx \frac{V_{max}}{K_m}\cdot C$$

    and elimination is "first order" as it is proportional to C.

    At high concentrations:

    C >> $K_m$, so

    $$v \approx V_{max}$$

    and elimination is zero-order (independent of C).
    """)
    return


if __name__ == "__main__":
    app.run()
