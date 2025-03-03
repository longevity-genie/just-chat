# GLUCOBENCH: CURATED LIST OF CONTINUOUS GLUCOSE MONITORING DATASETS WITH PREDICTION BENCHMARKS  

Renat Sergazinov1,∗ Elizabeth $\mathbf{Chun^{1}}$ , Valeriya Rogovchenko1, Nathaniel Fernandes2, Nicholas Kasman2, Irina Gaynanova1∗  

1Department of Statistics, Texas A&M University   
2Department of Electrical and Computer Engineering, Texas A&M University  

# ABSTRACT  

The rising rates of diabetes necessitate innovative methods for its management. Continuous glucose monitors (CGM) are small medical devices that measure blood glucose levels at regular intervals providing insights into daily patterns of glucose variation. Forecasting of glucose trajectories based on CGM data holds the potential to substantially improve diabetes management, by both refining artificial pancreas systems and enabling individuals to make adjustments based on predictions to maintain optimal glycemic range. Despite numerous methods proposed for CGMbased glucose trajectory prediction, these methods are typically evaluated on small, private datasets, impeding reproducibility, further research, and practical adoption. The absence of standardized prediction tasks and systematic comparisons between methods has led to uncoordinated research efforts, obstructing the identification of optimal tools for tackling specific challenges. As a result, only a limited number of prediction methods have been implemented in clinical practice.  

To address these challenges, we present a comprehensive resource that provides (1) a consolidated repository of curated publicly available CGM datasets to foster reproducibility and accessibility; (2) a standardized task list to unify research objectives and facilitate coordinated efforts; (3) a set of benchmark models with established baseline performance, enabling the research community to objectively gauge new methods’ efficacy; and (4) a detailed analysis of performance-influencing factors for model development. We anticipate these resources to propel collaborative research endeavors in the critical domain of CGM-based glucose predictions. Our code is available online at github.com/IrinaStatsLab/GlucoBench.  

# 1 INTRODUCTION  

According to the International Diabetes Federation, 463 million adults worldwide have diabetes with 34.2 million people affected in the United States alone (IDF, 2021). Diabetes is a leading cause of heart disease (Nanayakkara et al., 2021), blindness (Wykoff et al., 2021), and kidney disease (Alicic et al., 2017). Glucose management is a critical component of diabetes care, however achieving target glucose levels is difficult due to multiple factors that affect glucose fluctuations, e.g., diet, exercise, stress, medications, and individual physiological variations.  

Continuous glucose monitors (CGM) are medical devices that measure blood glucose levels at frequent intervals, often with a granularity of approximately one minute. CGMs have great potential to improve diabetes management by furnishing real-time feedback to patients and by enabling an autonomous artificial pancreas (AP) system when paired with an insulin pump (Contreras & Vehi, 2018; Kim & Yoon, 2020). Figure 1 illustrates an example of a CGM-human feedback loop in a recommender setting. The full realization of CGM potential, however, requires accurate glucose prediction models. Although numerous prediction models (Fox et al., 2018; Armandpour et al., 2021; Sergazinov et al., 2023) have been proposed, only simple physiological (Bergman et al., 1979; Hovorka et al., 2004) or statistical (Oviedo et al., 2017; Mirshekarian et al., 2019; Xie & Wang,  

![](images/91afc36a148b311121efbd9f4a58813d173d4a03ef9365dd51e5fc029998ef68.jpg)  
Figure 1: Sample of glucose curves captured by the Dexcom G4 Continuous Glucose Monitoring (CGM) system, with dates de-identified for privacy(Weinstock et al., 2016).  

2020) models are utilized within current CGM and AP software. The absence of systematic model evaluation protocols and established benchmark datasets hinder the analysis of more complex models’ risks and benefits, leading to their limited practical adoption (Mirshekarian et al., 2019).  

In response, we present a curated list of five public CGM datasets and a systematic protocol for models’ evaluation and benchmarking. The selected datasets have varying sizes and demographic characteristics, while the developed systematic data-preprocessing pipeline facilitates the inclusion of additional datasets. We propose two tasks: (1) enhancing the predictive accuracy; (2) improving the uncertainty quantification (distributional fti) associated with predictions. In line with previous works (Mirshekarian et al., 2019; Xie & Wang, 2020), we measure the performance on the first task with mean squared error (MSE) and mean absolute error (MAE), and on the second task with likelihood and expected calibration error (ECE) (Kuleshov et al., 2018). For each task, we train and evaluate a set of baseline models. From data-driven models, we select linear regression and ARIMA to represent shallow baselines, and Transformer (Vaswani et al., 2017), NHiTS (Challu et al., 2023), TFT (Lim et al., 2021), and Gluformer (Sergazinov et al., 2023) to represent deep learning baselines. We select the Latent ODE (Rubanova et al., 2019) to represent a hybrid data-driven / physiological model.  

Our work contributes a curated collection of diverse CGM datasets, formulation of two tasks focused on model accuracy and uncertainty quantification, an efficient benchmarking protocol, evaluation of a range of baseline models including shallow, deep and hybrid methods, and a detailed analysis of performance-influencing factors for model optimization.  

# 2 RELATED WORKS  

An extensive review of glucose prediction models and their utility is provided by Oviedo et al. (2017); Contreras & Vehi (2018); Kim & Yoon (2020); Kavakiotis et al. (2017). Following Oviedo et al. (2017), we categorize prediction models as physiological, data-driven, or hybrid. Physiological models rely on the mathematical formulation of the dynamics of insulin and glucose metabolism via differential equations (Man et al., 2014; Lehmann & Deutsch, 1991). A significant limitation of these models is the necessity to pre-define numerous parameters. Data-driven models rely solely on the CGM data (and additional covariates when available) to characterize glucose trajectory without incorporating physiological dynamics. These models can be further subdivided into shallow (e.g. linear regression, ARIMA, random forest, etc.) and deep learning models (e.g. recurrent neural network models, Transformer, etc.). Data-driven models, despite their capacity to capture complex  

Table 1: Summary of the glucose prediction models by dataset and model type. We indicate ”open” for datasets that are publicly available online, ”simulation” for the ones based on simulated data, ”proprietary” for the ones that cannot be released. We indicate deep learning models by ”deep”, non-deep learning models by ”shallow”, and physiological models by ”physiological.” We provide full table with references to all the works in Appendix A.  

![](images/96308a0dcd22ae54d473bf8a8a78d63fcc60c9096d394e02624558ea0e62990a.jpg)  

patterns, may suffer from overfitting and lack interpretability. Hybrid models use physiological models as a pre-processing or data augmentation tool for data-driven models. Hybrid models enhance the flexibility of physiological models and facilitate the fitting process, albeit at the expense of diminished interpretability. Table 1 summarizes existing models and datasets, indicating model type.  

Limitations. The present state of the field is characterized by several key constraints, including (1) an absence of well-defined benchmark datasets and studies, (2) a dearth of open-source code bases, and (3) omission of Type 2 diabetes from most open CGM studies. To address the second limitation, two benchmark studies have been undertaken to assess the predictive performance of various models (Mirshekarian et al., 2019; Xie & Wang, 2020). Nonetheless, these studies only evaluated the models on one dataset (Marling & Bunescu, 2020), comprising a limited sample of 5 patients with Type 1 diabetes, and failed to provide source code. We emphasize that, among the 45 methods identified in Table 1, a staggering 38 works do not offer publicly available implementations. For the limitation (3), it is important to recognize that Type 2 is more easily managed through lifestyle change and oral medications than Type 1 which requires lifelong insulin therapy.  

# 3 DATA  

# 3.1 DESCRIPTION  

We have selected five publicly available CGM datasets: Broll et al. (2021); Col´as et al. (2019);   
Dubosson et al. (2018); Hall et al. (2018); Weinstock et al. (2016).  

To ensure data quality, we used the following set of criteria. First, we included a variety of dataset sizes and verified that each dataset has measurements on at least 5 subjects and that the collection includes a variety of sizes ranging from only five (Broll et al., 2021) to over 200 (Cola´s et al., 2019; Weinstock et al., 2016) patients. On the patient level, we ensured that each subject has non-missing CGM measurements for at least 16 consecutive hours. At the CGM curve level, we have verified that measurements fall within a clinically relevant range of $20\;\mathrm{mg/dL}$ to $400\:\mathrm{mg/dL}$ , avoiding drastic fluctuations exceeding $40~\mathrm{mg/dL}$ within a 5-minute interval, and ensuring non-constant values.  

Finally, we ensured that the collection covers distinct population groups representing subjects with Type 1 diabetes (Dubosson et al., 2018; Weinstock et al., 2016), Type 2 diabetes (Broll et al., 2021), or a mix of Type 2 and none (Col´as et al., 2019; Hall et al., 2018). We expect that the difficulty of accurate predictions will depend on the population group: patients with Type 1 have significantly larger and more frequent glucose fluctuatons. Table 2 summarizes all five datasets with associated demographic information, where some subjects are removed due to data quality issues as a result of pre-processing (Section 3.2). We describe data availability in Appendix A.  

