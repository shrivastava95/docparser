import torch
import clip
import os
import PyPDF2

from .utils import *
from .pipeline_clip import image_to_string_v2
from .pipeline_dict import image_to_dict

poppler_path = 'C:\ai_sem_7\poppler-0.68.0_x86\poppler-0.68.0\bin' # note: change this to None in production??? idk??? forgot??? and include instructions in readme for this variable


clip_model_name = 'ViT-B/16'
tesseract_config = '--psm 3'
parser_mode = 'cliptesseract' # or 'tesseract'


class Page:
    def __init__(self, model, preprocess, device, page_image, lang, config, mode, openai_api_key=None, gpt_model=None):
        self.model = model
        self.preprocess = preprocess
        self.device = device
        self.page_image = page_image
        self.lang = lang
        self.config = config
        self.mode = mode
        self.openai_api_key = openai_api_key
        self.gpt_model = gpt_model

    def extract_text(self):
        self.extracted_text = image_to_string_v2(
            model=self.model, 
            preprocess=self.preprocess, 
            device=self.device, 
            image=self.page_image, 
            lang=self.lang, 
            config=self.config, 
            mode=self.mode,
        )
        return self.extracted_text
    
    def extract_table(self):
        self.extracted_table = image_to_dict(
            model=self.model, 
            preprocess=self.preprocess, 
            device=self.device, 
            image=self.page_image, 
            lang=self.lang, 
            config=self.config, 
            mode=self.mode,
            openai_api_key=self.openai_api_key,
            gpt_model=self.gpt_model,
        )
        return self.extracted_table


class PdfParser:
    def __init__(self, pdf_path, page_nums, page_langs, mode, dpi, device):
        assert mode in ['cliptesseract', 'tesseract']

        # if only one language provided as a string:
        if type(page_langs) == str: 
            page_langs = [page_langs[::] for _ in range(len(page_nums))]
        page_settings = {page_num: page_lang for page_num, page_lang in zip(page_nums, page_langs)}

        # 0. count pdf pages.
        num_pages = count_pdf_pages(pdf_path)

        # 1. very all pages and languages specified
        assert verify_langs(page_settings, num_pages)
        
        # 2. parse all pages that are verified and stage for processing in page objects
        page_nums = sorted(list(page_settings.keys()))
        page_langs = [page_settings[page_num] for page_num in page_nums]
        page_groups = group_pages(page_settings)
        page_images = [
            page_image
            for page_image_group in [get_page_images(pdf_path, dpi, first_page, last_page) for (first_page, last_page) in page_groups]
            for page_image in page_image_group
        ]
        
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        model, preprocess = clip.load(clip_model_name, device=device)
        self.pages = {
            page_num: Page(model, preprocess, device, page_image, page_lang, tesseract_config, parser_mode) 
            for page_num, page_image, page_lang 
            in zip(page_nums, page_images, page_langs)
        }


class DictParser:
    def __init__(self, pdf_path, page_nums, page_langs, mode, dpi, device, openai_api_key, gpt_model):
        assert mode in ['cliptesseract', 'tesseract']

        # if only one language provided as a string:
        if type(page_langs) == str: 
            page_langs = [page_langs[::] for _ in range(len(page_nums))]
        page_settings = {page_num: page_lang for page_num, page_lang in zip(page_nums, page_langs)}

        # 0. count pdf pages.
        num_pages = count_pdf_pages(pdf_path)

        # 1. very all pages and languages specified
        assert verify_langs(page_settings, num_pages)
        
        # 2. parse all pages that are verified and stage for processing in page objects
        page_nums = sorted(list(page_settings.keys()))
        page_langs = [page_settings[page_num] for page_num in page_nums]
        page_groups = group_pages(page_settings)
        page_images = [
            page_image
            for page_image_group in [get_page_images(pdf_path, dpi, first_page, last_page) for (first_page, last_page) in page_groups]
            for page_image in page_image_group
        ]
        
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        model, preprocess = clip.load(clip_model_name, device=device)
        self.pages = {
            page_num: Page(model, preprocess, device, page_image, page_lang, tesseract_config, parser_mode, openai_api_key, gpt_model) 
            for page_num, page_image, page_lang 
            in zip(page_nums, page_images, page_langs)
        }

        


        

