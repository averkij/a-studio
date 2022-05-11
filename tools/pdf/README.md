## Make your beautiful PDF book

Look at [this book](./result/agata.pdf).

You can make something like it by yourself!

## Requirements

- saxonb-xslt

  - To make html file from xml alignment exported from **Lingtrain Studio**
  - Install Java if needed
    - `sudo apt install default-jre`
  - Install saxon
    - `sudo apt-get install libsaxonb-java`

- [weasyprint](https://doc.courtbouillon.org/weasyprint/stable/)
  - To make PDF using **generated html**, **images**, **fonts** and **css styles**
  - Install dependencies
    - `sudo apt install libpango1.0-dev libjpeg-dev zlib1g-dev libgdk-pixbuf2.0-dev`
    - `python3 -m pip install --upgrade Pillow`
  - Install weasyprint
    - `pip3 install weasyprint==52.5`

## Usage

- Create a book with the following command:
  - `./create_pdf.sh ./example/data/agata.xml ./book2html.xslt ./example/styles/book-pt.css ./result/agata.pdf`
    - `./example/data/agata.xml`
      - XML alignment file exported from Lingtrain Studio.
    - `./book2html.xslt`
      - Template for generating html file. Use **./book2html-colors.xslt** for colored highlighting.
    - `./example/styles/book-pt.css`
      - CSS styles you can customize.
      - You need to customize fonts for texts in Chinese, Japanese, Korean, etc. For Japanese use **book-jp.css**, font is already in fonts folder.
    - `./result/agata.pdf`
      - Output pdf file
    - The cover image is **./example/img/cover.jpg**