Covariates. In addition to CGM data, each dataset has covariates (features), which we categorize based on their temporal structure and input type. The temporal structure distinguishes covariates as static (e.g. gender), dynamic known (e.g. hour, minute), and dynamic unknown (e.g. heart beat, blood pressure). Furthermore, input types define covariates as either real-valued (e.g. age) or ordinal (e.g. education level) and categorical or unordered (e.g. gender) variables. We illustrate different types of temporal variables in Figure 2. We summarize covariate types for each dataset in Appendix A.  

Table 2: Demographic information (average) for each dataset before (Raw) and after pre-processing (Processed). CGM indicates the device type; all devices have 5 minute measurment frequency.   

![](images/c79a2460de1c832a26fc7dd7a7991bc8b1a69f1a916520782282e041cef23a2b.jpg)  

![](images/1ea2601be0b08dc129e2e855fca5ee2f547d0fe0305baf3001fecceabfb2c53b.jpg)  
Figure 2: An illustration of static (Age), dynamic known (Date), and dynamic unknown (Heart Rate) covariate categories based on data from Hall et al. (2018) and Dubosson et al. (2018).  

Table 3: Interpolation parameters for datasets.   

![](images/d57062a594d9c3418b1dd9e667dfc54633005909d8925e5668ccb14a6b7a96ef.jpg)  

# 3.2 PRE-PROCESSING  

We pre-process the raw CGM data via interpolation and segmentation, encoding categorical features, data partitioning, scaling, and division into input-output pairs for training a predictive model.  

Interpolation and segmentation. To put glucose values on a uniform temporal grid, we identify gaps in each subject’s trajectory due to missing measurements. When the gap length is less than a predetermined threshold (Table 3), we impute the missing values by linear interpolation. When the gap length exceeds the threshold, we break the trajectory into several continuous segments. Green squares in Figure 3 indicate gaps that will be interpolated, whereas red arrows indicate larger gaps where the data will be broken into separate segments. In Dubosson et al. (2018) dataset, we also interpolate missing values in dynamic covariates (e.g., heart rate). Thus, for each dataset we obtain a list of CGM sequences $\mathcal{D}=\big\{\mathbf{x}_{j}^{(i)}\big\}_{i,j}$ with $i$ indexing the patients and $j$ the continuous segments. Each segment $\mathbf{x}_{j}^{(i)}$ has length $L_{j}^{(i)}>L_{m i n}$ , where $L_{m i n}$ is the pre-specified minimal value (Table 3).  

Covariates Encoding. While many of the covariates are real-valued, e.g., age, some covariates are categorical, e.g., sex. In particular, Weinstock et al. (2016) dataset has 36 categorical covariates with an average of 10 levels per covariate. While one-hot encoding is a popular approach for modeling categorical covariates, it will lead to 360 feature columns on Weinstock et al. (2016), making it undesirable from model training time and memory perspectives. Instead, we use label encoding by converting each categorical level into a numerical value. Given $R$ covariates, we include them in the dataset as $\mathcal{D}=\{\mathbf{x}_{j}^{(i)},\mathbf{c}_{1,j}^{(i)},\ldots\mathbf{c}_{R,j}^{(i)}\}_{i,j}$ where $\mathbf{c}_{r,j}^{(i)}\in\mathbb{R}$ for static and $\mathbf{c}_{r,j}^{(i)}\in\mathbb{R}^{L_{j}^{(i)}}$ for dynamic.  

Data splitting. Each dataset is split into train, validation, and in-distribution (ID) test sets using $90\%$ of subjects. For each subject, the sets follow chronological time order as shown in Figure 3, with validation and ID test sets always being of a fixed length of 16 hours each (192 measurements). The data from the remaining $10\%$ of subjects is used to form an out-of-distribution (OD) test set to assess the generalization abilities of predictive models as in Section 5.2. Thus, $\mathcal{D}=\mathcal{D}_{t r}\cup\mathcal{D}_{v a l}\cup\mathcal{D}_{i d}\cup\mathcal{D}_{o d}$ .  

![](images/aeda2f60b67077e7cedf7088463c32acaa54965c64249a7bb70c5ff7f1a23019.jpg)  
Figure 3: Example data processing on Weinstock et al. (2016). The red arrows denote segmentation, green blocks interpolate values, and red brackets indicate dropped segments due to length.  

Scaling. We use min-max scaling to standardize the measurement range for both glucose values and covariates. The minimum and maximum values are computed per dataset using $\mathcal{D}_{t r}$ , and then the same values are used to rescale $\mathcal{D}_{v a l}$ , $\mathcal{D}_{i d}$ , and $\mathcal{D}_{o d}$ .  

Input-output pairs. Let $\mathbf{x}_{j,k:k+L}^{(i)}$ be a length $L$ contiguous slice of a segment from index $k$ to $k+L$ . We define an input-output pair as $\{\mathbf{x}_{j,k:k+L}^{(i)},\mathbf{y}_{j,k+L+1:k+L+T}^{(i)}\}$ , where $\mathbf{y}_{j,k+L+1:k+L+T}^{(i)}=$ x(j,i)k+L+1:k+L+T and T is the length of prediction interval. Our choices of T, L and k are as follows. In line with the previous works (Oviedo et al., 2017) we focus on the 1-hour ahead forecasting $T=12$ for 5 minute frequency). We treat $L$ as a hyper-parameter for model optimization since different models have different capabilities in capturing long-term dependencies. We sample $k$ without replacement from among the index set of the segment during training, similar to Oreshkin et al. (2020); Challu et al. (2023), and treat the total number of samples as a model hyper-parameter. We found the sampling approach to be preferable over the use of a sliding window with a unit stride (Herzen et al., 2022), as the latter is computationally prohibitive on larger training datasets and leads to high between-sample correlation, slowing convergence in optimization. We still use the sliding window when evaluating the model on the test set.  

# 4 BENCHMARKS  

# 4.1 TASKS AND METRICS  

Task 1: Predictive Accuracy. Given the model prediction $\hat{\mathbf{y}}_{j,k+L:k+L+T}$ , we measure accuracy on the test set using root mean squared error (RMSE) and mean absolute error (MAE):  

$$
R M S E_{i,j,k}=\sqrt{\frac{1}{T}\sum_{t=1}^{T}\left(y_{j,k+L+t}^{(i)}-\hat{y}_{j,k+L+t}^{(i)}\right)^{2}};\quad M A E_{i,j,k}=\frac{1}{T}\sum_{t=1}^{T}\left|y_{j,k+L+t}^{(i)}-\hat{y}_{j,k+L+t}^{(i)}\right|.
$$  

Since the distribution of MAE and RMSE across samples is right-skewed, we use the median of the errors as has been done in Sergazinov et al. (2023); Armandpour et al. (2021).  

Task 2: Uncertainty Quantification. To measure the quality of uncertainty quantification, we use two metrics: log-likelihood on test data and calibration. For models that estimate a parametric predictive distribution over the future values, Pˆ j(,ik)+ $\hat{P}_{j,k+L+1:k+L+T}^{(i)}:\mathbb{R}^{T}\rightarrow[0,1]$ , we evaluate log-likelihood as  

$$
\log L_{i,j,k}=\log\hat{P}_{j,k+L+1:k+L+T}^{(i)}\left(\mathbf{y}_{j,k+L+1:k+L+T}^{(i)}\right),
$$  

where the parameters of the distribution are learned from training data, and the likelihood is evaluated on test data. Higher values indicate a better fit to the observed distribution. For both parametric and non-parametric models (such as quantile-based methods), we use regression calibration metric (Kuleshov et al., 2018). The original metric is limited only to the univariate distributions. To address the issue, we report an average calibration across marginal estimates for each time $t=1,\dots,T$ . To compute marginal calibration at time $t$ , we (1) pick $M$ target confidence levels $0<p_{1}<\cdot\cdot<$ $p_{M}<1$ ; (2) estimate realized confidence level $\hat{p}_{m}$ using $N$ test input-output pairs as  

$$
\hat{p}_{m}=\frac{\left|\left\{y_{j,k+L+t}^{(i)}|\hat{F}_{j,k+L+t}^{(i)}\left(y_{j,k+L+t}^{(i)}\right)\le p_{m}\right\}\right|}{N};
$$  

and (3) compute calibration across all $M$ levels as  

$$
C a l_{t}=\sum_{1}^{M}(p_{m}-\hat{p}_{m})^{2}.
$$  

The smaller the calibration value, the better the match between the estimated and true levels.  

# 4.2 MODELS  

