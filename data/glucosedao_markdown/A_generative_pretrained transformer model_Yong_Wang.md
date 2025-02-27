# A generative pretrained transformer model for decoding individual glucose dynamics from continuous glucose monitoring data  

Yong Wang  

ywang@amss.ac.cn  

Academy of Mathematics and Systems Science, Chinese Academy of Sciences  https://orcid.org/0000- 0003-0695-5273  

Yurun Lu Academy of Mathematics and Systems Science, Chinese Academy of Sciences  

Dan Liu Department of Endocrinology and Metabolism, Shanghai Jiao Tong University A liated Sixth Peoples   
Hospital   
Zhongming Liang School of Life Science, Hangzhou Institute for Advanced Study, University of Chinese Academy of   
Sciences  

Yitong Liu Institute of Mathematical Sciences, ShanghaiTech University  

Pei Chen School of Mathematics, South China University of Technology  

Rui Liu School of Mathematics, South China University of Technology  

Zhanying Feng CEMS, NCMIS, MDIS, Academy of Mathematics & Systems Science, Chinese Academy of Sciences   
https://orcid.org/0000-0002-5727-3929  

Lei Li Academy of Mathematics and Systems Science, Chinese Academy of Sciences  

Bin Sheng shanghai jiaotong university  https://orcid.org/0000-0001-8510-2556  

Weiping Jia Department of Endocrinology and Metabolism, Shanghai Sixth People's Hospital A liated to Shanghai Jiao Tong University School of Medicine  https://orcid.org/0000-0002-6244-2168  

Luonan Chen  

Shanghai Institute of Biochemistry and Cell Biology, Center for Excellence in Molecular Cell Science.Chinese Academy of Science  https://orcid.org/0000-0002-3960-0068  

Huating Li   
Shanghai Jiao Tong University A liated Sixth People's Hospital  https://orcid.org/0000-0003-0526-   
5545  

# Biological Sciences - Article  

Keywords:  

Posted Date: February 22nd, 2024  

DOI: https://doi.org/10.21203/rs.3.rs-3932671/v1  

License: $\circledcirc\textcircled{\div}\textcircled{\div}$ This work is licensed under a Creative Commons Attribution 4.0 International License. Read Full License  

Additional Declarations: There is NO Competing Interest.  

A generative pretrained transformer model for decoding individual glucose  

dynamics from continuous glucose monitoring data   
Yurun Lu1,2,13, Dan Liu3,13, Zhongming Liang5,6,13, Yitong Liu7, Pei Chen8, Rui Liu8, Zhanying Feng1,9,   
Lei M. Li1, Bin Sheng1012, Weiping Jia3,\*, Luonan Chen4,5,11,12,\*, Huating Li3,\*, and Yong Wang1,2,5,\*   
1.  CEMS, NCMIS, HCMS, MADIS, Academy of Mathematics and Systems Science, Chinese Academy of Sciences, Beijing 100190, China.   
2. School of Mathematics, University of Chinese Academy of Sciences, Chinese Academy of Sciences, Beijing 100049, China.   
3. Department of Endocrinology and Metabolism, Shanghai Sixth People's Hospital Affiliated to Shanghai Jiao Tong University School of Medicine, Shanghai Diabetes Institute, Shanghai Clinical Center for Diabetes, Shanghai 200233, China.   
4. State Key Laboratory of Cell Biology, Center for Excellence in Molecular Cell Science, Shanghai Institute of Biochemistry and Cell Biology, Chinese Academy of Sciences, Shanghai 200031, China.   
5. Key Laboratory of Systems Health Science of Zhejiang Province, School of Life Science, Hangzhou Institute for Advanced Study, University of Chinese Academy of Sciences, Hangzhou 310024, China.   
6. BGI-Research, Hangzhou 310030, China.   
7. Institute of Mathematical Sciences, ShanghaiTech University, Shanghai 201210, China.   
8. School of Mathematics, South China University of Technology, Guangzhou 510640, China.   
9. Department of Statistics, Department of Biomedical Data Science, Bio-X Program, Stanford University, Stanford CA 94305, USA.   
10. Department of Computer Science and Engineering, Shanghai Jiao Tong University, Shanghai 200240, China.   
11. Guangdong Institute of Intelligence Science and Technology, Hengqin, Zhuhai, Guangdong 519031, China.   
12. Pazhou Laboratory (Huangpu), Guangzhou, Guangdong 510555, China.   
13. These authors contributed equally to this work.   
\* Corresponding author.  wpjia@sjtu.edu.cn (W.P.J.), lnchen@sibcb.ac.cn (L.N.C.),   
huarting99@sjtu.edu.cn (H.T.L.), ywang@amss.ac.cn (Y.W.)  

# Abstract  

Capturing glucose dynamics including the rigorous fasting glucose homeostasis and postprandial glucose adaptation is central to the diagnosis, subtyping, early warning, lifestyle intervention, and treatment for type 2 diabetes (T2D). Recently, continuous glucose monitoring (CGM) technology has revolutionized fields to track real-time blood glucose levels and trends, and facilitated safe and effective decision making for diabetes management. Here, we developed an attention-based deep learning model, CGMformer, pretrained on a large-scale and diverse corpus of CGM data from a nationwide multi-center study in China to enable context-specific predictions and clinical applications to individuals. During pretraining, CGMformer gained a fundamental understanding of glucose dynamics, encoded glucose value, fluctuation pattern, hyperglycemia, and hypoglycemia in the attention weights of the model in a completely self-supervised manner. Fine-tuning towards a diverse panel of downstream tasks relevant to the diagnosis and treatment of diabetes and complications using task-specific data demonstrated that CGMformer consistently boosted predictive accuracy. By deciphering individual glucose dynamics, CGMformer allows us to subtype individuals with high T2D risk and identify a specific cluster of lean prediabetes that is easily overlooked by traditional glucose measurements. In particular, applied to dietary modification modelling, CGMformer predicted individual's postprandial glucose response or CGM curve, thereby provided personalized diet prescription suggestion. Overall, CGMformer represents a pretrained transformer model to decode individual glucose dynamics, from which fine-tuning towards a broad range of downstream applications can be pursued to promote T2D early warning and recommendation for therapeutic lifestyle modification in diabetes management.  

# Introduction  

Blood glucose concentration and dynamics of postprandial glycemic response are tightly regulated to make sure enough energy for brain, immune, muscle cells and protection of blood vessels to avoid further complications such as cardiovascular disease, kidney disease and retinopathy1. Type 2 diabetes (T2D) is a dysfunction in glucose dynamics occurred when insulin secretion from pancreatic beta cells is insufficient to compensate for insulin resistance2,3. Current diagnosis of abnormal glucose metabolism relies on single-time-point static measurement or on average measures of overall glycemia, while ignoring glucose dynamics4.  

Continuous glucose monitoring (CGM) system furnishes comprehensive and real-time data on glucose levels, enabling the detection of fluctuations and trends in blood glucose levels throughout the entire day and night5. Most CGMs report glucose levels at five-minute intervals, resulting in a total of 288 glucose readings per day, and can continue for 14 days. This allows people with type 1 diabetes (T1D) or T2D to closely track blood glucose levels and trends without fingerstick readings and combine with an insulin pump in a closed-loop insulin delivery system. Meanwhile, CGM helps individuals at risk of glucose dysregulation make informed decisions about food choices, exercise, and other aspects of diabetes management by knowing about daily glycemic patterns and fluctuations6. It’s crucial to understand the glucose dynamics from CGM data in order to reap its maximum benefit in the research and clinical application of diabetes.  

Recently, the concept of foundation model has revolutionized fields such as natural language understanding such as BERT7, GPT8–10, $\mathrm{\bfPaLM}^{11,12}$ , and LlaMA13 and computer vision such as DALL$\mathrm{E}^{14,15}$ ，Flamingo16, RETFound17, DeepDR18, DeepDR Plus19. It leverages deep learning transformer models pretrained on large-scale general datasets and achieves remarkable performance by fine-tuning towards a vast array of downstream tasks with limited task-specific data7,20. The usage of large volumes of high-quality labels and difficulty to yield meaningful predictions by training a new model from scratch for each isolated task are critical gaps for traditional methods in existing research. Foundation model could acquire broad information during the large-scale pretraining phase and transfer knowledge to a multitude of downstream new tasks. The advent of the self-attention mechanism has further captured large input spaces learnt which elements are most important to focus on in each context, generated context-aware models, and boosted predictions in a wide realm of applications21,22. Glucose dynamics are recorded as time series data in a highly context-dependent way. There are vast differences between individuals due to many factors such as weight, age, changes of pregnancy, diet or exercise. Attention-based transformer models hold promise to context-specific modelling of glucose dynamics from long term continuous time series measurement.  

Here, we proposed CGMformer, an attention-based generative transformer model pretrained on a diverse corpus of CGM data to capture individual’s glucose dynamics and enable clinical applications.  

We collected a nationwide multicenter CGM pretraining datasets with a total 552,096 glucose measurements from 964 participants in China. We then pretrained CGMformer on this dataset using a self-supervised masked learning objective to capture individual’s glucose dynamics into the embedded vectors, which enable diverse clinical applications, including diagnosis assistance, non-diabetes subtyping, and dietary recommendations. Notably, through integrating individual’s dietary records, CGMformer could predict post-meal glucose response or CGM curve by capturing individual response to dietary intake. Overall, CGMformer represents a pretrained deep learning model which provides insights to individual’s overall glucose dynamics in fasting glucose homeostasis and postprandial glucose adaptation and has great potential to assist diagnosis, subtyping, and treatment.  

# Results  

# CGMformer architecture and pretraining  

We develop CGMformer as an attention-based, context aware deep learning model pretrained on largescale and diverse corpus of CGM data to capture individual glucose dynamics and enable clinical applications20. CGMformer takes CGM profiles as input and utilizes the recent advent of self-attention mechanism to gain the fundamental knowledge in the full glucose dynamics across individuals and within individuals due to genetic, dietary, exercise, drugs intake, and various environmental factors. With the extractable contextual individual and time point embeddings integrating with individual’s clinical or lifestyle information, CGMformer is able to help in diagnosis assistance, non-diabetes subtyping, and dietary recommendations (Fig. 1a, Methods).  

First, we collect a pretraining CGM dataset from a nationwide multi-center CGM study, encompassing 964 Chinese subjects from 11 hospitals of 7 provinces or cities in China (Fig. S1a), spanning the years 2007 to $2009^{23-25}$ . This dataset covers diverse glucose management states including 450 individuals with NGT, 169 with IGR, and 345 with T2D, with non-biased age distribution and balanced gender ratio (Fig. 1b, Methods, Table S1). Participants received comprehensive clinical measurements including anthropometrics, glycolipid metabolism, and oral glucose tolerance test (OGTT) (Fig. 1b, Methods, Table S1). Each participant's CGM records were divided into single day time series and remained the median two days with complete full-day CGM records, resulting in 1,917 days CGM records and 552,096 glucose measurements in total (Fig. S2a-c, Methods). When tokenizing the single day CGM, the glucose values are discretized into 260 distinct glucose levels and ranked by time point to mimic a sentence. The discrete tokenization approach offers a flexible and robust model that effectively captures the dynamic patterns and provides tolerance to the CGM measurement error (Fig. 1c, Methods).  

