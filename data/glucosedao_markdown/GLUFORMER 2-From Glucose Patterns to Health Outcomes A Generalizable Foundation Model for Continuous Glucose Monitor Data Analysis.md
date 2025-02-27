# From Glucose Patterns to Health Outcomes: A Generalizable Foundation Model for Continuous Glucose Monitor Data Analysis  

Guy Lutsker1,2,3, Gal Sapir1,2,4, Anastasia Godneva1,2, Smadar Shilo1,2,5,6, Jerry R Greenfield7,8,9, Dorit Samocha-Bonet7,8, Shie Mannor3, Eli Meirom3, Gal Chechik3, Hagai Rossman1,2,4 & Eran Segal1,10,\*  

# Author affiliations  

1 Department of Computer Science and Applied Mathematics, Weizmann Institute of Science, Rehovot, Israel.   
2 Department of Molecular Cell Biology, Weizmann Institute of Science, Rehovot, Israel.   
3 NVIDIA, Israel.   
4 Pheno.AI, Tel-Aviv, Israel.   
5 Faculty of Medical and Health Sciences, Tel Aviv University, Tel-Aviv, Israel   
6 The Jesse $Z$ and Sara Lea Shafer Institute for Endocrinology and Diabetes, National Center for Childhood   
Diabetes, Schneider Children’s Medical Center of Israel, Petah Tikva, Israel   
7 Clinical Diabetes, Appetite and Metabolism Lab, Garvan Institute of Medical Research, Sydney, Australia   
$^8\,\mathrm{St}$ Vincent’s Clinical School, University of NSW, Sydney, Australia   
9 Department of Endocrinology and Diabetes, St Vincent’s Hospital, Sydney, Australia   
10 Mohamed bin Zayed University of Artificial Intelligence, Abu Dhabi, UAE.  

# Abstract  

Recent advances in self-supervised learning enabled novel medical AI models, known as foundation models (FMs) that offer great potential for characterizing health from diverse biomedical data. Continuous glucose monitoring (CGM) provides rich, temporal data on glycemic patterns, but its full potential for predicting broader health outcomes remains underutilized. Here, we present GluFormer, a generative foundation model on biomedical temporal data based on a transformer architecture, and trained on over 10 million CGM measurements from 10,812 non-diabetic individuals. We tokenized the CGM training data and trained GluFormer using next token prediction in a generative, autoregressive manner. We demonstrate that GluFormer generalizes effectively to 15 different external datasets, including 4936 individuals across 5 different geographical regions, 6 different CGM devices, and several metabolic disorders, including normoglycemic, prediabetic, and diabetic populations, as well as those with gestational diabetes and obesity. GluFormer produces embeddings which outperform traditional CGM analysis tools, and achieves high Pearson correlations in predicting clinical parameters such as HbA1c, liver-related parameters, blood lipids, and sleep-related indices. Notably, GluFormer can also predict onset of future health outcomes even 4 years in advance. We also show that CGM embeddings from pre-intervention periods in Randomized Clinical Trials (RCTs) outperform other methods in predicting primary and secondary outcomes. When integrating dietary data into GluFormer, we show that the enhanced model can accurately generate CGM data based only on dietary intake data, simulate outcomes of dietary interventions, and predict individual responses to specific foods. Overall, we show that GluFormer accurately predicts future health outcomes based on CGM data in a manner that generalizes across different populations and metabolic conditions, paving the way to utilizing CGM data in chronic disease management.  

# Introduction  

The emergence of self-supervised learning (SSL) in healthcare marks a shift in medical AI, enabling the creation of foundation models (FMs) capable of processing and analyzing vast amounts of unlabelled data 1 2 and application of diverse downstream tasks. Examples include FMs for retinal images 3, which improved detection rates of ophthalmic diseases in community setting 4, FM from wearable data has demonstrated the potential of SSL in analyzing continuous physiological signals from wearable devices 5, and FMs for sleep analysis have improved detection of sleep disorders 6. Furthermore, FM in pathology have shown remarkable accuracy in diagnosing complex diseases from histopathological images 7. SSL facilitates efficient training of AI systems without extensive annotated datasets, accelerating their integration into clinical practice 8. This convergence of AI advancements and the availability of high-quality datasets producing opportunities for major improvements in healthcare delivery and outcomes, particularly in managing chronic conditions like diabetes, which remains one of the leading causes of death and disability worldwide 9.  

Diabetes affects individuals across age groups and geographical regions. The prevalence of diabetes is increasing, with ${>}500$ million patients as of 2021, with the global expenditure estimated at over $\mathbb{S}900$ billion per annum 9. Type 2 diabetes (T2DM) is largely driven by preventable risk factors, such as poor diet, and lack of appropriate physical activity 9. Diabetes is a major risk factor for numerous comorbidities, including cardiovascular disorders (such as ischemic heart disease and stroke), liver disease, lung diseases, cancer conditions, chronic kidney disease, and mental health issues, many of which are leading causes of global morbidity and mortality10 11 12 13–17. As the impact of diabetes continues to grow, Continuous Glucose Monitoring (CGM) has emerged as a crucial tool in both managing the disease and enhancing overall patient care.  

CGM has shown several advantages over traditional self-monitoring of blood glucose (SMBG) in individuals with diabetes. These include improving glycemic control in adults18 and in children 19, reducing hypoglycemic events18, and improving overall quality of life18. Recently, in an important consensus statement endorsed by the American Diabetes Association (ADA) and the European Association for the Study of Diabetes (EASD), clinicians and researchers recommended that CGM-derived metrics be incorporated in clinical trials for diabetes 20, paving the way for wider adoption. The usage of CGM devices has also been studied in the non-diabetic population. It may assist in detecting early signs of glucose dysregulation 21, sports related performance enhancement21, and receiving personalized advice on diet 22. Additionally, recent research using CGM in non-diabetic adults has revealed substantial day-to-day variability in fasting glucose levels, suggesting the potential for CGM to refine glycemic status assessment 23. Importantly, the Food and Drug Administration (FDA) recently approved the first over-the-counter CGM device24, representing a significant shift towards widespread accessibility and glucose monitoring for the non-diabetic population.  