To benchmark the performance on the two tasks, we compare the following models. ARIMA is a classical time-series model, which has been previously used for glucose predictions (Otoom et al., 2015; Yang et al., 2019). Linear regression is a simple baseline with a separate model for each time step $t=1,\dots,T$ . XGBoost (Chen & Guestrin, 2016) is gradient-boosted tree method, with a separate model for each time step $t$ to support multi-output regression. Transformer represents a standard encoder-decoder auto-regressive Transformer implementation (Vaswani et al., 2017). Temporal Fusion Transformer (TFT) is a quantile-based model that uses RNN with attention. TFT is the only model that offers out-of-the-box support for static, dynamic known, and dynamic unknown covariates. NHiTS uses neural hierarchical interpolation for time series, focusing on the frequency domain (Challu et al., 2023). Latent ODE uses a recurrent neural network (RNN) to encode the sequence to a latent representation (Rubanova et al., 2019). The dynamics in the latent space are captured with another RNN with hidden state transitions modeled as an ODE. Finally, a generative model maps the latent space back to the original space. Gluformer is a probabilistic Transformer model that models forecasts using a mixture distribution (Sergazinov et al., 2023). For ARIMA, we use the code from (Federico Garza, 2022) which implements the algorithm from (Hyndman & Khandakar, 2008). For linear regression, XGBoost, TFT, and NHiTS, we use the open-source DARTS library (Herzen et al., 2022). For Latent ODE and Gluformer, we use the implementation in PyTorch (Rubanova et al., 2019; Sergazinov et al., 2023). We report the compute resources in Appendix C.  

# 4.3 TESTING PROTOCOLS  

In devising the experiments, we pursue the principles of reproducibility and fairness to all methods.  

Reproducibility. As the performance results are data split dependent, we train and evaluate each model using the same two random splits. Additionally, all stochastically-trained models (tree-based and deep learning) are initialized 10 times on each training set with different random seeds. Thus, each stochastically-trained model is re-trained and re-evaluated 20 times, and each deterministicallytrained model 2 times, with the final performance score taken as an average across evaluations. We report standard error of each metric across the re-runs in Appendix B.  

Fairness. To promote fairness and limit the scope of comparisons, we focus on out-of-the-box model performance when establishing baselines. Thus, we do not consider additional model-specific tuning that could lead to performance improvements, e.g., pre-training, additional loss functions, data augmentation, distillation, learning rate warm-up, learning rate decay, etc. However, since model hyper-parameters can significantly affect performance, we automate the selection of these parameters. For ARIMA, we use the native automatic hyper-parameter selection algorithm provided in (Hyndman & Khandakar, 2008). For all other models, we use Optuna (Akiba et al., 2019) to run Bayesian optimization with a fixed budget of 50 iterations. We provide a discussion on the selected optimal model hyperparameters for each dataset in the supplement (Appendix C).  

![](images/95fdd88753996e74c0751eb11dc5f362dd1924ecdd9081f121b962b08d8adb13.jpg)  
Figure 4: Analysis of errors by: (a) OD versus ID, (b) population diabetic type (healthy $\rightarrow$ Type $2\rightarrow$ Type 1), (c) daytime (9:00AM to 9:00PM) versus nighttime (9:00PM to 9:00AM).  

Table 4: Accuracy and uncertainty metrics for selected models based on in-distribution (ID) test set without covariates. The selected models are best on at least one dataset for at least one metric. The best results on each data set are highlighted in boldface. TFT lacks likelihood information as it is a quantile-based model. Standard errors are reported in Appendix B.  

![](images/eaa72414dce094867ae2b9912287fb19c9876278ed65dc55c0f5cad12f6373a7.jpg)  

# 4.4 RESULTS  

We trained and tested each model outlined above on all five datasets using the established protocols. Table 4 present the results for the best-performing models on Task 1 (predictive accuracy) and Task 2 (uncertainty quantification). Appendix B includes full tables for all models together with standard errors and the visualized forecasts for the best models on (Weinstock et al., 2016) dataset.  

On Task 1, the simple ARIMA and linear regression models have the highest accuracy on all but two datasets. On Hall et al. (2018) dataset (mixed subjects including normoglycemic, prediabetes and Type 2 diabetes), the Latent ODE model performs the best. On Weinstock et al. (2016) dataset (the largest dataset), the Transformer model performs the best.  

On Task 2, Gluformer model achieves superior performance as measured by model likelihood on all datasets. In regards to calibration, Gluformer is best on all but two datasets. On Col´as et al. (2019) and Weinstock et al. (2016) datasets (the largest datasets), the best calibration is achieved by TFT.  

# 5 ANALYSIS  

# 5.1 WHY DOES THE PERFORMANCE OF THE MODELS DIFFER BETWEEN THE DATASETS?  

Three factors consistently impact the results across the datasets and model configurations: (1) dataset size, (2) patients’ composition, and (3) time of day. Below we discuss the effects of these factors on accuracy (Task 1), similar observations hold for uncertainty quantification (Task 2).  

Tables 4 indicates that the best-performing model on each dataset is dependent on the dataset size. For smaller datasets, such as Broll et al. (2021) and Dubosson et al. (2018), simple models like ARIMA and linear regression yield the best results. In general, we see that deep learning models excel on larger datasets: Hall et al. (2018) (best model is Latent ODE) and Weinstock et al. (2016) (best model is Transformer) are 2 of the largest datasets. The only exception is Cola´s et al. (2019), on which the best model is linear regression. We suggest that this could be explained by the fact that despite being large, Cola´s et al. (2019) dataset has low number observations per patient: 100,000 glucose readings across 200 patients yeilds 500 readings or 2 days worth of data per patient. In comparison, Hall et al. (2018) has 2,000 readings per patient or 7 days, and Weinstock et al. (2016) has approximately 3,000 readings per patient or 10 days.  

Table 5: Change in accuracy and uncertainty tasks between ID and OD sets. We indicate increases in performance in blue and decreases in red. TFT lacks likelihood information as it is a quantile-based model.   

![](images/25ee2ca9cfb3d1cfd91b5423f1e3d8f2f1026929f789f12b1e4947a18e1c5b99.jpg)  

Table 6: Changes in accuracy and uncertainty tasks with and without covariates on ID test set. We indicate increases in performance in blue and decreases in red. TFT lacks likelihood information as it is a quantile-based model.   

![](images/b1123f1728af76229fbae34f065eb1579d00c661afdd2b8be349426dadf9f33d.jpg)  

Figure 4(b) demonstrates that the accuracy of predictions is substantially influenced by the patients’ population group. Healthy subjects demonstrate markedly smaller errors compared to subjects with Type 1 or Type 2 diabetes. This discrepancy is due to healthy subjects maintaining a narrower range of relatively low glucose level, simplifying forecasting. Patients with Type 1 exhibit larger fluctuations partly due to consistently required insulin administration in addition to lifestyle-related factors, whereas most patients with Type 2 are not on insulin therapy.  

Figure 4(c) shows the impact of time of day on accuracy, with daytime (defined as 9:00AM to 9:00PM) being compared to nighttime for Transformer model on Broll et al. (2021) dataset. The distribution of daytime errors is more right-skewed and right-shifted compared to the distribution of nighttime errors, signifying that daytime glucose values are harder to predict. Intuitively, glucose values are less variable overnight due to the absence of food intake and exercise, simplifying forecasting. We include similar plots for all models and datasets in Appendix B. This finding underscores the importance of accounting for daytime and nighttime when partitioning CGM data for model training and evaluation.  

Overall, we recommend using simpler shallow models when data is limited, the population group exhibits less complex CGM proflies (such as healthy individuals or Type 2 patients), or for nighttime forecasting. Conversely, when dealing with larger and more complex datasets, deep or hybrid models are the preferred choice. In clinical scenarios where data is actively collected, it is advisable to deploy simpler models during the initial stages and, in later stages, maintain an ensemble of both shallow and deep models. The former can act as a guardrail or be used for nighttime predictions.  

# 5.2 ARE THE MODELS GENERALIZABLE TO PATIENTS BEYOND THE TRAINING DATASET?  

Table 5 compares accuracy and uncertainty quantification of selected models on in-distribution (ID) and out-of-distribution (OD) test sets, while the full table is provided in Appendix B. Here we assume that each patient is different, in that the OD set represents a distinct distribution from the ID set.  

In both tasks, most models exhibit decreased performance on the OD data, emphasizing individuallevel variation between patients and the difficulty of cold starts on new patient populations. Figure 4(a) displays OD-to-ID accuracy ratio (measured in MAE) for each model and dataset: higher ratios indicate poorer generalization, while lower ratios indicate better generalization. In general, we observe that deep learning models (Transformer, NHiTS, TFT, Gluformer, and Latent ODE) generalize considerably better than the simple baselines (ARIMA and linear regression). We attribute this to the deep learning models’ ability to capture and recall more patterns from the data. Notably, XGBoost also demonstrates strong generalization capabilities and, in some instances, outperforms the deep learning models in the generalization power.  

