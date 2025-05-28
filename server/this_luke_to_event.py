# layered_eye_makeup.py  – גרסה משופרת
import cv2
import mediapipe as mp
import numpy as np
from typing import List, Tuple

mp_face_mesh = mp.solutions.face_mesh

# ------------------------------------------------------------
#  קבועי צבעים (BGR)
# ------------------------------------------------------------
LIGHT_BROWN: Tuple[int, int, int] = (80, 130, 250)
MID_BROWN  : Tuple[int, int, int] = (60,  90, 170)
DARK_BROWN : Tuple[int, int, int] = (30,  30,  30)
PURE_WHITE : Tuple[int, int, int] = (255,255,255)

# ------------------------------------------------------------
#  Landmark-ים לעין ימין  (אם התמונה מראה רק עין שמאל – החליפי מראה)
# ------------------------------------------------------------
EYE_FULL   : List[int] = [464, 413, 441, 442, 282, 283, 300,
                          383, 353, 342, 359, 263, 466, 388,
                          387, 386, 385, 384, 398, 362, 463]

EYE_INNER  : List[int] = [465, 464, 463, 414, 286, 441, 413]     # אזור פנימי
EYE_MIDDLE : List[int] = [384, 286, 442, 282, 283, 276, 353,
                          342, 467, 466, 388, 387, 386, 385]     # אמצע
EYE_OUTER  : List[int] = [260, 445, 276, 300, 383, 353,
                          342, 467]                              # חיצוני

# ------------------------------------------------------------
def _lm_to_pts(lm, idxs, w, h):
    return np.array([(int(lm[i].x * w), int(lm[i].y * h)) for i in idxs],
                    dtype=np.int32)

def paint_layer(overlay: np.ndarray,
                lm,
                idxs: List[int],
                color: Tuple[int, int, int],
                blur: int,
                opacity: float) -> None:
    """צובעת שכבה על-גבי overlay שקוף."""
    h, w = overlay.shape[:2]
    mask = np.zeros_like(overlay)

    cv2.fillPoly(mask, [_lm_to_pts(lm, idxs, w, h)], color)
    mask = cv2.GaussianBlur(mask, (blur, blur), 0)

    cv2.addWeighted(mask, opacity, overlay, 1.0, 0, dst=overlay)

# ------------------------------------------------------------
def apply_layered_eye_makeup(img: np.ndarray, lm) -> np.ndarray:
    overlay = np.zeros_like(img)     # נצבור עליו את כל השכבות

    # 1. שליש חיצוני – חום כהה
    paint_layer(overlay, lm, EYE_OUTER,  DARK_BROWN, blur=25, opacity=0.80)

    # 2. שליש אמצעי – חום בינוני
    paint_layer(overlay, lm, EYE_MIDDLE, MID_BROWN,  blur=31, opacity=0.60)

    # 3. שליש פנימי – לבן/שימר
    paint_layer(overlay, lm, EYE_INNER,  PURE_WHITE, blur=25, opacity=0.75)

    # ⭐ אם תרצי “בסיס” בהיר על כל העפעף, שימי אותו כאן עם אלפא נמוך
    # paint_layer(overlay, lm, EYE_FULL, LIGHT_BROWN, blur=41, opacity=0.25)

    # מיזוג חד-פעמי עם התמונה המקורית
    final = cv2.addWeighted(img, 1.0, overlay, 1.0, 0)
    return final

# ------------------------------------------------------------
def makeup_on_image(image_path: str,
                    save_as: str = "layered_eye_output.jpg") -> None:
    img_bgr = cv2.imread(image_path)
    if img_bgr is None:
        raise FileNotFoundError(f"לא נמצא קובץ: {image_path}")

    with mp_face_mesh.FaceMesh(static_image_mode=True,
                               max_num_faces=1,
                               refine_landmarks=True,
                               min_detection_confidence=0.5) as fm:
        res = fm.process(cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB))
        if not res.multi_face_landmarks:
            raise RuntimeError("❌ לא זוהו פנים בתמונה")

        for face in res.multi_face_landmarks:
            img_bgr = apply_layered_eye_makeup(img_bgr, face.landmark)

    cv2.imwrite(save_as, img_bgr)
    print(f"✅ נשמר: {save_as}")

    # תצוגה
    import matplotlib.pyplot as plt
    plt.imshow(cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB))
    plt.axis("off")
    plt.show()

# ------------------------------------------------------------
if __name__ == "__main__":
    makeup_on_image("captured_image.jpg")
