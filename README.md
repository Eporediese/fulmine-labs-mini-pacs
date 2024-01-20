# Fulmine Labs mini-PACS
Implement a basic Picture Archive Communication System (PACS) to manage DICOM images.

Date: 1/16/2024

Fulmine Labs LLC

## Overview
The challenge: Fulmine Labs will use medical images for various quality/testing related, machine learning (ML) initiatives. 
The best practice for managing this data is to use Digital Imaging and Communications in Medicine (DICOM) standard compliant images with a PACS-like system.

The code in this project implements and tests a basic PACS with the following architecture:

```
[ Orthanc Repository (Open Source component) ]
       |
       | (DICOM Images) <----------------------------------------->  [ OHIF Viewer (Open Source component) ]
       v
[ Fulmine-Labs-Mini-PACS - Data Setup Script ]      
       |								
       | (Metadata and generated images)   
       |                                          
[ SQLite Database ]							
       |								
       | (API Requests)						 
       v
[ Flask Application ]
       |
       | (HTTP Requests for Data)
       v
[ Client (Pytest, Browser) ]
       |
       | (Model Training Data)
       v
[ Anomaly Detection Model Training Script (separate repository) ]

```

The data setup script will traverse all folders in a specified location, identify DICOM images and if they have appropriate Window Center and Width DICOM header information, will convert them to PNG files at another specified location and add the related metadata to an SQLite database. 

The database maintains the Patient -> Study -> Series -> Image relationship, as well as tracking the output image file names and parameters used in their creation, allowing PACS-like SQL queries to be constructed. 

Currently supported endpoints (usually at `http://127.0.0.1:5000`) are:

* '/' - welcome message
* '/patients/<patient_id>' - get patient information
* '/studies/<study_id>' - get study information
* '/series/<series_id>' - get series information
* '/images/<image_id>' - get image information
* '/patients/<patient_id>/studies' - get studies for a patient
* '/patients/<patient_id>/studycount' - get study count for a patient
* '/patients/<patient_id>/seriescount' - get series count for a patient
* '/patients/<patient_id>/imagecount' - get image count for a patient
* '/patients/<patient_id>/counts' - get all counts for a patient
* '/patients/count' - get total patient count
* '/studies/count' - get total studies count
* '/series/count' - get total series count
* '/images/count' - get total images count
* '/imageinfo/<filename>' - get image info by providing the file name

## Datasources used

The Cancer Imaging Archive

## Current Version
The current stable version of the project is 0.1.0.
See the [CHANGELOG.md](CHANGELOG.md) file for details about this version.

## Prerequisites

* Anaconda, with an environment having the Python libraries listed in [requirements.txt](requirements.txt)
* The Orthanc open source DICOM server (optional)
* The OHIF Viewer integrated with Orthanc (optional). For this you will need a [Github](https://github.com/) account and Node Package Manager -> nodejs -> yarn.
* DICOM images

## Usage

Install Anaconda, create an environment and install the dependencies in requirements.txt

1) Orthanc Installation and configuration (if you need to download images):

* Install the Orthanc open source DICOM server from https://www.orthanc-server.com/
* Configure Orthanc by modifying the orthanc.json configuration file. 
This includes setting parameters like storage directories, enabling the DICOM and HTTP servers, and specifying network settings such as the port (defaults to 8042).
* Enable the CORS (Cross-Origin Resource Sharing) configuration in Orthanc by adding the following lines to Orthanc.json:

`"HttpServer" : {
  "EnableCors" : true,
  "CorsAllowedOrigins" : [ "*" ],
  "CorsAllowedMethods" : [ "GET", "POST", "PUT", "DELETE", "HEAD", "OPTIONS" ],
  "CorsAllowedHeaders" : [ "*" ]
}`

* Ensure that Orthanc is running properly by accessing its web interface: http://localhost:8042.
* Use Orthanc to retrieve studies of interest from public archives, such as the Cancer Imaging Archive.
* Test the Orthanc DICOM web interface by accessing _http://localhost:8042/dicom-web/studies_.

2) Integrating OHIF Viewer with Orthanc (if you need a reference viewer implementation):

* Fork the OHIF Viewer repository on GitHub to your own GitHub account.
* Clone the forked repository to your local machine using Git: `git clone https://github.com/YOUR-USERNAME/Viewers.git`
Navigate to the Cloned Directory: cd Viewers
Add the original OHIF Viewer repository as an upstream remote to your local repository: `git remote add upstream https://github.com/OHIF/Viewers.git`
* Run `yarn install` to install all necessary dependencies.
* Start the OHIF Viewer using the appropriate Yarn command: `yarn run dev:orthanc_`
* Viewing Studies: Once the viewer is running correctly, confirm that you are able to view the studies hosted on your Orthanc server.

