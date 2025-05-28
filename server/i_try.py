
import cv2
import mediapipe as mp
import matplotlib.pyplot as plt
import numpy as np

mp_face_mesh = mp.solutions.face_mesh

def draw_upper_eyelid_area(img, lm, idxs, colors, blur_size=35):
    h, w = img.shape[:2]
    overlay = img.copy()
    mask = np.zeros_like(img)

    # יצירת נקודות לפי המיפוי
    pts = [(int(lm[i].x * w), int(lm[i].y * h)) for i in idxs]
    pts_np = np.array(pts, np.int32)

    # מילוי כל האזור בצבע אמצעי
    cv2.fillPoly(mask, [pts_np], colors[1])

    # חלוקה לשלישים
    thirds = len(pts) // 3
    if thirds >= 1:
        cv2.fillPoly(mask, [np.array(pts[:thirds], np.int32)], colors[0])
        cv2.fillPoly(mask, [np.array(pts[-thirds:], np.int32)], colors[2])

    # טשטוש לקבלת מראה רך
    blurred = cv2.GaussianBlur(mask, (blur_size, blur_size), 0)
    return cv2.addWeighted(img, 1, blurred, 0.5, 0)

def detect_and_draw_event_luke(image_path: str):
    image = cv2.imread(image_path)
    if image is None:
        print("❌ לא ניתן לקרוא את הקובץ:", image_path)
        return

    img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    with mp_face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1, refine_landmarks=True, min_detection_confidence=0.5) as fm:
        res = fm.process(img_rgb)
        annotated = image.copy()

        if not res.multi_face_landmarks:
            print("❌ לא זוהו פנים בתמונה")
            return

        for face in res.multi_face_landmarks:
            lm = face.landmark

            upper_eyelid_idxs = [
                414, 286, 442, 282, 283, 276, 353, 342, 359,
                467, 260, 259, 257, 258, 286, 
                
            ]

            # צבעים: פנימי, אמצעי, חיצוני (BGR)
            colors = [(19, 69, 139),(19, 69, 139), (19, 69, 139)]

            annotated = draw_upper_eyelid_area(annotated, lm, upper_eyelid_idxs, colors)

        cv2.imwrite("event_makeup_output.jpg", annotated)
        print("✅ נשמר: event_makeup_output.jpg")
        plt.imshow(cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB))
        plt.axis("off")
        plt.show()

if __name__ == "__main__":
    detect_and_draw_event_luke("captured_image.jpg")
    
