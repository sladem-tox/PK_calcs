# PK_calcs
[Pharmacokinetic Calculations in Python](https://sladem-tox.github.io/PK_calcs/)
    *by Dr Slade Matthews, 2023, The University of Sydney*


## Single IV Dosing
The simplest model is of first order elimination following a single IV dose since we only have to consider the elimination process and we start with all the drug in the blood. There are many assumptions in all PK models and it is good to keep that in mind. You may ask "How is it possible that a given drug is guaranteed to behave in this way?" and you'd be right! There are many variables to consider. Gut metabolism, proportion of the molecule in salt form, hepatic extraction ratio. But for now, start with the single IV dose and you will begin to understand the most critical relationships between PK parameters used in drug design and clinical descision making.

![Single IV Dose Curve](docs/assets/img/SingleIV_curve.png)

**Click the "Open in Colab"** button below to open an easy to use Python-based implementation of the single IV dose plasma-time curve formula. Here you will be able to change the parameters of the single IV plasma-time curve and see how they change the curve behavior.

<a href="https://colab.research.google.com/github/sladem-tox/PK_calcs/blob/main/PlasmaTime_SingleIV.ipynb" target="_blank">
    <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab" style="width: 200px; height: auto;">
</a>

## Oral Dosing Plasma-time Curve
After a while thinking deeply about the single IV plasma-time curve you will be ready to think about the more general but more complicated single oral dose plasma-time curve. This introduces another variable which is the absorption rate constant but it is still a relatively simple situation since we are not looking at multiple doses or considering other factors affecting drug disposition.

![Single Oral Dose Curve](docs/assets/img/SingleOralDose.png)

**Click the "Open in Colab"** button below to open an easy to use Python-based implementation of the Single Oral dose plasma-time curve formula. Here you will be able to change the parameters of the Single Oral dose plasma-time curve and see how they change the curve behavior.

<a href="https://colab.research.google.com/github/sladem-tox/PK_calcs/blob/main/SingleOralDose.ipynb" target="_blank">
    <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab" style="width: 200px; height: auto;">
</a>


## Intravenous Infusion and Effect of Clearance
In these IV infusion cruves you can see the effect of different values of clearance on the steady state concentration of a drug. So drugs that have different clearance values that are dosed at the same mg/hour dose rate will settle at different steady state concentrations.

![Intravenous Infusion Curves](docs/assets/img/IV_infusion.png)

**Click the "Open in Colab"** button below to open an easy to use Python-based implementation of intravenous infusion curves. In the image above all the dose rates in mg/h are the same and only the clearance values are changed illustrating the dependence of steady-state concentration on clearance.

<a href="https://colab.research.google.com/github/sladem-tox/PK_calcs/blob/main/Infusion_curves.ipynb" target="_blank">
    <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab" style="width: 200px; height: auto;">
</a>

## Non-linear Pharmacokinetics - Zero Order Elimination with Pathway Saturation
This curve shows what happens when the elimination pathway is saturated initially and then, when to plasma concentration sinks low enough, the elimination returns to first order and starts to slow down. Notice that the curve is linear and then exponential at the end. So the elimination rate is constant at the begining, irrespective of plasma concentration. Then, in the last part of the curve, the elimination rate is proportional to plasma concentration. For simplicity we start with the drug at some concentration at time=0 but if we were considering an oral dose the situation would be far more complicated!

![Zero Order Elimination](docs/assets/img/NonLinearPK.png)

**Click the "Open in Colab"** button below to open an easy to use Python-based illustration of zero order elimination which changes to first order elimination when the concentration drops to below a threshold value.

<a href="https://colab.research.google.com/github/sladem-tox/PK_calcs/blob/main/ZeroOrderElimination.ipynb" target="_blank">
    <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab" style="width: 200px; height: auto;">
</a>

## Multiple Oral Dosing
Finally we consider multiple oral dosing. This is a much more difficult thing to work with because there are several variables to consider when plotting the resultant plasma-time curve. In the example below the equation for multiple oral dosing is used taking into account the regular dosing interval and deriving from that which dose number in the series we are up to at any given time-point.

![Multiple Oral Dosing](docs/assets/img/MultipleOralDose.png)

**Click the "Open in Colab"** button below to open an easy to use Python-based implementation of the multiple oral dosing curve. Here you can look at the effects of changes in dose and dose interval to the plasma curve. You can also see how long it takes for the plasma level to reach steady-state where the tops and bottoms of the plasma-time curves all land at the same y-axis value.

<a href="https://colab.research.google.com/github/sladem-tox/PK_calcs/blob/main/MultipleOralDose.ipynb" target="_blank">
    <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab" style="width: 200px; height: auto;">
</a>

<p>
<li></li>
<img src="qrcode_sladem-tox.github.io.png" alt="QRcode" width="600" height="600">
</p>


