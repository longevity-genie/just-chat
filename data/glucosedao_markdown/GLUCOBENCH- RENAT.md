# GlucoBench: Curated List of Continuous Glucose Monitoring Datasets with Prediction Benchmarks  

Renat Sergazinov1, Elizabeth Chun1, Valeriya Rogovchenko1, Nathaniel Fernandes2, Nicholas Kasman2, Irina Gaynanova1  

1Department of Statistics, 2Department of Electrical and Computer Engineering Texas A&M University  

![](images/682fb1f36d8256af995ae118e5561fbc66ea6077fb569991f42b88320a251dd2.jpg)  

March 25, 2024  

![](images/8d0cc2e035e2809ec8ff793fa37329c52cd3535a107a6f84090b6a5a20388f35.jpg)  

Figure: Sample of glucose curves captured by the Dexcom G4 Continuous Glucose Monitoring (CGM) system, with dates de-identified for privacy [5].  

Table: Summary of the glucose prediction models by dataset and model type.  

![](images/e77ff85e83873a1d1f2e488dc6e7ba659dbc7af966741871ad247ffc78d69e43.jpg)  

# Limitations:  

Lack of Benchmarks: few open datasets, no tasks, no pre-processing tools;   
Open-Source Shortage: 38 out of 45 surveyed methods released code;   
Narrow Focus: exclusion of Type 2 diabetes from the datasets.  

Table: Proposed suite of open datasets.   

![](images/2d95510ac544b864121a1b0fe02baed378835cc53085f6ebd2c48e4d1706622e.jpg)  

# Data Tasks Empirical analysis References Our approach: pre-processing and tasks  

# Systematic pre-processing across datasets:  

Interpolation and Segmentation: linear interpolation or segment division.   
Covariates Scaling and Encoding: scaling and label encoding.   
Data Splitting: chronologically ordered $^+$ out-of-distribution set.  

To create a fair comparison and highlight main dififculties in CGM prediction,we create the following task setup:  

In-distribution fit: for patients in training data;   
Out-distribution fit: for new patients (cold start);   
Inclusion of covariates: support for covariates.  

![](images/d8f3d2ceb0534ca4906afa39495999a5206a22fa06b8991790be3ab59b7c1fa7.jpg)  
Figure: Model forecasts on Weinstock [5] dataset.  

# In-distribution performance  

Table: In-distribution performance.   

![](images/be837f0f854d3cda1318a04cd058c6516c3acd08b0c030edfeb008ca10993605.jpg)  

# ask Empiric Out-of-distribution performance  

Table: with- vs. without-covariates, performance increase and decrease shown.  

![](images/c734f2b4daab9767fccc698417d4b357ed967cd08f0d997e9e2ce64cc20238e5.jpg)  

![](images/735a6e05a8c1e73b954df77c3767f8a4fc9d3f790b8cf9d35e02c88551e8df4d.jpg)  

Figure: Analysis of errors by: (a) OD versus ID, (b) population diabetic type (healthy $\rightarrow$ Type $_2\rightarrow$ Type 1), (c) daytime (9:00AM to 9:00PM) versus nighttime (9:00PM to 9:00AM).  

# Key takeaways:  

Model Performance Variation Factors:  

1 Dataset Size: deep learning models excel on larger datasets. 2 Patient Composition: healthy subjects being easier to predict than those with diabetes. 3 Time of Day: daytime predictions are more challenging. 2 Model Generalizability: 1 Deep learning models generally show better generalization. 2 Performance typically drops on out-of-distribution (OD) data. Impact of Covariates: 1 Integrating covariates is non-trivial, and currently no model is able to take full advantage of covariates.  

[1] S. Broll, J. Urbanek, D. Buchanan, E. Chun, J. Muschelli, N. M. Punjabi, and I. Gaynanova. Interpreting blood glucose data with r package iglu. PloS one, 16(4):e0248560, 2021.  

[2] A. Cola´s, L. Vigil, B. Vargas, D. Cuesta-Frau, and M. Varela. Detrended fluctuation analysis in the prediction of type 2 diabetes mellitus in patients at risk: Model optimization and comparison with other metrics. PloS one, 14(12):e0225817, 2019.  

[3] F. Dubosson, J.-E. Ranvier, S. Bromuri, J.-P. Calbimonte, J. Ruiz, and M. Schumacher. The open d1namo dataset: A multi-modal dataset for research on non-invasive type 1 diabetes management. Informatics in Medicine Unlocked, 13:92–100, 2018.  

[4] H. Hall, D. Perelman, A. Breschi, P. Limcaoco, R. Kellogg, T. McLaughlin, and M. Snyder. Glucotypes reveal new patterns of glucose dysregulation. PLoS biology, 16(7):e2005143, 2018.  

[5] R. S. Weinstock, S. N. DuBose, R. M. Bergenstal, N. S. Chaytor, C. Peterson, B. A. Olson, M. N. Munshi, A. J. Perrin, K. M. Miller, R. W. Beck, et al. Risk factors associated with severe hypoglycemia in older adults with type 1 diabetes. Diabetes Care, 39(4):603–610, 2016.  

# Thank You!  