# 5.3 HOW DOES ADDING THE COVARIATES AFFECT THE MODELING QUALITY?  

Table 6 demonstrates the impact of including covariates in the models on Task 1 (accuracy) and Task 2 (uncertainty quantification) compared to the same models with no covariates. As the inclusion of covariates represents providing model with more information, any changes in performance can be attributed to (1) the quality of the covariate data; (2) model’s ability to handle multiple covariates. We omit ARIMA, Gluformer, and Latent ODE models as their implementations do not support covariates.  

In both tasks, the impact of covariates on model performance varies depending on the dataset. For Cola´s et al. (2019) and Dubosson et al. (2018), we observe a decrease in both accuracy and uncertainty quantification performance with the addition of covariates. Given that these are smaller datasets with a limited number of observations per patient, we suggest that the inclusion of covariates leads to model overfitting, consequently increasing test-time errors. In contrast, for Broll et al. (2021) that is also small, unlike for all other datasets, we have covariates extracted solely from the timestamp, which appears to enhance model accuracy. This increase in performance is likely attributable to all patients within the train split exhibiting more pronounced cyclical CGM patterns, which could explain why the overfitted model performs better. This is further supported by the fact that the performance on the OD set deteriorates with the addition of covariates. Finally, in the case of Hall et al. (2018) and Weinstock et al. (2016), which are large datasets, the inclusion of covariates has mixed effects, indicating that covariates do not contribute significantly to the model’s performance.  

# 6 DISCUSSION  

Impact. We discuss potential negative societal impact of our work. First, inaccurate glucose forecasting could lead to severe consequences for patients. This is by far the most important consideration that we discuss further in Appendix D. Second, there is a potential threat from CGM device hacking that could affect model predictions. Third, the existence of pre-defined tasks and datasets may stifle research, as researchers might focus on overftiting and marginally improving upon well-known datasets and tasks. Finally, the release of health records must be treated with caution to guarantee patients’ right to privacy.  

Future directions. We outline several research avenues: (1) adding new public CGM datasets and tasks; (2) open-sourcing physiological and hybrid models; (3) exploring model training augmentation, such as pre-training on aggregated data followed by patient-specific fine-tuning and down-sampling night periods; (4) developing scaling laws for dataset size and model performance; and (5) examining covariate quality and principled integration within models. Related to the point (5), we note that out of the 5 collected datasets, only Dubosson et al. (2018) records time-varying covariates describing patients physical activity (e.g. accelerometer readings, heart rate), blood pressure, food intake, and medication. We believe having larger datasets that comprehensively track dynamic patient behavior could lead to new insights and more accurate forecasting.  

# 7 CONCLUSION  

In this work, we have presented a comprehensive resource to address the challenges in CGM-based glucose trajectory prediction, including a curated repository of public datasets, a standardized task list, a set of benchmark models, and a detailed analysis of performance-influencing factors. Our analysis emphasizes the significance of dataset size, patient population, testing splits (e.g., in- and out-of-distribution, daytime, nighttime), and covariate availability.  

# ACKNOWLEDGEMENTS  

The source of a subset of the data is the T1D Exchange, but the analyses, content, and conclusions presented herein are solely the responsibility of the authors and have not been reviewed or approved by the T1D Exchange.  

# REFERENCES  

Takuya Akiba, Shotaro Sano, Toshihiko Yanase, Takeru Ohta, and Masanori Koyama. Optuna: A next-generation hyperparameter optimization framework. In Proceedings of the 25th ACM SIGKDD international conference on knowledge discovery & data mining, pp. 2623–2631, 2019.  

Grazia Aleppo, Katrina J Ruedy, Tonya D Riddlesworth, Davida F Kruger, Anne L Peters, Irl Hirsch, Richard M Bergenstal, Elena Toschi, Andrew J Ahmann, Viral N Shah, et al. Replace-bg: a randomized trial comparing continuous glucose monitoring with and without routine blood glucose monitoring in adults with well-controlled type 1 diabetes. Diabetes care, 40(4):538–545, 2017.  

Alessandro Aliberti, Irene Pupillo, Stefano Terna, Enrico Macii, Santa Di Cataldo, Edoardo Patti, and Andrea Acquaviva. A multi-patient data-driven approach to blood glucose prediction. IEEE Access, 7:69311–69325, 2019.  

Radica Z Alicic, Michele T Rooney, and Katherine R Tuttle. Diabetic kidney disease: challenges, progress, and possibilities. Clinical journal of the American Society of Nephrology: CJASN, 12 (12):2032, 2017.  

Marios Anthimopoulos, Joachim Dehais, Sergey Shevchik, Botwey H Ransford, David Duke, Peter Diem, and Stavroula Mougiakakou. Computer vision-based carbohydrate estimation for type 1 patients with diabetes using smartphones. Journal of diabetes science and technology, 9(3): 507–515, 2015.  

Mohammadreza Armandpour, Brian Kidd, Yu Du, and Jianhua Z. Huang. Deep Personalized Glucose Level Forecasting Using Attention-based Recurrent Neural Networks. In International Joint Conference on Neural Networks (IJCNN), 2021. doi: 10.1109/IJCNN52387.2021.9533897.  

Naviyn Prabhu Balakrishnan, Lakshminarayanan Samavedham, and Gade Pandu Rangaiah. Personalized Hybrid Models for Exercise, Meal, and Insulin Interventions in Type 1 Diabetic Children and Adolescents. Industrial & Engineering Chemistry Research, 52(36):13020–13033, 2013. ISSN 0888-5885. doi: 10.1021/ie402531k. URL https://doi.org/10.1021/ie402531k.  

Jaouher Ben Ali, Takoua Hamdi, Nader Fnaiech, V´eronique Di Costanzo, Farhat Fnaiech, and Jean-Marc Ginoux. Continuous blood glucose level prediction of Type 1 Diabetes based on Artificial Neural Network. Biocybernetics and Biomedical Engineering, 38(4):828–840, 2018. ISSN 02085216. doi: 10.1016/j.bbe.2018.06.005. URL https://linkinghub.elsevier. com/retrieve/pii/S020852161830127X.  

Richard N Bergman, Y Ziya Ider, Charles R Bowden, and Claudio Cobelli. Quantitative estimation of insulin sensitivity. American Journal of Physiology-Endocrinology And Metabolism, 236(6): E667, 1979.  

Alain Bock, Gr´egory Franc¸ois, and Denis Gillet. A therapy parameter-based model for predicting blood glucose concentrations in patients with type 1 diabetes. Computer Methods and Programs in Biomedicine, 118(2):107–123, 2015. ISSN 0169-2607. doi: 10.1016/j.cmpb. 2014.12.002. URL https://www.sciencedirect.com/science/article/pii/ S0169260714003915.  

Dimitri Boiroux, Anne Katrine Duun-Henriksen, Signe Schmidt, Kirsten Nørgaard, Sten Madsbad, Ole Skyggebjerg, Peter Ruhdal Jensen, Niels Kjølstad Poulsen, Henrik Madsen, and John Bagterp Jørgensen. Overnight Control of Blood Glucose in People with Type 1 Diabetes. IFAC Proceedings Volumes, 45(18):73–78, 2012. ISSN 1474-6670. doi: 10.3182/ 20120829-3-HU-2029.00106. URL https://www.sciencedirect.com/science/ article/pii/S1474667016320766.  

