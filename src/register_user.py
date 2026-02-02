import cv2
import numpy as np
import os
import time
from insightface.app import FaceAnalysis

# ---------------- CONFIG ----------------
DATA_DIR = "data"
SCAN_DURATION = 5          # seconds to scan face
DUPLICATE_THRESHOLD = 0.65 # cosine similarity threshold
RESULT_DISPLAY_TIME = 2   # seconds to show result on camera
# ----------------------------------------


def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def load_existing_faces():
    faces = {}
    if not os.path.exists(DATA_DIR):
        return faces

    for file in os.listdir(DATA_DIR):
        if file.endswith(".npy"):
            name = file.replace(".npy", "")
            faces[name] = np.load(os.path.join(DATA_DIR, file))
    return faces


def show_result_on_camera(text, color=(0, 255, 0), duration=2):
    cap = cv2.VideoCapture(0)
    start = time.time()

    while time.time() - start < duration:
        ret, frame = cap.read()
        if not ret:
            break

        cv2.putText(
            frame,
            text,
            (40, 100),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.2,
            color,
            3
        )

        cv2.imshow("Face Registration", frame)
        cv2.waitKey(1)

    cap.release()
    cv2.destroyAllWindows()


def main():
    name = input("Enter user name: ").strip()
    if not name:
        print("❌ Name cannot be empty")
        return

    os.makedirs(DATA_DIR, exist_ok=True)

    # Load model
    app = FaceAnalysis(name="buffalo_l")
    app.prepare(ctx_id=0, det_size=(640, 640))

    cap = cv2.VideoCapture(0)
    print("📸 Scanning face for 5 seconds...")

    embeddings = []
    start_time = time.time()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        faces = app.get(frame)

        if len(faces) == 1:
            face = faces[0]
            embeddings.append(face.embedding)

            box = face.bbox.astype(int)
            cv2.rectangle(
                frame,
                (box[0], box[1]),
                (box[2], box[3]),
                (0, 255, 0),
                2
            )

        remaining = SCAN_DURATION - int(time.time() - start_time)

        cv2.putText(
            frame,
            f"Scanning... {max(0, remaining)}s",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 255),
            2
        )

        cv2.imshow("Register User", frame)

        if time.time() - start_time >= SCAN_DURATION:
            break

        if cv2.waitKey(1) & 0xFF == ord("q"):
            cap.release()
            cv2.destroyAllWindows()
            return

    cap.release()
    cv2.destroyAllWindows()

    if not embeddings:
        print("❌ No face detected. Try again.")
        show_result_on_camera("No Face Detected", (0, 0, 255))
        return

    avg_embedding = np.mean(embeddings, axis=0)

    # -------- DUPLICATE CHECK --------
    existing_faces = load_existing_faces()
    for existing_name, existing_emb in existing_faces.items():
        similarity = cosine_similarity(avg_embedding, existing_emb)
        if similarity > DUPLICATE_THRESHOLD:
            msg = f"Already Registered: {existing_name}"
            print(f"\n❌ {msg}\n")

            show_result_on_camera(
                text=msg,
                color=(0, 0, 255),
                duration=RESULT_DISPLAY_TIME
            )
            return
    # --------------------------------

    # -------- SAVE NEW USER --------
    np.save(os.path.join(DATA_DIR, f"{name}.npy"), avg_embedding)
    msg = f"Registered: {name}"
    print(f"\n✅ {msg}\n")

    show_result_on_camera(
        text=msg,
        color=(0, 255, 0),
        duration=RESULT_DISPLAY_TIME
    )


if __name__ == "__main__":
    main()
