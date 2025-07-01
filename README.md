# Disturbance Event Generator (DEG) Project Archive

This is an archive of the Disturbance Event Generator (DEG) project. 

## Background

This project, led by Gregory Paradis (at the time a postdoc at UBC), developed a custom software framework capable of generating disturbance event data in the format required for input for the GCBM forest carbon budget modelling framework. At the time, GCBM was quite new and there were no scalable upstream software tools capable of efficiently generating the raster-formatted disturbance event data required by GCBM to run. More specifically, the DEG was designed and implemented to generate GCBM input for a specific BC-wide study, led by the Carbon Accounting Team at the Canadian Forest Service (Smyth et al., 2020).

The DEG framework is built on top of ws3, which was upgraded to include new Model LP optimization modelling functions in this project. See Paradis (2018) for technical documentation describing DEG design and implementation. 

## References

Paradis, G. (2018). DEG : A Disturbance Event Generator for GCBM. Whitepaper. University of British Columbia.
[DOI](https://dx.doi.org/10.14288/1.0402620)

Smyth, C. E., Xu, Z., Lemprière, T. C., & Kurz, W. A. (2020). Climate change mitigation in British Columbia’s forest sector: GHG reductions, costs, and environmental impacts. Carbon balance and management, 15, 1-22.
[DOI](https://doi.org/10.1186/s13021-020-00155-2)