Ransford Henry Botwey, Elena Daskalaki, Peter Diem, and Stavroula G Mougiakakou. Multi-model data fusion to improve an early warning system for hypo-/hyperglycemic events. In 2014 36th Annual International Conference of the IEEE Engineering in Medicine and Biology Society, pp. 4843–4846. IEEE, 2014.   
Steven Broll, Jacek Urbanek, David Buchanan, Elizabeth Chun, John Muschelli, Naresh M Punjabi, and Irina Gaynanova. Interpreting blood glucose data with r package iglu. PloS one, 16(4): e0248560, 2021.   
Remei Calm, Maira Garc´ıa-Jaramillo, Jorge Bondia, MA Sainz, and Josep Veh´ı. Comparison of interval and monte carlo simulation for the prediction of postprandial glucose under uncertainty in type 1 diabetes mellitus. Computer methods and programs in biomedicine, 104(3):325–332, 2011.   
Marzia Cescon. Modeling and prediction in diabetes physiology. Department of Automatic Control, Lund University, Sweden, 2013.   
Cristian Challu, Kin G Olivares, Boris N Oreshkin, Federico Garza, Max Mergenthaler, and Artur Dubrawski. N-hits: Neural hierarchical interpolation for time series forecasting. 37th Conference on Artificial Intelligence (AAAI), 2023.   
Cheng-Liang Chen and Hong-Wen Tsai. Modeling the physiological glucose–insulin system on normal and diabetic subjects. Computer methods and programs in biomedicine, 97(2):130–140, 2010.   
Tianqi Chen and Carlos Guestrin. Xgboost: A scalable tree boosting system. 22nd International Conference on Knowledge Discovery and Data Mining (ACM SIGKDD), pp. 785–794, 2016.   
Ana Cola´s, Luis Vigil, Borja Vargas, David Cuesta-Frau, and Manuel Varela. Detrended fluctuation analysis in the prediction of type 2 diabetes mellitus in patients at risk: Model optimization and comparison with other metrics. PloS one, 14(12):e0225817, 2019.   
Ivan Contreras and Josep Vehi. Artificial Intelligence for Diabetes Management and Decision Support: Literature Review. Journal of Medical Internet Research, 20(5):e10775, 2018. ISSN 1439- 4456. doi: 10.2196/10775. URL https://www.ncbi.nlm.nih.gov/pmc/articles/ PMC6000484/.   
Diego De Pereda, Sergio Romero-Vivo, Beatriz Ricarte, and Jorge Bondia. On the prediction of glucose concentration under intra-patient variability in type 1 diabetes: A monotone systems approach. Computer methods and programs in biomedicine, 108(3):993–1001, 2012.   
Yixiang Deng, Lu Lu, Laura Aponte, Angeliki M. Angelidi, Vera Novak, George Em Karniadakis, and Christos S. Mantzoros. Deep transfer learning and data augmentation improve glucose levels prediction in type 2 diabetes patients. NPJ Digital Medicine, 4:109, 2021. ISSN 2398- 6352. doi: 10.1038/s41746-021-00480-x. URL https://www.ncbi.nlm.nih.gov/pmc/ articles/PMC8280162/.   
Fabien Dubosson, Jean-Eudes Ranvier, Stefano Bromuri, Jean-Paul Calbimonte, Juan Ruiz, and Michael Schumacher. The open d1namo dataset: A multi-modal dataset for research on noninvasive type 1 diabetes management. Informatics in Medicine Unlocked, 13:92–100, 2018.   
Anne Katrine Duun-Henriksen, Signe Schmidt, Rikke Meldgaard Røge, Jonas Bech Møller, Kirsten Nørgaard, John Bagterp Jørgensen, and Henrik Madsen. Model identification using stochastic differential equation grey-box models in diabetes. Journal of diabetes science and technology, 7 (2):431–440, 2013.   
Hajrudin Efendic, Harald Kirchsteiger, Guido Freckmann, and Luigi del Re. Short-term prediction of blood glucose concentration using interval probabilistic models. In 22nd Mediterranean conference on control and automation, pp. 1494–1499. IEEE, 2014.   
Meriyan Eren-Oruklu, Ali Cinar, and Lauretta Quinn. Hypoglycemia Prediction with Subject-Specific Recursive Time-Series Models. Journal of Diabetes Science and Technology, 4(1):25–33, 2010. ISSN 1932-2968. doi: 10.1177/193229681000400104. URL https://doi.org/10.1177/ 193229681000400104.  

Qiang Fang, Lei Yu, and Peng Li. A new insulin-glucose metabolic model of type 1 diabetes mellitus: An in silico study. Computer methods and programs in Biomedicine, 120(1):16–26, 2015.  

International Diabetes Federation. International Diabetes Federation Diabetes Atlas. International Diabetes Federation, 2021.  

Cristian Challu´ Kin G. Olivares Federico Garza, Max Mergenthaler Canseco. StatsForecast: Lightning fast forecasting with statistical and econometric models. PyCon Salt Lake City, Utah, US 2022, 2022. URL https://github.com/Nixtla/statsforecast.  

Ian Fox, Lynn Ang, Mamta Jaiswal, Rodica Pop-Busui, and Jenna Wiens. Deep Multi-Output Forecasting: Learning to Accurately Predict Blood Glucose Trajectories. 24th International Conference on Knowledge Discovery and Data Mining (ACM SIGKDD), pp. 1387–1395, 2018. doi: 10.1145/3219819.3220102. URL https://dl.acm.org/doi/10.1145/3219819. 3220102.  

Eleni Georga, Vasilios Protopappas, Alejandra Guillen, Giuseppe Fico, Diego Ardigo, Maria Teresa Arredondo, Themis P Exarchos, Demosthenes Polyzos, and Dimitrios I Fotiadis. Data mining for blood glucose prediction and knowledge discovery in diabetic patients: The metabo diabetes modeling and management system. In 2009 annual international conference of the IEEE engineering in medicine and biology society, pp. 5633–5636. IEEE, 2009.  

Eleni I. Georga, Vasilios C. Protopappas, Demosthenes Polyzos, and Dimitrios I. Fotiadis. Evaluation of short-term predictors of glucose concentration in type 1 diabetes combining feature ranking with regression models. Medical & Biological Engineering & Computing, 53(12):1305–1318, 2015. ISSN 1741-0444. doi: 10.1007/s11517-015-1263-1. URL https://doi.org/10.1007/ s11517-015-1263-1.  

Pe´ter Gyuk, Istva´n Vassa´nyi, and Istva´n Ko´sa. Blood Glucose Level Prediction for Diabetics Based on Nutrition and Insulin Administration Logs Using Personalized Mathematical Models. Journal of Healthcare Engineering, pp. 8605206, 2019. ISSN 2040-2295. doi: 10.1155/2019/8605206. URL https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6350605/.  

Heather Hall, Dalia Perelman, Alessandra Breschi, Patricia Limcaoco, Ryan Kellogg, Tracey McLaughlin, and Michael Snyder. Glucotypes reveal new patterns of glucose dysregulation. PLoS biology, 16(7):e2005143, 2018.  

Jinli He and Youqing Wang. Blood glucose concentration prediction based on kernel canonical correlation analysis with particle swarm optimization and error compensation. Computer Methods and Programs in Biomedicine, 196:105574, 2020. ISSN 0169-2607. doi: 10.1016/j.cmpb. 2020.105574. URL https://www.sciencedirect.com/science/article/pii/ S0169260720305083.  

Julien Herzen, Francesco La¨ssig, Samuele Giuliano Piazzetta, Thomas Neuer, Le´o Tafti, Guillaume Raille, Tomas Van Pottelbergh, Marek Pasieka, Andrzej Skrodzki, Nicolas Huguenin, et al. Darts: User-friendly modern machine learning for time series. Journal of Machine Learning Research, 23 (124):1–6, 2022. URL http://jmlr.org/papers/v23/21-1177.html.  

J. Ignacio Hidalgo, J. Manuel Colmenar, Gabriel Kronberger, Stephan M. Winkler, Oscar Garnica, and Juan Lanchares. Data Based Prediction of Blood Glucose Concentrations Using Evolutionary Methods. Journal of Medical Systems, 41(9):142, 2017. ISSN 1573-689X. doi: 10.1007/ s10916-017-0788-2. URL https://doi.org/10.1007/s10916-017-0788-2.  

Roman Hovorka, Valentina Canonico, Ludovic J Chassin, Ulrich Haueter, Massimo Massi-Benedetti, Marco Orsini Federici, Thomas R Pieber, Helga C Schaller, Lukas Schaupp, Thomas Vering, et al. Nonlinear model predictive control of glucose concentration in subjects with type 1 diabetes. Physiological measurement, 25(4):905, 2004.  

Rob J Hyndman and Yeasmin Khandakar. Automatic time series forecasting: the forecast package for r. Journal of statistical software, 27:1–22, 2008.  

Diabetes Research in Children Network (DirecNet) Study Group. Use of the direcnet applied treatment algorithm (data) for diabetes management with a real-time continuous glucose monitor (the freestyle navigator). Pediatric diabetes, 9(2):142–147, 2008.  

Redy Indrawan, Siti Saadah, and Prasti Eko Yunanto. Blood Glucose Prediction Using Convolutional Long Short-Term Memory Algorithms. Khazanah Informatika : Jurnal Ilmu Komputer dan Informatika, 7(2):90–95, 2021. ISSN 2477-698X. doi: 10.23917/khif.v7i2.14629. URL https: //journals.ums.ac.id/index.php/khif/article/view/14629.  

Mehrad Jaloli and Marzia Cescon. Long-term Prediction of Blood Glucose Levels in Type 1 Diabetes Using a CNN-LSTM-Based Deep Neural Network. Journal of Diabetes Science and Technology, pp. 19322968221092785, 2022. ISSN 1932-2968. doi: 10.1177/19322968221092785. URL https://doi.org/10.1177/19322968221092785.  

Ioannis Kavakiotis, Olga Tsave, Athanasios Salifoglou, Nicos Maglaveras, Ioannis Vlahavas, and Ioanna Chouvarda. Machine Learning and Data Mining Methods in Diabetes Research. Computational and Structural Biotechnology Journal, 15:104–116, 2017. ISSN 2001-0370. doi: 10.1016/j.csbj.2016.12.005. URL https://www.ncbi.nlm.nih.gov/pmc/articles/ PMC5257026/.  

