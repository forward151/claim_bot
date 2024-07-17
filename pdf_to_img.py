from pdf2image import convert_from_path

def pdf_to_img(path):
	images = convert_from_path(path, poppler_path="poppler-23.11.0/Library/bin")
	for i in range(len(images)):
		images[i].save('imgs/p' + str(i) + '.jpg', 'JPEG')

