import cv2
import numpy as np
import os
import time
from insightface.app import FaceAnalysis

DATA_DIR = "data"
MATCH_THRESHOLD = 0.65
DISPLAY_TIME = 2


def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def show_message(text, color=(0, 255, 0), duration=2):
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
        cv2.imshow("Delete User", frame)
        cv2.waitKey(1)

    cap.release()
    cv2.destroyAllWindows()


def main():
    name = input("Enter user name to delete: ").strip()

    file_path = os.path.join(DATA_DIR, f"{name}.npy")
    if not os.path.exists(file_path):
        print("❌ User not found")
        show_message("User Not Found", (0, 0, 255))
        return

    # Load face
    target_embedding = np.load(file_path)

    app = FaceAnalysis(name="buffalo_l")
    app.prepare(ctx_id=0, det_size=(640, 640))

    cap = cv2.VideoCapture(0)
    print("📸 Look at the camera to confirm identity...")

    confirmed = False
    start = time.time()

    while time.time() - start < 5:
        ret, frame = cap.read()
        if not ret:
            break

        faces = app.get(frame)

        if len(faces) == 1:
            face = faces[0]
            similarity = cosine_similarity(face.embedding, target_embedding)

            box = face.bbox.astype(int)
            cv2.rectangle(
                frame,
                (box[0], box[1]),
                (box[2], box[3]),
                (0, 255, 0),
                2
            )

            if similarity > MATCH_THRESHOLD:
                confirmed = True
                cv2.putText(
                    frame,
                    f"Confirmed: {name}",
                    (box[0], box[1] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.9,
                    (0, 255, 0),
                    2
                )
            else:
                cv2.putText(
                    frame,
                    "Face Mismatch",
                    (box[0], box[1] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.9,
                    (0, 0, 255),
                    2
                )

        cv2.imshow("Delete User", frame)
        cv2.waitKey(1)

    cap.release()
    cv2.destroyAllWindows()

    if not confirmed:
        print("❌ Face verification failed")
        show_message("Verification Failed", (0, 0, 255))
        return

    # 🔐 Final confirmation
    confirm = input(f"Type DELETE to remove '{name}': ").strip()
    if confirm != "DELETE":
        print("❌ Deletion cancelled")
        show_message("Deletion Cancelled", (0, 0, 255))
        return

    os.remove(file_path)
    print(f"✅ User '{name}' deleted successfully")

    show_message(
        f"Deleted: {name}",
        color=(0, 255, 0),
        duration=DISPLAY_TIME
    )


if __name__ == "__main__":
    main()
