import easyocr
import os

def get_data_by_ocr(path):
    res = []
    for i in os.listdir(path):
        reader = easyocr.Reader(['ru'])
        result = reader.readtext(f"{path}/{i}", detail=0)
        res.extend(result)

        os.remove(f"{path}/{i}")
    print("Распознанный текст:", res)
    return " ".join(res)