Here, we present GluFormer, a generative model for CGM data based on the transformer architecture 25, which efficiently learns over long sequences. It is trained in a self-supervised way using CGM data from the Human Phenotype Project (https://humanphenotypeproject.org/home) dataset, a large-scale, prospective, longitudinal study 26. During the study, CGM was recorded for 10,812 participants without prior diagnosis of diabetes for two weeks, during which meal-logging was performed. Participants underwent additional clinical testing including dual-energy $\mathrm{X}$ -ray absorptiometry (DXA), sleep assessment, liver and carotid ultrasound, blood serum NMR metabolomics and a plethora of other tests (for an exhaustive list, see link). We validated GluFormer on 15 external cohorts, encompassing a diverse range of populations and clinical conditions. These cohorts include individuals with pre-diabetes (Personalized Nutrition Project - PNP3, $\scriptstyle\mathtt{n}=225\ ^{27}$ ), type 2 diabetes (PREDICT, $\scriptstyle\mathtt{n=}264\ ^{28}$ 8, type 1 diabetes (T1DM PNP, $\scriptstyle\mathtt{n}=121^{\textit{29}}$ ), breast cancer survivors (BREACP, $\mathtt{n}{=}200^{\ 30}$ ), and healthy individuals (PNP1, $\scriptstyle\mathtt{n}=926\ ^{31}$ ). Additionally, data from multi-center clinical trials such as JDRF CGM RCT $\scriptstyle({\mathrm{n=}}451\ ^{\mathrm{~32~}}$ ) were utilized. The validation cohorts span multiple countries, including Israel, Australia, the United States, Spain, and China, providing a broad geographical representation. The population of these cohorts differs from that of the HPP cohort in terms of glycemic status at baseline, medical comorbidities, study designs and measurement devices, as well as geographical location and ancestry. The model generalizes well to external, out of distribution (OOD) data, predicting clinical information for populations from diverse geographical areas with different underlying metabolic disorders. Moreover, GluFormer produces embeddings which are able to predict clinical measures at the time of CGM recording, as well as future clinical measures up to 4 years into the future. Additionally, we show that we can use pre-intervention CGM of participants from RCTs and predict their outcome, following the intervention. These advancements represent a paradigm shift in our approach to precision metabolic health management and clinical research. By providing a robust framework for analyzing and predicting glycemic patterns, GluFormer has potential to transform diabetes care, enhance risk stratification, and optimize treatment strategies. Furthermore, its ability to forecast clinical trial outcomes may significantly accelerate drug development and precision health initiatives, ultimately leading to improved patient outcomes and reduced healthcare costs.  

# Results  

Figure 1 provides a schematic overview of the GluFormer model developed in this study. Initially, the model was trained on data from 10,812 non-diabetic participants in the HPP cohort, with ${>}10\mathrm{,}000\mathrm{,}000$ glucose measurements in total. To facilitate efficient training, CGM data is tokenized such that each measurement within each sample is a discrete token (See Methods). GluFormer was trained using next token prediction, and thus is capable of generating, or continuing CGM time series. In addition the model is capable of embedding CGM samples to a 1,024 dimensional space (see Methods), which can be used in various downstream tasks. Our approach includes a series of evaluations to demonstrate GluFormer's capabilities and versatility: (1) assessing the model's generative capabilities by producing CGM signals (Figure 1A); (2) testing GluFormer on out-of-distribution data from external validation cohorts, varying in geographical location, CGM devices used, and underlying disorders; (3) evaluating the model's performance through multiple downstream tasks such as disease prediction, CGM profile generation, and dietary suggestions (Figure 1B); (4) applying GluFormer to clinical trial data to forecast changes in primary and secondary outcomes based on baseline CGM measurements (Figure 1C); and (5) incorporating dietary intake data to enable glucose response predictions for various foods based on their nutritional content (Figure 1D).  

![](images/57d9fec8a470369e85a496ae7e7c52c2d6971857c5fd11f7edf75cf39281873e.jpg)  
Figure 1: Overview of GluFormer architecture, training pipeline and downstream tasks.  

A. Pretraining of the GluFormer model on CGM data from 10,812 individuals in the HPP cohort, with the objective of predicting subsequent glucose measurements (next token prediction). We evaluate GluFormers utility on a variety of downstream tasks, including generating CGM time-series data, fine-tuning for predicting clinical measures, and creating representations that can be used by simple linear models to predict medical outcomes. B. We test GluFormer’s generalization ability on 15 different external datasets including 5 clinical trials across various pathologies (T1DM, T2DM, GDM, etc..) using 6 different CGM devices from 5 different countries. C. GluFormer’s CGM representations are utilized to forecast treatment outcomes in clinical trial participants - using pre-intervention CGM data to predict clinical outcomes of interventions. D. An extended, multimodal, version of GluFormer with an added input of date and time information, and can accept tokens from both glucose modality, as well as dietary tokens.  

# GluFormer Latent Representation Space Encodes Physiological Parameters and Generates Reliable CGM Signals  

To evaluate the ability of GluFormer to capture clinically relevant information from continuous glucose monitoring (CGM) data, we analyzed the model's output representations using uniform manifold approximation and projection (UMAP) 33. We processed CGM time series through GluFormer to generate embedding vectors. These vectors were then aggregated using max-pooling to extract features34 (see Methods). We applied UMAP to visualize these embeddings in a two-dimensional space, with each point corresponding to a CGM sample from the HPP. When we colored the UMAP by fasting plasma glucose (FPG), we found clear clustering patterns related to glycemic control. Similarly, when we colored the UMAP by postprandial glucose response (PPGR), we observed distinct gradients indicating varying levels of glucose tolerance. These results demonstrate that GluFormer encodes clinically relevant information, effectively capturing glycemic profiles with related yet distinct characteristics (Figure 2A and 2B).  

To further evaluate GluFormer's embeddings within and between participants, we compared the cosine distances 35 between embeddings. We measured intra-participant distances using embeddings from the same participant on different days, and inter-participant distances using embeddings from different participants. Our results show that inter-participant distances are significantly higher than intra-participant distances (p-value $<0.001$ ), indicating that GluFormer captures individual-specific glycemic patterns (Figure 2C).  

To assess GluFormer's ability to predict clinically relevant outcomes, we examined its performance in predicting HbA1c values. We compared GluFormer's predictions to those of other model types, including convolutional neural networks 36,37 (CNNs) and multilayer perceptrons (MLPs), as well as to predictions based on iglu parameters 38, which are validated clinical measures. iglu is a widely used open-source tool that implements a comprehensive set of CGM-derived metrics for assessing glucose control and variability. Our analysis reveals that pre-training through self-supervised learning 39 (SSL) enhances GluFormer's predictive accuracy for HbA1c. Notably, transformer architectures outperform CNNs and MLPs in capturing complex CGM patterns. Furthermore, frozen embeddings from the pre-trained model yield better predictions than direct iglu measurements, suggesting more effective feature capture (Fig. 2D, see Supplementary Fig. S2).  

Overall, these findings validate the utility of pre-trained models in predicting key clinical outcomes like HbA1c from CGM data, demonstrating that leveraging SSL pre-training enhances model performance in downstream tasks.  

![](images/c1528a6c9a48742c8d7dec07015eefb664fdf024e1fa6be73ad1c74b3039198f.jpg)  

# Figure 2: Evaluation of GluFormer’s Pretraining.  

A. & B. UMAP visualization of CGM representation from our model. Here we show how the embeddings relate to clinical measures not seen by the model. A. Plot shows a UMAP colored by Postprandial Glucose Response (PPGR), showing that UMAP dimension 1 captures the diversity in PPGR. Low PPGR values appear on the right, progressing to high PPGR on the left. B. Plot, colored by fasting glucose levels obtained from blood tests, shows that UMAP dimension 2 captures the range of fasting glucose levels, with lower levels on the right and higher levels on the left. These visualizations provide insights into how different clinical measures, crucial in endocrinology, correlate with the learned CGM embeddings. C. A comparison of intra-participant and inter-participant cosine distances of CGM embeddings. The “Intra Distances” (blue box plot) shows the distribution of cosine distances between embeddings of the same participant across different days (with no overlap), reflecting day-to-day variability in the individual’s data. The “Inter Distances” (orange box plot) shows the distribution of distances between embeddings from different participants, showing variation across individuals. The significant difference between the two, indicated by three asterisks, was tested using the Mann-Whitney test. D. A plot of the effectiveness of different models in predicting HbA1c from CGM data, quantified by Pearson correlation coefficients.  

# The GluFormer model generates CGM signal and captures innate characteristics of glycemic dynamics, and generalizes well to different populations  

To evaluate GluFormer's ability to generate realistic CGM time series, we compared observed and generated CGM data using both visual inspection and quantitative metrics. We generated CGM signals for individuals and compared them to their actual recordings using iglu measures. These results show that the model captures glucose dynamics and generates signals that align with individuals' glycemic characteristics. The radar plots demonstrate the model's ability to reproduce clinically important variables, though some discrepancies occur due to unmodeled personal actions such as diet (Fig. 3A).  

To assess the accuracy of generated signals across multiple glycemic metrics, we compared key iglu measurements from real signals to the average of three generated signals. Our analysis reveals significant correlations between the iglu metrics of generated and original CGM curves. For instance, we observed correlations of $\mathrm{\bfr}{=}0.98$ $\scriptstyle{\mathrm{p}}{<}0.001\rangle$ ) for mean glucose, $\mathrm{\bfr}{=}0.98$ $\scriptstyle{\mathrm{p}}{<}0.001\$ ) for glucose management indicator (GMI), and $\mathbf{r}{=}0.89$ $({\tt p}{<}0.001)$ ) for glucose below $70~\mathrm{mg/dL}$ , indicating the model's ability to reproduce essential glycemic features (Fig. 3B).  

To test the model's generalizability, we evaluated its performance on out-of-distribution (OOD) data from cohorts in new geographical areas not included in the training set. We generated time-series for participants with diverse glycemic characteristics, including those with type 2 diabetes mellitus (T2DM) or gestational diabetes mellitus (GDM), across different continents (Middle East, Australia, North America). The results show that the model generates time-series with correlated glycemic metrics for these diverse populations. For the T2D cohort, all correlations were above 0.8 $({\mathfrak{p}}{<}0.001)$ ), demonstrating the model's adaptability to different populations (Fig. 3C).  

To examine the impact of input data length on model performance, we varied the duration of CGM data provided to the model. We observed that increasing the input time series from 0 to 10 days improved the quality of generated signals, with the average correlation increasing from 0.46 to 0.9 $({\mathsf{p}}{<}0.001$ for both). These findings suggest that longer input sequences enhance the model's predictive capability (See Supplementary Fig. S3, S4).  

![](images/4abe06abe0b7babce6b38940d962b1de3885164fb2247c9d701039eeb4b4eccd.jpg)  
Figure 3: Evaluation of GluFormer’s Capabilities in Simulating and Analyzing CGM Data  

A. Day-by-day analysis for three participants (one in each row). Each panel on the right column compares the observed CGM readings (black curve) with three predicted time-series generated by GluFormer using different seeds (colored in blue, orange, and green). Each time series spans two full days, with the first day’s CGM data providing context for the model prediction of the second day, which is compared with the true CGM profiles. Radar charts on the left evaluate iglu measures (Mean, Coefficient of Variation (CV), and Glucose Management Indicator (GMI), In Range 70-180, Above 180) and show similarity between observed CGM iglu measures, and generated CGM iglu measures..  

B. iglu statistics of observed versus generated time series across the test participants from the HPP cohort. For each test participant from the HPP, we generated 3 CGM days and calculated their iglu measures. To get a single iglu calculation per person, we averaged the 3 calculated iglus on the generated data. Each scatter plot depicts a different iglu measure, where each point corresponds to a sample from the test set from a particular day - observed and generated. Iglu measures shown here are: Below 70, In Range 70-180, Standard Deviation (SD), Mean, Coefficient of Variation (CV), and Glucose Management Indicator (GMI). We observe a strong agreement (all correlations are above 0.75, $\mathfrak{p}\,<\,0.001\$ ) between observed and predicted metrics, validating GluFormer’s precision in adhering to clinically significant metrics, affirming its potential for large-scale diagnostic and predictive healthcare applications.  

C. Plot illustrating the correlation of key iglu measurements between observed and generated CGM signals across cohorts. Metrics are the same from panel B. External cohorts include (from left to right):  

HPP: $\scriptstyle{\mathrm{n}}=10{,}812$ , Israel, Healthy, FSLP, FSL IQ PNP3: $\scriptstyle{\mathtt{n}=225}$ , Israel, Pre-diabetes, FSL T2D IL: $\scriptstyle\mathtt{n}=23$ , Israel, T2DM, FSL T1DM PNP: $_{\mathrm{n}=121}$ , Israel, T1DM, Dexcom, Freestyle Navigator, FSL IL Healthy: $\scriptstyle{\mathrm{n}}=1159$ , Israel, Healthy, iPro2; Medtronic PNP1: $\scriptstyle\mathtt{n=926}_{!}$ , Israel, Healthy, FSL Bread Study: $_{\mathrm{n=}20}$ , Israel, Healthy, iPro2 GDM: $_{\mathrm{n=}549}$ , Israel, GDM, FSL BREACP: $\scriptstyle{\mathtt{n}=200}$ , Israel, Breast Cancer Survivors, FSL PREDICT: $\scriptstyle{\ n=264}$ , Australia, T2DM and prediabetes, FSL US Obese: $\scriptstyle{\ n=156}$ , US, Obese / pre-diabetes, FSL US Healthy: $n{=}327$ , US, Healthy, FSL  

Correlation is significantly above random for all metrics and all cohorts, and is particularly high for T2D, PNP3 and BREACP.  

# The GluFormer model encodes a wide range of clinical information and predicts clinical parameters, even years into the future  

To test the ability of GluFormer embeddings to predict a wide range of clinical parameters both at baseline and in the future, we compared their performance against traditional iglu measures using ridge regression models. We assessed predictions at the time of CGM recording and for future time points up to 4 years to evaluate the model's capability for both immediate and long-term health assessments. Our results demonstrate that GluFormer embeddings consistently outperform iglu measures across multiple clinical parameters (Fig. 4). At baseline (Fig. 4A), GluFormer shows superior predictive performance for visceral adipose tissue (VAT) $\mathrm{\Delta}\mathbf{r}=0.41$ vs. 0.28 for iglu, ${\mathfrak{p}}<0.001]$ ), liver attenuation $\mathbf{r}=0.19$ vs. 0.09, $\mathfrak{p}<0.001]$ ).  

The model also effectively predicts sleep-related apnea-hypopnea index (AHI) $\mathbf{r}=0.22$ vs. 0.17, $\mathfrak{p}<$ 0.001) and systolic blood pressure (SBP) $(\mathbf{r}\ =\ 0.26$ vs. 0.17, $\mathfrak{p}\,<\,0.001\$ ). Importantly, GluFormer's predictive capabilities from CGM at baseline, extend to clinical parameters 2 and 4 years following the baseline measurements. At a 2-year horizon (Fig. 4B), the model maintains its superior performance, particularly for VAT $\mathrm{\Deltar}=0.41$ vs. 0.35, $\mathfrak{p}<0.001]$ ) and fasting glucose levels $\mathrm{\bfr}=0.52$ vs. 0.37, $\mathfrak{p}<0.001]$ ). Even at a 4-year horizon (Fig. 4C), GluFormer continues to outperform iglu measures in predicting fasting glucose levels $\mathrm{\Delta}\mathrm{r}=0.47$ vs. 0.28, $\mathfrak{p}<0.001]$ ) and maintains significant predictive power for VAT $\mathbf{r}\!=\!0.21$ vs. 0.14, $\mathfrak{p}\ <\ 0.001\$ ), although the overall correlation strength decreases over time. These findings demonstrate GluFormer's robust ability to extract meaningful health insights from CGM data, surpassing traditional metrics in both immediate and long-term health assessments. The model's capacity to predict a wide range of clinical measures up to four years in advance underscores its potential for long-term health monitoring and risk assessment.  

