## Make your beautiful PDF book

Look at [this book](./lingtrain.pdf).

You can make something like it by yourself!

## Requirements

- Html and css files like in the _./example_ folder.
  - TBD. Script for creating html and css will be provided soon.
- [weasyprint](https://doc.courtbouillon.org/weasyprint/stable/)
  - Insatall dependencies
    - `sudo apt install libpango1.0-dev libjpeg-dev zlib1g-dev libgdk-pixbuf2.0-dev`
    - `python3 -m pip install --upgrade Pillow`
  - Install weasyprint
    - `pip3 install weasyprint==52.5`

## Usage

- Create a book with the following command
  - `weasyprint -s example/book.css example/akutagawa.html lingtrain.pdf`
