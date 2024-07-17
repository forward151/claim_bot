from PyPDF2 import PdfReader
from ocr_recognition import get_data_by_ocr
from pdf_to_img import pdf_to_img
#
# pdf_document = "test.pdf"
# with open(pdf_document, "rb") as filehandle:
# 	pdf = PdfReader(filehandle)
#
# 	info = pdf.metadata
# 	print(info)
# 	pages = len(pdf.pages)
# 	print("Количество страниц в документе: %i\n\n" % pages)
# 	print("Мета-описание: ", info)
#
# 	for i in range(pages):
# 		page = pdf.pages[i]
# 		print("Стр.", i, " мета: ", page, "\n\nСодержание:\n")
# 		print(page.extract_text())
#
#

def get_text(file_name):
	data = []
	with open(file_name, "rb") as file:
		pdf = PdfReader(file)

		pages = len(pdf.pages)

		for i in range(pages):
			page = pdf.pages[i]
			text = page.extract_text().strip().replace("\n", " ")

			data.append(text)
	print("Считанный файл:", data)
	while "" in data:
		data.remove("")
	if data == []:
		pdf_to_img(file_name)
		return get_data_by_ocr("imgs")

	return " ".join(data)