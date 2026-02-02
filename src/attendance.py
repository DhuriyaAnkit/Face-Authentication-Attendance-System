import cv2
import numpy as np
import os
import csv
from datetime import datetime
from insightface.app import FaceAnalysis

DATA_DIR = "data"
ATTENDANCE_FILE = "attendance.csv"
THRESHOLD = 0.6


def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def load_known_faces():
    known_faces = {}
    for file in os.listdir(DATA_DIR):
        if file.endswith(".npy"):
            name = file.replace(".npy", "")
            known_faces[name] = np.load(os.path.join(DATA_DIR, file))
    return known_faces


def mark_attendance(name):
    now = datetime.now()
    date = now.strftime("%Y-%m-%d")
    time = now.strftime("%H:%M:%S")

    records = []
    if os.path.exists(ATTENDANCE_FILE):
        with open(ATTENDANCE_FILE, "r") as f:
            reader = list(csv.reader(f))
            records = reader[1:] if len(reader) > 1 else []

    user_today = [r for r in records if r[0] == name and r[1] == date]

    if not user_today:
        status = "Punch-In"
    else:
        last_status = user_today[-1][3]
        if last_status == "Punch-In":
            status = "Punch-Out"
        else:
            print(f"{name} already punched out today.")
            return False

    write_header = not os.path.exists(ATTENDANCE_FILE)

    with open(ATTENDANCE_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        if write_header:
            writer.writerow(["Name", "Date", "Time", "Status"])
        writer.writerow([name, date, time, status])

    print(f"{name} → {status} at {time}")
    return True


def main():
    known_faces = load_known_faces()
    if not known_faces:
        print("No registered users found.")
        return

    app = FaceAnalysis(name="buffalo_l")
    app.prepare(ctx_id=0, det_size=(640, 640))

    cap = cv2.VideoCapture(0)
    print("Attendance started. Look at the camera...")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        faces = app.get(frame)

        for face in faces:
            emb = face.embedding
            box = face.bbox.astype(int)

            best_match = None
            best_score = -1

            for name, known_emb in known_faces.items():
                score = cosine_similarity(emb, known_emb)
                if score > best_score:
                    best_score = score
                    best_match = name

            if best_score > THRESHOLD:
                success = mark_attendance(best_match)

                label = f"{best_match} ({best_score:.2f})"
                cv2.rectangle(frame, (box[0], box[1]),
                              (box[2], box[3]), (0, 255, 0), 2)
                cv2.putText(frame, label,
                            (box[0], box[1] - 10),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.8, (0, 255, 0), 2)

                cv2.imshow("Attendance", frame)
                cv2.waitKey(1500)

                if success:
                    cap.release()
                    cv2.destroyAllWindows()
                    print("Camera closed. Attendance complete.")
                    return

        cv2.imshow("Attendance System", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
