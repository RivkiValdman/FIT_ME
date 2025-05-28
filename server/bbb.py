import sys
import cv2
import mediapipe as mp
import numpy as np
import matplotlib.pyplot as plt

mp_face_mesh = mp.solutions.face_mesh

# ------------------------------------------------------------
#  צביעה רכה של פוליגון – שימר-לבן בזווית-העין
# ------------------------------------------------------------
def draw_soft_eye_fill(img, lm, idxs,
                       color=(255, 255, 255),
                       alpha=0.8,
                       blur_size=35):
    h, w = img.shape[:2]
    mask = np.zeros_like(img)

    pts = [(int(lm[i].x * w), int(lm[i].y * h)) for i in idxs]
    cv2.fillPoly(mask, [np.array(pts, np.int32)], color)

    blurred = cv2.GaussianBlur(mask, (blur_size, blur_size), 0)
    return cv2.addWeighted(img, 1.0, blurred, alpha, 0)


# ------------------------------------------------------------
#  צללית על כל העפעף – מחלקת לשלישים
# ------------------------------------------------------------
def draw_upper_eyelid_area(img, lm, idxs, colors,
                           blur_size=35,
                           alpha=0.6):
    h, w = img.shape[:2]
    mask = np.zeros_like(img)

    pts = [(int(lm[i].x * w), int(lm[i].y * h)) for i in idxs]
    thirds = len(pts) // 3

    if thirds >= 1:
        cv2.fillPoly(mask, [np.array(pts[:thirds],        np.int32)], colors[0])  # שליש פנימי
        cv2.fillPoly(mask, [np.array(pts[thirds:2*thirds], np.int32)], colors[1])  # אמצעי
        cv2.fillPoly(mask, [np.array(pts[2*thirds:],      np.int32)], colors[2])  # חיצוני
    else:
        cv2.fillPoly(mask, [np.array(pts, np.int32)], colors[1])

    blurred = cv2.GaussianBlur(mask, (blur_size, blur_size), 0)
    return cv2.addWeighted(img, 1.0, blurred, alpha, 0)


# ------------------------------------------------------------
#  פונקציה ראשית
# ------------------------------------------------------------
def apply_combined_eye_makeup(image_path="captured_image.jpg",
                              output_path="combined_eye_makeup.jpg"):
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"❌ לא ניתן לקרוא את הקובץ: {image_path}")

    img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    with mp_face_mesh.FaceMesh(
        static_image_mode=True,
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5,
    ) as fm:
        res = fm.process(img_rgb)
        if not res.multi_face_landmarks:
            raise ValueError("❌ לא זוהו פנים בתמונה")

        annotated = image.copy()

        # --- מערכי הנקודות ---
        inner_shimmer_idxs = [465, 464, 463, 414, 286, 441, 413]            # שימר-לבן בזווית-העין
        upper_eyelid_idxs  = [414, 286, 442, 282, 283, 276, 353, 342, 359,
                              467, 260, 259, 257, 258, 286]                 # כל העפעף העליון

        # --- צבעים (BGR) ---
        shimmer_white = (255, 255, 255)   # פנימי – בוהק
        dark_brown    = (42,  42,  42)    # אמצעי + חיצוני – חום-כהה

        for face in res.multi_face_landmarks:
            lm = face.landmark

            # שכבה 1: העפעף – לבן פנימי, ושני השלישים הנותרים חום-כהה
            annotated = draw_upper_eyelid_area(
                annotated, lm, upper_eyelid_idxs,
                colors=[shimmer_white, dark_brown, dark_brown],
                blur_size=35, alpha=0.6
            )

            # שכבה 2: שימר-לבן ממוקד בזווית-העין להדגשה
            annotated = draw_soft_eye_fill(
                annotated, lm, inner_shimmer_idxs,
                color=shimmer_white,
                alpha=0.75, blur_size=31
            )

    cv2.imwrite(output_path, annotated)
    print(f"✅ נשמר: {output_path}")

    plt.imshow(cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB))
    plt.axis("off")
    plt.show()


# ------------------------------------------------------------
#  הרצה משורת הפקודה
# ------------------------------------------------------------
if __name__ == "__main__":
    input_path = sys.argv[1] if len(sys.argv) > 1 else "captured_image.jpg"
    apply_combined_eye_makeup(input_path)
