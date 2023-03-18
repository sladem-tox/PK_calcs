# PK_calcs
PK calculations in Python

The simplest model is of first order elimination following a single IV dose since we only have to consider the elimination process and we start with all the drug in the blood. There are many assumptions in all PK models and it is good to keep that in mind. You may ask "How is it possible that a given drug is guaranteed to behave in this way?" and you'd be right! There are many variables to consider. Gut metabolism, proportion of the molecule in salt form, hepatic extraction ratio. But for now, start with the single IV dose and you will begin to understand the most critical relationships between PK parameters used in drug design and clinical descision making.

[Single IV Dosing](PlasmaTime_SingleIV.ipynb)

After a while thinking deeply about the single IV plasma-time curve you will be ready to think about the more general but more complicated single oral dose plasma-time curve. This is the simplest situation since you can then introduce multiple doses and also consider other factors affecting drug disposition.
Here is the basic [oral plasma-time curve](SingleOralDose.ipynb)
