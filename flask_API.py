# app.py
from flask import Flask, jsonify
import sqlite3

db_path="medical_imaging.db"

def count_patients():
    with sqlite3.connect("medical_imaging.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM Patients")
        study_count = cursor.fetchone()[0]
    return study_count

def count_studies():
    with sqlite3.connect("medical_imaging.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM Studies")
        study_count = cursor.fetchone()[0]
    return study_count

def count_series():
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM Series")
        series_count = cursor.fetchone()[0]
    return series_count

# Function to Count Data for a Patient:
def count_patient_data(patient_id):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        
        # Count studies
        cursor.execute("SELECT COUNT(*) FROM Studies WHERE PatientID = ?", (patient_id,))
        study_count = cursor.fetchone()[0]

        # Count series
        cursor.execute("SELECT COUNT(*) FROM Series JOIN Studies ON Series.StudyID = Studies.StudyID WHERE Studies.PatientID = ?", (patient_id,))
        series_count = cursor.fetchone()[0]

        # Count images
        cursor.execute("SELECT COUNT(*) FROM Images JOIN Series ON Images.SeriesID = Series.SeriesID JOIN Studies ON Series.StudyID = Studies.StudyID WHERE Studies.PatientID = ?", (patient_id,))
        image_count = cursor.fetchone()[0]

        return (study_count, series_count, image_count)

# Function to Count Images for a Patient:
def count_images_for_patient(patient_id):
    with sqlite3.connect("medical_imaging.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM Images JOIN Series ON Images.SeriesID = Series.SeriesID JOIN Studies ON Series.StudyID = Studies.StudyID WHERE Studies.PatientID = ?", (patient_id,))
        image_count = cursor.fetchone()[0]

        return image_count

# Function to Count Series for a Patient:
def count_series_for_patient(patient_id):
    with sqlite3.connect("medical_imaging.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM Series JOIN Studies ON Series.StudyID = Studies.StudyID WHERE Studies.PatientID = ?", (patient_id,))
        series_count = cursor.fetchone()[0]
    return series_count

# Function to Count Studies for a Patient:
def count_studies_for_patient(patient_id):
    with sqlite3.connect("medical_imaging.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM Studies WHERE PatientID = ?", (patient_id,))
        study_count = cursor.fetchone()[0]
    return study_count

app = Flask(__name__)

def query_database(query, args=()):
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query, args)
            data = cursor.fetchall()
        return data
    except sqlite3.DatabaseError as e:
        print(f"Database error: {e}")
        return []

@app.route('/')
def home():
    return "Welcome to the Fulmine Labs Medical Imaging API!"

@app.route('/patients/<patient_id>', methods=['GET'])
def get_patient(patient_id):
    patient = query_database("SELECT * FROM Patients WHERE PatientID = ?", (patient_id,))
    return jsonify(patient)

@app.route('/studies/<study_id>', methods=['GET'])
def get_study(study_id):
    study = query_database("SELECT * FROM Studies WHERE StudyID = ?", (study_id,))
    return jsonify(study)

@app.route('/series/<series_id>', methods=['GET'])
def get_series(series_id):
    series = query_database("SELECT * FROM Series WHERE SeriesID = ?", (series_id,))
    return jsonify(series)

@app.route('/images/<image_id>', methods=['GET'])
def get_image(image_id):
    image = query_database("SELECT * FROM Images WHERE ImageID = ?", (image_id,))
    return jsonify(image)

@app.route('/patients/<patient_id>/studies', methods=['GET'])
def get_patient_studies(patient_id):
    studies = query_database("SELECT * FROM Studies WHERE PatientID = ?", (patient_id,))
    return jsonify(studies)

# Endpoint for Patient's Study Count:
@app.route('/patients/<patient_id>/studycount', methods=['GET'])
def get_patient_study_count(patient_id):
    study_count = count_studies_for_patient(patient_id)
    return jsonify({"patient_id": patient_id, "study_count": study_count})

# Endpoint for Patient's Series Count:
@app.route('/patients/<patient_id>/seriescount', methods=['GET'])
def get_patient_series_count(patient_id):
    series_count = count_series_for_patient(patient_id)
    return jsonify({"patient_id": patient_id, "series_count": series_count})

# Endpoint for Patient's Image Count:
@app.route('/patients/<patient_id>/imagecount', methods=['GET'])
def get_patient_image_count(patient_id):
    image_count = count_images_for_patient(patient_id)
    return jsonify({"patient_id": patient_id, "images_count": image_count})

@app.route('/patients/count', methods=['GET'])
def get_patient_count():
    patient_count = count_patients()
    return jsonify({"patient_count": patient_count})

@app.route('/studies/count', methods=['GET'])
def get_study_count():
    study_count = count_studies()
    return jsonify({"study_count": study_count})

@app.route('/series/count', methods=['GET'])
def get_series_count():
    series_count = count_series()
    return jsonify({"series_count": series_count})

@app.route('/images/count', methods=['GET'])
def get_images_count():
    series_count = count_images()
    return jsonify({"images_count": images_count})

@app.route('/patients/<patient_id>/counts', methods=['GET'])
def get_patient_counts(patient_id):
    study_count, series_count, image_count = count_patient_data(patient_id)
    return jsonify({
        "patient_id": patient_id,
        "study_count": study_count,
        "series_count": series_count,
        "image_count": image_count
    })

@app.route('/imageinfo/<filename>', methods=['GET'])
def get_image_info(filename):
    # SQL query to retrieve information
    query = """
    SELECT 
        Patients.PatientID, 
        Studies.StudyDescription, 
        Series.SeriesDescription, 
        Images.InstanceNumber,
        Images.WindowCenter,
        Images.WindowWidth,
        Images.RescaleIntercept,
        Images.RescaleSlope
    FROM 
        Images
    JOIN 
        Series ON Images.SeriesID = Series.SeriesID
    JOIN 
        Studies ON Series.StudyID = Studies.StudyID
    JOIN 
        Patients ON Studies.PatientID = Patients.PatientID
    WHERE 
        Images.FilePath LIKE ?
    """
    # Execute query with filename
    data = query_database(query, ('%' + filename + '%',))
    
    # Format the data into a JSON-friendly structure
    if data:
        image_info = {
            "PatientID": data[0][0],
            "StudyDescription": data[0][1],
            "SeriesDescription": data[0][2],
            "InstanceNumber": data[0][3],
            "WindowCenter": data[0][4],
            "WindowWidth": data[0][5],
            "RescaleIntercept": data[0][6],
            "RescaleSlope": data[0][7]
        }
        return jsonify(image_info)
    else:
        return jsonify({"error": "No data found for the provided filename"}), 404


if __name__ == '__main__':
    app.run(debug=True)