We then processed the assembled corpus through four transformer encoder units, each comprising a self-attention layer with eight self-attention heads and a feedforward neural network layer. Pretraining adopts a masked learning objective, a technique widely used in various domains to enhance the generalizability of foundational knowledge for diverse downstream fine-tuning objectives and applications (Fig. 1c, Methods).  

During pretraining, $45{-}60\%$ tokens within CGM records are masked, and the model is trained by utilizing the context of the remaining unmasked glucose levels to predict the glucose level within each masked position. To glean more insights into abnormal glycemia, we gave tokens representing hyperglycemia and hypoglycemia higher mask weights with TF-IDF weighted masking26. We included sin/cos positional encoding in the transformer to ensure the continuity of time representation (Fig. 1c, Methods). The CGMformer architecture is entirely self-supervised and enables training on unlabeled data. This inherent strength in inclusivity allows for the incorporation of vast amounts of training data without the constraint of requiring large volumes of high-quality labels. We implemented recent advancements in distributed graphical processing unit (GPU) training to execute efficient pretraining on the large-scale dataset27,28. We performed ablation study to choose 128 dimensions for the embedding vector to balance both the accuracy to recover the glucose value and the diagnosis label for the participants (Fig. S3a-b). We also compared the different mask strategies and TF-IDF weighted masking shows the best performance (Fig. S3c-d). Our model retained good performance when restricting the input sequence to fewer measurements with longer measuring intervals, thereby ensuring generativity across various equipment types (Fig. S3e). The mean vectors across all tokens in the final transformer layer serve as the embedding vector for the recorded day. In the case of individuals with multiple days recorded, the mean embedding vector across days is computed and utilized as the embedding vector for the individual, demonstrating superior performance (Fig. S3f).  

# CGMformer captures individual glucose dynamics via self-supervised attention mechanism  

We first show that CGMformer autonomously learns the intricate dynamics of glucose value through the contextual attention weight and low-dimensional vector embedding in a latent space and allows time/day/individual embedding, pathophysiological prediction, and individual glucose prediction. In initial assessments, we scrutinize whether these embedded vectors preserve individual characteristics and effectively convey their clinical implications by representing each individual’s characteristics with the mean vectors of the tokens within the entire input time series. We visually examine these vectors using uniform manifold approximation and projection (UMAP) and label them with each individual’s clinical measurement. Firstly, there is a discernible progression from NGT to IGR and onwards to T2D (Fig. 2a), indicating the consistency between clinically diagnosed diabetes state and glucose dynamics captured by CGMformer. Secondly, these vectors encapsulate HbA1c, FPG, and homeostatic model assessment for insulin sensitivity (HOMA-IS)29 (Fig. 2b, Fig. S4a), which are clinical indexes for blood glucose over the past 3-4 months, glucose value in fasting period, and insulin resistance. Additionally, we comprehensively calculated 48 CGM derived metrics30 in our dataset and they are correlated in some extent with diagnosed diabetes state (Fig. S2a, Methods) and clinical measurement (Fig. S2b), and clustered into three groups indicating glucose homeostasis, adaption, and in-range measure for glucose values (Fig. S2c). We picked three representative metrics in each group: standard deviation (SD), estimated A1C (eA1C)31, and time in range $\mathrm{(TIR)}^{32}$ showing their moderate consistency with CGMformer’s embedded vectors (Fig. 2b, Fig. S4b). This robust representation of both clinical and CGM characteristics in the latent space attest to the effectiveness of CGMformer in encapsulating diverse aspects of an individual's CGM profile, offering a comprehensive perspective for further analysis and clinical interpretation. Importantly, we noticed that our CGM embedded vector better recovering the continuous disease progression while the clinical measurement (Fig. S4a) and single CGM derived metrics (Fig. S4b) tends to show binary changes (Fig. 2b). This encourages us to further investigate CGMformer’s ability to capture the full-time dynamics, combines various statistics, and improve the data representing resolution.  

We analyzed the extractable contextual attention weights of CGMformer for each head concerning specific glucose levels or times to gain insights into how CGMformer captures individual glucose dynamic characteristics. Heatmaps were used to examine those attention weights in various context regarding to glucose concentration and fluctuation $(\mathbf{Fig}.\ 2\mathbf{c})^{7,20}$ . Notably, abnormal glucose levels, encompassing hyperglycemia $({>}180\mathrm{mg/dl})$ and hypoglycemia $({<}70\mathrm{mg/dl})$ , are prominently captured by the attention weights of the first two layers. In contrast, the last two layers demonstrate a heightened focus on specific times, such as the fasting or post-meal periods $(\mathbf{Fig},\,2\mathbf{c})^{32}$ . Clearly distinct layers of CGMformer capture complementary information. This observation supports that CGMformer exhibits a robust capability to capture both static homeostasis (fasting period) and the dynamic adaption to high glucose  (post-meal  period).  Our  layered  architecture  ensures  a  comprehensive  and  nuanced understanding of an individual's glucose profile, further emphasizing the versatility and efficacy of CGMformer in capturing diverse aspects of glucose dynamics.  

Importantly, CGMformer obtains abundant information neglected by traditional single-time-point or on average clinical measurement in both fasting glucose homeostasis and postprandial high glucose adaptation during pretraining. For example, the glucose variation during fasting period and post-meal glycemic rate, are overlooked by clinical measurements including fasting plasma glucose (FPG) and HbA1c. However, those are crucial glucose dynamic characteristics to quantify the blood glucose dysfunction in diabetes and pre-diabetes (Fig. 2d). This allows us to identify a group of NGT participants, noted as high-variance NGT (HV-NGT), with relatively higher fasting period standard deviation and post-meal glycemic rate, and subsequently, higher global standard deviation comparing with other NGTs (Fig. 2d-e). The traditional clinical measurements, including FPG, HbA1c, and postmeal 120 min glucose (PG120), of individuals with HV-NGT remain not significantly different from NGTs (Fig. 2f). However, the embedded vectors of HV-NGTs from CGMformer tend to close to T2D patients in UMAP visualization (Fig. 2g) and are significantly similar to T2Ds comparing with other NGTs (t-test, p-value<2.92e-13, Fig. 2h). HV-NGTs tend to have similar distribution in age and BMI indexes but distant insulin level with NGTs (Fig. S5a). Together this indicates CGMformer can identify a group of NGTs with potential impaired glucose regulation but failed by the static clinical measurement. We further checked the CGM profile for Shanghai_NGT_A183, an example of HVNGTs (Fig. 2i) and its corresponding contextual attention weights in fasting and post-meal period (Fig. 2j). This participant clearly shows normal range of traditional clinical measurements (Fig. 2i), but large glycemic fluctuation during fasting period and quite rapid increase in glucose values after meal in a short time, indicating possible glucose control dysfunction. Other two examples show the attention weights can learn the high variability and hyperglycemia (Fig. S5b) and hypoglycemia during fasting period and low variability in afternoon (Fig. S5c). The promising ability of CGMformer to adeptly capture the abnormal dynamics with contextual attention allows us to perform CGMformer based clinical diagnosis and subtyping of individuals at elevated risk for type 2 diabetes.  

# CGMformer with fine-tuning assists clinical diagnosis and prediction  

We next tested whether the pretrained transformer model could transfer learned knowledge to a diverse set of downstream tasks with limited supervised data via fine-tuning. CGMformer embeds each glucose level at each time point into a 128-dimensional space that encodes the characteristics of glucose dynamics specific to the context of that participant.  One step further, CGMformer integrates the annotation labels of the participant by designing a task-specific fine-tune layer tailored for precise prediction tasks (Fig. 3a). We perform subsequent evaluations aimed to gauge the effectiveness of CGMformer in improving predictions and assisting diagnosis when confronted with a shortage of labeled data across a diverse range of downstream fine-tuning applications.  

Finetuning CGMformer with labeled data assists clinical diagnosis. Clinical diagnosis of IGR or T2D relies on clinical measures, including FPG, HbA1c, and PG120 during OGTT33. After pretraining with unlabeled data from the nationwide multi-center CGM data in China, we first fine-tuned CGMformer with the unseen clinical diagnosis labels during pretraining and compared it with alternative methods. CGMformer achieves average five-fold test accuracy 0.771 for NGT/IGR/T2D three classes and outperforms machine learning methods, such as long short-term memory (LSTM)34 and multi-layer perceptron $\mathrm{(MLP)}^{35}$ , using CGM records as input (Fig. 3b). Particularly, it significantly outperforms the LSTM by $8\%$ percent in terms of accuracy (t-test, p-value $!\!=\!\!0.008]$ ) and demonstrates the advantage of keeping track of arbitrary long-term dependencies in the input sequences by selfattention. Moreover, CGMformer outperforms other feature extracting methods such as SVM and SGD in terms of accuracy (Fig. S6a). When diagnosing T2D from IGR or NGT samples, CGMformer exhibits the highest precision (0.88) and recall (0.86) compared to all baseline methods (Fig. 3c). Again, in binary classification, CGMformer significantly outperforms LSTM and MLP. In addition, CGMformer consistently outperforms the diagnosis based on single metric derived from CGM records, including mean glucose (Mean), SD, MAGE, TIR, and TAR (Fig. 3c, Methods). When we combine these 48 metrics by machine-learning methods including ridge regression, MLP, and SGD (Methods), CGMformer also outperforms those predictors (Fig. S6b, Methods). Furthermore, in cases identified as T2D through various clinical metrics, the diagnostic performance based on LSTM or Mean and  

TAR demonstrates comparable recall rates to CGMformer in instances characterized by elevated fasting plasma glucose (FPG). However, these approaches fall short in predicting cases featuring overarching abnormal glucose dynamics, such as elevated HbA1c and PG120. (Fig. S6c).  

We delve deeper into the alterations of the attention weights after fine-tuning in task-specific supervised training. We found that 17 out of the 32 transformer units exhibit higher attention weights on tokens or time periods associated with homeostasis states, including hypoglycemia tokens and the fasting phase (Fig. S6d-e). This observation aligns with the fact that individuals are primarily labeled based on their fasting clinical measurements, including FPG and HbA1c.  

T1D and T2D have different glucose dynamics. We next conduct diagnosing of T1D/T2D based on CGM data with CGMformer finetuned on this limited labeled data from Zhao et al.36 with 125 subjects including 109 T2Ds and 16 T1Ds. CGMformer consistently outperforms baseline methods including state-of-arts machine learning based diagnosis including $\mathrm{LSTM}^{34}$ and MLP, as well as combining metrics-based predictors in T1D/T2D diagnosis (Fig. 3d, Fig. S6b), with accuracy over 0.9 in fivefold cross validation.  