Hun-Sung Kim and Kun-Ho Yoon. Lessons from Use of Continuous Glucose Monitoring Systems in Digital Healthcare. Endocrinology and Metabolism, 35(3):541–548, 2020. ISSN 2093-596X. doi: 10.3803/EnM.2020.675. URL https://www.ncbi.nlm.nih.gov/pmc/ articles/PMC7520582/.  

Volodymyr Kuleshov, Nathan Fenner, and Stefano Ermon. Accurate uncertainties for deep learning using calibrated regression. 35th International Conference on Machine Learning (ICML), pp. 2796–2804, 2018.  

Alejandro J Laguna, Paolo Rossetti, F Javier Ampudia-Blasco, Josep Vehi, and Jorge Bondia. Experimental blood glucose interval identification of patients with type 1 diabetes. Journal of Process Control, 24(1):171–181, 2014a.  

Alejandro J Laguna, Paolo Rossetti, F Javier Ampudia-Blasco, Josep Veh´ı, and Jorge Bondia. Identification of intra-patient variability in the postprandial response of patients with type 1 diabetes. Biomedical Signal Processing and Control, 12:39–46, 2014b.  

Sa´ul Langarica, Maria Rodriguez-Fernandez, Felipe N´u˜nez, and Francis J. Doyle. A meta-learning approach to personalized blood glucose prediction in type 1 diabetes. Control Engineering Practice, 135:105498, 2023. ISSN 0967-0661. doi: 10.1016/j.conengprac.2023.105498. URL https: //www.sciencedirect.com/science/article/pii/S0967066123000679.  

Yann LeCun, Le´on Bottou, Genevieve B Orr, and Klaus-Robert Mu¨ller. Efficient backprop. In Neural networks: Tricks of the trade, pp. 9–50. Springer, 2002.  

ED Lehmann and T Deutsch. A physiological model of glucose-insulin interaction. In Proceedings of the Annual International Conference of the IEEE Engineering in Medicine and Biology Society Volume 13: 1991, pp. 2274–2275. IEEE, 1991.  

Kezhi Li, John Daniels, Chengyuan Liu, Pau Herrero, and Pantelis Georgiou. Convolutional Recurrent Neural Networks for Glucose Prediction. IEEE Journal of Biomedical and Health Informatics, 24 (2):603–613, 2020. ISSN 2168-2208. doi: 10.1109/JBHI.2019.2908488.  

Bryan Lim, Sercan ¨O Arık, Nicolas Loeff, and Tomas Pfister. Temporal fusion transformers for interpretable multi-horizon time series forecasting. International Journal of Forecasting, 37(4): 1748–1764, 2021.  

Chengyuan Liu, Josep Vehi, Nick Oliver, Pantelis Georgiou, and Pau Herrero. Enhancing Blood Glucose Prediction with Meal Absorption and Physical Exercise Information. arXiv Preprint, (arXiv:1901.07467), 2018. URL http://arxiv.org/abs/1901.07467.  

Chiara Dalla Man, Francesco Micheletto, Dayu Lv, Marc Breton, Boris Kovatchev, and Claudio Cobelli. The uva/padova type 1 diabetes simulator: new features. Journal of diabetes science and technology, 8(1):26–34, 2014.  

Cindy Marling and Razvan Bunescu. The ohiot1dm dataset for blood glucose level prediction: Update 2020. In CEUR workshop proceedings, volume 2675, pp. 71. NIH Public Access, 2020.  

John Martinsson, Alexander Schliep, Bj¨orn Eliasson, and Olof Mogren. Blood Glucose Prediction with Variance Estimation Using Recurrent Neural Networks. Journal of Healthcare Informatics Research, 4(1):1–18, 2020. ISSN 2509-498X. doi: 10.1007/s41666-019-00059-y. URL https: //doi.org/10.1007/s41666-019-00059-y.  

Nelly Mauras, Roy Beck, Dongyuan Xing, Katrina Ruedy, Bruce Buckingham, Michael Tansey, Neil H White, Stuart A Weinzimer, William Tamborlane, Craig Kollman, et al. A randomized clinical trial to assess the efficacy and safety of real-time continuous glucose monitoring in the management of type 1 diabetes in young children aged 4 to¡ 10 years. Diabetes care, 35(2): 204–210, 2012.  

Sadegh Mirshekarian, Hui Shen, Razvan Bunescu, and Cindy Marling. LSTMs and Neural Attention Models for Blood Glucose Prediction: Comparative Experiments on Real and Synthetic Data. Annual International Conference of the IEEE Engineering in Medicine and Biology Society. IEEE Engineering in Medicine and Biology Society., 2019:706–712, 2019. ISSN 2375-7477. doi: 10. 1109/EMBC.2019.8856940. URL https://www.ncbi.nlm.nih.gov/pmc/articles/ PMC7890945/.  

Mario Munoz-Organero. Deep Physiological Model for Blood Glucose Prediction in T1DM Patients. Sensors (Basel, Switzerland), 20(14):3896, 2020. doi: 10.3390/s20143896. URL https://www. ncbi.nlm.nih.gov/pmc/articles/PMC7412558/.  

Natalie Nanayakkara, Andrea J Curtis, Stephane Heritier, Adelle M Gadowski, Meda E Pavkov, Timothy Kenealy, David R Owens, Rebecca L Thomas, Soon Song, Jencia Wong, et al. Impact of age at type 2 diabetes mellitus diagnosis on mortality and vascular complications: systematic review and meta-analyses. Diabetologia, 64:275–287, 2021.  

C. Novara, N. Mohammad Pour, T. Vincent, and G. Grassi. A Nonlinear Blind Identification Approach to Modeling of Diabetic Patients. IEEE Transactions on Control Systems Technology, 24(3):1092–1100, 2016. ISSN 1558-0865. doi: 10.1109/TCST.2015.2462734.  

Boris N Oreshkin, Dmitri Carpov, Nicolas Chapados, and Yoshua Bengio. N-beats: Neural basis expansion analysis for interpretable time series forecasting. 8th International Conference on Learning Representations (ICLR), 2020.  

Mwaffaq Otoom, Hussam Alshraideh, Hisham M. Almasaeid, Diego Lo´pez-de Ipin˜a, and Jose´ Bravo. Real-Time Statistical Modeling of Blood Sugar. Journal of Medical Systems, 39(10):123, 2015. ISSN 1573-689X. doi: 10.1007/s10916-015-0301-8. URL https://doi.org/10.1007/ s10916-015-0301-8.  

Silvia Oviedo, Josep Veh´ı, Remei Calm, and Joaquim Armengol. A review of personalized blood glucose prediction strategies for T1DM patients. International Journal for Numerical Methods in Biomedical Engineering, 33(6):e2833, 2017. ISSN 2040-7947. doi: 10.1002/cnm.2833. URL https://onlinelibrary.wiley.com/doi/abs/10.1002/cnm.2833.  

Francesco Prendin, Simone Del Favero, Martina Vettoretti, Giovanni Sparacino, and Andrea Facchinetti. Forecasting of Glucose Levels and Hypoglycemic Events: Head-to-Head Comparison of Linear and Nonlinear Data-Driven Algorithms Based on Continuous Glucose Monitoring Data Only. Sensors, 21(5):1647, 2021. ISSN 1424-8220. doi: 10.3390/s21051647. URL https://www.mdpi.com/1424-8220/21/5/1647.  

Maximilian P. Reymann, Eva Dorschky, Benjamin H. Groh, Christine Martindale, Peter Blank, and Bjoern M. Eskofier. Blood glucose level prediction based on support vector regression using mobile platforms. 38th Annual International Conference of the IEEE Engineering in Medicine and Biology Society (EMBC), pp. 2990–2993, 2016. ISSN 1558-4615. doi: 10.1109/EMBC.2016.7591358.  

Yulia Rubanova, Ricky TQ Chen, and David K Duvenaud. Latent ordinary differential equations for irregularly-sampled time series. Advances in Neural Information Processing Systems (NeurIPS), 32, 2019.  

Renat Sergazinov, Mohammadreza Armandpour, and Irina Gaynanova. Gluformer: Transformerbased personalized glucose forecasting with uncertainty quantification. IEEE ICASSP, 2023.  

