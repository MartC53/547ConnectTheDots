# Users Stories 
## Assay developers:
Advanced user that uses and modifies the software to apply the workflow to develop new assays for different diseases. This user applies their sample and standards to produce a new model for quantification of new diseases. Ideally interacts with the software at a deeper level (command line) to alter the parameters to match their setup (focal length, target recognition, etc.). This user has fundamental assay knowledge to allow them to produce the imaging prototype box, understands the fluorescence readout mechanism (what fluorescent channels are being utilized). 
- Produce new standard curves
  - Fundamentally change the ML model
- Produce Experimental imaging set up
  - Alter the image color channel for different molecular probes

## Lab bench user:
More advanced user that makes edits or is trying to implement the software for the purpose of subtype or variant detection of existing models. This user has major interaction with the software and has background knowledge in python. This user is the primary user until “at home” version is created. Ideally interacts with the software from a cloned repo or website. Compared to the assay developer, the lab bench user is an optimizer or a new project member who is trying to extend the model rather than create a new model.
- Can upload their data and make predictions based on a pre-defined model.
- Can alter image pre-processing steps to increase image clarity.

## Clinicians:
Demonstrates point of care use case, takes the samples from the patient, and runs a diagnostic test and reports results to the patient. This user would be the primary user for an at home/ in clinic software planned for future development. This user has limited to no background knowledge of jupyter notebooks/python.
- Images samples 
- Ideally interacts with a web interface or app to load in images 
- reads out results 

## Programmer:
Trains the machine learning algorithm for software. Programmers need to get access to many sample images, run the codes for analysis and compare the results with PCR data. The images the patient got from the cellphone should be locally processed. 
- Fundamentally changes model 
- Validates the model by comparing clinical samples to test data sets

## Patient:
Provides sample and then receives results in further versions will be the only user that interacts with the application for “at home” use. Limited or no background knowledge of jupyter notebooks/python.
- Images samples 
- Ideally interacts with a web interface or app to load in images 
- reads out results 

# USE CASES
1. User uploads image to GUI for classification and receives initial copy classification with a visual display
2. User can select a preloaded image for comparison in a visual display.

## User inputs:
- Feeding Images
- *Future inputs*
  - Select operation create new quantification / Upload New standard / Change assay (disease)
  - Post quantification actions: save to device, send to doctor, call healthcare.
  - Trends in history

## GUI- Interaction
- Return classification
- Return Number
   - Graph of counts, visual display of counts on standard curve
   - Output to show accuracy of each image with error bar *not implemented yet*
   - Android app integration 
   
## Components 

```import_data```

What it does: First step to allow users to load their data. Takes in a directory of image location. Then applies ```autocrop``` functions that crop the images down to the membrane. functions also blur images and apply a contrasting algorithm to aid in visualization.<br />
Inputs: User acquired RGB jpg images.<br />
Outputs: .npy files containing the image data flattened to grayscale and cropped to the membrane.<br />
Interactions: User calls ```import_data``` function at a script level. Ideally users would upload images to website, and this would be the first part of the workflow.

```get_data```

What it does: Allows for simple loading of datasets created by the ```import_data``` functions.<br />
Inputs: Named dataset created in ```import_data```<br />
Outputs: NumPy arrays or Pandas dataframes preprocessed and ready for the ML model<br />
Interactions: User calls ```get_data``` function at a script level. Ideally would automatically follow ```import_data``` in a GUI interface.

```dicts_train_input.csv```

What it does: Serves as a reference to which images were used for training for users who want to make their own .pkl file.<br />
Inputs: none-reference material <br />
Outputs: none-reference material <br />
Interactions: Use reference to ensure the correct images are in training, all other images should be in the testing split..

```model.pkl```

What it does: Saved scipy decision tree model. The model is pre-trained on data from ```decision_tree_trainer.py```.<br />
Inputs: Together with ```starting_copies_prediction.py``` and ```streamlit_app.py``` takes a tiff image and makes a classification prediction.<br /> 
Outputs: Capability to make a classification prediction.<br />
Interactions: *Future use case* User copies to android app or used for streamlit app. 

```starting_copies_prediction.py```

What it does: Reads in the ```model.pkl``` file along with an image supplied as a path to make a prediction to the starting copy number.<br />
Inputs: Image data is read in and converted into a matrix. Pickle file is also read in with stored model weights.<br />
Outputs: model priction as a string.<br />
Interactions: called in the android app and streamlit app.

```environment.yml```

What it is: This is the conda environment used to produce the decision tree model and run the streamlit GUI.<br />
Inputs: none. <br />
Outputs: Conda environment capable of using the scripts in the repo.<br />
Interactions: User creates working environment with ```conda env create -f environment.yml```

```model.py```

What it is: Defines functions needed for the streamlit GUI.<br />
Inputs: Directory folder for the saved model and an image to predict on.<br />
Outputs: A loaded model for GUI and an image rescaled appropriately to be fed into the model.<br />
Interactions: Current, none. * Future* User Changes model name as necessary to load in custom model.

```streamlit_app.py```

What it is: Source code for the streamlit GUI.<br />
Inputs: The inputs are the functions defined in ```model.py```.<br />
Outputs: GUI where the user can upload an image for classification prediction or select an image from the test set to see the model output.<br />
Interaction: None, user interacts with GUI after running ``` streamlit run streamlit_app.py```

   
## Idealized Future Process flow
1. Images collected on smartphone
    - Automated app based on android APK exists allowing for complete camera control (focal length, iso, flash time, exposure time, time between frames)
      - Built on python for android with kivy, considerations may need to be realized to allow integration with python for android (no scikit learn, yes open cv)
2. Image preprocessing 
  - Evaluate effect on ML with existing techniques
    - cropping
    - adaptive contrasting 
    - blurring
    - adaptive thresholding
3. Train/ test iterations of ML models on smartphone .jpg images
    - Due to small dataset image augmentation may be needed
    - Microscope images could be used as supplement, check for bias
      - Microscope images are .tiff and much larger
4. Display results as numerical answer (# copies) from regressor prediction 
5. Display results on a standard curve that is annotated with clinical decision-making matrix
6. Display results with overlayed with previously developed spot counter as sanity check.