Predicting T2D complications only from individual glucose dynamics is a relatively harder task due to complicate causes and impacts of macrovascular or microvascular37. We investigated the performance of CGMformer in the diagnosis of diabetic complications based on glucose dynamics. According to labeled data from Zhao et al.36, we further design three prediction tasks including the total complications, macrovascular complications, and microvascular complications. We finetuned CGMformer with the limit label of complications diagnosis, CGMformer achieves accuracy 0.8 in predicting microvascular complications and about 0.7 in macrovascular complications. Again, CGMformer outperforms other machine-learning based methods as well as metrics-based predictors. (Fig. 3e, Fig. S6b).  

Overall, CGMformer demonstrates its capability to achieve accurate clinical diagnosis in various contexts based on a pretrained model and limited labeled data. We show that the predictive power exhibits continuous improvement with an increasing pretraining corpus (Fig. S6f).  

The finetuned CGMformer provides explainable early warning for T2D risk. CGMformer can accurately discriminate low- and high-risk groups for incident T2D based solely on CGM data (pvalue<0.82e16, Kaplan–Meier test, Fig. 3f) in Colas's dataset, which provides follow-up clinical diagnosis of T2D every 6 months (6-72, median 33) in their study. To confirm CGMformer learned the glucose dynamics for early warning, we employ the third-party dynamic network biomarker (DNB) method38–40 to correlate with our results (Methods). The DNB's SD calculation indicated that subjects early-diagnosed by CGMformer exhibited significantly higher variation in glucose dynamics, despite having relatively similar HbA1c levels (Fig. 3g, Fig. S7a-b, Methods). Furthermore, specimens exhibiting elevated SD by DNB are, to some extent, classified as IGR in the fine-tuned CGMformer with non-diabetes follow-up outcomes. This observation implies a notable false positive rate associated with the early warning provided by DNB. In contrast, CGMformer demonstrates a mitigation of such false positives. CGMformer reaches highest area under curve (AUC) and AUPR when predicting instances of T2D development, outperforming SD calculated by DNB and traditional clinical measurements, including HbA1c and FPG (Fig. S7c-d). These findings underscore the potential of CGMformer to provide explainable and clinically relevant early warnings for diabetes by capturing intricate aspects of glucose dynamics.  

CGMformer provides a quantified index for the impairment glucose regulation. We next test the ability of CGMformer in quantifying the impairment of individual glucose regulation from its CGM profile. Comparing with the CGM derived single metric such as eA1C, CV, and TIR, CGMformer integrates  the  embedded  vectors  encompass  abundant  glucose  dynamic  characteristics  and NGT/IGR/T2D label information from the individual in a supervised manner. We proposed a multitask deep learning-based framework to extract an index CGMformer_C, to achieve a more comprehensive understanding of the process of glucose regulatory impairment (Fig. S8a, Methods). A higher CGMformer_C indicates a more severe dysfunction of individual glucose regulation. CGMformer_C demonstrated its comprehensive ability to elucidate the state of glucose regulation and its correlation with clinical diagnosis and measurements on the nationwide multi-center CGM cohort (Fig. S8b-c). On the independent Zhao's dataset, CGMformer_C exhibits a significant correlation with the duration of diabetes (Fig. 3h) as well as other clinical measurements (Fig. S8d), which offers exciting opportunity to use CGM profile to predict T2D duration since longer durations and poorer glucose regulation indicating a higher risk of complications. Moreover, CGMformer_C outperforms existing metrics including TIR, eA1C, and CV in correlating with diverse clinical measurements (Fig. 3i). CGMformer_C also showes a positive correlation with the risk of complications (Fig. 3j) and achieved the highest AUC in predicting complications compared to other CGM-derived metrics (Fig. 3k). The aforementioned results indicates that CGMformer_C achieves a great performance of predicting clinical characteristics and diabetic complications superior to other CGM-derived metrics, providing a valuable tool to evaluate glycemic status in individuals.  

# CGMformer provides non-diabetes subtypes with different risks to develop diabetes  

We next show that CGMformer can enhance the early identification of abnormal glycemic status in individuals with NGT and prediabetes based on CGM data, preceding the onset of clinical manifestation of T2D. As OGTT might fail to capture the complete dynamics of glucose adaptation due to the static time points33,41,42, CGMformer might provide subtypes that are more closely related to diabetes risks and offers possibility for refining diabetes managements.  

Using CGMformer embedded vectors, we performed hierarchical clustering analysis with cosine similarity as distance metrics for the NGT and IGT participants. We identified six clusters showing distinctive median CGM patterns in UMAP visualization (Fig. 4a). Clusters are named according to the percentage of NGTs and T2Ds in the group and roughly there are three clusters as Normal, Pre_I, and Pre_II, with increasing ratio of IGRs. We can further divide the Pre_I, and Pre_II clusters and finally gives one normal cluster and five prediabetes clusters, named as CGMformer_type (Fig. 4a). We summarize the distribution of anthropometrics and pathophysiological characteristics in Table 1 within different time periods (Fig. S9a) and compare the CGMformer_type by correlating with CGM derived metrics (Fig. S9b) and clinical measures (Fig. S9b). The median profiles of CGMs from these subtypes, when juxtaposed with samples from individuals with diabetes, exhibit discernible patterns (Fig. 4b-d, Fig. S9a). Pre_IIb stands out with the highest glucose levels among non-diabetic individuals, closely resembling the diabetic group. During the fasting phase, Pre_IIb exhibits analogous glucose levels to those with diabetes but demonstrates superior glucose adaptation, evident in lower post-meal glucose levels and variance. Conversely, Pre_IIc manifests relatively lower fasting phase glucose levels but experiences substantial glucose fluctuation after meals (Fig. 4b-d). Normal, Pre_Ib, and Pre_Ia performs elevated average glucose concentrateon, but remains similar and relatively low glucose variance. Whereas Pre_IIa, with a higher glucose concentration, shows significantly higher glucose variance comparing with the three subtypes.  

Notably, the majority of participants categorized as Normal, Pre_Ia, and Pre_Ib were diagnosed as  

NGT, while individuals in Pre_IIb were predominantly diagnosed with IGR or IGT/CGI by OGTT41 (Fig. 4e). We further compared with a glucose variation-based subtyping approach, termed "glucotype"4, leverages CGM data and spectral clustering to subtype pre-diabetes based on glucose fluctuations. CGMformer_type demonstrated overall a high concordance with glucotype, but provided a more granular insight into the intricate landscape of glucose dynamics (Fig. 4f). he CGM patterns of CGMformer_type support that those participants show similar fluctuation levels but may be caused by different underlying mechanisms (Fig. 4g).  

We further take insight into the clinical measurements of different CGMformer_type (Fig. 4h). Consistent with the preceding findings, individuals in Pre_IIb exhibit poorer metabolic profiles, marked by advanced age, being overweight or obese, reduced insulin sensitivity, and hyperinsulinemia. Notably, participants classified as Pre_IIc showed lower FPG and PG120 levels but displayed $\upbeta$ -cell dysfunction and insulin deficiency, evident through lower fasting and postprandial serum insulin levels, indicating a role in the pathogenesis of diabetes. Pre_Ia and Pre_IIa both present with a slight insulin deficiency and relatively low insulin sensitivity. Pre_IIa, characterized by higher age, suggest potential age-related glucose regulatory changes. Pre_Ib mostly exhibit similar clinical measurements to the normal subtype, displaying average insulin sensitivity and adequate insulin secretion. We then validate our CGMformer_type of non-diabetes on an independent Colas. Dataset43 (Methods), which conducts longitude follow-up study for the development of diabetes. Participants categorized as Pre_IIb exhibited highest propensity for developing diabetes, $37.5\%$ (3 out of 8) progressed to diabetes. $25\%$ (1 out of 4) in Pre_IIc developed diabetes, while individuals in other subtypes exhibited a lower incidence rate (Fig. 4i). This observation aligns with the preceding results and analysis. To sum up, the CGMformer embedded vector captures the full dynamics in CGM data and allows us to draw a schematic representation of the glucose characteristics of the subtypes on a two-dimensional plane. The $\mathbf{X}$ -axis dimension is for the fasting glucose homeostasis maintains and the y-axis is for postprandial glucose adaptation (Fig 4j). CGMformer_type offers a comprehensive subtyping of nondiabetic individuals, which provides valuable insights into glycemic homeostasis and adaptation mechanisms and yields distinct profiles with variable diabetes risk.  

# CGMformer predicts postprandial glucose and provides personalized dietary recommendations  

Lifestyle management, including dietary and exercise interventions, has proven effective in enhancing glucose control for individuals with diabetes44. Notably, dietary changes exert an immediate and highly correlated impact on post-meal glucose dynamics but individual response to the same meal is highly heterogeneous45,46,  which  highlighting  the  importance  of  personalized  dietary  intervention. CGMformer demonstrated its ability to capture individual’s full glucose dynamics encompassing both homeostasis and adaptive responses to perturbations like meal intake. We utilize its power to predict personalized postprandial glycemic response to real life meals and provides dietary recommendations. We introduce CGMformer_Diet, a model built upon CGMformer, designed to predict post-meal glucose by integrating individual CGM records, real-time glucose data, and dietary information, including nutritional content (Fig. 5a, Fig. S10a, Methods). We combine the CGM data of individual, before meal glucose and dietary perturbation in the latent space and output the post-meal glucose prediction. The model was trained and tested in Zhao’s dataset, aligning meal information with glucose dynamics and considering nutrition content such as calories, carbohydrates, proteins, fats, and dietary fiber.  

CGMformer_Diet demonstrates accurate and robust postprandial glucose prediction with Pearson correlation coefficient with true glucose values larger than 0.8 in the whole 2-hour period (Fig. 5b). It clearly surpasses the baseline model LSTM34 with identical architecture but without the CGMformer encoded vectors as input. This outcome highlights the significance of the vectors encoded by CGMformer during pretraining with unlabeled CGM data and they offer crucial information for understanding individual glucose dynamic characteristics and responses to perturbation (Fig. 5b). We next devised an in-silico dietary perturbation experiment based on the predictive model by leveraging the predictive capability of CGMformer_Diet for individual postprandial glucose dynamics (Fig. S10a, Methods). This requires designing simulated meals with fixed calories and adjusting the ratios of the three major nutrients—carbohydrates, protein, and fat. We chose four different simulated meals with different energy supply ratio of carbohydrates, protein, and fat, including a standard balance meal and three adjusted meals (Methods). These meals served as in-silico perturbations to dietary intake. The model provides various post-meal glucose predictions for different dietary scenarios (Fig. 5c), and the predictions aligned well with the grouped input meals based on energy supply ratios of nutrition, including carbohydrate, protein, and fat (Fig. 5d, Fig. S10b-c). This validation confirms the model's ability to predict postprandial glucose dynamics under different dietary conditions.  

To offer recommendation based on dietary predictions and perturbations, we extract five metrics from postprandial glucose values, including the post-meal mean glucose (Mean), PG120, post-meal max glucose (Max), SD, and AUC. These metrics’ rate of change after perturbation were calculated to compare simulated diets with the standard diet. The results align with the consensus that decreasing carbohydrate intake is beneficial for controlling mean glucose levels and reducing glucose variation (Fig. 5e). Additionally, an increased protein ratio appears to be advantageous, while an excess of fat may contribute adversely to glucose dynamics. The results suggest that CGMformer holds potential for tailoring precise and effective dietary interventions for individuals with diabetes.  

