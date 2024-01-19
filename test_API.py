import pytest
import requests

# Define a fixture for base_url
@pytest.fixture
def base_url():
    return "http://127.0.0.1:5000"

def test_hello_message(base_url):

    # Test for the message produced from the default URL
    response = requests.get(base_url)
    assert response.status_code == 200, "Failed to get the message produced from the default URL"
    assert response.text == "Welcome to the Fulmine Labs Medical Imaging API!", "Incorrect message from the default URL; expected: Welcome to the Fulmine Labs Medical Imaging API!"

def test_patient_for_study_count(base_url):

    # Test for study count
    study_count_response = requests.get(f"{base_url}/patients/TCGA-34-7107/studycount")
    assert study_count_response.status_code == 200, "Failed to get study count for patient TCGA-34-7107"
    assert study_count_response.json()["study_count"] == 3, "Incorrect number of studies for patient TCGA-34-7107; expected 3"

def test_patient_for_series_count(base_url):

    # Test for series count
    series_count_response = requests.get(f"{base_url}/patients/TCGA-34-7107/seriescount")
    assert series_count_response.status_code == 200, "Failed to get series count for patient TCGA-34-7107"
    assert series_count_response.json()["series_count"] == 8, "Incorrect number of series for patient TCGA-34-7107; expected 8"

def test_patient_for_image_count(base_url):

    # Test for image count
    image_count_response = requests.get(f"{base_url}/patients/TCGA-34-7107/imagecount")
    assert image_count_response.status_code == 200, "Failed to get image count for patient TCGA-34-7107"
    assert image_count_response.json()["images_count"] == 1057, "Incorrect number of images for patient TCGA-34-7107; expected 1057"

def test_image_info_endpoint(base_url):

    filename = "1fa2a798-770f-4542-b877-946c0757cac2"

    response = requests.get(f"{base_url}/imageinfo/{filename}")
    assert response.status_code == 200, "Failed to get image info"

    expected_data = {
        "InstanceNumber": "165",
        "PatientID": "TCGA-34-7107",
        "RescaleIntercept": "-1024",
        "RescaleSlope": "1",
        "SeriesDescription": "STD CTAC",
        "StudyDescription": "PET / CT TUMOR IMAGING",
        "WindowCenter": "40.0",
        "WindowWidth": "400.0"
    }

    # Convert response to JSON and compare with expected data
    response_data = response.json()
    assert response_data == expected_data, "Incorrect data returned from image info endpoint"


