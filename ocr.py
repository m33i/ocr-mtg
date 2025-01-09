import cv2
import pytesseract
import api
import re
import requests
import numpy as np
from io import BytesIO

#pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
cap = cv2.VideoCapture(0) 

def processed_frame(frame):
    # Adjust contrast and sharpness while keeping the image in color
    contrast = cv2.convertScaleAbs(frame, alpha=1.3, beta=20)  # Slight contrast and brightness adjustment
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])  # Sharpening kernel
    sharpened = cv2.filter2D(contrast, -1, kernel)
    return sharpened

def process_from_url(url):
    response = requests.get(url)
    if response.status_code != 200:
        print("can't fetch from url")
        return

    image = np.array(bytearray(response.content), dtype=np.uint8)
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    if image is None:
        print("can't decode from url")
        return

    p_frame = processed_frame(image)
    cv2.imshow('Processed Image', p_frame)
    text = pytesseract.image_to_string(p_frame, lang='eng')
    print("text detected:" + text)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

def detect_card():
    #camera setup
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')) # doesnt work without this for me
    cap.set(cv2.CAP_PROP_FPS, 60)

    if not cap.isOpened():
        print("cam not found")
        return

    frame_count = 0
    process_every_n_frames = 30

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        p_frame = processed_frame(frame)
        cv2.imshow('Original Camera', frame)
        cv2.imshow('Processed Frame', p_frame)

        if frame_count % process_every_n_frames == 0:
            text = pytesseract.image_to_string(p_frame, lang='eng')
            print("text detected:" + text)
            api.autocomplete(text)  #api call

        frame_count += 1

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def main():
    detect_card()
    #process_from_url("https://cards.scryfall.io/large/front/3/c/3cee9303-9d65-45a2-93d4-ef4aba59141b.jpg?1730489152")

if __name__ == "__main__":
    main()