![](images/d0c3c28425f30dc30fc37001246e37c46f293aa914bd3be12f036b7dea078201.jpg)  
  
Figure 4: Predictive performance of clinical measures using GluFormer embeddings and iglu measures  

Predictive correlations for various clinical measures at different time points using embeddings from GluFormer (blue) and iglu measures (red), processed through a ridge regression model. Each data point represents the average of 10 prediction iterations with different random seeds, and error bars show standard deviations.  

A. Prediction of clinical measures from CGM embeddings at the time of CGM recording. B. Prediction of clinical measures from CGM embeddings 2 years after CGM recording. C. Prediction of clinical measures from CGM embeddings 4 years after CGM recording. Clinical measures include HbA1C, glucose, triglycerides (T.G), waist circumference (W.C), systolic blood pressure (SBP), visceral adipose tissue (VAT), apnea-hypopnea index (AHI), LDL cholesterol, albumin, creatinine, and liver attenuation (Liver Att).  

The shape of the data points indicates the modality of the measure: blood (circle), body (square), DXA (triangle), NMR metabolomics - Nightingale (diamond), sleep (cross), and ultrasound (X). Statistical significance between the two groups (embeddings and iglu) was determined using the Mann-Whitney U test, marked by asterisks $\mathfrak{F}_{\mathfrak{p}}<0.05$ , $**_{\mathrm{p}}<0.01$ , $****\mathrm{\Deltap}<0.001$ , n.s. not significant). GluFormer outperforms iglu measures, showing significant improvements in predictive performance in all comparisons across panels A and B, while in panel C, GluFormer outperforms iglu in all measures except for HbA1C.  

# GluFormer embeddings predict glycemic and other clinically relevant outcomes for OOD data, across geographical areas  

To test whether GluFormer generalizes across diverse cohorts, geographies, devices, and diseases, we applied its embeddings to predict outcomes using CGM data from external research cohorts. We evaluated the model's performance on varied populations, including patients with type 2 diabetes mellitus (T2DM), breast cancer survivors, and pregnant women with gestational diabetes. Our results show that GluFormer successfully created embeddings reflecting aspects of personal clinical pictures and predicted outcomes more accurately than iglu metrics, consistently across these diverse populations (Figure 5). The embeddings demonstrated strong correlations with disease-specific features. In T2DM patients, GluFormer predicted creatinine levels $\mathbf{r}=0.27$ , $\mathfrak{p}<$ 0.001), a key indicator of kidney function. For breast cancer survivors, the model effectively estimated albumin $\mathbf{r}=\!0.19$ , $\mathtt{p}<0.001$ ) and creatinine levels $\mathbf{r}=0.12$ , $\mathtt{p}<0.001$ ), which reflect the impact of treatments on renal function and overall health. In pregnant women with gestational diabetes, GluFormer accurately predicted hemoglobin $\mathbf{r}=0.42$ , $\mathfrak{p}<0.001]$ ) and platelet counts $\mathbf{(r=}$ 0.35, $\mathsf{p}<0.001]$ ), important markers for maternal and fetal health.  

These findings indicate that GluFormer's latent space encompasses a broad spectrum of health indicators beyond glycemic metrics, reflecting overall health status and disease-specific characteristics. Clinically, this means GluFormer has the potential to not only predict glycemic outcomes but also provide valuable insights into a patient's broader health profile, making it a powerful tool for personalized health prediction and management across various medical conditions and demographic groups.  

![](images/cca272a2f92ad17d83ced7f634cd426a4bfa2c2dd3434a474e18bed1b77b4392.jpg)  

# Figure 5: Predictive performance of clinical measures across out-of-distribution cohorts using GluFormer embeddings and iglu measures.  

Predictive correlations for various clinical measures across diverse patient populations not seen during model training. These populations include the cohorts: PREDICT (Australia), PNP1 (Israel), T2D (Israel), US Obese (United States), BREACP (Israel), GDM (Israel), PNP3 (Israel), IL Healthy (Israel), and T1D (Israel). Clinical measures include HbA1C, glucose tolerance test (OGTT 2h), gamma-glutamyl transferase (GGT), waist circumference (WC), creatinine, albumin (Alb), hemoglobin, and platelets, Predictions were generated using a ridge regression model using GluFormer embeddings (blue) or iglu measures (red). Each data point represents the average of 10 prediction iterations with different random seeds, and error bars show standard deviations.  

Statistical significance between the two groups (embeddings and iglu) was determined using the Mann-Whitney U test, marked by asterisks $\mathfrak{F}\mathfrak{p}<0.05$ , $**_{\mathrm{p}}<0.01$ , $***\mathfrak{p}<0.001$ , n.s. not significant). The results demonstrate that GluFormer generally outperforms iglu measures, showing significant improvements in predictive performance in 12 out of the examined comparisons, while iglu only outperformed the embeddings significantly in two instances.  

# GluFormer CGM embeddings predict outcomes of clinical trials  

To test whether GluFormer embeddings could predict clinical trial outcomes from baseline data, potentially enabling personalized treatment decisions and improved patient care, we used pre-intervention CGM data from completed clinical trials. We embedded this data using GluFormer and predicted the studies' clinical outcomes, comparing our results to traditional iglu measures. Our results show that GluFormer embeddings consistently outperform iglu measures in forecasting clinical outcomes across diverse studies (Figure 6A). In the PREDICT cohort, GluFormer showed superior predictive power relative to iglu metrics for HbA1c, creatinine, and waist circumference $\mathrm{p}<$ 0.001). In the BREACP study, the model significantly improved predictions for HbA1c, body fat percentage $(\mathfrak{p}\ <\ 0.001)$ ), lymphocyte levels and creatinine. For the PNP3 diet intervention study, GluFormer achieved improvements in predicting changes in HbA1c, LDL, and glucose levels $({\mathfrak{p}}<$ 0.001). These predictions used only pre-intervention CGM data and a binary variable indicating the intervention arm. GluFormer also outperformed iglu in predicting primary outcomes for open access clinical trials with CGM data (Figure 6B). These results demonstrate the model's robust ability to predict medical intervention effects across various measures and studies. This suggests that CGM-derived embeddings could substantially benefit precision health and clinical trial design by providing insights into patient-specific treatment responses based on pre-intervention metabolic states.  

![](images/3f38aad84f448b039b775bb35e2eda9d7fe50717c70397bae9dcecd12c28a3dc.jpg)  
Figure 6: Forecasting Clinical Outcomes Following Interventional Studies Using Pre-Intervention CGM Embeddings  

A. Predictive correlations for clinical measures post-intervention across three different clinical studies, each featuring two intervention arms. Each panel represents data from one of the studies, specifically focusing on populations from Australia (metformin plus diet intervention), Breast Cancer (metformin interventionו), and PNP3 (diet intervention). The measures evaluated include Hemoglobin A1c (HbA1c), creatinine, LDL cholesterol, hemoglobin, lymphocyte count, visceral adipose tissue (VAT) mass, body fat percentage, waist circumference (WC), and more, depending on the specific conditions and interventions of each study.  

Predictive correlations shown here measure the efficacy of using CGM-derived embeddings (blue points) versus iglu measures (red points) to forecast changes in clinical measures 26 weeks following the intervention. The embeddings are derived from CGM data recorded pre-intervention, while the clinical outcomes are analyzed post-intervention, incorporating the binary intervention variable $\left(0\,/\,1\right)$ representing the absence or presence of a specific clinical intervention.  

B. Open access clinical trials prediction results. In each trial we chose the primary outcome, and predicted it using GluFormer Embeddings and iglu. For JDRM CGM RCT we predict HbA1C in 26 weeks, using CGM from 1-6 months of measurements. For Shanghai T2D we predict HbA1C in 26 weeks from 2 weeks of measurement. For Colas we predict baseline HbA1C. For Hypoglycemia, we predict based on a week of  

CGM, whether there will be an event of hypoglycemia in the following week.. Each data point represents the average of 10 predictions, each utilizing a different random seed, to ensure robustness and reliability of the results. Error bars indicate the standard deviation across these predictions. Statistical significance between the prediction capabilities of CGM-derived embeddings and iglu measures is assessed using the Mann-Whitney U test, annotated with asterisks indicating levels of significance $\mathfrak{F}\mathfrak{p}<0.05$ , $**_{\mathrm{p}}<0.01$ , $****\mathrm{p}<0.001$ , n.s. $=$ not significant).  

# Temporal encoding increases generation performance  

To improve GluFormer’s ability to capture temporal information we added date and time into the architecture of GluFormer through learned embeddings for minute, hour, day of the week, and month (see Methods). We then trained two versions of the model using a pre-processed HPP dataset (see Methods) and evaluated their performance in generating CGM data for test participants (See Fig. S5). The temporal informed model achieved a correlation of 0.22 $(\mathtt{p}<0.001)$ ) with the observed participant CGM data, outperforming the original GluFormer, which had a correlation of 0.15 $\ensuremath{\mathbb{p}}<0.001)$ .  

# Diet encoding to create a multimodal GluFormer model on HPP  

To test whether incorporating dietary information could improve glucose prediction accuracy, we developed a multimodal version of GluFormer that includes macronutrient content alongside glucose data. We tokenized both glucose measurements and diet macronutrients, creating a synchronized sequence for training. The model was trained using a next-token prediction strategy, learning to predict subsequent glucose tokens based on the combined sequence of glucose and diet tokens, with diet tokens masked out of the loss function to focus on glucose response prediction (See Methods). We then evaluated the impact of dietary data inclusion by comparing two versions of the model: one learned with diet tokens and one without. These models were tested on a generation task using data from test participants. Our results show that incorporating dietary information significantly enhances prediction accuracy (Fig. 7). The multimodal GluFormer achieved an average correlation of 0.5 with observed CGM data across test participants, surpassing the original GluFormer's correlation of 0.22 (p-value $<0.001$ ). In addition we show that $91\%$ of test participants showed better correlation (Fig. 7.A.1), and $92\%$ exhibited improved mean absolute error (MAE) when diet information was included (Fig. 7.A.2). These findings are further supported by a qualitative inspection of generated CGM time series plots, which demonstrate that glucose predictions incorporating dietary data more closely track the original glucose curves, particularly around meal times (Fig. 7.C.1, Fig. 7.C.2). To ensure robustness, we conducted tests across different random seeds, with consistent outcomes (Fig. S8). This enhancement suggests a significant advancement in our ability to model and predict glucose responses, potentially leading to improved management strategies for diverse populations.  

