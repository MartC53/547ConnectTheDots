# Connect the Dots ![Test status](https://github.com/MartC53/547ConnectTheDots/actions/workflows/python-package-conda.yml/badge.svg)
The goal of this project is to produce a model that accurately quantifies fluorescent images showing DNA amplification to known starting concentrations. Previous work in the Posner Research group has shown that these fluorescent reactions cause nucleation sites which correlate to the initial DNA concentration.

Note: The previous QIAML repo has been switched to private and reverted to status before 547 in order to maintain the past CNN model structure and weights for future few shot or adaptive learning models. This repo is unlisecened at the request of the stakeholder.

## Current Functionality:
- [x] Last quarter (545/546)
  - [x] Proof of concept
    - [x] Pre-process image by filter separation, auto-cropping, resizing, and pixel normalization 
    - [x] Load preprocessed image into Tensorflow tensor
    - [x] Produce CNN for image classification:
      - [x] Train model for image classification
      - [x] Sequential model
      - [x] 2D convolution
      - [x] Compile model
      - [x] Save and load model 
    - [x] Make predictions based on input pictures
      - [x] Visualize predictions and image on GUI
- [x] This quarter (547)
  - [x] Use time resolved data  
  - [x] Evaluate other model types
      - [x] Image augmentation- Images were cut into fourths and the previous CNN was re-trained. Accuracy increased to 52%
      - [x] Few Shot learning- Still dataset limited train on 1 test on 2 gives poor stats
      - [x] Adaptive fast learning - Still dataset limited, see above
      - [x] Autoecoder dataset limited- could not produce images outside of negative control
      - [x] Decision tree regressor- model of choice for following work
    - [x] Visualize prediction
      - [x] Streamlit webapp
      - [ ] Android app for edge computing
        - [x] Front end gui completed
        - [x] Back end model wrapped with Chaquopy
        - [ ] Integration of phone camera with analysis 
        - [ ] Integration of front and back end     
- [ ] Future work 
  - [ ] Further evaluated Decision tree model when more data is available (train on one test on two)
  - [ ] Investigate One-shot/few-shot models
    - [ ] Utilize past model weights when more data is available
  - [ ] Fully integrate Android app, see above   

  

## Motivation
### Abstract
Nucleic Acid Tests (NATs) detect nucleic acid from disease and infection. Detection is based on amplifying low levels of DNA/RNA allowing for detection of a single strand of DNA/RNA. The gold standard for quantitative nucleic acid testing is quantitative polymerase chain reaction (qPCR). However, qPCR is:
* slow
* expensive 
* fragile 

Isothermal DNA amplification technologies, like recombinase polymerase amplification (RPA) have been put forth that are faster, cheaper, and more robust than qPCR. Yet isothermal amplification technologies are limited in their diagnostic capabilities as they are qualitative. However, **Recent studies in the Posner Lab Group have shown that RPA, an isothermal NAT, can also be quantitative through a spot nucleation to initial copy correlation** [1]. Similar nucleation site analysis has been applied to other assays and targets that used ML to produce a quantification model which rivals our linear range [2]. Thus, we are interested in applying ML models to improve the linear range of our assay.
1.  Quantitative Isothermal Amplification on Paper Membranes using Amplification Nucleation Site Analysis
Benjamin P. Sullivan, Yu-Shan Chou, Andrew T. Bender, Coleman D. Martin, Zoe G. Kaputa, Hugh March, Minyung Song, Jonathan D. Posner
bioRxiv 2022.01.11.475898; doi: https://doi.org/10.1101/2022.01.11.475898 
2. Membrane-Based In-Gel Loop-Mediated Isothermal Amplification (mgLAMP) System for SARS-CoV-2 Quantification in Environmental Waters
Yanzhe Zhu, Xunyi Wu, Alan Gu, Leopold Dobelle, Clément A. Cid, Jing Li, and Michael R. Hoffmann
Environmental Science & Technology 2022 56 (2), 862-873
DOI: 10.1021/acs.est.1c04623