# Discussion  

Considering the occult and heterogeneous pathophysiology of diabetes3, early detection and effective intervention based on individual’s full glucose dynamics are critical for the prevention and management of diabetes. In this study, we developed a context-aware deep-learning model, CGMformer, pretrained on CGM data to enable clinical diagnosis assistant, non-diabetes subtyping, and dietary recommendation. Through self-supervised learning on large-scale unlabeled data, CGMformer gained a fundamental understanding of glucose dynamics, which improved the performance in assisting clinical diagnosis of diabetes and subtyping non-diabetes. CGMformer_Diet is further put forward to provide precise prediction of individual’s postprandial glucose, and further in-silico perturbation of dietary intake indicated its potential to provide recommendations for lifestyle intervention. These results demonstrated that CGMformer may serve as an adjunctive tool to promote the identification of high-risk individuals and the personalized lifestyle intervention for diabetes management.  

The duration of diabetes is closely associated with various manifestation and risk of complications3,37, while diabetes is diagnosed mainly according to blood glucose level at static time points33. CGMformer could capture individual glucose dynamic characteristics and provide more information of diabetes duration. To demonstrate the ability of CGMformer to improve diagnosis and prediction of diabetes and complications, we compared the performance of CGMformer, $\mathrm{LSTM}^{34}$ and MLP35. The performances of CGMformer in detecting diabetes was substantially better regardless of the criteria of diabetes based on FPG, PG120, or HbA1c33. CGMformer also outperformed other methods in the diagnosis of diabetic complications. Furthermore, our model can accurately discriminate low- and high-risk groups for developing diabetes, and reduce the false positive rate for the development of glycemic status. These findings underscore the potential of CGMformer to provide explainable and clinically relevant early warnings for diabetes by capturing intricate aspects of glucose dynamics. Additionally, CGMformer offered a synthesized index, CGMformer_C, that effectively captured the impairment of individual glucose regulation. CGMformer_C demonstrated a significant correlation with diabetes duration, clinical measurements, and the risk of complications, providing a valuable tool for assessing the state of glucose regulation in individuals.  

CGM provides comprehensive and real-time information about glucose levels, and detects the fluctuations and trends of blood glucose throughout the day and night5, which implies rich glucose dynamics neglected by single-time-point or on-average clinical measurement. To the best of our knowledge, CGMformer is the first work to develop an attention-based deep learning model for subtyping of non-diabetic individuals based on CGM data alone, resulting in the identification of six distinct clusters characterized by diverse CGM patterns, clinical characteristics, and risk of diabetes. Prediabetes is characterized by the presence of $\upbeta$ -cell dysfunction and insulin resistance that exist before glucose abnormalities are detectable42. In our study, Pre_IIb was predominantly diagnosed with IGR or IGT/CGI and identified as the very high-risk subtype for diabetes, which exhibited highest propensity for developing diabetes and worst metabolic profile, with advanced age, overweight or obese, and insulin resistance. Interestingly, individuals classified as Pre_IIc had relatively normal BMI and glucose levels, including FPG, PG120, and HbA1c, but showed significantly lower insulin secretion and higher glycemic variability, which indicates potential impaired glucose regulation due to $\upbeta$ -cell dysfunction. Previous studies found that lean patients with T2D had distinct clinical characteristics, gut microbiota, and risks of diabetic complications compared with obese patients with $\mathrm{T}2\mathrm{D}^{47-49}$ . A study of the Hong Kong Diabetes Registry reported that patients with diabetes diagnosed before the age of 40 years had higher risks of all-cause death and cardiovascular–renal events than those diagnosed after that age, and more than $20\%$ of people diagnosed of T2D before the age of 40 years were normal weight50,51. Thus, Pre_IIc, with relatively normal weight and glucose levels, might be overlooked but require early detection and timely treatment. In addition, Pre_IIc seems to be more prevalent in Asian with a 4-fold increase (about $8\%$ in NGT/IGR from our Asian nationwide multicenter cohort while $2\%$ in Cola’s European cohort). The above results suggest that CGMformer could reveal the underlying pathophysiological process of diabetes, and individuals identified as Pre_IIb and Pre_IIc (in total account $16\%$ in NGT/IGR from nationwide multi-center cohort) by CGMformer had a higher risk of diabetes and complications and should be provided with intensive management and timely therapeutic interventions, which is consistent with previous studies2. Further combining with traditional pathophysiology-based subtyping such as NGT/IGR, CGMformer is able to precisely identify individuals at elevated risk for T2D.  

Importantly, CGMformer exhibits great potential in lifestyle intervention recommendations. Previous studies  reported  accurate  postprandial  glycemic  responses  to  simple,  identical,  and  standard meals45,46,52, but such meals are not representative of multicomponent meals in free-living conditions. In our study, CGMformer_Diet demonstrated accurate and robust postprandial glucose prediction based on various meals, suggesting that our model could offer crucial information for understanding individual glucose dynamic characteristics and responses to perturbation. Furthermore, through insilico perturbations of dietary intake, the model demonstrated its potential to offer personalized suggestions for lifestyle modifications based on individualized glucose dynamics. CGMformer_Diet leveraged the rich glucose dynamic knowledge in the encoded vectors to predict glucose responses to dietary perturbation. In this way, our pretraining data does not necessitate perturbation information and laborious workload, including meal data. Additionally, individual previous meal records are not a prerequisite for training, indicating that the model is predictive for any individual with a complete day of CGM records. These findings support that our model may be reliable and informative for developing personalized diet recommendations.  

CGMformer captures individual glucose dynamics by pretraining on extensive unlabeled datasets, employing a transformer attention mechanism. Furthermore, it demonstrates enhanced performance across various clinical tasks through subsequent fine-tuning on limited labeled data. Additional training CGMformer on a wider variety of CGM data and clinical datasets could further improve its performance,  generality,  and  usefulness  across  multiple  populations  as  a  foundation  model. Additionally, future studies and randomized clinical trials are needed to evaluate the effectiveness of integrating CGMformer into clinical workflow.  

In conclusion, we developed a CGM data based CGMformer model to capture glucose dynamics and enable clinical applications. In the supervised scenario, CGMformer demonstrated its proficiency in clinical diagnosis when fine-tuned with specific tasks. For the unsupervised subtyping of non-diabetic individuals, CGMformer identified six distinct clusters characterized by diverse CGM patterns and clinical features. Moreover, we successfully utilized CGMformer to predict post-meal glucose responses, showcasing its ability to provide precise insights into postprandial glycemic patterns and personalized dietary guidance. Taken together, our CGMformer model has great potential to be an ancillary tool for clinical diagnosis assistance, non-diabetes subtyping, and personalized dietary recommendations in diabetes management.  

472 Tables  

473 Table 1. Characteristics of participants in the nationwide multicenter cohort.   

![](images/57a9c3d50baab2b3a3481f00f84f1af6384d8e931a426d7919d695bbbf65f096.jpg)  

![](images/a7c155f1b596d8b310a88f5fc82b97b5a17db652f9d13e8b917a993be9352573.jpg)  

# Methods  

# Datasets  

Nationwide multi-center CGM dataset: The nationwide multi-center CGM study was independently approved by the ethics committee of each hospital in accordance with the Declaration of Helsinki. Chinese subjects were enrolled from 11 hospitals in China from 7 provinces and cities between 2007 and 2009. Written informed consent was obtained from all subjects. Participants recruited to the study were connected to a CGM system (CGMS) sensor (Medtronic, Northridge, CA) for three consecutive days. Meanwhile, clinical measures were taken for the participants including anthropometry, vital signs, and biochemical assessments (liver enzymes, renal function, HbA1c, GA, blood lipid, glucose, insulin, and C peptide). Details of the inclusion and exclusion criteria to the study, biochemical measurements, and anthropometric data collection have been described previously23–25. A total of 964 subjects with complete CGM data were included in this study. Among them, 450 had normal glucose tolerance (NGT), 169 had prediabetes, and 345 subjects had diabetes. We selected a complete 24h CGM data to calculate the following parameters: mean glucose, standard deviations (SD), coefficient of variation (CV), TAR, and TBR.  

Zhao’s dataset: Zhao et al.36 collected CGM data from 112 subjects including 12 T1DM and 100 T2DM patients in Shanghai. The continuous glucose monitoring readings with 3 to 14 days as a period together with the daily dietary information are provided. This dataset also contains the clinical characteristics, laboratory measurements, and medications of the patients.  

Colas’s dataset: Colas et al.43 collected CGM data from 208 subjects with a previous diagnosis of essential hypertension and the exclusion of a previous diagnosis of diabetes mellitus or treatment with antidiabetic drugs. Patients were then followed every 6 months (6-72, median 33) until the clinical diagnosis of T2D or end of study. A diagnosis of T2D was established with either basal glucose tests≥126mg/dl, and/or HbA1c≥6.5, both confirmed in a second measurement.  

# CGM derived metrics  

CGM-derived metrics for glucose control and glucose variability were calculated using the iglu R package30. Iglu provides an accessible tool to obtain comprehensive CGM evaluation metrics, as opposed to other packages which only provide reading and organizing capabilities or only partial summary measures. Pairwise Pearson correlations were calculated to characterize the relationships between CGM-derived metrics and CGM-derived metrics were clustered using hierarchical clustering (Figure S2). As a result, the CGM-derived metrics can be divided into three groups indicting fasting glucose homeostasis, including Mean, eA1C; postprandial glucose adaptation, including SD, MAGE; and others in range and composite metrics, including TIR, J-Index. The detailed descriptions of CGMderived measures are listed in Table S3.  

# CGMformer architecture and pretraining  

CGMformer architecture. CGMformer is composed of four transformer encoder blocks, each composed of a self-attention layer and feed forward neural network layer with the following parameters: input size of 289/97 (The CGM device monitors blood glucose every 5/15 minutes, yielding a total of 288/96 lengths of time-series data throughout a day. With the additional CLS token, it results in a final input of 289/97 lengths of each piece of data), 128 embedding dimensions, 8 attention heads per layer, and 512 feed forward size. CGMformer uses full dense self-attention across the input size of 289/97. Depth was chosen on the basis of the maximum depth for which there were sufficient data to pretrain as it has been established that this approach yields the greatest predictive potential in natural language understanding, computer vision, mathematical problem-solving, and other domains. Detailed parameters in pretraining are listed in Table S2.  

CGMformer pretraining and performance optimization. Pre-training is achieved through a masking-based learning strategy, a method that has shown to enhance the transferability of foundational knowledge acquired during pre-training to a wide range of downstream fine-tuning tasks in other domains. In the pre-training phase, the masking strategy is designed as follows: for each batch of input data, the TF-IDF (term frequency–inverse document frequency) score of each token within the batch is computed and subsequently normalized to determine the actual masking probability, with lower and upper limits set at $45\%$ and $60\%$ . We employed TF-IDF here to highlight the importance of a relatively high or low glucose value in a collection of CGM measurements, adjusted for the fact that some glucose value around hemostasis appear more frequently in general. It’s the product of two statistics, term frequency and inverse document frequency and is a well-established technique in information retrieval and text mining to quantify the weight of a word within a given document26.  