![](images/7aefe56f7ce0ffaa1d1af8c9f590ac99d0f1cd56cf7a16fd3f31fa74ffcdf88f.jpg)  
Figure 7: Impact of Dietary Data on GluFormer Model Performance.  

A. Comparison of Pearson correlation A.1 and mean absolute error (MAE) A.2 between the original and generated CGM data, with and without the inclusion of dietary data. Scatter plots show the improvements in correlation and MAE when dietary data is included, indicated by the majority of points falling above the diagonal line on correlation, and below on MAE metrics. B. Box plots summarizing the overall performance, showing the average correlation B.1 and MAE B.2 across all test participants, for 5 different random seeds (used for generation) with lower MAE and higher correlation for models including dietary data. C. Time series plots demonstrating glucose level predictions for two example participants C.1 and C.2. The observed CGM data (blue line) is compared to data generated with dietary tokens (green line) and without dietary tokens (orange line). Red bars indicate times of dietary events, highlighting the model’s improved performance in capturing glucose spikes when dietary information is included.  

# Discussion  

This work introduces GluFormer, a novel foundation model trained on continuous glucose monitoring (CGM) data from 10,812 non-diabetic individuals. GluFormer demonstrates versatility and predictive power across diverse applications. The model's latent space encodes physiological parameters, enabling accurate generation of CGM signals that capture individual glycemic dynamics. GluFormer outperforms traditional CGM metrics in predicting a wide range of clinical outcomes from diverse modalities, including HbA1c, liver function, blood lipids, and sleep indices, using only baseline CGM measurements to forecast these outcomes up to four years in advance. Notably, the model generalizes well to other populations, CGM devices, and diseases, predicting clinical outcomes across various geographical regions and metabolic disorders. GluFormer's embeddings also show promise in forecasting clinical trial outcomes based on baseline CGM data. Furthermore, the integration of dietary information into the model significantly enhances its predictive accuracy, allowing the model to simulate dietary interventions, and predict postprandial glucose response. These results collectively demonstrate GluFormer's potential to enhance metabolic health management and clinical research through comprehensive analysis of CGM data.  

The latent space represented in Figure 2 by model embeddings reveals its capacity to capture nuanced aspects of glucose metabolism. While increased PPGR is associated with beta cell dysfunction 40 and elevated fasting glucose correlates with insulin resistance 41, these metrics are interconnected in the pathophysiology of diabetes. The ability of GluFormer to distinguish these related but temporally distinct aspects of glucose dysregulation suggests its potential in capturing the nuanced progression of metabolic dysfunction. This aligns with our understanding that overproduction of endogenous glucose in the basal state and impaired suppression of postprandial glucose production are both markers of insulin resistance, with clinical hyperglycemia emerging when insulin secretion can no longer compensate for the degree of insulin resistance. Typically, postprandial hyperglycemia develops before fasting hyperglycemia in the natural progression of the disease. The model's capacity to encode these differences may prove valuable in early detection and monitoring of diabetes progression. Future studies could explore how GluFormer's embeddings correlate with different stages of diabetes development, potentially offering new insights into the prognosis of the transition from prediabetes to clinical diabetes.  

The choice of next token prediction as our pretraining strategy has proven to be highly effective. This approach, inspired by the success of models like GPT 25,42, compels the model to utilize past knowledge to predict future events. By focusing on the task of predicting subsequent glucose measurements based on previous readings, the model learns intricate patterns and dependencies within the data. This strategy not only enhances the model’s ability to generate realistic glucose signals but also prepares it for diverse downstream tasks, as evidenced by its performance across various clinical predictions. The results demonstrate the versatility of this pretraining method, making it a powerful approach for self-supervised learning in the biomedical domain.  

GluFormer represents a significant advancement over existing methods for analyzing CGM data. While current approaches provide valuable validated metrics and summary statistics, they are primarily focused on diabetes-specific outcomes. Previous innovations like glucodensities 43 have shown some predictive power but remain limited to the diabetes domain. In contrast, GluFormer's foundation model approach extends beyond traditional glycemic analysis, demonstrating predictive capabilities for a broad spectrum of health outcomes across metabolic states and geographical regions.  

Our analysis reveals that CGM data contains a wealth of information beyond traditional glycemic metrics, offering insights into a broad spectrum of health parameters. The latent space encoded by GluFormer demonstrates an ability to capture and distinguish different aspects of metabolic health. For instance, we observed distinct representations of insulin resistance and glucose response within this latent space, suggesting a nuanced understanding of different aspects of glycemic health. The richness of this latent representation extends to a wide array of phenotypes, indicating that CGM data may serve as a window into diverse physiological processes. This comprehensive encoding likely reflects metabolic health in the context of various bodily systems, from chronic stress responses to inflammatory processes and even aging markers.  

Our findings demonstrate that pretraining significantly enhances the predictive capabilities of our model, as illustrated in Figure 2D. By utilizing embeddings generated from the pretrained model without any finetuning, we achieved superior predictions of clinical measures compared to traditional CGM-based metrics. Interestingly, in some scenarios, our model struggled to significantly outperform traditional metrics, which are closely related to diabetes diagnosis and management. This is a well-documented phenomenon in self-supervised learning (SSL), given that traditional CGM-based statistics were specifically designed to proxy measures like HbA1c.  

However, GluFormer demonstrated superior performance in predicting outcomes not directly tied to these conventional metrics. Notably, it outperforms traditional CGM-based metrics on measures less directly related to glycemic health, such as creatinine and hemoglobin levels. These metrics are critical for assessing kidney function in T2DM, the impact of chemotherapy in cancer survivors, and maternal health in gestational diabetes. GluFormer's superior performance across this broader range of clinical parameters stems from its general self-supervised task of next token prediction, encouraging the model to learn general patterns without bias towards specific medical aspects. Currently, clinicians typically rely on limited metrics such as fasting glucose and HbA1c for prediabetes and general health assessments. Even for individuals with CGM, clinical focus is often restricted to time in range, hypo/hyperglycemic events, GMI/eHBA1C, and coefficient of variation 44. In contrast, GluFormer's unbiased analysis of CGM data potentially uncovers subtle patterns and predictors currently underutilized in diabetes care.  

The model's generative capabilities further validate its deep representation of glycemic dynamics, successfully producing CGM signals that closely match clinical parameters of original data, even for out-of-distribution populations. Intriguingly, when applied to external cohorts, GluFormer's latent space reveals cohort-specific information. We observed strong correlations with disease-specific features, such as creatinine levels in T2DM patients, albumin and creatinine in cancer survivors, and hemoglobin and platelet counts in pregnancy. This suggests that the model captures not just glycemic health, but also broader indicators of overall health status for different health and disease states.  

These findings point to a profound implication: CGM data may contain an intrinsic representation of general health, aligning with previous research showing relationships between inflammatory markers like IL-6 and CGM parameters 45. The ability of GluFormer to extract and utilize this hidden layer of health-related information opens new avenues for comprehensive health assessment and monitoring, potentially revolutionizing our approach to personalized medicine and early disease detection.  

Incorporating temporal information into GluFormer has led to notable improvements in model performance, notably in improved correlations between generated and observed data. This finding highlights the importance of temporal dynamics in modeling physiological processes and the potential for further enhancing predictive accuracy by integrating additional time-based data (e.g. sleep stages and physical activity logging).  

GluFormer's integration of CGM and dietary data offers promising potential for enhancing clinical trial design and execution in metabolic health research. While traditional trials often rely on average treatment effects, GluFormer's approach could potentially enable more nuanced, individual-level simulations of treatment responses. This capability may allow for more precise participant selection and stratification, potentially reducing sample size requirements and associated costs. However, it's crucial to note that while GluFormer shows promising results in predicting glucose responses to dietary inputs, we have yet to demonstrate true counterfactual or causal inference capabilities. Future research should focus on validating these potential applications. If successful, GluFormer could revolutionize trial design by enabling pre-trial simulations of dietary interventions, potentially identifying responders and non-responders. This could lead to more efficient, cost-effective trials and accelerate the development of personalized dietary interventions. Nonetheless, challenges such as participant compliance and data reliability remain important considerations in realizing these potential benefits.  

The use of nutrient-based dietary data rather than specific food items offers significant advantages in terms of generalizability. By focusing on the macronutrient content of meals, our model can theoretically predict responses to new foods not seen during training. This abstraction allows the model to generalize across various dietary patterns and cultural food practices, enhancing its applicability to diverse populations. While we have not explicitly tested this capability, the underlying principle suggests that GluFormer can potentially extend its predictive power to novel food items, paving the way for broader applications in personalized nutrition and metabolic health research.  

The convergence of increasing CGM data availability, in light of recent FDA clearance of over-the-counter devices for non-diabetic use 46, and advancements in AI technology presents an unprecedented opportunity for metabolic health research. GluFormer represents a significant step towards utilizing this wealth of information. As demonstrated, the model's ability to incorporate additional modalities, such as dietary data, suggests potential for further expansion to include sleep patterns, continuous photoplethysmogram (PPG) signals, exercise logs, and medication data. This points towards the development of a comprehensive multimodal health model based on continuous signals and tracking. As CGM devices become more affordable and accessible, applications in the wellness realm, such as personalized diet planning for weight loss, are likely to proliferate. The model's generalizability across diverse geographical regions and disease states demonstrates its potential for wide-ranging applications, with exciting possibilities for personalized health management and clinical research that extend beyond our current expectations.  

The recent global initiative to deliver precision health in diabetes 47, emphasizes the need for a paradigm shift in understanding diabetes heterogeneity. This initiative calls for redefinition of diabetes subtypes 48, integration of multiple data sources, and development of novel biomarkers. GluFormer aligns closely with these objectives, offering a powerful tool for capturing diabetes heterogeneity across diverse populations. Trained on the HPP dataset, which includes a diverse population encompassing various ethnicities and nationalities, GluFormer is designed to be applicable to all demographics. By leveraging large-scale CGM data and demonstrating strong predictive capabilities for various clinical outcomes, GluFormer represents a significant step towards the precision diabetology envisioned by this global initiative, potentially revolutionizing diabetes classification, prevention, and management strategies worldwide.  

Despite the robust performance and broad applicability of GluFormer, several limitations must be acknowledged. First, the dataset predominantly comprises healthy, non-diabetic individuals, which may limit the model’s generalizability to populations with more rare metabolic conditions. The dietary data integrated into the model relies on self-reported logs, which are prone to inaccuracies and omissions, potentially affecting predictions related to dietary interventions. Additionally, the integration of dietary data required extensive engineering efforts to quantify the nutrient content of each food item. This process is both expensive and time-consuming, creating a barrier to scalability and widespread implementation.  

