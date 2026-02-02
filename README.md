# Face Authentication Attendance System

## Overview
A Python-based Face Authentication Attendance System that uses a webcam and deep learning face recognition to automatically record Punch-In and Punch-Out attendance.

## Features
- Face registration using camera
- Real-time face recognition
- Automatic Punch-In / Punch-Out
- Duplicate face detection
- User deletion support
- Attendance stored in CSV
- CLI-based interface

## Model Used
- InsightFace `buffalo_l`
- 512-D face embeddings
- Cosine similarity matching

## Project Structure
1. Face_Authentication_Medoc/
2. src/
   a. register_user.py
   b. attendance.py
   c. delete_user.py
     i. ui_cli.py
4. data/
5. attendance.csv
6. env/


## Installation
python3 -m venv venv  
source venv/bin/activate  
pip install insightface onnxruntime opencv-python numpy pandas  

## Run Project
python3 src/ui_cli.py

## Attendance Logic
- 1st scan → Punch-In  
- 2nd scan → Punch-Out  
- Continues alternately

## Output
Attendance is saved in `attendance.csv`.

## Author
Dhuriya Ankit Subhash