In the context of CGM time-series data, this strategy carries particular significance. In the context of blood glucose time-series data, instances of hypoglycemia $(<\!70)$ and hyperglycemia events $(>\!180)$ are of heightened clinical interest to indicate the potential failure of glucose regulation and insulin production. However, such events represent a minority within the dataset. The computation of IDF (Inverse Document Frequency) accentuates the importance of these events, emphasizing their clinical significance. Meanwhile, TF (Term Frequency) measures the frequency of token occurrence within a sequence, facilitating contextual learning of common tokens. To strike a balance between preventing under-learning and over-learning of tokens, we impose upper and lower limits on the masking probability, maintaining it within the range of $45\%$ to $60\%$ . Formally the TF-IDF is defined as  

$$
\mathrm{idf}(t,D)=\log\,\frac{|D|}{1+\mathrm{df}(t,D)}
$$  

where tf⁡ $(t,d)$ is the frequency of the word $t$ in the document $d$ . idf⁡ $(t,d)$ is the inverse document frequency of word $t$ in corpus $D.\ |D|$ is the number of documents $|D|$ in the corpus. ${\mathrm{df}}(t,D)$ is the number of documents in which the word $t$ has appeared in the corpus $D$ . Specifically, in CGMformer, $t$ represents the blood glucose token, $d$ represents the sequence in which $t$ is located, $D$ represents all sequences entered in a mini-batch.  

The cross-entropy loss is employed to optimize the glucose level token prediction, which is defined as  

$$
\mathcal{L}_{t o k e n s}=\sum_{j\in n_{\mathrm{unk}}}p(x){\mathrm{log}}q(x)
$$  

where $n_{\mathrm{unk}}$ denotes the number of masked tokens. $p(x)$ denotes the predictions and $q(x)$ denotes the real blood glucose token. Detailed parameters in pretraining are listed in Table S2.  

# Ablation study for hyperparameters selection  

To elucidate the hyperparameter selection in our model, we investigated into the influence of key hyperparameters such as hidden space dimension and masking strategies for both pretraining stage and downstream tasks.  

Hidden space dimension. We evaluated the effect of three hidden space dimensions (dim $_{1}{=}32$ , 64, 128) on the reconstruction accuracy of masked tokens during the training phase. For clinical medical significance, we classified the masked tokens into three categories based on the level of blood glucose values, including normal glycemia ( $70{-}180~\mathrm{mg/dl})$ , hyperglycemia $[>\!180~\mathrm{mg/dl}]$ , and hypoglycemia $(<\!70{\mathrm{~mg/dl}})$ . The highest reconstruction accuracy is achieved on all three types of tokens when the hidden space dimension is taken as 128 (Fig. S3a). We further consider the performance of different hidden space representation dimensions on downstream multiclassification tasks. To evaluate whether larger hidden space dimensions lead to better performance, we consider four hidden space dimensions ( $\mathrm{dim}{=}32$ , 64, 128, 256), and find that the hidden space dimension 128 is slightly lower than 64, but higher than the others for the metrics on the multiclassification tasks. Notably, when the hidden space dimension is 256, no better results are achieved (Fig. S3b). To balance token- and sample-level performance, we chose a hidden layer dimension of 128, achieving favorable results in both pretraining and downstream applications, particularly in clinical medicine.  

Masking rate. We explored masking rate deviating from the $15\%$ masking employed in Huggingface Transformers (where $80\%$ of tokens were replaced with ${\mathrm{<MASK>}}$ , $10\%$ with random tokens, and $10\%$ remained unchanged). Experimenting with rates of $15\%$ , $45\%$ , and $60\%$ , we observed increased representational capacity and label classification accuracy as the rate increased from $15\%$ to $45\%$ . However, further increasing the rate to $60\%$ led to a decline in representational capacity (Fig. S3c). We targeted a masking rate within the $45\%{-}60\%$ range. Additionally, considering the clinical significance of CGM data, we implemented an adaptive masking strategy based on each token's TFIDF value, normalized and truncated within the $45\%{-}60\%$ range, which results in a higher mask probability for hyperglycemia and hypoglycemia tokens. Random sampling within this range served as a control experiment, verifying the effectiveness of our adaptive masking strategy in enhancing label classification performance (Fig. S3c-d).  

# CGMformer individual embeddings  

We evaluated two strategies for representing samples: (1) Direct ${\tt C L S}{\tt>}$ Token Representation: Leveraging the ${\tt{<}}\mathrm{{CLS}}{\tt{>}}$ token, specifically designed to encapsulate global sample-level information; (2) Average Token Representation: Capturing a more distributed representation by averaging the embeddings of all tokens within a sample. The results in downstream tasks (finetuned NGT/IGR/T2D diagnosis) revealed no significant differences in performance across these sample representation approaches (Fig. S3f), while the unsupervised UMAP visualization using direct ${\mathrm{-CLS}}{\mathrm{>}}$ token representation revealed a confluence of distinct individuals with diverse labels. Thus we used the average token embeddings from the last layer as representation for individuals.  

# Input sequence length  

Accommodating and harmonizing diverse CGM data formats was a key challenge in our study. Different devices monitor blood glucose at varying intervals, resulting in day-long data lengths of 96 or 288 points. Since our nationwide multi-center data originated from 5-minute monitoring devices, we down-sampled the 288-point sequences to 144, 96, and 48 points (Specifically, we average the values of the three time points in the sequence of length 288 to obtain a point in the corresponding sequence of length 96). Each down-sampled sequence was then used to train a pre-trained model with identical parameters. The dataset with a length of 288 (implying more frequent sampling) achieves the best results in label prediction for NGT/IGR/T2D (Fig. S3e), while the model remains capacity for label prediction after input down-sampling, illustrating the generality of the pretrained model.  

# Contextual attention weights  

Each of CGMformer’s four layers has eight attention heads that are meant to learn in an unsupervised manner to pay attention to distinct classes of blood glucose value to jointly improve predictions. Contextual CGMformer attention weights are extracted for each attention head within each selfattention layer for each blood glucose value within the given CGM sequences evaluated by forward pass through the CGMformer model.  

# Time phase partition  

Fasting phase. For samples with recorded meal intake times, fasting phases are defined as the period starting at least 2 hours after dinner intake on the last day until the subsequent breakfast intake. In cases where meal intake times are available, fasting phases are alternatively defined as the time interval from 0:00 to 6:00.  

Post-meal phase. Post-meal phases are characterized as the duration spanning from meal intake to 2 hours after the meal intake.  

# Identification of HV-NGT as individual with high variant and rapid increasing glucose value  

We choose the individual with high variant and rapid increasing glucose value by calculating two indexes, Fasting SD $S D_{f a s t}$ and glycemic rate $G_{r}$ , from CGM records for samples. Fasting SD is calculated as standard deviation during fasting phase, that is $S D_{f a s t}=S D([g_{t}]_{t}$ ⁡𝑖𝑛⁡𝑓𝑎𝑠𝑡𝑖𝑛𝑔⁡𝑝ℎ𝑎𝑠𝑒) . Glycemic rate is calculated as $G_{r}=(g_{m a x}-g_{0})/T$ , where $g_{m a x}$ is the maximum glucose after meal intake, $g_{0}$ is the glucose before meal intake, $T$ is the time interval to reach the maximum after meal intake. HV-NGT are identified as individuals with both top $25\%\ S D_{f a s t}$ and $G_{r}$ in NGTs.  

# CGMformer finetuning  

Fine-tuning of CGMformer was accomplished by initializing the model with the pretrained CGMformer weights and adding a final task-specific transformer layer. The fine-tuning objective was either predicting binary diabetes labels or regressing numerical clinical characterization. The trainer from the Huggingface Transformers library was used for pretraining with the substitution of a custom tokenizer as described above and a custom data collator for dynamic token mask policy.  

Label classification (NGT/IGR/T2D diagnosis) in nationwide multi-center CGM data. Our nationwide multicenter data includes 1,917 training data, and each CGM record is labeled as one of the three IGR, NGT, and T2D labels. We divided the 1,917 data into five groups according to the fivefold cross-validation, and then loaded the pre-training model for fine-tuning. The output of CGMformer was a 128-dimensional vector corresponding to each blood glucose value token. A onelayer neural network was then applied as the classification head and transformed the token embeddings into the probability for each label. Cross-entropy loss was employed as the label prediction loss, calculated as:  

$$
L_{\mathrm{Pred}}=-\sum_{i=1}^{M}\,z_{i}\mathrm{log}\left(q_{i}\right)
$$  

Where $M$ is the number of CGM sequences, $z_{i}$ and $q_{i}$ indicate the ground-truth label and predicted label of CGM sequences $i$ , respectively.  

T1D/T2D diagnosis and complication diagnosis in Zhao’s dataset. In Zhao’s dataset36, each participants has records with complications including macrovascular (cerebrovascular disease, coronary heart disease, and peripheral arterial disease) and microvascular (nephropathy, neuropathy, and retinopathy). Since the CGM device for this dataset was testing blood glucose once every 15 minutes, the sequence length for one day was 96, we inserted two <PAD> tokens between two measurements into the sequence to ensure it is capable for the pretrained CGMformer. We finetuned the model pretrained on out nationwide multi-center data, with task-specific labels. Similar as previous, a one-layer neural network was then applied as the classification head and transformed the token embeddings into the probability for each label. Cross-entropy loss was also employed as the label prediction loss, calculated as:  

$$
L_{\mathrm{Pred}}=-\sum_{i=1}^{M}\,z_{i}\mathrm{log}\left(q_{i}\right)
$$  

Where $M$ is the number of CGM sequences, $z_{i}$ and $q_{i}$ indicate the ground-truth label and predicted label of CGM sequences $i$ , respectively.  

# Pretraining data volume  

To investigate the relationship between pre-training data size and downstream tasks performance, we trained CGMformer models on six datasets of varying sizes, ranging from 250 to 1,917 samples (250, 450, 750, 1,150, 1,650, and 1,917), subsampling randomly from our nationwide multi-center CGM study. As anticipated, the model's classification accuracy consistently increased with larger data volumes. This finding underscores the importance of leveraging extensive CGM datasets for enhanced model performance in downstream tasks. This paves the way for incorporating even larger datasets in future iterations of CGMformer and potentially unlocking better performance gains.  

# Baseline methods for disease diagnosis  

ML-based diagnosis: The LSTM model is implemented using PyTorch with a three-layer architecture. The  MLP  is  implemented  using  scikit-learn,  featuring  a  three-layer  architecture  with  node configurations of (128, 64, 1).  

CGM derived metrics-based diagnosis: Samples are diagnosed as T2D if meeting the following thresholds according to Jia et al.23:  

