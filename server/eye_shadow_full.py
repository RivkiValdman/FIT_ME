"""
eye_shadow_full.py
------------------
מוסיף צללית מלאה ורכה על העפעפיים בעזרת MediaPipe FaceMesh.
- ממלא 100 % משטח העפעף העליון בצבע שבוחרים.
- מטשטש לקבלת מעבר טבעי.
- שומר קובץ פלט ומציג אותו.

דרישות:
    pip install opencv-python mediapipe matplotlib numpy
"""

import cv2
import mediapipe as mp
import matplotlib.pyplot as plt
import numpy as np

# יצירת אובייקט FaceMesh
mp_face_mesh = mp.solutions.face_mesh


# -------------------------------------------------
# פונקציה שממלאת את כל העפעף העליון בצבע אחיד ומטשטשת
# -------------------------------------------------
def draw_full_upper_lid(img,
                        lm,
                        idxs,
                        color=(90, 140, 180),  # BGR – חום-בז’ לדוגמה
                        alpha=0.5,              # שקיפות הצללית
                        blur_size=35):
    """
    img   – תמונת BGR
    lm    – רשימת FaceMesh landmarks
    idxs  – אינדקסים של כל נקודות העפעף העליון (ברצף סגור!)
    color – צבע הצללית בפורמט BGR
    alpha – כמה הצללית תיראה (0-1)
    blur_size – גודל הקרנל לטשטוש (מספר אי-זוגי)
    """
    h, w = img.shape[:2]

    overlay = img.copy()             # שכבה לערבוב
    mask = np.zeros_like(img)        # מסיכת צבע בגודל התמונה

    # ממירים אינדקסים לקואורדינטות פיקסל בתמונה
    pts = np.array(
        [(int(lm[i].x * w), int(lm[i].y * h)) for i in idxs],
        np.int32
    )

    # מילוי כל הפוליגון בצבע המבוקש
    cv2.fillPoly(mask, [pts], color)

    # טשטוש לקבלת קצוות רכים
    mask = cv2.GaussianBlur(mask, (blur_size, blur_size), 0)

    # ערבוב עם התמונה המקורית
    return cv2.addWeighted(overlay, 1, mask, alpha, 0)


# -------------------------------------------------
# פונקציה ראשית: קוראת תמונה → מזהה פנים → מוסיפה צללית → שומרת ומציגה
# -------------------------------------------------
def apply_shadow_to_image(image_path: str,
                          output_path: str = "event_makeup_output.jpg"):
    image = cv2.imread(image_path)
    if image is None:
        print(f"❌ לא ניתן לקרוא את הקובץ: {image_path}")
        return

    img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # הגדרות FaceMesh
    with mp_face_mesh.FaceMesh(
        static_image_mode=True,
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5
    ) as fm:
        res = fm.process(img_rgb)
        if not res.multi_face_landmarks:
            print("❌ לא זוהו פנים בתמונה")
            return

        annotated = image.copy()

        for face in res.multi_face_landmarks:
            lm = face.landmark

            # --------
            # עין ימין  (FaceMesh – הצד שלנו שמאל)
            # --------
            right_upper_idxs = [
                263, 249, 390, 373, 374, 386, 385, 384, 398,
                362, 382, 381, 380, 374, 263  # סוגרים חזרה לנקודה הראשונה
            ]

            # --------
            # עין שמאל (FaceMesh – הצד שלנו ימין)
            # --------
            left_upper_idxs = [
                # 33, 7, 163, 144, 145, 153, 154, 155, 133,
                # 246, 161, 160, 159, 158, 157, 173, 33

                 414, 286, 442, 282, 283, 276, 353, 342, 359,
                467, 260, 259, 257, 258, 286, 
                
            ]

            # צבע צללית (BGR) – אפשר לשנות
            shadow_color = (0, 0, 255)  # חום-בז’ בהיר

            # החלת הצללית על שתי העיניים
            annotated = draw_full_upper_lid(
                annotated, lm, right_upper_idxs,
                color=shadow_color, alpha=0.45, blur_size=41
            )
            annotated = draw_full_upper_lid(
                annotated, lm, left_upper_idxs,
                color=shadow_color, alpha=0.45, blur_size=41
            )

        # שמירה והצגה
        cv2.imwrite(output_path, annotated)
        print(f"✅ קובץ נשמר: {output_path}")

        plt.imshow(cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB))
        plt.axis("off")
        plt.show()


# -------------------------
# הרצה ישירה מהטרמינל
# -------------------------
if __name__ == "__main__":
    # החלף כאן לשם הקובץ שלך
    apply_shadow_to_image("captured_image.jpg")
