import sys
import cv2
import mediapipe as mp
import numpy as np
import matplotlib.pyplot as plt

mp_face_mesh = mp.solutions.face_mesh

# ------------------------------------------------------------
#  פונקציה כללית לצביעה רכה של אזור עיניים
# ------------------------------------------------------------

def draw_soft_eye_fill(img,
                       lm,
                       idxs,
                       color=(255, 255, 255),  # BGR
                       alpha=0.7,
                       blur_size=35):
    """מקבל תמונה + Landmark‑ים וממלא פוליגון בצבע רך."""

    h, w = img.shape[:2]
    mask = np.zeros_like(img)

    # Landmark -> פיקסלים
    pts = [(int(lm[i].x * w), int(lm[i].y * h)) for i in idxs]
    cv2.fillPoly(mask, [np.array(pts, np.int32)], color)

    # טשטוש רך
    blurred = cv2.GaussianBlur(mask, (blur_size, blur_size), 0)

    return cv2.addWeighted(img, 1.0, blurred, alpha, 0)


# ------------------------------------------------------------
#  פונקציה ראשית
# ------------------------------------------------------------

def apply_eye_makeup(image_path: str = "captured_image.jpg",
                     output_path: str = "eye_makeup_output.jpg") -> None:
    """מזהה פנים ומוסיף שתי שכבות צללית: שימר לבן + חום‑בהיר."""

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

        # ----- שכבה 1: שימר לבן -----
        shimmer_white_idxs = [465, 464, 463, 414, 286, 441, 413]
        shimmer_white_color = (255, 255, 255)  # לבן בוהק

        # ----- שכבה 2: חום‑בהיר -----
        light_brown_idxs = [441, 442, 282, 283, 444, 259, 257, 258, 286]
        # BGR   (כחול, ירוק, אדום): חום‑בהיר רך
        light_brown_color = (64, 74, 92)

        #------שכבה 3 חום כהה -------
        dark_brown_idxs = [259, 444, 283, 276, 353,342,359,467, 260,259]
        dark_brown_color = (42, 42, 42)  # חום כהה

        for face in res.multi_face_landmarks:
            lm = face.landmark

            # שימר לבן
            annotated = draw_soft_eye_fill(
                annotated,
                lm,
                shimmer_white_idxs,
                color=shimmer_white_color,
                alpha=0.75,
                blur_size=35,
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
    apply_eye_makeup(input_path)