The complexity and interpretability of transformer models, including GluFormer, also pose significant challenges. These models are often regarded as “black boxes”, making it difficult to understand the reasoning behind their predictions. Currently, clinical practice primarily relies on simpler metrics such as HbA1c and fasting glucose levels, and even metrics like iglu have not yet been widely adopted. Consequently, the advanced architecture of GluFormer, while offering greater predictive power for complex tasks, remains far from clinical adoption. Additionally, the model may inherit biases present in the training data, which need to be meticulously managed to ensure accurate and fair predictions. Also, GluFormer, similarly to many advanced analytical methods, produces a distribution of possible scenarios rather than a single prediction can complicate decision-making processes, as users must interpret a range of potential outcomes, which can be less straightforward than dealing with a singular prediction.  

In conclusion, GluFormer demonstrates impressive capabilities in metabolic health analysis. It outperforms traditional metrics in predicting diverse clinical outcomes across geographical regions and metabolic disorders. The model's latent space encodes rich physiological information, suggesting CGM data contains intrinsic representations of general health. GluFormer aligns with global initiatives for precision diabetes care and shows potential for enhancing clinical trial design. This work represents a significant advancement towards comprehensive, personalized metabolic health management and research, opening new avenues for early disease detection and intervention.  

# Methods  

# GluFormer  

The training dataset comprises Continuous Glucose Monitoring (CGM) records from 10,812 subjects, each monitored over a two-week period using the Freestyle Libre Pro 2 device (Abbott, US), which captures glucose levels subcutaneously every 15 minutes. These values typically range from 30 to 200 $\mathrm{mg/dL}$ . Initial day readings were excluded to mitigate noise from device calibration errors, commonly observed during the first 24 hours. Further, participants with fewer than 100 readings were removed from the dataset. Missing data points, occurring in less than $0.1\%$ of instances, were addressed through linear interpolation to fill gaps due to time skips in measurements.  

# Tokenization  

Glucose measurements were quantized into 460 evenly spaced intervals, each one representing a discrete glucose value between $40{-}500~\mathrm{md/dL}$ based on the distribution of the training set, which constituted $80\%$ of the data. Each such glucose value constitutes a token. To create a valid tensor with constant shape, the discretized tokens were then organized into segments of 1200 measurements each (equivalent to 300 hours or 12.5 continuous days of data). These 1200 measurements could be thought of as context length as it is described by Large Language Models (LLMs). Samples with fewer than the 1200 measurements were supplemented with a special ${\mathrm{<MASK>}}$ token to maintain uniform length. Data division into training, validation, and testing sets was participant-based rather than sample-based to ensure consistency in model evaluation. The division was made randomly, and was divided into these sizes : train set: $80\%$ of participants, validation set: $10\%$ , test set: $10\%$ .  

# Model Architecture  

We employed a transformer-based model 25 structured primarily around an encoder mechanism. The architecture was defined by the following parameters: embedding dimension of 1024, 16 attention heads, 16 transformer layers (or blocks), and a feed-forward dimension of 2048. The model was designed to process sequences up to 25,000 tokens in length and was trained with a context length of 1200 tokens. These choices were made based on a hyper parameter search.  

The vocabulary size of the model is 461 - 460 representing glucose values from 40 to $500\;\mathrm{md/dL}$ , and one masking token.  

The model initially embeds all tokens using the embedding layer (vocabulary size $X$ embedding dimension), such that a single sample is embedded into a matrix of context length $X$ embedding dimension. These then enter the transformer blocks, and exit having the same dimensions. These are then inputted into the un-embedding layer (same dimension as the embedding matrix), and are transformed to a distribution over possible token - context length X vocabulary size. Each position is trained to predict the next token, and so these distributions are compared with the observed next tokens using cross-entropy to match the observed distribution. We also added positional encoding 25 to model the global positions on the tokens in the sequence. To create a generative autoregressive model, we used a causal masking technique 25 during training. This approach ensures that the attention mechanism only considers past tokens as context, effectively preventing access to information from future tokens.  

# Pretraining and Optimization  

The objective during pretraining was to forecast subsequent tokens using a causal masking technique. This task was structured to enhance predictive accuracy by learning from unmasked tokens to predict the subsequent masked ones, employing cross-entropy loss calculated across the distribution of the 460 possible tokens.  

# Optimization Details  

Model optimization was conducted using the AdamW optimizer 49 with a learning rate of 3e-5, with no weight decay, and dropout at 0.1, with batch size of 32 per GPU (effective batch size of $32\mathrm{X}8=$ 256). A StepLR scheduler was applied to adjust the learning rate with a decay factor of 0.99 every 10 steps over a total of 100 epochs. Model selection was based on performance metrics from the validation set, accounting for $10\%$ of the data. The final model was evaluated using the test set, also representing $10\%$ of the data. Training was performed on 8 NVIDIA A40.  

# Producing an Output Embedding per Sample  

To represent each CGM sample, we wanted to use the output of the model, to get the processed version of the sample. Each CGM sample, containing 1200 glucose measurements (tokens), is passed through the transformer, which outputs a 1024-dimensional vector for each token. We keep these vectors in the high-dimensional representation space rather than convert back to token probabilities. Aggregation of Vectors: We needed to reduce the 1200 vectors from each sample into a single representative vector. We evaluated three pooling methods: Average Pooling: Calculates the mean of the 1200 vectors, assuming equal contribution from all time points.  

Maximum Pooling: Selects the maximum value for each of the 1024 dimensions across the 1200 vectors, highlighting the most prominent features in the sequence.  

Minimum Pooling: Selects the minimum value for each dimension, capturing the lowest bounds of the glucose measurements.  

Note, we removed the ${\mathrm{<MASK>}}$ token before doing any of the pooling methods, to remove any non-informative data from the representation.  

Evaluation and Selection: These methods were evaluated based on their ability to predict clinical outcomes using embeddings generated from the validation set. Max-pooling emerged as the most effective method, consistently providing better performance in predicting key clinical measures like HbA1c.  

# CGM-Derived Clinical Metrics Using iglu  

To extract meaningful clinical insights from Continuous Glucose Monitoring (CGM) data, we utilized the R package iglu 38,50) . Iglu is designed to derive a comprehensive set of metrics from CGM data, which are pivotal in assessing glucose control and variability across individuals.  

# Functionality and Application of iglu  

Iglu integrates advanced computational algorithms to process CGM data, providing more than just basic reading and organizing functionalities. Unlike other tools which may offer limited analysis capabilities, iglu supports a full spectrum of CGM-derived metrics. This tool facilitates an in-depth evaluation of glucose dynamics, enabling the categorization of glucose management into several clinically relevant aspects 51.  

Mean-glucose measures: Metrics such as Mean Glucose Levels and estimated A1C (eA1C) are calculated to evaluate glycemic control.   
Postprandial Glucose Adaptation: Measures like Standard Deviation (SD) and Mean Amplitude of Glycemic Excursions (MAGE) assess responses to meal intake.   
Composite and Range Metrics: This includes Time in Range (TIR) and the J-Index, which provide insights into overall glucose exposure and variability.  

All iglu measurements used in this study are detailed in ref, see Table S2.1.  

# Predictive Modeling of Medical Measures on HPP Using Embeddings vs iglu  

To evaluate the predictive power of GluFormer embeddings for future health outcomes, we conducted a series of analyses targeting a broad range of clinical metrics. These metrics included blood tests, body measurements, anthropometric data, and body composition parameters such as muscle and fat mass. The primary goal was to assess the ability of GluFormer embeddings to forecast these health metrics over different time horizons, thereby validating their clinical applicability.  

For each health metric, we trained a ridge regression model using either iglu measures and GluFormer output embeddings as input features. The embeddings, representing the CGM data for each participant, were used to predict various clinical metrics recorded for those individuals. Specifically, we used a KFold cross-validation approach, dividing the data into 5 folds and iteratively using each fold as the test set while aggregating results across all folds. We used this aggregated result to compute a Pearson correlation between observed and predicted values for all samples in the set. This process was repeated 10 times with different random seeds to ensure robustness, and the results were averaged, with standard deviations calculated. We evaluated the significance of our predictions using a permutation test across 100 different seeds, considering results as significant when random performance did not exceed the model performance more than 5 times (P-value $<0.05$ ).  

# Out-of-Cohort Generalization  

To evaluate the generalizability of our model to out-of-distribution (OOD) data, we focused on assessing performance using all datasets that have CGM data, including the Human Phenotype Project (HPP), PNP1, PNP3, BREACPNT, PREDICT, T1DM, GDM, BREAD, IL Healthy, US Healthy, US-Obese, Colas 2019, JDRF CGM RCT, Shanghai T2DM, and Hypoglycemia in Older Adults. Using these datasets we wanted to evaluate the performance of GluFormer under different clinical conditions (T1D, T2D, GDM, etc..), different devices (iPro2, Dexcom, Medtronic etc..), and different geographies (Australia, US, Spain, China).  

# Data Preparation and Embedding for Out-of-Cohort  

To be consistent with the HPP dataset preprocessing, glucose measurements from the external cohorts were discretized using the same bins that were established in the Tokenization section, based on the $80\%$ training partition of the 10,812 participant dataset. If the data was from clinical trials, we further divided into two distinct phases: pre-intervention and post-intervention. We embedded the full sequence of glucose measurements directly into the 1024-dimensional space, applying the max-pooling to generate a single representative vector for each phase of the study.  

# Predicting outcome of Randomized Clinical Trials  

For the Randomized Clinical Trials (RCTs) outcome prediction, we used the pre-intervention CGM GluFormer embeddings and added a binary variable to indicate the allocation of the participants. Each  

RCT had 2 intervention arms, so each representation vector was increased to be of size 1,025, where the last entry was either 0 or 1 depending on their allocation. We then used either iglu or the embeddings to predict the primary and secondary outcomes of the study, evaluating the results using Pearson correlation. The RCT cohorts in this category are PREDICT, BREACP, and PNP3.  

For the open-source datasets, we focused on primary outcomes and, using the same scheme, attempted to predict the primary outcome for each dataset:   
JDRF: We aimed to predict HbA1c at 26 weeks using CGM data from 1-6 months, evaluating the results using Pearson correlation.   
Shanghai T2D: We aimed to predict HbA1c after 26 weeks using 2 weeks of baseline CGM data, evaluating the results using Pearson correlation.   
Colas: We aimed to predict baseline HbA1c using 2 weeks of CGM data, evaluating the results using Pearson correlation.   
Hypoglycemia: We used 1 week of CGM data to predict whether there would be an event of  

hypoglycemia in the following weeks, evaluating the results using ROC AUC.  

# Predictive Modeling of Randomized Clinical Trials  

The predictive analysis was again conducted using ridge regression, consistent with our previous methodological approach to ensure comparability. We used ridge regression with KFold optimized over 10 different seeds. P-values were obtained over a permutation test over 100 different seeds.  