Mean: Mean≥6.6 mmol/L   
SD: SD≥1.8 mmol/L   
MAGE: MAGE $\geq\!3.9$ mmol/L   
TAR: Time above range $(>\!140\;\mathrm{mg/dL})\!\!\geq\!17\%$  

TIR: Time in range $(70{\sim}140\mathrm{~mg/dL}){\le}70\%$  

Combing CGM-derived metrics for diagnosis: We employ three machine-learning models, namely Ridge Regression, MLP, and SGD, for disease diagnosis by integrating CGM-derived metrics calculated by iglu. The machine-learning models are implemented using scikit-learn with default parameters.  

# Glucotype  

Glucotype4 first classify different patterns of glycemic responses based on their variability with spectral clustering, obtain fraction of time with low/moderate/severe variability, and classify individuals into low/moderate/severe variability groups. The calculation for glucotype in nationwide multi-center CGM study was done with the released code at https://github.com/abreschi/shinySpecClust .  

# Subtyping for non-diabetic individuals  

We conduct hierarchal clustering for embedded vectors for the pretrained NGT and IGR CGM corpus encoded by CGMformer with cosine similarity as distance metrics. Clusters are named according to the percentage of NGTs and T2Ds in the group. Three clusters as Normal, Pre_I, and Pre_II are first classified, with increasing ratio of IGRs. In order to obtain better resolution into the subtypes, a more detailed clustering is conducted for the two pre-diabetes clusters. In the end, six clusters, including Normal, Pre_Ia, Pre_Ib, Pre_IIa, Pre_IIb, and Pre_IIc are identified from NGT and IGR CGM corpus. For an individual, the embedded vector is first calculated from the mean vector of each day. Then we calculated the cosine similarity of the embedded vector to the vectors in each cluster. The sample is classified as the cluster with higher mean cosine similarity.  

# CGMformer_C  

CGMformer_C takes the CGMformer encoded vector $v_{s}$ as input and outputs a value C between 0 and 1. It us designed with an encoder which encode the input vector into a value C between 0 and 1, and a decoder which links the value C with clinical measurements, as well as labels. The encoder is composed of three linear layers followed with a nonlinear sigmoid activation layer, and encoded the input vector $\ v_{s}\in\mathbb{R}^{d}$ in to $C\in(0,1)$ :  

The decoder conducts multi tasks prediction, including prediction for labels and clinical measurements. For the prediction of label, the standard index $I$ is defined as 0 for NGT, 0.5 for IGR, and 1 for T2D. We further decode $C$ into multi-task prediction with a linear layer followed with an activation function to predicting clinical measurements, including age, BMI, HbA1c, FPG, PG120, Ins, Ins120.  

$$
M=D e c o d e r(C)\in\mathbb{R}^{N}
$$  

where $N$ is the number of predicted targets.  

The parameter in CGMformer_C model is optimized to minimize the loss function:  

$$
\mathcal{L}_{C G M f o r m e r\_C}=p\cdot M S E(C,I)+(1-p)\cdot M S E(M,\widehat{M})
$$  

where $\widehat{M}$ is individual clinical measurements, $p$ is parameter to balance the loss of label prediction and clinical measurements regression. The encoded value, $C$ , is defined as the CGMformer derived course of diabetes, indicating the impairment of individual glucose regulatory.  

# Postprandial glucose prediction  

CGMformer_Diet takes the individual's embedding vector from CGMformer, before-meal 1h glucose value, and dietary intake as input and output this individual’s glucose values within 2h post-meal. Three inputs include individual embedding vector encoded from CGMformer $v_{S}\in\mathbb{R}^{d}$ ; before-meal 1h glucose $G^{B}\in\mathbb{R}^{t}$ , where $t$ is the number of CGM measurements in one hour, and $t=4$ for FGM used in Zhao et al. 36 which measure glucose every 15 minutes; and the information of the dietary intake, $D=(H,C,P,F,B)\in\mathbb{R}^{5}$ ,  containing  the  calories  ( $H$ ⁡in⁡unit⁡of⁡𝑘𝑐𝑎𝑙 ),  carbohydrates ( $C$ ⁡in⁡unit⁡of $g$ ), proteins ( $P$ ⁡in⁡unit⁡of⁡ $g$ ), fats ( $\overrightarrow{F}$ ⁡in⁡unit⁡of⁡ $g$ ), and dietary fiber ( $B$ ⁡in⁡unit⁡of⁡ $g$ ). CGMformer_Diet predicts post-meal 2h glucose $G^{P}\in R^{2t}$ as output. The dietary information is encoded as a pulsed perturbation, $\widehat{D}\in\mathbb{R}^{5*t}$ , with $\widehat{D}_{\cdot,t}=D$ indicating a dietary intake at time $t$ , and $\widehat{D}_{\cdot,j}=0$ , for $j\neq t$ , indicating no dietary intake at other times. $\widehat{D}$ is further concatenated with beforemeal glucose $G^{B}$ into $T\in\mathbb{R}^{6\ast t}$ , with $T_{1,\cdot}=G^{P}$ and $T_{i,}=\widehat{D}$ .  

In CGMformer_Diet, $v_{s}$ is firstly encoded into a vector $\widehat{v_{s}}\in\mathbb{R}^{l}$ in $l$ -dimension latent space for dietary perturbation via a linear encoder $f_{e n c}\ldots\;\widehat{v_{s}}$ is then adjusted with $T$ through LSTM. Specifically, denoting $v_{1}=\widehat{v_{s}}$ , we have  

$$
v_{k+1},o_{k+1}=L S T M(v_{k},T_{\cdot,k})
$$  

for $1\leq k\leq t$ , results in $v_{t}=f(v_{s},G^{B})$ indicating the state of sample before meal, and $v_{t+1}=$ $g(v_{s},G^{B},D)$ the instant state after dietary perturbation. The outputs, $o$ , are decoded to recover the glucose through a linear decoder $g_{k}=f_{d e c}(o_{k})\in\mathbb{R}.$  

We iteratively predict post-meal glucose. Specifically, for $k>t$ , we have  

$$
v_{k+1},o_{k+1}=L S T M(v_{k},\widehat{T_{.k}})
$$  

where $\widehat{T_{1,k}}=f_{d e c}(o_{k})$ indicating the estimated glucose from previous time, and $\widehat{T_{\iota,k}}=0$ for $i\neq1$ . The CGMformer_Diet model is optimized by minimizing the following loss function:  

$$
\mathcal{L}_{C G M f o r m e r\_D i e t}=M S E(G_{p r e d},G_{2:}^{B}|\widehat{G^{P}})
$$  

where $G_{p r e d}=(g_{k})_{1<k\leq3t}$ , and $\widehat{G^{P}}$ is the observed post-meal glucose, $G_{2:}^{B}|\widehat{G^{P}}$ indicating the concatenation of before-meal and post-meal glucose. The predicted post-meal glucose $G^{P}$ can be obtained as 𝐺𝑃= (𝑔𝑘)𝑡<𝑘≤3𝑡.  

# In silico dietary perturbation  

For each meal recorded in Zhao et al. 36, we established a standard balanced meal plan with fixed calories and an energy supply ratio of carbohydrate: protein: fat $=5{:}2{:}3$ . To assess the glucose response to different dietary intake plan, we designed three additional simulated meal plans with adjusted ratios—low carbohydrate-high protein (carbohydrate: protein: fat $=4;3;3]$ ), low carbohydrate-high fat (carbohydrate: protein: fat $=4;2;4_{,}$ ), and high protein (carbohydrate: protein: fat $=5;3;2\rangle$ . The calories for carbohydrate, protein and fat are estimated as: carbohydrate: $4\,k c a l/g$ , protein: $4\,k c a l/g$ , fat: 9⁡𝑘𝑐𝑎𝑙/𝑔.  

Specifically, for a raw meal recorded with $H\left(k c a l\right)$ calories, $C\ (g)$ carbohydrate, $P\left(g\right)$ protein, and $B\left(g\right)$ dietary fiber, $D_{r a w}=(H,C,P,F,B)$ , simulated meals are defined as:  

$$
\begin{array}{r l}&{)_{s t a n d a r d}=(H,0.5*H/4,0.2*H/4,0.3*H/9,B)}\\ &{\quad D_{433}=(H,0.4*H/4,0.3*H/4,0.3*H/9,B)}\\ &{\quad D_{424}=(H,0.4*H/4,0.2*H/4,0.4*H/9,B)}\\ &{\quad D_{532}=(H,0.5*H/4,0.3*H/4,0.2*H/9,B)}\end{array}
$$  

# Dynamic Network Biomarker (DNB)  

According to the DNB theory, for a discrete-time dynamical system, the appearance of a strongly fluctuating and highly correlated group of elements implies a tipping point or an upcoming transition into the after-transition stage38–40. In other words, critically collective fluctuation of a group of elements means the imminent critical transition. The DNB conditions were computed to assess if a subject is going to experience a critical transition into T2D. Temporal segmentation of CGM data: for each subject and each day, the CGM time-series data were segmented according to the following rules:  

Segmentation was performed based on the three main meals: breakfast, lunch, and dinner.  

Meal times were determined using local maxima in the CGM data. Breakfast: within the time range 6:00 to 9:00, identified by the local maximum T1, corresponding to the period [T1-3h, $\mathrm{T}1{+}1\mathrm{h}]$ ]. Lunch: within the time range 11:00 to 14:00, identified by the local maximum T2, corresponding to the period [T2-3h, $\mathrm{T}2+1\mathrm{h}]$ . Dinner: within the time range 17:00 to 21:00, identified by the local maximum T3, corresponding to the period [T3-3h, T3+1h].  

Additionally, two segments were added for the early morning (2:00 to 6:00) and fasting (21:00 to 1:00 of the next day) periods on the first day. Consequently, each subject's CGM time-series was divided into eight segments, each containing continuous CGM data measured over a 4-hour interval, representing a 48-dimensional vector.  

The standard deviation SD for CGM data within each of the eight time-segments were computed for every subject, and the average variance across all segments was obtained (Supplementary notes).  

# References  

