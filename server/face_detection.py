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

def draw_eyelashes(img, lm, idxs, length=4, color=(40,40,40), thickness=1, density=5):
    h, w = img.shape[:2]
    for i in range(len(idxs)-1):
        x1, y1 = int(lm[idxs[i]].x*w), int(lm[idxs[i]].y*h)
        x2, y2 = int(lm[idxs[i+1]].x*w), int(lm[idxs[i+1]].y*h)
        for j in range(density):
            t = j/density
            x = int(x1 + t*(x2-x1))
            y = int(y1 + t*(y2-y1))
            ang = random.uniform(-0.5,0.5)
            dx = int(np.sin(ang)*length)
            dy = -int(np.cos(ang)*length)
            cv2.line(img, (x,y), (x+dx,y+dy), color, thickness)

def draw_eyeliner(img, lm, idxs, color=(0,0,0), thickness=1):
    pts = [(int(lm[i].x*img.shape[1]), int(lm[i].y*img.shape[0])) for i in idxs]
    for i in range(len(pts)-1):
        cv2.line(img, pts[i], pts[i+1], color, thickness)

# -------------------------------------------------
#   Main processing
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

            # ---------- skin tone ----------
            skin_tone = np.mean(np.array([
                sample_color(image, lm, [10,338,297]),
                sample_color(image, lm, [234,93]),
                sample_color(image, lm, [454,323]),
                sample_color(image, lm, [1,2,168]),
                sample_color(image, lm, [152,199])
            ]), axis=0).astype(np.uint8)

            # ---------- brows ----------
            brow_R = [70,63,105,66,107,55,65,52]
            brow_L = [285,336,296,334,293,300,282,295]

            col_R = sample_color(image, lm, brow_R)
            col_L = sample_color(image, lm, brow_L)
            brow_col = ((col_R.astype(np.float32)+col_L.astype(np.float32))/2).astype(np.uint8)
            brow_col = tuple(int(c) for c in brow_col)

            draw_contour(annotated, lm, brow_R+[brow_R[0]], brow_col, thickness=1)
            draw_contour(annotated, lm, brow_L+[brow_L[0]], brow_col, thickness=1)

            # ✅ מילוי טבעי כמו צללית
            def fill_brow(img, lmks, idxs, color, alpha=0.6):
                h, w = img.shape[:2]
                mask = np.zeros((h, w), dtype=np.uint8)
                pts = np.array([(int(lmks[i].x * w), int(lmks[i].y * h)) for i in idxs], np.int32)
                cv2.fillPoly(mask, [pts], 255)
                mask = cv2.GaussianBlur(mask, (15, 15), 0)
                color_layer = np.full_like(img, color)
                for c in range(3):
                    img[..., c] = img[..., c] * (1 - (alpha * mask / 255.0)) + color_layer[..., c] * (alpha * mask / 255.0)

            fill_brow(annotated, lm, brow_R, brow_col)
            fill_brow(annotated, lm, brow_L, brow_col)

            # ---------- eyeliner & lashes ----------
            upper_R = [33,160,158,157,173]
            upper_L = [263,387,385,384,398]
            draw_eyeliner(annotated, lm, upper_R)
            draw_eyeliner(annotated, lm, upper_L)
            draw_eyelashes(annotated, lm, upper_R)
            draw_eyelashes(annotated, lm, upper_L)

            # ---------- rest of makeup ----------
            outline = [10,338,297,332,284,251,389,356,454,323,361,288,397,365,
                       379,378,400,377,152,148,176,149,150,136,172,58,132,
                       93,234,127,162,21,54,103,67,109]
            mask = np.zeros((h,w), dtype=np.uint8)
            cv2.fillPoly(mask, [np.array([
                (int(lm[i].x*w), int(lm[i].y*h)) for i in outline
            ], np.int32)], 255)

            eye_R = [33,160,158,157,173,133,155,154,153,145]
            eye_L = [263,387,385,384,398,362,382,381,380,374]
            lips_out = [61,185,40,39,37,0,267,269,270,409,291,308,415,310,
                        311,312,13,82,81,80,191,78]
            lips_in  = [61,76,62,78,95,88,178,87,14,317,402,318,324,308,291,
                        375,321,405,314,17,84,181,91,146]
            no_make = np.zeros((h,w), dtype=np.uint8)
            for region in [eye_R,eye_L,brow_R,brow_L,lips_out,lips_in]:
                cv2.fillPoly(no_make, [np.array([
                    (int(lm[i].x*w), int(lm[i].y*h)) for i in region
                ], np.int32)], 255)
            mask = cv2.bitwise_and(mask, cv2.bitwise_not(no_make))
            annotated[:] = apply_makeup(annotated, mask.astype(bool), skin_tone, alpha=0.4)

            # lips
            lip_col = (80,35,150)
            overlay = annotated.copy()
            cv2.fillPoly(overlay, [np.array([
                (int(lm[i].x*w), int(lm[i].y*h)) for i in lips_out
            ], np.int32)], lip_col)
            cv2.fillPoly(overlay, [np.array([
                (int(lm[i].x*w), int(lm[i].y*h)) for i in lips_in
            ], np.int32)], lip_col)
            cv2.addWeighted(overlay, 0.4, annotated, 0.6, 0, annotated)
            draw_contour(annotated, lm, lips_out+[lips_out[0]], lip_col, 1)
            draw_contour(annotated, lm, lips_in+[lips_in[0]], lip_col, 1)

        # ---------- save & show ----------
        cv2.imwrite("output_cllase_makup.jpg", annotated)
        print("✅ נשמר: output_cllase_makup.jpg")
        plt.imshow(cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB))
        plt.axis("off")
        plt.show()

if __name__ == "__main__":
    detect_and_draw_all_contours("captured_image.jpg")