# Comparative Analysis of SSL, Plain Transformer, and CNN Models  

This section outlines the comparative performance of four distinct models—GluFormer, a Transformer with the same architecture as GluFormer, Frozen GluFormer Embeddings, and Convolutional Neural Network (CNN) - in downstream task of prediction HbA1C from CGM, as detailed in Supp Figure S2. Each model was trained using the same dataset, evaluated on the same validation and test sets to ensure comparability. The split was $80\%$ train, $10\%$ validation, $10\%$ test.  

# Fine Tuning the Pretrained CGM Transformer  

To tailor the GluFormer architecture for the specific task of HbA1C prediction, we modified its output mechanism. Initially trained to predict the next token, the model’s output layer transformed embeddings into the token space. For fine-tuning, we replaced this output layer with a 1D adaptive pooling layer that aggregates the 1200 embeddings into a single vector. We then added a small, 3-layer MLP with GELU activation and a single neuron output to predict the measure from this vector. The fine-tuned model was optimized using Mean Squared Error (MSE) for regression tasks and employed the AdamW optimizer.  

# Training CGM Transformer from Scratch (No SSL)  

To evaluate the intrinsic benefit of SSL, a CGM Transformer model with the same architecture (including the transformer backbone, the 1d pooling, and the 3-layer MLP) was trained from scratch with randomly initialized weights. This approach aimed to isolate the effect of SSL from the architectural benefits. The model was optimized using MSE, with AdamW.  

# Finetuning Frozen Transformer Embeddings  

In this variant, the Transformer's weights were frozen, and only the added 1D adaptive pooling layer and the 3-layer MLP were trained. This model setup tested the efficacy of the transformer embeddings when not allowed to adapt during the training of the downstream task. Optimization and hyperparameter tuning followed the same protocol as the other models, focusing on MSE and AdamW optimization.  

# CNN Model  

A convolutional neural network (CNN) was also tested for comparison. The CNN model was extensively tuned across a range of hyperparameters, including different kernel sizes, numbers of layers, and MLP configurations. The best-performing setup in the validation set featured a five-layer CNN with a kernel size of 3, followed by a 3-layer MLP. This model was similarly optimized using MSE with AdamW.  

# Temporal Modeling  

To capture the temporal impacts of glucose fluctuations over time, we incorporated date & time information into our model. We explored two methods to directly integrate temporal information into the embeddings used by our transformer model.  

# 1. Temporal Positional Encoding  

Building on the positional encoding framework presented in “Attention is All You Need,” we introduced additional sine and cosine waves to represent temporal dimensions. This method, we named “temporal positional encoding”, extends traditional positional encoding by incorporating time-specific waveforms corresponding to minute, hour, day of the week, and month.  

To tailor these encodings to the physiological context of glucose measurements, we adjusted the phase and wavelength of the sine and cosine functions to align with real-world time cycles.  

# 2. Learned Temporal Embeddings  

Our second approach involved the use of learned embeddings for temporal values—minute, hour, day of the week, and month. These embeddings were added directly to the corresponding data embeddings within the transformer architecture. Unlike the fixed mathematical formulations of sinusoidal encodings, these learned embeddings were optimized during training, allowing the model to dynamically adjust and refine its understanding of time as it related to physiological changes and glucose measurements.  

In practice, the learned temporal embeddings outperformed the sinusoidal temporal positional encoding is the generation task over the test set (see Fig.S5).  

# GluFormer with Diet Tokens  

# Preprocessing of CGM and Diet Data  

To integrate continuous glucose monitoring (CGM) data with dietary logs, we established a preprocessing pipeline that combines these datasets, ensuring accurate alignment and comprehensive representation of nutritional intake alongside glucose measurements. Glucose measurements were recorded every 15 minutes, and dietary intake was aligned to the nearest 15 minute glucose measurement. Additionally, the diet was further broken into its macronutrient values.  

Data Collection and Initial Processing: We collected CGM and dietary data from 10,844 participants. The CGM device recorded glucose levels subcutaneously at regular intervals, while participants logged dietary intake through a mobile application, detailing their consumption of calories, carbohydrates, proteins, lipids, and water.  

Temporal Alignment and Data Cleaning: Dietary entries were aligned with CGM timestamps to ensure temporal correspondence between nutrient intake and glucose readings. We excluded any dietary data not temporally coinciding with CGM records. Additionally, glucose values were clipped to a physiological range of 40 to $500~\mathrm{mg/dL}$ , and nutrient values exceeding the 99th percentile were trimmed to reduce the impact of outliers.  

Caloric and Meal Filters: Entries from participants who logged less than 1,000 calories throughout the monitoring period were removed. Days with total caloric intake outside the range of 500 to 7,000 calories, or with fewer than three meal logs, were also excluded to maintain consistency in dietary patterns.  

Data Imputation: In rare instances of device recording lapses, missing CGM measurements were linearly imputed to maintain a continuous glucose profile.  

Meal Consolidation and Adjustment: Multiple dietary logs recorded within the same hour were consolidated into a single meal entry to simplify the dataset. Optionally, we adjusted meal timings to correlate better with observed glucose spikes, enhancing the model’s ability to associate dietary intake with glycemic responses. This was done by observing that high sugar meals that did not have a subsequent spike in blood glucose, were probably mis-logged, and so we looked in a window of an hour before and after the meal to see it we can locate a glucose spike - if we found one, we moved the logging to be 15 minutes before the spike.  

Data Binning and Tokenization: Nutrients were categorized into quantile-based bins, facilitating uniformity in representation. Similarly, minutes were binned into 15-minute intervals to synchronize with the frequency of CGM recordings. Glucose measurements and nutrient intakes were then discretized and tokenized into integers, providing a standardized scale for model input.  

Statistics: The preprocessing steps reduced the initial dataset from 10,844 to 5,875 participants, with the number of analyzable days decreasing from 76,862 to 57,137. This refinement was crucial in ensuring that the dataset comprised only the most reliable and representative entries for model training.  

Usage: The models that used this preprocessing were the models using temporal information, as well as the diet variant. Previous results, used the previous preprocessing that does not take into account temporal or nutrient based information.  

# Tokenization and Temporal Encoding  

To effectively process and analyze the CGM and dietary data within our GluFormer $^+$ Diet model, a comprehensive tokenization strategy was adopted as detailed above. This approach not only standardizes the data but also integrates crucial temporal information, facilitating the model’s ability to capture temporal dynamics associated with glucose fluctuations and dietary intakes.  

One-Dimensional Sequence Formation: Both CGM and dietary data were tokenized into a unified one-dimensional sequence. This linear sequence format is crucial for the model, allowing it to process time-series data as a continuous stream of events, which is essential for capturing the dynamics of glucose responses and nutrient effects over time.  

Incorporation of Temporal Tokens: Alongside each glucose and diet token, we included four additional temporal tokens representing the minute, hour, day of the week, and month. These tokens are vital for providing the model with context about the timing of glucose readings and dietary logs, enriching the input data with layers of temporal granularity. For diet-related tokens, time does not progress between entries on macronutrients of the same log.  

Tokenization Details: All glucose measurements and nutrient values were discretized into predefined bins before tokenization, ensuring that each entry conforms to a standardized integer value. Glucose values were tokenized as before - into integer units, and diet nutrients were binned into bins based on quantiles.  

The nutrients used for the diet a   
1. Calories (kcal)   
2. Carbohydrates (grams)   
3. Protein (grams)   
4. Caffeine (mg)   
5. Water (grams)   
6. Total Lipid (grams)   
7. Alcohol (grams)   
8. Sugars Total (grams)  

The bin values:   
energy_kcal: [0.02, 31.68, 84.52, 146.04, 195.00, 262.12, 340.58, 423.10, 518.50, 623.53, 745.56,   
891.08, 1069.25, 1317.02, 1726.57, 5832.24]  

carbohydrate_g: [0.00, 3.47, 9.05, 15.00, 21.60, 28.87, 36.13, 43.08, 51.81, 61.97, 73.86, 88.02, 106.90, 132.38, 177.13, 608.09]  

protein_g: [0.00, 0.66, 1.63, 2.81, 4.42, 6.80, 9.61, 13.64, 18.23, 23.76, 30.46, 38.61, 49.34, 65.22, 93.21, 354.53]  

caffeine_mg: [0.30, 188.52, 377.04, 754.08, 2639.28] water_g: [0.00, 4.56, 36.15, 78.24, 129.46, 182.26, 247.63, 311.44, 389.16, 468.20, 498.60, 575.58, 687.39, 855.37, 1109.35, 4507.10]  

totallipid_g: [0.00, 0.41, 0.89, 2.59, 5.68, 8.74, 11.97, 15.84, 19.97, 24.95, 30.71, 37.91, 47.38, 60.38, 83.04, 306.73]  

alcohol_g: [0.02, 0.88, 2.60, 6.60, 9.90, 13.20, 18.00, 20.00, 26.40, 28.80, 33.00, 49.50, 66.00, 172.84]  

sugarstotal_g: [0.00, 1.25, 2.82, 4.67, 6.88, 9.27, 12.12, 14.70, 18.02, 22.04, 26.04, 31.28, 37.90, 48.22, 65.61, 266.78]  

This method simplifies the model’s processing by reducing the complexity of input data and ensuring consistency across the dataset.  

Parallel Temporal Information: To ensure that the model recognizes the sequence of events accurately, temporal tokens accompany each glucose or diet token without advancing time unnecessarily during diet entries. This approach keeps the temporal data consistent and precise, reflecting the actual timing of meals and glucose measurements without artificial shifts.  

# Transformer Configuration  

The GluFormer $^{+}$ Diet model employs a transformer architecture that has been specifically tailored to handle both CGM and dietary data effectively. This setup enables the model to learn from the complex relationships between nutrient intake and glucose levels while incorporating temporal dynamics. Here are the key components of the model’s architecture:  

Embedding Size: Each input token is represented in a 1024-dimensional space.  

Heads and Layers: The model features 8 attention heads and 10 transformer layers.  

Feedforward Dimension: A dimension of 2048 for the feedforward networks in each transformer block.  

# Additional Training Parameters  

The model is trained on sequences that include both glucose and diet tokens. However, the diet tokens serve exclusively as contextual information. The predictive task is focused on forecasting glucose tokens only. This selective prediction approach helps the model specialize in glucose dynamics while still understanding the impact of dietary inputs as contextual modifiers.  

# Positional and Modality Encodings  

Positional Encoding: Traditional positional encodings are utilized to preserve the order of tokens within the sequence, which is crucial for the model to understand sequence-dependent changes in glucose levels.  

Modality Tokens: Each token type (glucose, calories, sugars, carbohydrates, proteins, lipids, alcohol, water) is associated with a learned modality embedding. These embeddings are added to the input embeddings and provide the model with information about the nature of each token, enhancing its ability to process mixed data types effectively. This is similar to segment embeddings in BERT (ref), where they add learned embeddings to indicate sentence structure.  

