# Face Authentication Attendance System

## 📌 Project Overview
The **Face Authentication Attendance System** is a Python-based application that uses deep learning and real-time face recognition to automatically mark attendance.  
It captures live webcam input to **register users**, **recognize faces**, and **log attendance** using an intelligent **Punch-In / Punch-Out** mechanism.

This system is lightweight, reliable, and ideal for real-world use cases such as **offices, colleges, and laboratories**.

---

## 🚀 Key Features

- Real-time face registration using webcam  
- Face recognition using deep learning embeddings  
- Automatic Punch-In / Punch-Out attendance logic  
- Duplicate face prevention during registration  
- User deletion functionality  
- Attendance stored in CSV format  
- Command-line based user interface (CLI)

---

## 🛠 Tech Stack

- **Programming Language:** Python 3  
- **Face Recognition Model:** InsightFace (ArcFace – `buffalo_l`)  
- **Computer Vision:** OpenCV  
- **Embedding Matching:** Cosine Similarity  
- **Runtime Engine:** ONNX Runtime  
- **Storage:**  
  - `.npy` files for face embeddings  
  - `attendance.csv` for attendance records  

---

## 🧠 Model & Approach

### Face Detection & Recognition
- Uses the pretrained **InsightFace `buffalo_l`** ArcFace model  
- Generates **512-dimensional face embeddings**  
- No custom training required  

### Face Matching
- Face embeddings are compared using **Cosine Similarity**  
- A configurable similarity threshold determines identity matching  

---

## 👤 Face Registration Flow

1. User enters their name  
2. Webcam scans the face for **5 seconds**  
3. Multiple face embeddings are collected  
4. Average embedding is computed  
5. **Duplicate face check** is performed  
   - If face already exists → registration is blocked  
   - If new → embedding is saved successfully  

---

## ⏱ Attendance Logic (Punch-In / Punch-Out)

- Attendance is **fully automatic**
- Logic per user per day:
  - 1st recognition → **Punch-In**
  - 2nd recognition → **Punch-Out**
  - 3rd recognition → **Punch-In**, and so on
- Records are saved in `attendance.csv`

---

## 🔒 Duplicate Face Prevention

- During registration, the new face embedding is compared with all existing users  
- If similarity exceeds the threshold:
  - System displays **“Face already registered”**
  - Registration is stopped  
- User must delete the existing record before re-registering  

---

## 🛡 Basic Spoof / Misuse Prevention

- Requires **live webcam input**
- Captures face data across multiple frames
- Uses embedding consistency to reduce random spoof attempts  

> ⚠️ **Note:** This is basic spoof prevention, not enterprise-grade liveness detection.

---


---

## ⚙️ Installation

### Create Virtual Environment
-----python3 -m venv venv
-----source venv/bin/activate

## Run the Project
python src/ui_cli.py

## 📋 CLI Menu
1. Register New User
2. Start Attendance (Punch In / Out)
3. Delete User
4. Exit

## 🎯 Accuracy Expectations

Works Best In
--Normal lighting conditions
--Front or slightly angled faces
--Clear webcam input

Accuracy Depends On
--Lighting quality
--Camera resolution
--Face visibility

## ⚠️ Known Limitations

-- Reduced performance in very low light
--Extreme face angles may fail
--Basic spoof prevention only
--Single-face focus (not optimized for crowds)

## 🔮 Future Improvements

--Advanced liveness detection (blink / depth-based)
--Multi-face attendance handling
--GUI / Web interface (Streamlit)
--Database-based storage
--Cloud deployment

## 👨‍💻 Author
Dhuriya Ankit Subhash
