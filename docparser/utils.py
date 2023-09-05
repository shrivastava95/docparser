import pandas
import os
import json
import PyPDF2
from pdf2image import convert_from_path

from .data import lang_mapping


def count_pdf_pages(pdf_path):
    try:
        pdf_file = open(pdf_path, 'rb')
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        num_pages = len(pdf_reader.pages)
        pdf_file.close()
        return num_pages

    except FileNotFoundError:
        raise FileNotFoundError(f"No PDF file found at {pdf_path}")

    except Exception as e:
        raise Exception(f"An error occurred while counting pages: {str(e)}")


def verify_lang(lang): # checks if lang is a proper string that can be passed to tesseract. for example: 'ori+eng', 'ori', etc...
    for lang_i in lang.split('+'):
        if lang_i not in lang_mapping:
            return False
    return True


def verify_langs(page_settings, num_pages):
    # print(page_settings)
    for page_no in page_settings:
        if page_no < 1 or page_no > num_pages or type(page_no) != int:
            return False
    
    for lang in page_settings.values():
        if not verify_lang(lang):
            return False
        
    return True


def group_pages(page_settings):
    page_nums = sorted(list(page_settings.keys()))[::-1]
    groups = [[page_nums.pop()]]
    while len(page_nums):
        if groups[-1][-1] + 1 != page_nums[-1]:
            groups.append([page_nums.pop()])
        else:
            groups[-1].append(page_nums.pop())
    groups = [[min(group), max(group)] for group in groups]
    return groups


def get_page_images(pdf_path, dpi, first_page, last_page):
    pages = convert_from_path(
        pdf_path,
        dpi,
        poppler_path=r'C:\ai_sem_7\poppler-0.68.0_x86\poppler-0.68.0\bin',
        first_page=first_page, last_page=last_page,
    )
    return pages