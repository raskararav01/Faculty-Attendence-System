🎓 Faculty Attendance System using Face Recognition
An automated, web-based attendance management system built with Flask, OpenCV, and JavaScript to track faculty attendance using real-time facial recognition.

## 🚀 Features
* **Facial Recognition**: Automatically marks attendance using a live webcam feed.
* **Faculty Registration**: Captures face dataset samples for new faculty during onboarding.
* **Model Training**: Retrains recognition models directly through script integration.
* **Role-Based Web Dashboards**:
  * **Admin**: View attendance reports, register new faculty, and view overall analytics.
  * **Faculty**: Check personal attendance percentages and mark daily attendance.
* **Visual Analytics**: Interactive charts generated with `charts.js`.

## 📁 Folder Structure

```text
FACULTY ATTENDANCE SYSTEM/
├── attendance/               # Holds attendance CSV logs
├── dataset/faculty_faces/    # Face training dataset folders
├── face_recognition_module/  # Scripts for capture, training, and recognition
├── models/                   # Serialized model files (.yml / embeddings)
├── static/                   # CSS styles and frontend JavaScript (camera, charts)
├── templates/                # HTML templates (admin, faculty, auth, analytics)
├── app.py                    # Main Flask application entry point
├── config.py                 # System configurations
└── requirements.txt          # Python dependencies

## 4. Tech Stack : 
* **Backend**: Python 3.x, Flask
* **Computer Vision**: OpenCV, NumPy
* **Frontend**: HTML5, CSS3, JavaScript (WebRTC, Chart.js)
* **Storage**: CSV / File-based Database

To Start :- 
* Python 3.8+ installed on your machine
* A working webcam / camera module

*Create and activate a virtual environment:

Bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

*Install required dependencies:

Bash
pip install -r requirements.txt

Running the App
Train the model (if you added new face images):

Bash
python face_recognition_module/train_model.py
Start the Flask web server:

Bash
python app.py
Open your browser and navigate to http://127.0.0.1:5000/.

## 💡 Quick Tips for Markdown Writing
* **Use Code Blocks (\`\`\`):** For command line commands, code snippets, and folder structures.
* **Use Emojis:** They help visually separate sections and make the README engaging.
* **Keep paths accurate:** Make sure any file path mentioned matches your actual folder names exactly (e.g., `face_recognition_module/train_model.py`).
   