3) Clone the Fulmine-Labs-Mini-PACS repository to your local machine and navigate to the cloned directory in Anaconda Powershell Prompt: 'cd Fulmine-Labs-Mini-PACS'
4) Install the dependencies listed in requirements.txt with `'pip install -r requirements.txt'`
5) Open Jupyter Notebook or Jupyter Lab from Anaconda. It should start in your default web browser.
6) Open _Fulmine-Labs-Mini-PACS.ipynb_ from the cloned directory inside Jupyter
7) Edit any test parameters in the second cell, as needed. Currently, the following parameters can be set:
* _verbose_, True or False. True will enable logging in Jupyter Notebook, but all messages will be logged to the log file for the run.
* _source_dir = r'D:\\Orthanc'_, the location of the folder containing DICOM images
* _target_dir = r'D:\\training'_, the location of the output PNG files, for ML training
* _training_ratio, validation_ratio = 0.7, 0.15_, the DICOM files will be randomly assigned for model training based on these ratios
* _delete_db = True_ - Variable to control database deletion on script re-run
* _db_path = 'medical_imaging.db'_ - location of created SQLite database
8) In Jupyter, 'Run All Cells'
9) Start the provided Flask API interface to the database by opening an Anaconda command prompt and then using `python Flask_API.py` (ensure that the database name in the Python file is the same as the one that you generated). 

Navigate to http://127.0.0.1:5000/ 
You should see a message: 'Welcome to the Fulmine Labs mini-PACS API!'

## Testing

This code was run in Jupyter Notebook and Jupyter Lab from Anaconda 2.5.2 on Windows 11.

The tests were run from a Jupyter Lab session in Brave 1.61.114 and from an Anaconda CMD.exe session.

THe OHIF Viewer was version 3.8.0-beta.36

Orthanc DICOM server was version 1.1.2, for Windows 64 bit

Anonymized Lung CT images were downloaded from 12 patients, from the Cancer Imaging Archive

* Downloaded studies for 12 Lung CT patients, including all studies for patient with patient ID 'TCGA-34-7107' from the Cancer Imaging Archive, in Orthanc.
* Tested the DICOM web interface of Orthanc by accessing http://localhost:8042/dicom-web/studies.
* Ran the _Fulmine-Labs-Mini-PACS.ipynb_ data setup script and tested the database and API after starting the provided Flask server using _python flask_API.py_. 
* Ran _python -v test_API.py_, which tests some of the API endpoints. This produces output similar to:

![alt text](pytest_DB_API_screenshot.png "DB API tests passed")
* Used the 'DB Browser for SQLite' tool to browse the created database contents
* Used the OHIF Viewer as a reference, to visually compare the PNG training images created and managed by Fulmine LABS mini-PACS with the same images displayed in the viewer. Note: The API can be used to identify the patient, study, series and image number for a particular output image PNG file name, as well as the image information used to generate the PNG image. 
For example this endpoint: 

`http://127.0.0.1:5000/imageinfo/1fa2a798-770f-4542-b877-946c0757cac2` 

returns this data:
```
{
  "InstanceNumber": "165",
  "PatientID": "TCGA-34-7107",
  "RescaleIntercept": "-1024",
  "RescaleSlope": "1",
  "SeriesDescription": "STD CTAC",
  "StudyDescription": "PET / CT TUMOR IMAGING",
  "WindowCenter": "40.0",
  "WindowWidth": "400.0"
}
```
 
## Known issues

1) Even accounting for scaling differences, the images generated by the OHIF Viewer and the Fulmine Labs output PNG training images are very similar, but not identical at the pixel level. The reason for this should be investigated further, but it is probably due to some pixel interpolation being done by the OHIF Viewer, that the PNG image creation is not currently doing. 
Examining the OHIF source code could help explain this and potentially enhance the Fulmine Labs PNG image creation process. 
See below for examples:

![alt text](generated_000c2fcd-63c0-4f4d-a96d-d519c00c1d0f.png "Generated image example 1")
Fulmine

![alt text](OHIF_000c2fcd-63c0-4f4d-a96d-d519c00c1d0f.png "OHIF image example 1")
OHIF

![alt text](generated_1fa2a798-770f-4542-b877-946c0757cac2.png "Generated image example 2")
Fulmine

![alt text](OHIF_1fa2a798-770f-4542-b877-946c0757cac2.png "OHIF image example 2")
OHIF

2) The OHIF Viewer handles images that do not have Window Center and/or Window Width in the DICOM header. The PNG creation process currently ignores these images. Again, examining the OHIF source code and the DICOM standard could help explain the OHIF methodology and potentially include a wider range of images in the PNG training image creation process.

## Acknowledgements

This code was written collaboratively with [GPT-4V](https://chat.openai.com/). Thank you Assistant!

[The Open Health Imaging Foundation](https://ohif.org/)

[Orthanc open source DICOM server](https://www.orthanc-server.com/)

[DB Browser SQLite](https://sqlitebrowser.org/)

[The Cancer Imaging Archive](https://imaging.cancer.gov/informatics/cancer_imaging_archive.htm)

## License
MIT open source license

## Collaboration
We welcome contributions at all levels of experience, whether it's with code, documentation, tests, bug reports, feature requests, or other forms of feedback. If you're interested in helping improve this tool, here are some ways you can contribute:

Ideas for Improvements: Have an idea that could make the Fulmine Labs mini-PACS better? Open an issue with the tag enhancement to start a discussion about your idea.

Bug Reports: Notice something amiss? Submit a bug report under issues, and be sure to include as much detail as possible to help us understand the problem.

Feature Requests: If you have a suggestion for a new feature, describe it in an issue with the tag feature request.

Documentation: Good documentation is just as important as good code. Although this is currently a very simple tool, if you'd like to contribute documentation, we'd greatly appreciate it.

Code: If you're looking to update or write new code, check out the open issues and look for ones tagged with good first issue or help wanted.

## Contact
Duncan Henderson, Fulmine Labs LLC henderson.duncanj@gmail.com
