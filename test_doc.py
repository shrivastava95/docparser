import docparser
import torch
import time

# pdf_path = r'C:\summerterm\c4gt\OFFICIAL\week9\docu-digest\Hanuman_Chalisa_In_Odia.pdf'
# pdf_path = r'en-or.pdf'
pdf_path = r'English_Odia_Hindi_Text.pdf'
print(docparser.tesseract_config)
docparser.tesseract_config = '--psm 3'

start_time = time.time()
reader = docparser.PdfParser(pdf_path,
                             page_nums=[1, 6, 12],
                             page_langs=['eng', 
                                         'eng+hin',
                                         'eng+ori',],
                             mode='cliptesseract',
                             dpi=200,
                             device='cuda' if torch.cuda.is_available() else 'cpu')
end_time = time.time()
print(f'loading time:  {end_time - start_time}')

# for page_id in range(len(reader.pages)):
for page_id in [1, 6, 12]:
    start = time.time()
    reader.pages[page_id].extract_text()        # extract the text for the page
    print(reader.pages[page_id].extracted_text)
    end = time.time()
    print(end-start)
    print('-'*50)
    print('-'*50)
    print('-'*50)