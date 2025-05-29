import cv2
import mediapipe as mp
import matplotlib.pyplot as plt
import numpy as np
import random

mp_face_mesh = mp.solutions.face_mesh

# -------------------------------------------------
#   Helper utilities
# -------------------------------------------------

def draw_contour(img, lm, idxs, color, thickness=1, closed=True):
    pts = [(int(lm[i].x * img.shape[1]), int(lm[i].y * img.shape[0])) for i in idxs]
    for i in range(len(pts) - 1):
        cv2.line(img, pts[i], pts[i+1], color, thickness)
    if closed and len(pts) > 2:
        cv2.line(img, pts[-1], pts[0], color, thickness)

def sample_color(img, lm, idxs):
    return np.mean(
        [img[int(lm[i].y * img.shape[0]), int(lm[i].x * img.shape[1])] for i in idxs],
        axis=0
    ).astype(np.uint8)

def apply_makeup(img, mask, color, alpha=0.4):
    overlay = img.copy()
    overlay[mask] = (1 - alpha) * overlay[mask] + alpha * color
    return overlay.astype(np.uint8)

def _lm_to_pts(lm, idxs, w, h):
    return np.array([(int(lm[i].x * w), int(lm[i].y * h)) for i in idxs], dtype=np.int32)

def paint_layer(overlay, lm, idxs, color, blur, opacity):
    h, w = overlay.shape[:2]
    mask = np.zeros_like(overlay)
    cv2.fillPoly(mask, [_lm_to_pts(lm, idxs, w, h)], color)
    mask = cv2.GaussianBlur(mask, (blur, blur), 0)
    cv2.addWeighted(mask, opacity, overlay, 1.0, 0, dst=overlay)

def draw_eyeliner(img, lm, idxs, color=(0, 0, 0), thickness=1):
    h, w = img.shape[:2]
    pts = [(int(lm[i].x * w), int(lm[i].y * h)) for i in idxs]
    for i in range(len(pts) - 1):
        cv2.line(img, pts[i], pts[i + 1], color, thickness, lineType=cv2.LINE_AA)

def draw_eyelashes(img, lm, idxs, length=6, color=(40, 40, 40), thickness=1, density=8, long_factor=1.6):
    h, w = img.shape[:2]
    LONG_LASH_POINTS = {387, 388, 466, 263, 359}
    for i in range(len(idxs) - 1):
        idx_a, idx_b = idxs[i], idxs[i + 1]
        x1, y1 = int(lm[idx_a].x * w), int(lm[idx_a].y * h)
        x2, y2 = int(lm[idx_b].x * w), int(lm[idx_b].y * h)
        seg_length = length * (long_factor if (idx_a in LONG_LASH_POINTS or idx_b in LONG_LASH_POINTS) else 1.0)
        for j in range(density):
            t = j / density
            x = int(x1 + t * (x2 - x1))
            y = int(y1 + t * (y2 - y1))
            angle = random.uniform(-0.5, 0.5)
            dx = int(np.sin(angle) * seg_length)
            dy = -int(np.cos(angle) * seg_length)
            cv2.line(img, (x, y), (x + dx, y + dy), color, thickness, lineType=cv2.LINE_AA)