1. Alon, U. Systems Medicine: Physiological Circuits and the Dynamics of Disease. (2023).   
2. Wagner, R. et al. Pathophysiology-based subphenotyping of individuals at elevated risk for type 2 diabetes. Nature medicine 27, 49–57 (2021).   
3. Pearson, E. R. Type 2 diabetes: a multifaceted disease. Diabetologia 62, 1107–1112 (2019).   
4. Hall, H. et al. Glucotypes reveal new patterns of glucose dysregulation. PLOS Biology 16, e2005143 (2018).   
5. Danne, T. et al. International consensus on use of continuous glucose monitoring. Diabetes care 40, 1631–1640 (2017).   
6. Lawton, J. et al. Patients’ and caregivers’ experiences of using continuous glucose monitoring to support diabetes self-management: qualitative study. BMC endocrine disorders 18, 1–10 (2018).   
7. Kenton, J. D. M.-W. C. & Toutanova, L. K. Bert: Pre-training of deep bidirectional transformers for language understanding. in Proceedings of naacL-HLT vol. 1 2 (2019).   
8. Floridi, L. & Chiriatti, M. GPT-3: Its nature, scope, limits, and consequences. Minds and Machines   
9. Achiam, J. et al. GPT-4 Technical Report. arXiv preprint arXiv:2303.08774 (2023).   
10. Brown, T. et al. Language models are few-shot learners. Advances in neural information processing systems 33, 1877–1901 (2020).   
11. Chowdhery, A. et al. Palm: Scaling language modeling with pathways. Journal of Machine Learning Research 24, 1–113 (2023).   
12. Anil, R. et al. Palm 2 technical report. arXiv preprint arXiv:2305.10403 (2023).   
13. Touvron, H. et al. Llama: Open and efficient foundation language models. arXiv preprint arXiv:2302.13971 (2023).   
14. Radford, A. et al. Learning transferable visual models from natural language supervision. in International conference on machine learning 8748–8763 (PMLR, 2021).   
15. Ramesh, A., Dhariwal, P., Nichol, A., Chu, C. & Chen, M. Hierarchical text-conditional image generation with clip latents. arXiv preprint arXiv:2204.06125 1, 3 (2022).   
16. Alayrac, J.-B. et al. Flamingo: a visual language model for few-shot learning. Advances in Neural Information Processing Systems 35, 23716–23736 (2022).   
17. Zhou, Y. et al. A foundation model for generalizable disease detection from retinal images. Nature   
622, 156–163 (2023).   
18. Dai, L. et al. A deep learning system for detecting diabetic retinopathy across the disease spectrum. Nature communications 12, 3242 (2021).   
19. Dai, L. et al. A deep learning system for predicting time to progression of diabetic retinopathy. Nature Medicine 1–11 (2024).   
20. Vaswani, A. et al. Attention is All you Need. in Advances in Neural Information Processing Systems vol. 30 (Curran Associates, Inc., 2017).   
21. Theodoris, C. V. et al. Transfer learning enables predictions in network biology. Nature 1–9 (2023) doi:10.1038/s41586-023-06139-9.   
22. Yang, F. et al. scBERT as a large-scale pretrained deep language model for cell type annotation of single-cell RNA-seq data. Nat Mach Intell 4, 852–866 (2022).   
23. Zhou, J. et al. Reference values for continuous glucose monitoring in Chinese subjects. Diabetes care 32, 1188–1193 (2009).   
24. Zhou, J. et al. Relationship between HbA1c and continuous glucose monitoring in Chinese population: a multicenter study. PloS one 8, e83827 (2013).   
25. Cheng Li, X. M. Decreasing complexity of glucose time series derived from continuous glucose monitoring is correlated with deteriorating glucose regulation. Front. Med. 17, 68–74 (2023).   
26. Ramos, J. Using tf-idf to determine word relevance in document queries. in Proceedings of the first instructional conference on machine learning vol. 242 29–48 (Citeseer, 2003).   
27. Ren, J. et al. {ZeRO-Offload}: Democratizing {Billion-Scale} model training. in 2021 USENIX Annual Technical Conference (USENIX ATC 21) 551–564 (2021).   
28. Rajbhandari, S., Rasley, J., Ruwase, O. & He, Y. Zero: Memory optimizations toward training trillion parameter models. in SC20: International Conference for High Performance Computing, Networking, Storage and Analysis 1–16 (2020).   
29. Bonora, E. et al. Homeostasis model assessment closely mirrors the glucose clamp technique in the assessment of insulin sensitivity: studies in subjects with various degrees of glucose tolerance and insulin sensitivity. Diabetes Care 23, 57–63 (2000).   
30. Broll, S. et al. Interpreting blood GLUcose data with R package iglu. PLoS ONE 16, e0248560 (2021).   
31. Nathan, D. M. et al. Translating the A1C assay into estimated average glucose values. Diabetes care 31, 1473–1478 (2008).   
32. Battelino, T. et al. Clinical targets for continuous glucose monitoring data interpretation: recommendations from the international consensus on time in range. Diabetes care 42, 1593–1603 (2019).   
33. Association, A. D. 2. Classification and diagnosis of diabetes: standards of medical care in diabetes—2021. Diabetes care 44, S15–S33 (2021).   
34. Hochreiter, S. & Schmidhuber, J. Long short-term memory. Neural computation 9, 1735–1780 (1997).   
35. Hornik, K., Stinchcombe, M. & White, H. Multilayer feedforward networks are universal approximators. Neural networks 2, 359–366 (1989).   
36. Zhao, Q. et al. Chinese diabetes datasets for data-driven machine learning. Sci Data 10, 35 (2023).   
37. Tuomi, T. et al. The many faces of diabetes: a disease with increasing heterogeneity. The Lancet 383, 1084–1094 (2014).   
38. Chen, L., Liu, R., Liu, Z.-P., Li, M. & Aihara, K. Detecting early-warning signals for sudden deterioration of complex diseases by dynamical network biomarkers. Scientific reports 2, 342 (2012).   
39. Liu, R., Chen, P., Aihara, K. & Chen, L. Identifying early-warning signals of critical transitions with strong noise by dynamical network markers. Scientific reports 5, 17501 (2015).   
40. Liu, R. et al. Predicting local COVID-19 outbreaks and infectious disease epidemics based on landscape network entropy. Science Bulletin 66, 2265–2270 (2021).   
41. Consultation, W. H. O. Definition, Diagnosis and Classification of Diabetes Mellitus and Its Complications. (Part, 1999).   
42. Tabák, A. G., Herder, C., Rathmann, W., Brunner, E. J. & Kivimäki, M. Prediabetes: a high-risk state for diabetes development. The Lancet 379, 2279–2290 (2012).   
43. Colás, A., Vigil, L., Vargas, B., Cuesta–Frau, D. & Varela, M. Detrended Fluctuation Analysis in the prediction of type 2 diabetes mellitus in patients at risk: Model optimization and comparison with other metrics. PloS one 14, e0225817 (2019).   
44. Gallwitz, B. Implications of postprandial glucose and weight control in people with type 2 diabetes: understanding and implementing the International Diabetes Federation guidelines. Diabetes care 32, S322 (2009).   
45. Zeevi, D. et al. Personalized Nutrition by Prediction of Glycemic Responses. Cell 163, 1079–1094 (2015).   
46. Berry, S. E. et al. Human postprandial responses to food and potential for precision nutrition. Nature medicine 26, 964–973 (2020).   
47. Zhang, J. et al. Decreased abundance of Akkermansia muciniphila leads to the impairment of insulin secretion and glucose homeostasis in lean type 2 diabetes. Advanced Science 8, 2100536 (2021).   
48. Ahlqvist, E. et al. Novel subgroups of adult-onset diabetes and their association with outcomes: a data-driven cluster analysis of six variables. The lancet Diabetes & endocrinology 6, 361–369 (2018).   
49. Barma, P. D., Ranabir, S., Prasad, L. & Singh, T. P. Clinical and biochemical profile of lean type 2 diabetes mellitus. Indian journal of endocrinology and metabolism 15, S40 (2011).   
50. Chan, J. C., Zhang, Y. & Ning, G. Diabetes in China: a societal solution for a personal challenge. The lancet Diabetes & endocrinology 2, 969–979 (2014).   
51. Chan, J. C. et al. Premature mortality and comorbidities in young-onset diabetes: a 7-year prospective analysis. The American journal of medicine 127, 616–624 (2014).   
52. Rein, M. et al. Effects of personalized diets by prediction of glycemic responses on glycemic control and metabolic health in newly diagnosed T2DM: a randomized dietary intervention pilot trial. BMC medicine 20, 56 (2022).  

# Data availability  

The clinical data and CGM data in nationwide multi-center CGM study used in this study is available upon request from the corresponding authors. The embedded vectors of the three datasets used in this study and pretrained CGMformer are available at https://github.com/YurunLu/CGMformer/ .  

# Code availability  

All code for pretraining and fine-tuning CGMformer model and downstream tasks are available at https://github.com/YurunLu/CGMformer/ .  

# Acknowledgements  

We acknowledge funding from the National Key Research and Development Program of China (2022YFA1004800), CAS Project for Young Scientists in Basic Research (YSBR-077), the National Natural Science Foundation of China (12025107, 12326610, 31930022, 12131020, T2350003, T2341007), and JST Moonshot R&D (JPMJMS2021). We would like to appreciate the kind suggestions on the subtyping of pre-T2D from Xiaoding Peng, and helpful scientific discussions from Jiarui Wu, Zhiming Ma, Songmao Zhang and Wing Hung Wong.  

# Author contributions  

Y.R.L. and Y.W. conceived the study. Y.R.L and Z.M.L. designed and developed CGMformer. Y.R.L, L.D. and Z.M.L. assembled the CGM data from nationwide multi-center CGM study and performed computational analyses. Y.T.L. and L.M.L. performed collection of dietary data and calculation of glucotype. R.L and P.C. performed analyses of DNB. W.P.J, L.N.C, H.T.L., and Y.W. designed analyses and supervised the work. Y.R.L, L.D., Z.M.L. and Y.W. wrote the manuscript. All authors edited and approved the manuscript.  

Competing interests  

The authors declare that they have no conflict of interest.  

# Additional information  

Correspondence and requests for materials should be addressed to Weiping Jia, Luonan Chen, Huating Li and Yong Wang.  

# Figure Legends  

Fig 1: CGMformer architecture and pretraining. a. Schematic of CGMformer. CGMformer is first self-supervised pretrained on nationwide multi-center CGM data to gain fundamental knowledge of the glucose dynamics, and then applied to a multitude of downstream clinical applications. The extractable contextual time point and individual embeddings can be used in unsupervised clustering and fine-tuning with limited task-specific data, generating glucose values after perturbation, assisting diagnosis, predicting glucose and providing treatment suggestion. b. Overview of nationwide multicenter CGM study. A total of 964 Chinese subjects were enrolled from 11 academic hospitals in China between 2007 and 2009, including 450 NGTs (normal glucose tolerance), 169 IGRs (impaired glucose regulation), and 345 T2Ds (type 2 diabetes). Participants recruited to the study were connected to a CGM system for three consecutive days. Meanwhile, clinical measurements taken for the participants in the study including anthropometrics, glycolipid metabolism, and OGTT. c. Pretrained CGMformer architecture. Each CGM records are first split by day and tokenized to CGM corpus according to glucose records. The CGM corpus is then processed through four layers of transformer encoder units with eight attention heads per layer. Extractable output includes contextual time point and individual embeddings, contextual attention weights and contextual predictions.  

# Fig 2: CGMformer adeptly captures individual glucose dynamics through attention. a. UMAP  

visualizations of pretrained CGMformer’s individual embeddings colored by NGT/IGR/T2D labels capture continuous trajectory from NGT to T2D. b. UMAP visualizations of pretrained CGMformer individual embeddings with clinical and CGM-derived measurements. Pretrained CGMformer individual embeddings align well with individual clinical or CGM-derived measurements. c.  

