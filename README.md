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

## 👨‍💻 Author
Dhuriya Ankit Subhash