def apply_layered_eye_makeup(img, lm):
    overlay = np.zeros_like(img)
    EYE_INNER = [465, 464, 463, 414, 286, 441, 413]
    EYE_MIDDLE = [384, 286, 442, 282, 283, 276, 353, 342, 467, 466, 388, 387, 386, 385]
    EYE_OUTER = [260, 445, 276, 300, 383, 353, 342, 467]
    EYE_LINER = [398, 384, 385, 386, 387, 388, 466, 263, 359]

    EYE_INNER_R = [243 ,244 ,189 ,221 ,56 ,157 ,173]
    EYE_MIDDLE_R = [157 ,221 ,55 ,65, 52, 53 ,56 ,124, 113 ,247, 246 ,161 ,160, 159 ,158]
    EYE_OUTER_R = [130, 35 ,246 ,161 ,30 ,225 ,46 ,124 ,113 ]
    EYE_LINER_R = [243 ,173, 157, 158 ,159 ,160, 161, 246, 33, 130]



    paint_layer(overlay, lm, EYE_OUTER, (30, 30, 30), blur=25, opacity=0.80)
    paint_layer(overlay, lm, EYE_MIDDLE, (60, 90, 170), blur=31, opacity=0.60)
    paint_layer(overlay, lm, EYE_INNER, (255, 255, 255), blur=25, opacity=0.75)

    paint_layer(overlay, lm, EYE_INNER_R, (255, 255, 255), blur=25, opacity=0.75)
    paint_layer(overlay, lm, EYE_MIDDLE_R, (60, 90, 170), blur=31, opacity=0.60)
    paint_layer(overlay, lm, EYE_OUTER_R, (30, 30, 30), blur=25, opacity=0.80)


    final = cv2.addWeighted(img, 1.0, overlay, 1.0, 0)
    draw_eyeliner(final, lm, EYE_LINER, color=(40, 40, 40), thickness=1)
    draw_eyelashes(final, lm, EYE_LINER, length=3, density=2, color=(40, 40, 40), thickness=1, long_factor=1.2)

        # אייליינר וריסים לעין ימין
    draw_eyeliner(final, lm, EYE_LINER_R, color=(40, 40, 40), thickness=1)
    draw_eyelashes(final, lm, EYE_LINER_R, length=3, density=2, color=(40, 40, 40), thickness=1, long_factor=1.2)

    return final
def draw_soft_cheek_contour(img, lm, idxs,
                            color=(30, 50, 100),  # גוון חום כהה BGR
                            alpha=0.5,
                            blur_size=65):
    h, w = img.shape[:2]
    mask = np.zeros_like(img)
    pts = [(int(lm[i].x * w), int(lm[i].y * h)) for i in idxs]
    cv2.fillPoly(mask, [np.array(pts, np.int32)], color)
    blurred = cv2.GaussianBlur(mask, (blur_size, blur_size), 0)
    return cv2.addWeighted(img, 1.0, blurred, alpha, 0)

