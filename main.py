import os
import cv2
import numpy as np
import pytesseract
import csv


# ===============================
# KONFIGURASI
# ===============================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_DIR = os.path.join(BASE_DIR, "data")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")


NOMOR_ASLI = "571012022000056"



# ===============================
# ROI NOMOR IJAZAH (T5)
# ===============================

def crop_number_roi(image):

    x1 = 2194
    y1 = 2506

    x2 = 2374
    y2 = 3324


    roi = image[y1:y2, x1:x2]

    return roi



# ===============================
# OCR NOMOR IJAZAH (T5)
# ===============================

def run_ocr(image):


    image = cv2.rotate(
        image,
        cv2.ROTATE_90_CLOCKWISE
    )


    image = cv2.resize(
        image,
        None,
        fx=3,
        fy=3,
        interpolation=cv2.INTER_CUBIC
    )


    config = (
        "--psm 7 "
        "-c tessedit_char_whitelist=0123456789"
    )


    result = pytesseract.image_to_string(
        image,
        config=config
    )


    result = "".join(
        c for c in result
        if c.isdigit()
    )


    return result



# ===============================
# CER
# ===============================

def levenshtein(a,b):

    m = len(a)
    n = len(b)

    dp = np.zeros(
        (m+1,n+1),
        dtype=int
    )


    for i in range(m+1):
        dp[i][0]=i


    for j in range(n+1):
        dp[0][j]=j


    for i in range(1,m+1):

        for j in range(1,n+1):

            cost = 0

            if a[i-1] != b[j-1]:
                cost = 1


            dp[i][j]=min(
                dp[i-1][j]+1,
                dp[i][j-1]+1,
                dp[i-1][j-1]+cost
            )


    return dp[m][n]



def calculate_cer(ref,pred):

    if pred == "":
        return 1.0


    return levenshtein(
        ref,
        pred
    ) / len(ref)



# ===============================
# ROI TANDA TANGAN (T6)
# ===============================

ROI_SIGNATURE = (
    0.7055,
    0.8140,
    0.1290,
    0.3604
)



def crop_signature_roi(image):

    h,w = image.shape[:2]


    x1,x2,y1,y2 = ROI_SIGNATURE


    roi = image[
        int(y1*h):int(y2*h),
        int(x1*w):int(x2*w)
    ]


    scale = 400 / roi.shape[1]


    roi = cv2.resize(
        roi,
        None,
        fx=scale,
        fy=scale,
        interpolation=cv2.INTER_AREA
    )


    return roi



# ===============================
# ANALISIS TANDA TANGAN
# ===============================

def analyze_signature(roi):


    gray = cv2.cvtColor(
        roi,
        cv2.COLOR_BGR2GRAY
    )


    gray = cv2.GaussianBlur(
        gray,
        (3,3),
        0
    )


    _,binary = cv2.threshold(
        gray,
        0,
        255,
        cv2.THRESH_BINARY_INV+
        cv2.THRESH_OTSU
    )


    kernel_open = cv2.getStructuringElement(
        cv2.MORPH_ELLIPSE,
        (2,2)
    )


    kernel_close = cv2.getStructuringElement(
        cv2.MORPH_ELLIPSE,
        (5,5)
    )


    morph = cv2.morphologyEx(
        binary,
        cv2.MORPH_OPEN,
        kernel_open
    )


    morph = cv2.morphologyEx(
        morph,
        cv2.MORPH_CLOSE,
        kernel_close
    )



    foreground = np.count_nonzero(
        morph
    )


    ratio = foreground / morph.size



    n,labels,stats,centroid = cv2.connectedComponentsWithStats(
        morph,
        connectivity=8
    )


    if n > 1:
        largest = stats[1:,cv2.CC_STAT_AREA].max()
    else:
        largest = 0



    contrast = (
        np.median(gray)
        -
        np.percentile(gray,1)
    )



    if (
        contrast >= 40
        and ratio >= 0.02
        and largest >= 150
    ):

        status = "SIGNATURE PRESENT"

    else:

        status = "SIGNATURE ABSENT"



    return status, foreground, morph



# ===============================
# PREPROCESSING
# ===============================

def enhance(image):

    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )


    clahe = cv2.createCLAHE(
        clipLimit=2.0,
        tileGridSize=(8,8)
    )


    return clahe.apply(gray)



# ===============================
# PROSES UTAMA
# ===============================

def process(filename):


    path = os.path.join(
        DATA_DIR,
        filename
    )


    image=cv2.imread(path)


    if image is None:
        return None



    enhanced = enhance(image)



    # OCR

    number_roi = crop_number_roi(
        cv2.cvtColor(
            image,
            cv2.COLOR_BGR2GRAY
        )
    )


    ocr = run_ocr(
        number_roi
    )


    cer = calculate_cer(
        NOMOR_ASLI,
        ocr
    )



    # Signature

    signature_roi = crop_signature_roi(
        image
    )


    status,pixel,mask = analyze_signature(
        signature_roi
    )



    name = filename.replace(
        ".jpg",
        ""
    )


    cv2.imwrite(
        os.path.join(
            OUTPUT_DIR,
            name+"_enhanced.jpg"
        ),
        enhanced
    )


    cv2.imwrite(
        os.path.join(
            OUTPUT_DIR,
            name+"_signature_mask.jpg"
        ),
        mask
    )



    return {

        "file":filename,

        "ocr_number":ocr,

        "CER":cer,

        "signature_status":status,

        "signature_pixel":pixel

    }




def main():

    os.makedirs(
        OUTPUT_DIR,
        exist_ok=True
    )


    files = sorted(
        [
            f for f in os.listdir(DATA_DIR)
            if f.lower().endswith((".jpg",".jpeg",".png"))
        ]
    )


    print(
        "Jumlah citra:",
        len(files)
    )


    results=[]


    for f in files:

        print(
            "Memproses:",
            f
        )


        result=process(f)


        if result:
            results.append(result)



    csv_path=os.path.join(
        OUTPUT_DIR,
        "hasil_verifikasi.csv"
    )


    with open(
        csv_path,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:


        writer=csv.DictWriter(
            file,
            fieldnames=[
                "file",
                "ocr_number",
                "CER",
                "signature_status",
                "signature_pixel"
            ]
        )


        writer.writeheader()

        writer.writerows(
            results
        )



    print("\nSELESAI")
    print("Hasil ada di folder output")




if __name__=="__main__":

    main()