Ge Shi, Shihong Zou, and Anpeng Huang. Glucose-tracking: A postprandial glucose prediction system for diabetic self-management. In 2015 2nd International Symposium on Future Information and Communication Technologies for Ubiquitous HealthCare (Ubi-HealthTech), pp. 1–9. IEEE, 2015.   
Bharath Sudharsan, Malinda Peeples, and Mansur Shomali. Hypoglycemia Prediction Using Machine Learning Models for Patients With Type 2 Diabetes. Journal of Diabetes Science and Technology, 9(1):86–90, 2015. ISSN 1932-2968. doi: 10.1177/1932296814554260. URL https://doi. org/10.1177/1932296814554260.   
Qingnan Sun, Marko V. Jankovic, Lia Bally, and Stavroula G. Mougiakakou. Predicting Blood Glucose with an LSTM and Bi-LSTM Based Deep Neural Network. In 2018 14th Symposium on Neural Networks and Applications (NEUREL), pp. 1–5, 2018. doi: 10.1109/NEUREL.2018. 8586990.   
Ilya Sutskever, James Martens, George Dahl, and Geoffrey Hinton. On the importance of initialization and momentum in deep learning. In International conference on machine learning, pp. 1139–1147. PMLR, 2013.   
William PTM van Doorn, Yuri D Foreman, Nicolaas C Schaper, Hans HCM Savelberg, Annemarie Koster, Carla JH van der Kallen, Anke Wesselius, Miranda T Schram, Ronald MA Henry, Pieter C Dagnelie, et al. Machine learning-based glucose prediction with use of continuous glucose and physical activity monitoring data: The maastricht study. PloS one, 16(6):e0253125, 2021.   
Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N Gomez, Łukasz Kaiser, and Illia Polosukhin. Attention is all you need. Advances in Neural Information Processing Systems (NeurIPS), 30, 2017.   
Youqing Wang, Xiangwei Wu, and Xue Mo. A novel adaptive-weighted-average framework for blood glucose prediction. Diabetes technology & therapeutics, 15(10):792–801, 2013.   
Ruth S Weinstock, Stephanie N DuBose, Richard M Bergenstal, Naomi S Chaytor, Christina Peterson, Beth A Olson, Medha N Munshi, Alysa JS Perrin, Kellee M Miller, Roy W Beck, et al. Risk factors associated with severe hypoglycemia in older adults with type 1 diabetes. Diabetes Care, 39(4):603–610, 2016.   
JM W´ojcicki. “j”-index. a new proposition of the assessment of current glucose control in diabetic patients. Hormone and metabolic research, 27(01):41–42, 1995.   
Zimei Wu, C-K Chui, G-S Hong, and Stephen Chang. Physiological analysis on oscillatory behavior of glucose–insulin regulation by model with delays. Journal of theoretical biology, 280(1):1–9, 2011.   
Charles C Wykoff, Rahul N Khurana, Quan Dong Nguyen, Scott P Kelly, Flora Lum, Rebecca Hall, Ibrahim M Abbass, Anna M Abolian, Ivaylo Stoilov, Tu My To, et al. Risk of blindness among patients with diabetes and newly diagnosed diabetic retinopathy. Diabetes care, 44(3):748–756, 2021.   
Jinyu Xie and Qian Wang. Benchmarking Machine Learning Algorithms on Blood Glucose Prediction for Type I Diabetes in Comparison With Classical Time-Series Models. IEEE Transactions on Biomedical Engineering, 67(11):3101–3124, 2020. ISSN 1558-2531. doi: 10.1109/TBME.2020. 2975959.   
He Xu, Shanjun Bao, Xiaoyu Zhang, Shangdong Liu, Wei Jing, and Yimu Ji. Blood Glucose Prediction Method Based on Particle Swarm Optimization and Model Fusion. Diagnostics, 12(12): 3062, 2022. ISSN 2075-4418. doi: 10.3390/diagnostics12123062. URL https://www.ncbi. nlm.nih.gov/pmc/articles/PMC9776993/.   
Jun Yang, Lei Li, Yimeng Shi, and Xiaolei Xie. An ARIMA Model With Adaptive Orders for Predicting Blood Glucose Concentrations and Hypoglycemia. IEEE Journal of Biomedical and Health Informatics, 23(3):1251–1260, 2019. ISSN 2168-2208. doi: 10.1109/JBHI.2018.2840690.   
Konstantia Zarkogianni, Konstantinos Mitsis, M-T Arredondo, Giuseppe Fico, Alessio Fioravanti, and Konstantina S Nikita. Neuro-fuzzy based glucose prediction model for patients with type 1 diabetes mellitus. IEEE-EMBS International Conference on Biomedical and Health Informatics (BHI), pp. 252–255, 2014.   
Yan Zhang, Tim A Holt, and Natalia Khovanova. A data driven nonlinear stochastic model for blood glucose dynamics. Computer methods and programs in biomedicine, 125:18–25, 2016.   
Taiyu Zhu, Kezhi Li, Pau Herrero, and Pantelis Georgiou. Personalized blood glucose prediction for type 1 diabetes using evidential deep learning and meta-learning. IEEE Transactions on Biomedical Engineering, 70(1):193–204, 2022a.   
Zhenyu Zhu, Fanghui Liu, Grigorios Chrysos, and Volkan Cevher. Robustness in deep learning: The good (width), the bad (depth), and the ugly (initialization). Advances in Neural Information Processing Systems, 35:36094–36107, 2022b.  

# A DATASETS  

Previous works. We summarize previous work on the CGM datasets in Table 7.  

Table 7: Summary of the glucose prediction models by dataset and model type. We indicate ”open” for datasets that are publicly available online, and ”proprietary” for the ones that cannot be released.   

![](images/4f493ae27d4fa45828cf7a1f8f7df53f0ec52e48ea189c872a1d5a943fa8f078.jpg)  

Access. The datasets are distributed according to the following licences and can be downloaded from the following links:  

1. Broll et al. (2021) License: GPL-2 Source: link   
2. Col´as et al. (2019) License: Creative Commons 4.0 Source: link   
3. Dubosson et al. (2018) License: Creative Commons 4.0 Source: link   
4. Hall et al. (2018) License: Creative Commons 4.0 Source: link   
5. Weinstock et al. (2016) License: Creative Commons 4.0 Source: link  

Covariates. We summarize covariate types for each dataset in Table 8. For each dataset, we extract the following dynamic known covariates from the time stamp: year, month, day, hour, minute, and second (only for Broll). Broll provides no covariates aside from the ones extracted from the time stamp. Colas, Hall, and Weinstock provide demographic information for the patients (static covariates). Dubosson is the only dataset for which dynamic unknown covariates such as heart rate, insulin levels, and blood pressure are available.  

Table 8: Covariate information for each dataset.   

![](images/5f58412702c4cbf1f68611f45d1a5aecd44eeb3ea37c2c3fee9b1cb22657e55f.jpg)  

# B ANALYSIS  

# B.1 VISUALIZED PREDICTIONS  

We provide visualized forecasts for the same 5 segments of Weinstock et al. (2016) data for the best performing models: linear regression, Latent ODE (Rubanova et al., 2019), and Transformer (Vaswani et al., 2017) on Task 1 (accuracy), and Gluformer (Sergazinov et al., 2023) and TFT (Lim et al., 2021) on Task 2 (uncertainty). For the best models on Task 2, we also provide the estimated confidence intervals or the predictive distribution, whichever is available. For visualization, we have truncated the input sequence to 1 hour (12 points); however, we note that different models have different input length and require at least 4 hours of observations to forecast the future trajectory.  

![](images/4e0d228a9f0b9ebd121d4ddb7bfef237a0346a8bec022a55d6498ba94a8d9aac.jpg)  
Figure 5: Model forecasts on Weinstock et al. (2016) dataset.  

# B.2 PERFORMANCE  

For reference, we include results for all models both with and without covariates evaluated on ID and OD splits in Table 9 on Task 1 (accuracy) and in Table 10 on Task 2 (uncertainty quantification).  

Table 9: Model results on the data sets for Task 1 (accuracy).   

![](images/39b4d8e37381aef73d59d61a41bffa0119c5329f213bbc58c11c77f29a4c6514.jpg)  

# B.3 FEATURE IMPORTANCE  

Based on the performance results reported in Tables 9 on Task 1 (accuracy) and in Table 10, XGBoost (Chen & Guestrin, 2016) is the only model that consistently works better with inclusion of extraneous covariates, improves in accuracy on 3 out of 5 datasets and uncertainty quantification on 4 out of 5 datasets. Table11 lists the top 10 covariates selected by XGBoost for each dataset. For time-varying features, such as the 36 heart rate observations in Dubosson, the maximum importance across the input length is considered as the feature importance. Below, we provide a discussion on the selected features.  

Table 10: Model results on the data sets for Task 2 (uncertainty quantification).   

![](images/441b9b9e4bd13a0ce4a35b4212e55ab684561bc5fca9feca9f63c39b0e395029.jpg)  

Among features available for all datasets, dynamic time features, such as hour and day of the week, consistently appear in the top 3 important features across all datasets. This could serve as indication that patients tend to adhere to daily routines; therefore, including time features helps the model to predict more accurately. At the same time, patient unique identifier does not appear to be important, only appearing in the top 10 for Broll (Broll only has 7 covariates in total) and Colas. This could be indicative of the fact that differences between patients is explained well by other covariates.  

Dynamic physical activity features such as heart rate and blood pressure are only available for Dubosson. Based on the table, we see that medication intake, heart rate and blood pressure metrics, and physical activity measurements are all selected by XGBoost as highly important.  