# -------------------------------------------------
def detect_and_draw_all_contours(image_path: str):
    image = cv2.imread(image_path)
    if image is None:
        print("❌ לא ניתן לקרוא את הקובץ:", image_path)
        return

    img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    with mp_face_mesh.FaceMesh(
        static_image_mode=True,
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5
    ) as fm:
        res = fm.process(img_rgb)
        annotated = image.copy()

        if not res.multi_face_landmarks:
            print("❌ לא זוהו פנים בתמונה")
            return

        for face in res.multi_face_landmarks:
            lm = face.landmark
            h, w = annotated.shape[:2]

            # גבות
            brow_R = [70,63,105,66,107,55,65,52]
            brow_L = [285,336,296,334,293,300,282,295]
            col_R = sample_color(image, lm, brow_R)
            col_L = sample_color(image, lm, brow_L)
            brow_col = ((col_R.astype(np.float32)+col_L.astype(np.float32))/2).astype(np.uint8)
            brow_col = tuple(int(c) for c in brow_col)

            draw_contour(annotated, lm, brow_R+[brow_R[0]], brow_col, thickness=1)
            draw_contour(annotated, lm, brow_L+[brow_L[0]], brow_col, thickness=1)

            def fill_brow(img, lmks, idxs, color, alpha=0.6):
                mask = np.zeros((h, w), dtype=np.uint8)
                pts = np.array([(int(lmks[i].x * w), int(lmks[i].y * h)) for i in idxs], np.int32)
                cv2.fillPoly(mask, [pts], 255)
                mask = cv2.GaussianBlur(mask, (15, 15), 0)
                color_layer = np.full_like(img, color)
                for c in range(3):
                    img[..., c] = img[..., c] * (1 - (alpha * mask / 255.0)) + color_layer[..., c] * (alpha * mask / 255.0)

            fill_brow(annotated, lm, brow_R, brow_col)
            fill_brow(annotated, lm, brow_L, brow_col)

            # מייקאפ כללי
            outline = [10,338,297,332,284,251,389,356,454,323,361,288,397,365,
                       379,378,400,377,152,148,176,149,150,136,172,58,132,
                       93,234,127,162,21,54,103,67,109]
            mask = np.zeros((h,w), dtype=np.uint8)
            cv2.fillPoly(mask, [np.array([(int(lm[i].x*w), int(lm[i].y*h)) for i in outline], np.int32)], 255)
            eye_R = [33,160,158,157,173,133,155,154,153,145]
            eye_L = [263,387,385,384,398,362,382,381,380,374]
            lips_out = [61,185,40,39,37,0,267,269,270,409,291,308,415,310,
                        311,312,13,82,81,80,191,78]
            lips_in  = [61,76,62,78,95,88,178,87,14,317,402,318,324,308,291,
                        375,321,405,314,17,84,181,91,146]
            no_make = np.zeros((h,w), dtype=np.uint8)
            for region in [eye_R,eye_L,brow_R,brow_L,lips_out,lips_in]:
                cv2.fillPoly(no_make, [np.array([(int(lm[i].x*w), int(lm[i].y*h)) for i in region], np.int32)], 255)
            mask = cv2.bitwise_and(mask, cv2.bitwise_not(no_make))
            skin_tone = np.mean(np.array([
                sample_color(image, lm, [10,338,297]),
                sample_color(image, lm, [234,93]),
                sample_color(image, lm, [454,323]),
                sample_color(image, lm, [1,2,168]),
                sample_color(image, lm, [152,199])
            ]), axis=0).astype(np.uint8)
            annotated[:] = apply_makeup(annotated, mask.astype(bool), skin_tone, alpha=0.4)

            # שפתיים
            lip_col = (80,35,150)
            overlay = annotated.copy()
            cv2.fillPoly(overlay, [np.array([(int(lm[i].x*w), int(lm[i].y*h)) for i in lips_out], np.int32)], lip_col)
            cv2.fillPoly(overlay, [np.array([(int(lm[i].x*w), int(lm[i].y*h)) for i in lips_in], np.int32)], lip_col)
            cv2.addWeighted(overlay, 0.4, annotated, 0.6, 0, annotated)
            draw_contour(annotated, lm, lips_out+[lips_out[0]], lip_col, 1)
            draw_contour(annotated, lm, lips_in+[lips_in[0]], lip_col, 1)

            # עיניים
            annotated = apply_layered_eye_makeup(annotated, lm)

            # הצללת לחי ימין
            CHEEK_R = [356, 447, 352, 376, 433,401,323]
            annotated = draw_soft_cheek_contour(annotated, lm, CHEEK_R)

            # הצללת לחי שמאל    
            CHEEK_L = [127, 227, 123, 147, 213, 177,63,234]
            annotated = draw_soft_cheek_contour(annotated, lm, CHEEK_L) 

            # סומק ורוד בלחי
            BLUSH_AREA = [280, 346, 340, 372, 264, 447, 352]
            annotated = draw_soft_cheek_contour(
                annotated, lm, BLUSH_AREA,
                color=(180, 105, 255),  # BGR של ורוד בהיר
                alpha=0.4,
                blur_size=65
            )

            # סומק ורוד בלחי שמאל
            BLUSH_AREA_L = [50, 123, 227, 34, 143, 111, 117]
            annotated = draw_soft_cheek_contour(
                annotated, lm, BLUSH_AREA_L,
                color=(180, 105, 255),  # ורוד בהיר BGR
                alpha=0.4,
                blur_size=65
            )

            # שימר לבן מעל הסומק בלחי שמאל
            annotated = draw_soft_cheek_contour(
                annotated, lm, BLUSH_AREA_L,
                color=(255, 255, 255),
                alpha=0.25,
                blur_size=45
            )

            # שימר לבן מעל הסומק
            annotated = draw_soft_cheek_contour(
                annotated, lm, BLUSH_AREA,
                color=(255, 255, 255),
                alpha=0.25,
                blur_size=45
            )


        cv2.imwrite("output_final_makeup.jpg", annotated)
        print("✅ נשמר: output_final_makeup.jpg")
        plt.imshow(cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB))
        plt.axis("off")
        plt.show()

if __name__ == "__main__":
    detect_and_draw_all_contours("captured_image.jpg")
