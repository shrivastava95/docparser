# Requirements

- First make sure [PyTorch - 1.7.1 (or later)](https://pytorch.org/get-started/locally/) and torchvision are installed.
- `pip install git+https://github.com/openai/CLIP.git` - OpenAI's CLIP model for matching text with images
- `pip install numpy pandas ftfy regex tqdm PyPDF2 python-dotenv openai`
- Setup `pdf2image`. Instructions given here:

    **Linux and MacOS**
    1. setup poppler using  the isntructions given in https://pdf2image.readthedocs.io/en/latest/installation.html
    2. `pip install pdf2image`

    **Windows**
    1. Download the latest poppler package from https://github.com/oschwartz10612/poppler-windows/releases/ which is the most up-to-date.
    2. Move the extracted directory to the desired place on your system
    3. Add the `bin/` directory to your PATH
    4. Test that all went well by opening cmd and making sure that you can call `pdftoppm -h`
    5. If still not working, point the `poppler_path` argument to the `\bin` folder like already done inside the file.
    6. `pip install pdf2image`
- Setup `pytesseract`. Instructions given here:

    **Linux and MacOS**
    1. Setup the latest version of pytesseract (5+) using https://studysection.com/blog/quick-guide-to-install-and-remove-tesseract-ocr-5-on-ubuntu-18-04/
    2. Make sure the correct tesseract language packages are installed for your use. Helpful guide - https://ocrmypdf.readthedocs.io/en/latest/languages.html
    **Windows**
    1. 