Pretrained CGMformer attention weights of token with abnormal glycemia including hyperglycemia $\left(>\mid80\mathrm{~mg/mL}\right)$ ) and hypoglycemia $(<\!70\;\mathrm{mg/dL})$ ), as well as woken within different fluctuation period, including fasting and post-meal. d. Mean fasting SD and mean glycemic rate in HV-NGT and NGT. e. Median CGM profile form HV-NGT and NGT. f. Comparison of clinical measurements, including FPG, HbA1c, and PG120, of individuals among HV-NGT, NGT, IGR, and T2D. g. UMAP visualizations for embedding vectors of HV-NGTs. h. Comparison of mean cosine similarity to T2Ds after encoded by CGMformer among HV-NGT, NGT, IGR and T2D. i. CGM profile for an individual in HV-NGT with normal clinical measurements and CGM derived metrics. j. Higher attention weights to time points from different layers and heads in fasting period or post-meal period. Each row corresponds to an attention head denoted as Hn_Lm, where 'n' signifies the head number and $"_{\mathrm{m}}"$ denotes the layer, and the columns aligns with the CGM profile in i indicates the timepoints.  

# Fig. 3 Fine-tuning CGMformer with labeled data assists clinical diagnosis and prediction. a.  

Architecture for CGMformer finetuning. b. Accuracy of CGMformer fine-tuned to diagnosis NGT/IGR/T2D from CGM data, compared to alternative methods. c. Precision and recall score of CGMformer fine-tuned to diagnosis T2D from ND, compared to alternative methods. b. Accuracy of CGMformer fine-tuned to diagnosis T1D/T2D from CGM data using independent data, compared to alternative methods. e. Accuracy of CGMformer fine-tuned to diagnosis complications and macro or microvascular from CGM data using independent data, compared to alternative methods. f. Survival curve for finetuned CGMformer predicted T2D and NDs in independent longitude cohort. g. Comparison of SD calculated by DNB from samples grouped with finetuned CGMformer predicted results,  hued  by  follow-up  outcome.  h.  Scatter  for  CGMformer_C  with  diabetes  duration. CGMformer_C significantly correlates with disease duration. i. Correlation of CGMformer_C with clinical measurements, compared to alternative CGM derived metrics. j. KDE plot for distribution of CGMformer_C in samples with or without complications and micro or macrovascular. k. AUROC in predicting complications with CGMformer_C, compared to alternative CGM derived metrics.  

Fig. 4 CGMformer enables detailed and comprehensive subtyping for non-diabetes. a. UMAP visualizations for individuals in CGMformer_type. Non-diabetic individuals were classified into one normal subtype and five pre-diabetic subtypes. b. Median CGM profile for subtypes, offering insights into the unique glucose dynamics of different subtypes. cd. Schematic representations of mean and variation during the fasting and post-meal phases for each subtype. ef. Correspondence between CGMformer_type and OGTT subtyping and Glucotype. CGMformer_type improves the subtyping resolution. gh. Characteristics extracted from both CGM and clinical measurements for each subtype. HBGI: high blood glucose index. $10\mathrm{{w}\%}$ : fraction of time with low glucose variability, calculated from glucotype; severe $\%$ : fraction of time with severe glucose variability, calculated from glucotype. i. Diabetes risk for each subtype, validated in a longitudinal cohort from Colas’s dataset. The normal group demonstrates a $0\%$ risk, while the other subtypes exhibit increasing risk of developing diabetes. j. Schematic representation of subtypes elucidates glucose regulatory dynamics, encompassing fasting glucose homeostasis and postprandial glucose adaptation.  

Fig.  5  CGMformer_Diet  predicts  personalized  postprandial  glucose  and  suggests  diet prescription. a. Schematic of CGMformer_Diet. CGMformer_Diet generates predictions for postmeal glucose levels following dietary perturbations, leveraging individual embeddings encoded by CGMformer, before-meal glucose values, and meal intake information. b. Correlation of predicted post-meal glucose with real glucose values from CGMformer_Diet, compared with alternative method, LSTM, which has same architecture but without the individual embedding as input. c. Predicted postmeal glucose after different meal intake. d. Comparison of CGMformer_Diet predicted post-meal glucose with real post-meal glucose for various dietary intakes. e. Rate of change for metrics derived from post-meal glucose when perturb meal intake from standard balanced meal.  

# Figures  

![](images/5bed0ff2cd541f841c88f79396c02aaa676110dbab0c5ecc11f12cdebde8659b.jpg)  

# Figure 1  

CGMformer architecture and pretraining. a. Schematic of CGMformer. CGMformer is  rst self-supervised pretrained on nationwide multi-center CGM data to gain fundamental knowledge of the glucose dynamics, and then applied to a multitude of downstream clinical applications. The extractable  

contextual time point and individual embeddings can be used in unsupervised clustering and  ne-tuning with limited task-speci c data, generating glucose values after perturbation, assisting diagnosis, predicting glucose and providing treatment suggestion. b. Overview of nationwide multi-center CGM study. A total of 964 Chinese subjects were enrolled from 11 academic hospitals in China between 2007 and 2009, including 450 NGTs (normal glucose tolerance), 169 IGRs (impaired glucose regulation), and 345 T2Ds (type 2 diabetes). Participants recruited to the study were connected to a CGM system for three consecutive days. Meanwhile, clinical measurements taken for the participants in the study including anthropometrics, glycolipid metabolism, and OGTT. c. Pretrained CGMformer architecture. Each CGM records are  rst split by day and tokenized to CGM corpus according to glucose records. The CGM corpus is then processed through four layers of transformer encoder units with eight attention heads per layer. Extractable output includes contextual time point and individual embeddings, contextual attention weights and contextual predictions.  

![](images/3504443d30d5bc0ef28167ffb14666f13c42e6bd4d5ad1f1fe23cd480bae1306.jpg)  
Figure 2  

CGMformer adeptly captures individual glucose dynamics through attention. a. UMAP visualizations of pretrained CGMformer’s individual embeddings colored by NGT/IGR/T2D labels capture continuous trajectory from NGT to T2D. b. UMAP visualizations of pretrained CGMformer individual embeddings with clinical and CGM-derived measurements. Pretrained CGMformer individual embeddings align well with individual clinical or CGM-derived measurements. c. Pretrained CGMformer attention weights of token  

with abnormal glycemia including hyperglycemia $(>180\ m g/\mathsf{m L})$ and hypoglycemia $(<\neg0\sf{\sf\ m g}/{\sf d L})$ , as well as woken within different  uctuation period, including fasting and post-meal. d. Mean fasting SD and mean glycemic rate in HV-NGT and NGT. e.Median CGM pro le form HV-NGT and NGT. f. Comparison of clinical measurements, including FPG, HbA1c, and PG120, of individuals among HV-NGT, NGT, IGR, and T2D. g. UMAP visualizations for embedding vectors of HV-NGTs. h. Comparison of mean cosine similarity to T2Ds after encoded by CGMformer among HV-NGT, NGT, IGR and T2D. i. CGM pro le for an individual in HV-NGT with normal clinical measurements and CGM derived metrics. j. Higher attention weights to time points from different layers and heads in fasting period or post-meal period. Each row corresponds to an attention head denoted as Hn_Lm, where 'n' signi es the head number and 'm' denotes the layer, and the columns aligns with the CGM pro le in i indicates the timepoints.  

![](images/4988db31edca204ba4f24225c92af8028a0d08a93109b65ebca5735b1279010c.jpg)  

Figure 3  

Fine-tuning CGMformer with labeled data assists clinical diagnosis and prediction. a. Architecture for CGMformer  netuning. b. Accuracy of CGMformer  ne-tuned to diagnosis NGT/IGR/T2D from CGM data, compared to alternative methods. c. Precision and recall score of CGMformer  ne-tuned to diagnosis T2D from ND, compared to alternative methods. b. Accuracy of CGMformer  ne-tuned to diagnosis T1D/T2D from CGM data using independent data, compared to alternative methods. e. Accuracy of CGMformer ne-tuned to diagnosis complications and macro or microvascular from CGM data using independent data, compared to alternative methods. f. Survival curve for  netuned CGMformer predicted T2D and NDs in independent longitude cohort. g. Comparison of SD calculated by DNB from samples grouped with netuned CGMformer predicted results, hued by follow-up outcome. h. Scatter for CGMformer_C with diabetes duration. CGMformer_C signi cantly correlates with disease duration. i. Correlation of CGMformer_C with clinical measurements, compared to alternative CGM derived metrics. j. KDE plot for distribution of CGMformer_C in samples with or without complications and micro or macrovascular. k. AUROC in predicting complications with CGMformer_C, compared to alternative CGM derived metrics.  

![](images/d29b617baa1bd22bdf5451c54725a1ce6936142caa1f2e521222aaf3523624bb.jpg)  
Figure 4  

CGMformer enables detailed and comprehensive subtyping for non-diabetes. a. UMAP visualizations for individuals in CGMformer_type. Non-diabetic individuals were classi ed into one normal subtype and  ve pre-diabetic subtypes. b. Median CGM pro le for subtypes, offering insights into the unique glucose dynamics of different subtypes. cd. Schematic representations of mean and variation during the fasting and post-meal phases for each subtype. ef. Correspondence between CGMformer_type and OGTT  

subtyping and Glucotype. CGMformer_type improves the subtyping resolution. gh. Characteristics extracted from both CGM and clinical measurements for each subtype. HBGI: high blood glucose index. low%: fraction of time with low glucose variability, calculated from glucotype; severe $\%$ : fraction of time with severe glucose variability, calculated from glucotype. i. Diabetes risk for each subtype, validated in a longitudinal cohort from Colas’s dataset. The normal group demonstrates a $0\%$ risk, while the other subtypes exhibit increasing risk of developing diabetes. j. Schematic representation of subtypes elucidates glucose regulatory dynamics, encompassing fasting glucose homeostasis and postprandial glucose adaptation.  

![](images/b2cfaea7bb0fea67f2817c656c134f032b41b593127e37fd3171d72c8a3e6400.jpg)  
Figure 5  

CGMformer_Diet predicts personalized postprandial glucose and suggests diet prescription. a. Schematic of CGMformer_Diet. CGMformer_Diet generates predictions for post-meal glucose levels following dietary perturbations, leveraging individual embeddings encoded by CGMformer, before-meal glucose values, and meal intake information. b. Correlation of predicted post-meal glucose with real glucose values from CGMformer_Diet, compared with alternative method, LSTM, which has same architecture but without the individual embedding as input. c. Predicted post-meal glucose after different meal intake. d. Comparison of CGMformer_Diet predicted post-meal glucose with real post-meal glucose for various dietary intakes. e. Rate of change for metrics derived from post-meal glucose when perturb meal intake from standard balanced meal.  

# Supplementary Files  

This is a list of supplementary  les associated with this preprint. Click to download.  

SupplementaryInformation.docx  

FigS1.pdf FigS2.pdf FigS3.pdf FigS4.pdf FigS5.pdf FigS6.pdf FigS7.pdf FigS8.pdf FigS9.pdf FigS10.pdf  