Temporal Positional Encoding: To integrate temporal information more directly, the model includes an additional positional encoding for time:  

Non-Learned Temporal Encoding: The last eight dimensions of the embedding space are reserved for sinusoidal positional encodings that represent minute, hour, week, and month. Each unit of time is encoded using both sine and cosine functions, resulting in eight dimensions that help the model grasp the cyclic nature of time.  

This encoding ensures that at any point in the sequence, the model has immediate access to precise temporal information, enhancing its ability to make time-sensitive predictions.  

Temporal Learned Tokens  

Alongside the static temporal encodings, the model also incorporates learned temporal tokens for minute, hour, day, and month. These tokens are pre-processed and added to each token’s embedding before entering the transformer blocks. This setup allows the model to adjust its response based on learned patterns associated with specific times, providing a dynamic and responsive predictive mechanism.  

# Statistical analysis of generation  

To evaluate the quality of the generated samples, we ran GluFormer in an autoregressive manner to generate whole CGM days on unseen test samples. To evaluate them we compared them using correlation computed over each sample. P values for the correlations were determined using a two-tailed t-test.  

# Optimization and Training Details  

For optimizing the GluFormer $^+$ Diet model, we utilized a carefully configured setup designed to promote stable learning while effectively minimizing the loss over time. Here’s a detailed overview of the optimization parameters and training conditions:  

Optimizer: AdamW, a variant of the Adam optimizer that incorporates weight decay, was selected for its robustness and effectiveness in managing sparse gradients and complex dependencies in high-dimensional data.  

Learning Rate (lr): Set at 0.0001, this relatively low learning rate helps prevent the model from overshooting minima, allowing for finer adjustments in weight updates.  

Beta Coefficients (b1 and b2): Values of 0.9 and 0.99 for the first and second moment estimates, respectively, balance the trade-off between momentum and stability.  

Weight Decay: A value of 0.01 is used to regularize and prevent overfitting, particularly useful in complex models with a high capacity like this transformer.  

Learning Rate Scheduler: Employing a gamma of 0.0001, the learning rate decays by this factor, gradually reducing the step size to fine-tune the model’s weights as training progresses.  

# Training Dynamics  

Epochs: The model is trained for 20 epochs, providing sufficient time for the complex patterns in the dataset to be learned without leading to excessive training times.  

Dropout: Set at 0.2, dropout is used as a regularization method to prevent overfitting by randomly dropping units (along with their connections) during the training process.   
Batch Size per GPU: 16 samples per batch,  

# Hardware and Computational Details  

GPU: The training utilizes a single NVIDIA A100, known for its powerful computational capabilities and efficiency in handling large datasets and complex models.  

Floating Point Precision: Training is conducted using 16-bit floating point precision (FP16), which reduces memory consumption and can speed up training without significantly impacting the accuracy of the results.  

Gradient Clipping: A maximum gradient norm (max_grad_norm) of 1 is used to prevent the exploding gradient problem, which can lead to destabilized training dynamics.  

Random Seed: A consistent numpy, torch, and random math seed of 42 is set to ensure reproducibility of the results, enabling consistent initialization and stochastic processes across different runs.  

Warm-Up Phase: The model employs 100 warmup steps at the start of training. This gradual ramp-up in learning rate helps stabilize the model’s parameters before entering the full training regime.  

# Comparative Analysis Setup: GluFormer With and Without Diet  

To rigorously evaluate the impact of integrating dietary data into the GluFormer model, we conducted a comparative analysis between two versions of the model: one incorporating diet data (GluFormer $^+$ Diet) and the other excluding it (GluFormer). This comparison aims to assess the added value of dietary information in enhancing the model’s predictive accuracy and understanding of glucose dynamics.  

# Data Consistency Across Models  

Unified Preprocessing Pipeline: Both versions of the GluFormer model were trained using the same preprocessing pipeline detailed previously for the GluFormer $^+$ Diet model. This ensures that any  

observed differences in model performance can be directly attributed to the inclusion of dietary data, rather than discrepancies in data handling or preprocessing.   
Identical Datasets: To ensure a fair comparison, the training, validation, and test sets were identical across both model variants. This approach eliminates variability in data distribution as a confounding factor, allowing for a clear assessment of the impact of diet data integration.   
Hyper parameter search for these models was in this values:   
Beta Coefficients (b1 and b2):   
b1: {0.85, 0.88, 0.9}   
b2: {0.9, 0.95, 0.99}   
Diet Modeling (diet_modeling):   
Values: {true, false} — Determines whether dietary data is incorporated into the model.   
Dimension of Feedforward Network (dim_feedforward): {512, 2048}   
Dropout Rate (dropout): {0, 0.1, 0.2} —   
Number of Training Epochs (epochs):{10, 15, 20, 30}   
Learning Rate Decay: {0.1, 0.01, 0.001} — Specifies the ration between starting lr (after warm up), and ending lr   
Learning Rate (lr): {1e-06, 1e-05, 0.0001, 0.0005, 0.001}   
Maximum Gradient Norm):{1, 10, 100}   
Embedding Size (n_embd): {256, 512, 1024} — Size of each token embedding.   
Number of Attention Heads (n_heads): {8, 16}   
Number of Transformer Layers (n_layers): {8, 10, 12, 16}   
Warmup Steps: {10, 100, 1000} — Number of steps to increase the learning rate at the beginning of training.   
Weight Decay: $\{0,\,0.001,\,0.01,\,0.1\}$  

Data   

![](images/46406ca827c2e77e49da7472d257ce0c0e5ccc5c63605329e1d6219da07b536c.jpg)  

![](images/a9292a139e8ba2a3c297dda8e1087632cebc7def15d478fd69652a37b9daaac2.jpg)  

# Declarations  

# Acknowledgments  

We thank all Segal lab members, Pheno.ai data science members, and NVIDIA, Tel Aviv, Research group members  

# Ethical approval  

All participants signed an informed consent form upon arrival to the research site. All identifying details of the participants were removed prior to the computational analysis. The 10K cohort study is conducted according to the principles of the Declaration of Helsinki and was approved by the Institutional Review Board (IRB) of the Weizmann Institute of Science.  

# Data availability  

The data used in this paper is part of the Human Phenotype Project (HPP) and is accessible to researchers from universities and other research institutions at:  

https://humanphenotypeproject.org/data-access. Interested bona fide researchers should contact  

# Code availability  

Implementation of GluFormer is available at: https://github.com/Guylu/GluFormer  

# Competing Interests  

G.S.. and H.R. are employees in Pheno.AI Ltd. a biomedical data science company from Tel-Aviv, Israel. E.S. is a paid consultant of Pheno.AI Ltd. Other authors declare no competing interests.  

G.L’s work was done during an internship at NVIDIA Research.  

# Author contribution  

G.L conceived the project, designed and conducted all analyses, interpreted the results, and wrote the manuscript. G.S developed protocols, interpreted the results, and wrote the manuscript. A.G designed pipelines and created preprocessing scripts. S.S reviewed the manuscript. J.R.G & D.S.B acquired the PREDICT cohort. S.M guided computational analyses. E.M guided computational analyses and managed code running infrastructure. G.C directed the project. H.R conceived and directed the project and analyses, designed the analyses, interpreted the results and wrote the manuscript. E.S. conceived and directed the project and analyses, designed the analyses, interpreted the results and wrote the manuscript.  

Supplementary Appendix  

![](images/1cf27fe404b3cb3917458e0661d538566a6d0702b451037fd526915113704433.jpg)  

Figure S1.A: UMAP of GluFormer embeddings of HPP cohort, colored by their independently taken blood HbA1C results.  

![](images/80b2d6ca54e19a6aa55e355a8d4f15c6854f4c8903688778abb30ad21daacf25.jpg)  
Figure S1.B: UMAP of GluFormer embeddings of HPP cohort, colored by their independently taken DXA visceral fat mass results.  

![](images/f93267b04532e8b68a0e1d063aeafbb9c8cc4002e75a736fe6563919ec8475a5.jpg)  

Figure S1.C: UMAP of GluFormer embeddings of HPP cohort, colored by the percentage of time their CGM values were above 140 (left), and below 70 (right)  

![](images/e2b1fcf72b05bf3a4baa46c96bd07b9e2fe922f25fbb1fb4459b70b3719b8937.jpg)  
umap by age  

Figure S1.D: UMAP of GluFormer embeddings of HPP cohort, colored by participants' age at CGM recording time.  

![](images/e78b4596bc10d5fb60d0096a54e4cfcde72cb293806f2b1926d4a81fb823510e.jpg)  
Figure S1.E: UMAP of GluFormer embeddings of HPP cohort, colored by participants' gender at CGM recording time.  

![](images/ef750d05c97619b2789ae086e8b68e9f5c20dca25785affb613455b0b4d13490.jpg)  

Figure S2: Performance of different models on CGM data predicting HbA1C.  

![](images/6189ae20c6336c56e13fa0edcc269de684558fbc8859ea2561d2d1219668e503.jpg)  

Figure S3: CDF of distances of iglu measures between observed HPP test set samples and generated samples given differing context length (left). Value of CDF at 50th percentile for differing context length. Distances become shorter as we add more context, suggesting GluFormer is able to make use of more context from participants to generate better CGMs.  

![](images/565a69927c65cf0a517b9eeab3437885f84c704e00cd20e5239af70d613740a4.jpg)  
Figure S4: Pearson correlations of iglu measures between observed HPP test set samples and generated samples given differing context length. Correlations become higher for all  

iglu measures as we add more context, suggesting GluFormer is able to make use of more context from participants to generate better CGMs.  

![](images/e47d37ebda8ea7853b522e32ea8ce22a3f81abe3ec921c4980b77ef270728cd5.jpg)  

Figure S5: Pearson correlations of generated CGM vs observed CGM on HPP test set. We can see that adding temporal date and time information increases performance by XXX, and adding diet tokens increases performance even more to 0.5.  

![](images/6fe0f20be3c49edfa8d4b4510c93717cf49b90fda5316cb77557f0d3c0d0e9b5.jpg)  
Figure S6: Example of a typical CGM recording with diet information.  

![](images/11d6920ef7efdcb72fe0e9bca2552208f374f6da45368420f8d8a4f0cb0d5dc5.jpg)  

Figure S7: Example of the hierarchy of food items from food categories, to names, and macro-nutrient features.  

![](images/a148b519ff2fb84c3270bf2ad93381f9b45aa156a5969e6e98cf4344e635208a.jpg)  

Figure S8: Showing results of generation of CGM with and without diet for different random seeds, showing the generatio is robust to seed configuration.  