## Methods
### Import Images
Due to their size, all data set images are cropped and pre-processed using the ``auto_crop.py``. This function isolates the green fluorescent channel (the detection channel of our FAM fluorophore) applied an adaptive blurring and contrasting to the images to improve visual representation. The images are then cropped based on contours of the image, and saved as a 2D NumPy array in an .npy file. To access the images, the ``get_data.py`` file reads in the .npy and saves the data arrays as either a NumPy array or a pandas dataframe. The data available is triplicate images of the end point of the RPA reaction. To ensure the train and test splits contain all data in the range of interest (30-10,000 cp) the triplicate data is split into train and test groups. Here the data in AB,BC, or AC represent the train groups while A, B, or C are the test groups for the training sets BC, AC,AB respectively.
### Image processing 
The time resolved data can be challenging to work with as the data is stored in .tiff stacks. The stacks are composed of a single experiment at a given input concentration but each stack contains 1,200 images- one image is taken every second for 20 minutes. Some phones and websites have issues displaying the images. Additionally, slight variation between images results in uneven distribution of pixel intensities in successive images. In order to solve these issues the .tiff stacks are read in with `tifffile` and converted into a stacked matrix. Then each image is normalized to a float64 number taking the average of the four corner pixels and background subtracted from the initial frame before the reaction begins.
### Model training  
The decision tree classifier model is actually multiple decision tree regressor. The model is set up so that a variable branch depth regressor is trained for each of the desired copy sets. The depth of the model is chosen to be the depth with the lowest mean squared error and highest  coefficient of determination. For the eight regressors, the depth range is [2-7] with the average depth being 5 branches. When making a prediction, the model runs the data through call eight models and reports the model with the highest coefficient of determination as being the starting copy type, essentially a classifier.

## Application Usage

### Streamlit webapp
There are a few requirements to run the webapp GUI. These are that the model needs to be re-made or trusted and the computer to run on needed 16 gb of ram. To remake the model run the model ```decision_tree_trainer.py``` to make the ```model.pkl``` file. Make sure that the ```model.pkl``` file is in the main branch of the repo. 

After remaking the ```model.pkl``` or trusting the file in the exsiting repo, to run the GUI, users should clone our repository, activate the provided environment, and run ```streamlit run streamlit_app.py``` from the terminal. The user should follow their command line instructions to open the GUI on their internet browser. 
The model does take a long time to load.
Once the model is loaded you can either select a file that has already been prepared by using the drop menu or import your own file. The widget will display the predicated range of the image.

### Android app
<p align="center">
<img src="https://github.com/MartC53/547ConnectTheDots/blob/main/Documentation/res/AppGui.png" width="212" height="443">
</p>

To run the android app navigate to the app branch and download the code as a compressed file. Extract the file in the desired destination then open with android studio. The model is stored as a .pkl file, for your security the .pkl file is not added to the build. To add the .pkl first run the model from the main branch of the repo then or copy the file to the following directory:
```
.
├── Project
│   └── ConnecttheDots
│       └── app
│         └── src
│           └── python
│             └── model.pkl
```
Re-sync the gradle files and rebuild the app. The app can then be evaluated using a virtual device in the device manager or installed on an android phone that has developer mode and usb debugging enabled.

The hands on demo and virtual demo were both done using a Google Pixel 4a running current android 11 API level 30.

## Current limitations
The desired model is a regressor, however, due to a lack of data available this was not possible. Using simple regression models, our validation error would increase with each epoch which would eventually kill the model. We believe the validation error continued to increase due to the limited number of validation images available, a 20% validation split is only two images. Thus, there are no 1:1 validations available. What we believe to be happening is that images of one input copy number (ie 100 copies) was being validated against a different (1,000 copies) or no image whatsoever. 

Last quarter we investigated a CNN that achieved 40% accuracy by classifying images into three categories. This model was fundamentally flawed as it predicted all images were of the "low" category. The accuracy was due to the fact that 40% of the images belonged to the low category. Early this quarter we evaluated image augmentation were each image was split into fourths. We then also applied a random 90 degree rotation to the split images to increase our datasets by 8x. The image splitting was somewhat successful as it saw an increase in accuracy to 52%. The image splitting and rotation yield no gain in accuracy.

### Confusion Matrix
<p align="center">
<img src="https://github.com/MartC53/547ConnectTheDots/blob/main/Documentation/res/ConfusionMatrix.png" width="400" height="390">
</p>

The decision tree classifier is able to accurately classify images above 300 copies (1000-10,000). In order to accurately detect at lower copy numbers the existing site counting analysis published in Sullivan *et al* 2022 will be used as it was able to quantify in the range of 30-1000 copies.

## Future plans
The model is not currently available to be installed via pip of conda due to a few limiting factors. The first limiting factor is that size of the datasets. The data sets and saved models are multiple gigabytes in size. These large sizes make storing this data on GitHub impractical. Future work in this space will require the data to be uploaded to a data sharing platform like Zenodo. Second, this work and work around this project area are under active development and should not be utilized for the diagnosis of disease and should not be used in the attempt to make a diagnosis. In the future, a setup.py file will be added once more training data is available, the datasets and model will be available for download and local training if desired or for modification of other assay types.

Future work includeds collecting more data and plans to implement a one shot/few shot model to reduce training data dependency while still making predictions based on spot pattern, spot number, or spot morphology analysis. this analysis will liekly included the image splitting developed here as the old model was inproved using the splitting augmentation. 
