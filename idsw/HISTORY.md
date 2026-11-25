# History

## 1.2.0

### Fixed

* Deprecated structures

### Added

* New functionalities added.

### Reshape of project design.

* New division into modules and new names for functions and classes.

### Removed

* Removed support for Python < 3.7

## 1.2.1

### Fixed

* Setup issues.

## 1.2.2

### Fixed

* Setup issues: need for rigid and specific versions of the libraries.

## 1.2.3

### Fixed

* Setup issues.

## 1.2.4

### Fixed

* Import bugs.
* Introduced function for Excel writing.

## 1.2.5

### Fixed

* Matplotlib export figures bugs.
* 'quality' argument is no longer supported by plt.savefig function (Matplotlib), so it was removed.
* This modification was needed for allowing the correct functioning of the steelindustrysimulator, which is based on idsw.
* Check simulator project on: https://github.com/marcosoares-92/steelindustrysimulator

  * The Ideal Tool for Process Improvement, and Data Collection, Analyzing and Modelling Training.

## 1.2.6

### Fixed

* Export of figures generated a message like with '{new\_file\_path}.png.png'. Fixed to '{new\_file\_path}.png'.

## 1.3.0

### Added

* New functionalities added.

### Reshape of project design.

* New division of functions and classes and correspondent modules.
* Refactoring of functions and classes to improve code efficiency.
* Added new pipelines for fetching data and modified the storage of connectors.
* It includes pipelines for fetching table regions in Excel files, even if they are stored in a same tab; and a pipeline for downloading files stored in MS SharePoint.
* Added ControlVars dataclass to store if the user wants to hide results and plots.

## 1.3.1

### Improved

* Benford algorith for fraud and outlier detection.
* Pipeline for fetching SharePoint and downloading files.

## 1.4

* Module datafetch.texts added: functions based on LangChain for extracting texts from PDFs, DOCX, CSV, HTML and TXT and creating a text database.
* Several bugs fixed, specially in functions based on Pandas and NumPy deprecated structures.

## 1.4.1

* Bug fixed in linear regression function.
* Bug fixed: Python ~ operator deprecated, and replaced by "not".

## 2.0.0

### Major New Modules Added
* **`idsw.computer_vision`**: Full computer vision pipeline covering image I/O, class-directory organization (`organize_images_into_class_directories`), image processing (thresholding, edge detection, morphology, denoising), 3D biomedical imaging (Hounsfield windowing, volume segmentation, morphological features, resampling), Keras & PyTorch CNNs, transfer learning (MobileNetV2, ResNet50, VGG16), GANs, Siamese networks, and YOLO object detection.
* **`idsw.geospatial`**: Geospatial data loading, CRS transformations, spatial joins, buffers, dissolves, feature calculations, choropleth plotting, interactive Folium web maps, marker clusters, and spatial heatmaps.

### New Submodules Added
* **`idsw.modelling.tuning`**: Exhaustive Grid Search, Random Search, Coarse-to-Fine informed search, Bayesian Optimization (Gaussian Process surrogate with UCB), and Genetic Algorithm hyperparameter tuning.
* **`idsw.modelling.bayes`**: Gaussian, Multinomial, and Bernoulli Naive Bayes classifiers, Bayesian Linear Regression (Ridge & ARD with predictive uncertainty), and Bayesian Logistic Regression.
* **`idsw.modelling.recommendation_engines`**: PySpark MLlib ALS and pure-NumPy ALS fallback recommenders (explicit & implicit feedback), user-based and item-based collaborative filtering, and wide-to-long rating matrix conversions.

### Improved & Updated
* **Generalized Linear Models (GLMs)** in `idsw.modelling.linear`: `glm_regression`, `poisson_regression`, `negative_binomial_regression`, `gamma_regression`, and `lognormal_glm_regression` with overdispersion diagnostics and exponentiated coefficients.
* **Bayesian Deep Learning & Siamese Parity** in `idsw.modelling.deep`: Monte Carlo Dropout Bayesian Neural Networks (`get_bayesian_tf_model`, `get_siamese_bayesian_model`, `predict_with_uncertainty`) and 1:1 architectural parity across all 7 neural network types.
* **Interactive Plotly Support (`plotly=True`)**: Standardized `PlotlyHandler` (`idsw.plotly_utils`) enabling interactive HTML exports and visualizations across ETL, Time Series, Mean Difference, GLMs, Hyperparameter Tuning, and Geospatial plotting functions for Dash UI integration.
* **Time Series & ARIMA Optimization** (`idsw.etl.timeseries`): Fixed `lag_diagnosis`, `test_d_parameters`, and `best_arima_model` information-criterion selection with prediction intervals.
* **Statistics & Characterize** (`idsw.etl.characterize` & `meandifference`): Added discrete/continuous distribution testing (Poisson, Negative Binomial, Lognormal), `partition_and_rank_df`, `discrete_fourier_transform`, cross-validated `adv_imputation_missing_values`, non-parametric ANOVA / A/B testing, `test_proportion_diffs`, `monte_carlo_simulation`, `generate_sampling_distribution`, `bayesian_inference_analysis`, and `generate_and_fit_distribution`.
* **Design of Experiments (`idsw.etl.doe`)**: Added `create_factorial_design` (Full $2^k$, Central Composite / Star, Box-Behnken), `analyze_factorial_experiment` (ANOVA, Pareto of effects, Main Effects & Interaction plots), `plot_cube_plot`, `response_surface_analysis` (3D Surface & Contour), and `box_cox_transformation_analysis`.
* **Model I/O & SHAP** (`idsw.datafetch.pipes`, `idsw.modelling.utils`): Modular dispatch refactoring in `import_export_model_list_dict`, distribution-parameterized `AnomalyDetector`, modern TF 2.x SHAP explainability fixes, and pure-Python PDF-1.4 support in `idsw.datafetch.texts` (`export_as_pdf`, `convert_text_db_format`).
* **Automated Test Suite**: Comprehensive unit tests established in `idsw/test/`.
