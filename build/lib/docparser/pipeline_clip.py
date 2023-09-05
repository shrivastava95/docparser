import clip
import torch
from pytesseract import pytesseract, Output
from PIL import Image
import os
from .data import lang_mapping

# lang = 'eng+ori'
# custom_config = '--psm 3'
# classification_strings = ['image of odiya language text', 'image of english language text']
# languages_clip = ['english', 'odiya']
# languages_ocr = ['eng', 'ori']
# image_path = 'GUI_sample_orig.png'


def string_template(language):
    return f'image of {language} language text'


def clip_classify_images(model, preprocess, device, images, strings):
    logits_per_image, logits_per_text = model(
        torch.stack([preprocess(image) for image in images], dim=0).to(device),
        clip.tokenize(strings).to(device)
    ) # [N-img, N-txt], [N-txt, N-img]
    return logits_per_image.cpu().detach().numpy()


def reprocess(model, preprocess, device, mode, idx, ocr_data, image, languages_clip, languages_ocr, offset=4):
    x, y, w, h = ocr_data['left'][idx], ocr_data['top'][idx], ocr_data['width'][idx], ocr_data['height'][idx]
    x0, y0, x1, y1 = (x - offset, y - offset, x + w + offset, y + h + offset)
    region = image.crop((x0, y0, x1, y1))

    classification_strings = [string_template(langname) for langname in languages_clip]
    logits_per_region = clip_classify_images(
        model, preprocess, device, 
        [region],
        classification_strings
    )
    class_idx = logits_per_region.argmax(axis=1)[0]
    predicted_lang_ocr = languages_ocr[class_idx]
    word = pytesseract.image_to_string(region, 
                                    lang=predicted_lang_ocr, 
                                    config='--psm 8') # word level parsing
    return word


# dict_keys(['level', 'page_num', 'block_num', 'par_num', 'line_num', 'word_num', 'left', 'top', 'width', 'height', 'conf', 'text'])
def image_to_string_v2(model, preprocess, device, image, lang, config, mode):
    assert mode in ['tesseract', 'cliptesseract']

    if mode == 'tesseract':
        string = pytesseract.image_to_string(image, lang=lang, config=config)
        return string
    
    elif mode == 'cliptesseract':
        if type(image) == str:
            image = Image.open(image)
        data = pytesseract.image_to_data(image, lang=lang, config=config, output_type=Output.DICT)

        languages_ocr = lang.split('+')
        languages_clip = [lang_mapping[lang_i] for lang_i in languages_ocr]
        total_text = []
        for i in range(len(data['level'])):
            if data['level'][i] == 5:
                data['text'][i] = reprocess(model, preprocess, device, mode, i, data, image, languages_clip, languages_ocr)
                total_text.append(data['text'][i] + ' ')
            elif data['level'][i] == 4:
                total_text.append('\n')
            elif data['level'][i] == 3:
                total_text.append('\n')
        total_text = ''.join(total_text)
        return total_text