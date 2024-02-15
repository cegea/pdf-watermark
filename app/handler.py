from tempfile import NamedTemporaryFile
from typing import Union

import pypdf

from app.draw import draw_watermarks
from app.options import DrawingOptions, FilesOptions, GridOptions, InsertOptions
from app.utils import convert_content_to_images


def add_watermark_to_pdf(
    input: str,
    output: str,
    drawing_options: DrawingOptions,
    specific_options: Union[GridOptions, InsertOptions],
):
    pdf_to_transform = pypdf.PdfReader(input)
    pdf_box = pdf_to_transform.pages[0].mediabox
    page_width = pdf_box.width
    page_height = pdf_box.height

    with NamedTemporaryFile() as temporary_file:
        # The watermark is stored in a temporary pdf file
        draw_watermarks(
            temporary_file.name,
            page_width,
            page_height,
            drawing_options,
            specific_options,
        )

        watermark_pdf = pypdf.PdfReader(temporary_file.name)
        pdf_writer = pypdf.PdfWriter()

        for page in pdf_to_transform.pages:
            page.merge_page(watermark_pdf.pages[0])
            pdf_writer.add_page(page)

    with open(output, "wb") as f:
        pdf_writer.write(f)

    if drawing_options.save_as_image:
        convert_content_to_images(output, page_width, page_height, drawing_options.dpi)


def add_watermark_from_options(
    files_options: FilesOptions,
    drawing_options: DrawingOptions,
    specific_options: Union[GridOptions, InsertOptions],
):
    for input_file, output_file in files_options:
        add_watermark_to_pdf(input_file, output_file, drawing_options, specific_options)