![](images/f0d556a12ecf38c6f7ef8482d01b4b7e0247c250ca4a3c232571a4ce56f85105.jpg)  
Histogram of CGM Signal Length   
Figure S9: Histogram of lengths of CGM recordings on HPP. Showing why we chose to cap at 1200 measures per sample.  

![](images/c8355a25ccd073d05dab80efbc56867401a0a80d63882b09b18d1c2e076e6f0f.jpg)  
Figure S10: Histogram of daily caloric intake before preprocessing (left), and after preprocessing  

# (right).  

Bibliography  

1. Saab, K. et al. Capabilities of Gemini Models in Medicine. arXiv (2024) doi:10.48550/arxiv.2404.18416.   
2. [2406.06474] Towards a Personal Health Large Language Model. https://arxiv.org/abs/2406.06474.   
3. Zhou, Y. et al. A foundation model for generalizable disease detection from retinal images. Nature   
622, 156–163 (2023).   
4. Zhang, J. et al. RETFound-enhanced community-based fundus disease screening: real-world evidence and decision curve analysis. npj Digital Med. 7, 108 (2024).   
5. Yuan, H. et al. Self-supervised learning for human activity recognition using 700,000 person-days of wearable data. npj Digital Med. 7, 91 (2024).   
6. Thapa, R. et al. SleepFM: Multi-modal Representation Learning for Sleep Across Brain Activity, ECG and Respiratory Signals. arXiv (2024) doi:10.48550/arxiv.2405.17766.   
7. Chen, R. J. et al. Towards a general-purpose foundation model for computational pathology. Nat. Med. 30, 850–862 (2024).   
8. Krishnan, R., Rajpurkar, P. & Topol, E. J. Self-supervised learning in medicine and healthcare. Nat. Biomed. Eng. 6, 1346–1352 (2022).   
9. GBD 2021 Diabetes Collaborators. Global, regional, and national burden of diabetes from 1990 to   
2021, with projections of prevalence to 2050: a systematic analysis for the Global Burden of Disease Study 2021. Lancet 402, 203–234 (2023).   
10. Khunti, K. et al. Diabetes and Multiple Long-term Conditions: A Review of Our Current Global Health Challenge. Diabetes Care 46, 2092–2101 (2023).   
11. Piché, M.-E., Tchernof, A. & Després, J.-P. Obesity phenotypes, diabetes, and cardiovascular diseases. Circ. Res. 126, 1477–1500 (2020).   
12. Amiri Dash Atan, N. et al. Type 2 diabetes mellitus and non-alcoholic fatty liver disease: a systematic review and meta-analysis. Gastroenterol. Hepatol. Bed Bench 10, S1–S7 (2017).   
13. Ho, I. S. S. et al. Measuring multimorbidity in research: Delphi consensus study. bmjmed 1, e000247 (2022).   
14. Abudawood, M. Diabetes and cancer: A comprehensive review. J. Res. Med. Sci. 24, 94 (2019).   
15. Natesan, V. & Kim, S.-J. Diabetic Nephropathy - a Review of Risk Factors, Progression, Mechanism, and Dietary Management. Biomol Ther (Seoul) 29, 365–372 (2021).   
16. Andreoulakis, E., Hyphantis, T., Kandylis, D. & Iacovides, A. Depression in diabetes mellitus: a comprehensive review. Hippokratia 16, 205–214 (2012).   
17. Chaturvedi, S. K. et al. More anxious than depressed: prevalence and correlates in a 15-nation study of anxiety disorders in people with type 2 diabetes mellitus. Gen. Psych. 32, e100076 (2019).   
18. Kieu, A., King, J., Govender, R. D. & Östlundh, L. The benefits of utilizing continuous glucose monitoring of diabetes mellitus in primary care: A systematic review. J. Diabetes Sci. Technol. 17,   
762–774 (2023).   
19. Moser, E. G., Crew, L. B. & Garg, S. K. Role of continuous glucose monitoring in diabetes management. Avances en Diabetología 26, 73–78 (2010).   
20. Battelino, T. et al. Continuous glucose monitoring and metrics for clinical trials: an international consensus statement. Lancet Diabetes Endocrinol. 11, 42–57 (2023).   
21. Holzer, R., Bloch, W. & Brinkmann, C. Continuous Glucose Monitoring in Healthy Adults-Possible Applications in Health Care, Wellness, and Sports. Sensors 22, (2022).   
22. Zahedani, A. D. et al. Digital health application integrating wearable data and behavioral patterns improves metabolic health. npj Digital Med. 6, 216 (2023).   
23. Shilo, S. et al. Continuous glucose monitoring and intrapersonal variability in fasting glucose. Nat. Med. 30, 1424–1431 (2024).   
24. FDA Clears First Over-the-Counter Continuous Glucose Monitor | FDA. https://www.fda.gov/news-events/press-announcements/fda-clears-first-over-counter-continuous-glu cose-monitor.   
25. Vaswani, A. et al. Attention is all you need. arXiv (2017) doi:10.48550/arxiv.1706.03762.   
26. Shilo, S. et al. 10 K: a large-scale prospective longitudinal study in Israel. Eur. J. Epidemiol. 36, 1187–1194 (2021).   
27. Ben-Yacov, O. et al. Personalized Postprandial Glucose Response-Targeting Diet Versus Mediterranean Diet for Glycemic Control in Prediabetes. Diabetes Care 44, 1980–1991 (2021).   
28. Htet, T. D. et al. Rationale and design of a randomised controlled trial testing the effect of personalised diet in individuals with pre-diabetes or type 2 diabetes mellitus treated with metformin. BMJ Open 10, e037859 (2020).   
29. Shilo, S. et al. Prediction of personal glycemic responses to food for individuals with type 1 diabetes through integration of clinical and microbial data. Diabetes Care 45, 502–511 (2022).   
30. Rein, M. S. et al. BREAst Cancer Personalised NuTrition (BREACPNT): dietary intervention in breast cancer survivors treated with endocrine therapy - a protocol for a randomised clinical trial. BMJ Open 12, e062498 (2022).   
31. Zeevi, D. et al. Personalized nutrition by prediction of glycemic responses. Cell 163, 1079–1094 (2015).   
32. Juvenile Diabetes Research Foundation Continuous Glucose Monitoring Study Group et al. Continuous glucose monitoring and intensive treatment of type 1 diabetes. N. Engl. J. Med. 359, 1464–1476 (2008).   
33. McInnes, L., Healy, J. & Melville, J. UMAP: Uniform Manifold Approximation and Projection for Dimension Reduction. arXiv (2018) doi:10.48550/arxiv.1802.03426.   
34. Krizhevsky, A., Sutskever, I. & Hinton, G. E. ImageNet classification with deep convolutional neural networks. Commun. ACM 60, 84–90 (2012).   
35. Manning, C., Raghavan, P. & Schütze, H. Introduction to information retrieval. (Cambridge University Press, 2008).   
36. LeCun, Y. & Yoshua, B. Convolutional networks for images, speech, and time series. The handbook  

of brain theory and neural networks 3361, (1995). 37. LeCun, Y. et al. Handwritten Digit Recognition with a Back-Propagation Network. Advances in Neural Information Processing Systems (1989). 38. Broll, S. et al. Interpreting blood GLUcose data with R package iglu. PLoS ONE 16, e0248560 (2021). 39. Balestriero, R. et al. A Cookbook of Self-Supervised Learning. arXiv (2023) doi:10.48550/arxiv.2304.12210. 40. Cersosimo, E., Solis-Herrera, C., Trautmann, M. E., Malloy, J. & Triplitt, C. L. Assessment of pancreatic $\upbeta$ -cell function: review of methods and clinical applications. Curr. Diabetes Rev. 10, 2–42 (2014). 41. Abdul-Ghani, M. A. et al. The relationship between fasting hyperglycemia and insulin secretion in subjects with normal or impaired glucose tolerance. Am. J. Physiol. Endocrinol. Metab. 295, E401-6 (2008). 42. Brown, T. B. et al. Language models are few-shot learners. arXiv (2020) doi:10.48550/arxiv.2005.14165. 43. Matabuena, M., Petersen, A., Vidal, J. C. & Gude, F. Glucodensities: A new representation of glucose profiles using distributional data analysis. Stat. Methods Med. Res. 30, 1445–1464 (2021). 44. Danne, T. et al. International consensus on use of continuous glucose monitoring. Diabetes Care 40, 1631–1640 (2017). 45. Buscemi, S. et al. Glycaemic variability and inflammation in subjects with metabolic syndrome. Acta Diabetol. 46, 55–61 (2009). 46. FDA approves first continuous glucose monitoring system with a fully implantable glucose sensor and compatible mobile app for adults with diabetes | FDA. https://www.fda.gov/news-events/press-announcements/fda-approves-first-continuous-glucose-monit oring-system-fully-implantable-glucose-sensor-and. 47. Cefalu, W. T. et al. A global initiative to deliver precision health in diabetes. Nat. Med. 30,  

1819–1822 (2024).  

48. Ahlqvist, E., Prasad, R. B. & Groop, L. Subtypes of type 2 diabetes determined from clinical parameters. Diabetes 69, 2086–2093 (2020).   
49. Loshchilov, I. & Hutter, F. Decoupled Weight Decay Regularization. arXiv (2017) doi:10.48550/arxiv.1711.05101.   
50. Rodbard, D. New and improved methods to characterize glycemic variability using continuous glucose monitoring. Diabetes Technol. Ther. 11, 551–565 (2009).   
51. Keshet, A. et al. CGMap: Characterizing continuous glucose monitor data in thousands of non-diabetic individuals. Cell Metab. 35, 758-769.e3 (2023).   
52. Korem, T. et al. Bread Affects Clinical Parameters and Induces Gut Microbiome-Associated Personal Glycemic Responses. Cell Metab. 25, 1243-1253.e5 (2017).   
53. Mendes-Soares, H. et al. Assessment of a personalized approach to predicting postprandial glycemic responses to food among individuals without diabetes. JAMA Netw. Open 2, e188102 (2019).   
54. Rein, M. et al. Effects of personalized diets by prediction of glycemic responses on glycemic control and metabolic health in newly diagnosed T2DM: a randomized dietary intervention pilot trial. BMC Med. 20, 56 (2022).   
55. Shilo, S. et al. The gut microbiome of adults with type 1 diabetes and its association with the host glycemic control. Diabetes Care 45, 555–563 (2022).   
56. Weinstock, R. S. et al. Risk factors associated with severe hypoglycemia in older adults with type 1 diabetes. Diabetes Care 39, 603–610 (2016).   
57. Colás, A., Vigil, L., Vargas, B., Cuesta-Frau, D. & Varela, M. Detrended Fluctuation Analysis in the prediction of type 2 diabetes mellitus in patients at risk: Model optimization and comparison with other metrics. PLoS ONE 14, e0225817 (2019).   
58. Zhao, Q. et al. Chinese diabetes datasets for data-driven machine learning. Sci. Data 10, 35 (2023).  