Demographic and medical record information is not available for Broll and Dubosson. For the rest of the datatsets, we observe medication (e.g. Vitamin D, Lisinopril for Weinstock), disease indicators (e.g. Diabetes T2 for Colas, Osteoporosis for Weinstock), health summary metrics (Body Mass Index for Colas), as well as indices derived from CGM measurements (e.g. J-index (Wo´jcicki, 1995)) being selected as highly important.  

Table 11: Top-10 features with importance weights selected by XGBoost for each dataset.   

![](images/8c828f2a1005b48839612a1787b355d27dc3a90c1e5b29fdee3d9b723157f204.jpg)  

# B.4 STABILITY  

Reproducible model performance is crucial in the clinical settings. In Table 16, we report standard deviation of MAE across random data splits. As expected, the smallest datasets (Broll et al. (2021) and Dubosson et al. (2018)) have largest variability. The number of patients in Broll et al. (2021) and Dubosson et al. (2018) is 5 and 9, respectively, thus randomly selecting 1 subject for OD test set has large impact on the model performance as the training set is altered drastically.  

Prior works on deep learning has found that initial weights can have large impact on the performance (LeCun et al., 2002; Sutskever et al., 2013; Zhu et al., 2022b). Therefore, we re-run each deep learning model 10 times with random initial weights for each data split and report the average. We also report standard deviation of deep learning model results across random model initializations (indicated in parentheses). We find that good initialization indeed matters as we observe that the results differ across re-runs with different starting weights. Such behavior could be undesirable in the clinical settings as the model training cannot be automated. The Transformer is the only robust deep learning model that consistently converges to the same results irrespective of the initial weights, which is reflected in near 0 standard deviation. At the same time, Transformer-based models such as Gluformer and TFT do not exhibit this feature.  

We include standard errors of each metric: RMSE (Task 1) in Table 12, MAE (Task 1) in Table 16, likelihood (Task 2) in Table 14, and calibration in Table 15. For deep learning models, there are 2 sources of randomness: random data split and model initialization. Therefore, we report two values for standard deviation: one across data splits (averaged over model initializations) and one for model initialization (averaged across data splits).  

# B.5 DAYTIME VERSUS NIGHTTIME ERROR DISTRIBUTION  

We provide daytime and nighttime error (MAE) distribution for all models and datasets in Figure 6. In general, we note that for larger datasets (Colas and Weinstock), the difference in daytime and nighttime error distribution appears smaller.  

Table 12: Standard error of MSE across data splits and model random initializations.   

![](images/0d67f71e94f328b8da0270a8a2a44f3e43fa227147b9e5041ba1dbec08815273.jpg)  

Table 13: Standard error of MAE across data splits and model random initializations.   

![](images/dfc2a9e05271a46c08ff3d5fc73194c284932e30d0b73fa9dc57d72ace910e67.jpg)  

Table 14: Standard error of likelihood across data splits and model random initializations.   

![](images/10645983f3ddca32f6e00e779a779a60c8583db4f31333bc0a54d2baa17e070e.jpg)  

Table 15: Standard error of calibration error across data splits and model random initializations.   

![](images/dd859df6d0d3536c9829622d0fd03dab06dc66753933a0dfaa3837aa729eada6.jpg)  

![](images/02db0cd8912cd037ba8c453a899c15477628f814f30e8a798e04d65ead1e9167.jpg)  
Figure 6: Distribution of daytime (9:00AM to 9:00PM) versus nighttime (9:00PM to 9:00AM) errors (MAE) for models with no covariates on the ID set.  

# C REPRODUCING RESULTS  

# C.1 COMPUTE RESOURCES  

We conducted all experiments on a single compute node equipped with 4 NVIDIA RTX2080Ti 12GB GPUs. We used Optuna (Akiba et al., 2019) to tune the hyperparameters of all models except ARIMA and saved the best configurations in the config/ folder of our repository. For ARIMA, we used the native hyperparameter selection algorithm (AutoARIMA) proposed in Hyndman & Khandakar (2008). The search grid for each model is available in the lib/ folder. The training time varied depending on the model and the dataset. We trained all deep learning models using the Adam optimizer for 100 epochs with early stopping that had a patience of 10 epochs. For AutoARIMA, we used the implementation available in Federico Garza (2022). For the linear regression, XGBoost (Chen & Guestrin, 2016), NHiTS (Challu et al., 2023), TFT (Lim et al., 2021), and Transformer (Vaswani et al., 2017), we used Darts (Herzen et al., 2022) library. For the Gluformer (Sergazinov et al., 2023) and Latent ODE (Rubanova et al., 2019) models, we adapted the original implementation available on GitHub.  

The shallow baselines, such as ARIMA, linear regression, and XGBoost, fti within 10 minutes for all datasets. Among the deep learning models, NHiTS was the fastest to fit, taking less than 2 hours on the largest dataset (Weinstock). Gluformer and Transformer required 6 to 8 hours to fti on Weinstock. Latent ODE and TFT were the slowest to fit, taking 10 to 12 hours on Weinstock on average.  

# C.2 HYPERPARAMETERS  

In this section, we provide an extensive discussion of hyperparameters, exploring their impact on forecasting models’ performance across studied datasets. For each model, we have identified the crucial hyperparameters and their ranges based on the paper where they first appeared. We observe that certain models, such as the Latent ODE and TFT, maintain consistent hyperparameters across datasets. In contrast, models like the Transformer and Gluformer exhibit notable variations. We provide a comprehensive list of the best hyperparameters for each datasets in Table 16 and provide intuition below.  

Linear regression and XGBoost (Chen & Guestrin, 2016). These models are not designed to capture the temporal dependence. Therefore, their hyperparameters change considerably between datasets and do not exhibit any particular patterns. For example, the maximum tree depth of XGBoost varies by $67\%$ , ranging from 6 to 10, while tree regularization remains relatively consistent.  

Transformer (Vaswani et al., 2017), TFT (Lim et al., 2021), Gluformer (Sergazinov et al., 2023). Both TFT and Gluformer are based on the Transformer architecture and share most of its hyperparameters. For this set of models, we identify the critical parameters to be the number of attention heads, the dimension of the fully-connected layers (absent for TFT), the dimension of the model (hidden size for TFT), and the number of encoder and decoder layers. Intuitively, each attention head captures a salient pattern, while the fully-connected layers and model dimensions control the complexity of the pattern. The encoder and decoder layers allow models to extract more flexible representations. With respect to these parameters, all models exhibit similar behavior. For larger datasets, e.g. Colas, Hall, and Weinstock, we observe the best performance with larger values of the parameters. On the other hand, for smaller datasets, we can achieve best performance with smaller models.  

Latent ODE (Rubanova et al., 2019). Latent ODE is based on the RNN (Sutskever et al., 2013) architecture. Across all models, Latent ODE is the only one that consistently shows the best performance with the same set of hyperparameter values, which we attribute to its hybrid nature. In Latent ODE, hyperparameters govern the parametric form of the ODE. Therefore, we believe the observed results indicate that Latent ODE is potentially capturing the glucose ODE.  

NHiTS (Challu et al., 2023). In the case of NHiTS, its authors identify kernel sizes as the only critical hyperparameter. This hyperparameter is responsible for the kernel size of the MaxPool operation and essentially controls the sampling rate for the subsequent blocks in the architecture. A larger kernel size leads model to focus more on the low-rate information. Based on our findings, NHiTS selects similar kernel sizes for all datasets, reflecting the fact that all datasets have similar patterns in the frequency domain.  

Table 16: Best hyperparameters for each model and dataset selected by Optuna Akiba et al. (2019). For models that support covariates, we indicate best hyperparameters with covariates in parantheses.   

![](images/767a0ec0da988a21960f85c02a1d999de4a0ef8b398a12f7f5d3cb38c41eb2ea.jpg)  

# D CHALLENGES  

In addressing the challenges associated with the implementation of our predictive models in clinical settings, we recognize three pivotal obstacles. Firstly, the challenge posed by computing power necessitates a strategic refinement of our models to guarantee their effectiveness on devices grappling with resource limitations and potential disruptions in internet connectivity. The delicate balance between the complexity of the model and its real-time relevance emerges as a critical factor, especially within the dynamic contexts of diverse healthcare settings.  

Secondly, the challenge of cold starts for new enrolling patients presents a significant hurdle. We acknowledge the importance of devising strategies to initialize and tailor the predictive models for individuals who are newly enrolled in the system. This consideration underscores the need for a dynamic and adaptable framework that ensures the seamless integration of our models into the continuum of patient care.  

The third challenge pertains to data privacy and transmission. To address this, our models must either possess on-device training capabilities or facilitate the secure and anonymized transmission of data to external servers. This emphasis on safeguarding patient information aligns with contemporary standards of privacy and ethical considerations, reinforcing the responsible deployment of our models in clinical practice.  