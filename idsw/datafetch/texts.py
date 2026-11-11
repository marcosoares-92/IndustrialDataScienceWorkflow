"""
FUNCTIONS FROM INDUSTRIAL DATA SCIENCE WORKFLOW (IDSW) PACKAGE
Pipelines for reading and preprocessing text files like PDFs, CSVs, HTML, TXT and DOCX.
"""

import os
import re
import numpy as np
import pandas as pd

from idsw import InvalidInputsError, ControlVars


def _generate_pure_pdf(file_path, text):
    """
    Pure Python minimal valid PDF-1.4 generator with zero external dependencies.
    Wraps text lines and writes out a standard PDF file.
    """
    # Replace non-ascii characters for standard Type 1 Helvetica font
    safe_text = text.encode('ascii', errors='replace').decode('ascii')
    raw_lines = safe_text.split('\n')

    # Wrap long lines to ~85 characters per line
    wrapped_lines = []
    for line in raw_lines:
        line = line.strip('\r')
        if len(line) <= 85:
            wrapped_lines.append(line)
        else:
            for i in range(0, len(line), 85):
                wrapped_lines.append(line[i:i + 85])

    # 45 lines per page
    lines_per_page = 45
    pages = [wrapped_lines[i:i + lines_per_page] for i in range(0, max(1, len(wrapped_lines)), lines_per_page)]
    if len(pages) == 0:
        pages = [[""]]

    # Construct PDF objects
    objects = []
    # 1: Font
    font_obj = "1 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>\nendobj"
    objects.append(font_obj)

    page_obj_ids = []
    current_obj_id = 2

    # Reserve IDs for Pages catalog and individual pages
    pages_catalog_id = current_obj_id
    current_obj_id += 1

    page_content_pairs = []
    for _ in pages:
        p_id = current_obj_id
        c_id = current_obj_id + 1
        page_obj_ids.append(p_id)
        page_content_pairs.append((p_id, c_id))
        current_obj_id += 2

    catalog_id = current_obj_id
    current_obj_id += 1

    # Pages catalog object
    kids_str = " ".join([f"{pid} 0 R" for pid in page_obj_ids])
    pages_obj = f"{pages_catalog_id} 0 obj\n<< /Type /Pages /Kids [{kids_str}] /Count {len(pages)} >>\nendobj"
    objects.append(pages_obj)

    # Individual page and content objects
    for idx, (p_id, c_id) in enumerate(page_content_pairs):
        page_lines = pages[idx]
        stream_content = "BT\n/F1 10 Tf\n40 760 Td\n14 TL\n"
        for line in page_lines:
            # Escape parentheses and backslashes in PDF text strings
            escaped = line.replace('\\', '\\\\').replace('(', '\\(').replace(')', '\\)')
            stream_content += f"({escaped}) '\n"
        stream_content += "ET\n"
        stream_bytes = stream_content.encode('ascii')

        page_dict = f"{p_id} 0 obj\n<< /Type /Page /Parent {pages_catalog_id} 0 R /MediaBox [0 0 612 792] /Contents {c_id} 0 R /Resources << /Font << /F1 1 0 R >> >> >>\nendobj"
        content_dict = f"{c_id} 0 obj\n<< /Length {len(stream_bytes)} >>\nstream\n{stream_content}endstream\nendobj"
        objects.append(page_dict)
        objects.append(content_dict)

    # Root Catalog object
    root_obj = f"{catalog_id} 0 obj\n<< /Type /Catalog /Pages {pages_catalog_id} 0 R >>\nendobj"
    objects.append(root_obj)

    # Assemble PDF with cross-reference table (xref)
    output_bytes = bytearray(b"%PDF-1.4\n")
    xref_offsets = [0]

    for obj_str in objects:
        xref_offsets.append(len(output_bytes))
        output_bytes.extend(obj_str.encode('ascii') + b"\n")

    xref_start = len(output_bytes)
    output_bytes.extend(b"xref\n")
    output_bytes.extend(f"0 {len(xref_offsets)}\n".encode('ascii'))
    output_bytes.extend(b"0000000000 65535 f \n")
    for offset in xref_offsets[1:]:
        output_bytes.extend(f"{offset:010d} 00000 n \n".encode('ascii'))

    output_bytes.extend(b"trailer\n")
    output_bytes.extend(f"<< /Size {len(xref_offsets)} /Root {catalog_id} 0 R >>\n".encode('ascii'))
    output_bytes.extend(b"startxref\n")
    output_bytes.extend(f"{xref_start}\n%%EOF\n".encode('ascii'))

    with open(file_path, 'wb') as f:
        f.write(output_bytes)


def _write_pdf_file(file_path, text):
    """Writes text as a PDF document using reportlab or fallback pure python generator."""
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas

        c = canvas.Canvas(file_path, pagesize = letter)
        width, height = letter
        y = height - 40
        c.setFont("Helvetica", 10)

        for line in text.split('\n'):
            line_str = str(line).strip('\r')
            if y < 40:
                c.showPage()
                c.setFont("Helvetica", 10)
                y = height - 40
            c.drawString(40, y, line_str[:90])
            y -= 14
        c.save()
    except Exception:
        _generate_pure_pdf(file_path, text)


def _read_pdf_file(file_path):
    """Reads text from a PDF file using pypdf, PyPDF2, or stream text extraction."""
    # Try pypdf
    try:
        import pypdf
        reader = pypdf.PdfReader(file_path)
        pages_text = []
        for p in reader.pages:
            t = p.extract_text()
            if t:
                pages_text.append(t)
        return "\n".join(pages_text)
    except Exception:
        pass

    # Try PyPDF2
    try:
        import PyPDF2
        reader = PyPDF2.PdfReader(file_path)
        pages_text = []
        for p in reader.pages:
            t = p.extract_text()
            if t:
                pages_text.append(t)
        return "\n".join(pages_text)
    except Exception:
        pass

    # Raw fallback
    with open(file_path, 'rb') as f:
        content = f.read()
    text = content.decode('ascii', errors = 'ignore')
    extracted = re.findall(r'\((.*?)\)\s*[\'Tj]', text)
    if len(extracted) > 0:
        return "\n".join(extracted)
    return text


def read_txt_database(file_path, split_strings = True, doc_separator = '\n\n-----\n\n'):
    """
    read_txt_database:
    Reads a text database saved as a TXT or PDF file.
    The different files in the database are returned as elements of a list separated by doc_separator.

    : param: file_path: str, path of the file to be read (.txt or .pdf).
    : param: split_strings: bool (default True). If True, splits into document elements; if False, returns 1-element list.
    : param: doc_separator: str (default '\\n\\n-----\\n\\n'), separator used between documents.
    : return: list of strings containing the read texts.
    """
    if not os.path.exists(file_path):
        raise InvalidInputsError(f"Database file '{file_path}' does not exist.")

    if file_path.lower().endswith('.pdf'):
        db = _read_pdf_file(file_path)
    else:
        try:
            with open(file_path, 'r', encoding = 'utf-8') as f:
                db = f.read()
        except UnicodeDecodeError:
            with open(file_path, 'r', encoding = 'latin-1') as f:
                db = f.read()

    if split_strings:
        texts = db.split(doc_separator)
    else:
        texts = [db]

    return texts


def create_txt_db(file_path, strings_to_save, doc_separator = '\n\n-----\n\n', export_as_pdf = False):
    """
    create_txt_db:
    Creates a text database from the provided strings.
    If a list of strings is provided, combines all of them using doc_separator.
    Supports exporting as TXT or PDF format based on export_as_pdf flag.

    : param: file_path: str, destination path of the file.
    : param: strings_to_save: str or list of strings to combine and save.
    : param: doc_separator: str (default '\\n\\n-----\\n\\n'), document delimiter.
    : param: export_as_pdf: bool (default False). When True, saves as PDF; if False, saves as TXT.
    : return: None (file is exported).
    """
    if isinstance(strings_to_save, list):
        content = doc_separator.join([str(s) for s in strings_to_save])
    else:
        content = str(strings_to_save)

    if export_as_pdf:
        # Guarantee .pdf extension if user didn't provide it
        out_path = file_path if file_path.lower().endswith('.pdf') else file_path + '.pdf'
        _write_pdf_file(out_path, content)
        if ControlVars.show_results:
            print(f"Database successfully exported as PDF: '{out_path}'.")
    else:
        out_path = file_path if file_path.lower().endswith('.txt') else file_path + '.txt'
        with open(out_path, 'w', encoding = 'utf-8') as f:
            f.write(content)
        if ControlVars.show_results:
            print(f"Database successfully exported as TXT: '{out_path}'.")


def convert_text_db_format(file_path, output_format, exported_file_path, doc_separator = '\n\n-----\n\n'):
    """
    convert_text_db_format:
    Converts a text database file between 'txt' and 'pdf' formats.
    Reads the file using read_txt_database, converts to output_format, and saves to exported_file_path.
    If input format already matches output_format or source equals destination, skips conversion.

    : param: file_path: str, source database file path.
    : param: output_format: str, desired output format ('txt' or 'pdf').
    : param: exported_file_path: str, destination file path.
    : param: doc_separator: str, separator between documents.
    : return: None.
    """
    fmt_clean = str(output_format).strip().lower().replace('.', '')
    if fmt_clean not in ['txt', 'pdf']:
        raise InvalidInputsError(f"output_format must be either 'txt' or 'pdf', got '{output_format}'.")

    if not os.path.exists(file_path):
        raise InvalidInputsError(f"Source file '{file_path}' does not exist.")

    in_ext = 'pdf' if file_path.lower().endswith('.pdf') else 'txt'

    # Check if conversion is unnecessary
    is_same_format = (in_ext == fmt_clean)
    is_same_file = (os.path.abspath(file_path) == os.path.abspath(exported_file_path))

    if is_same_format or is_same_file:
        if ControlVars.show_results:
            print(f"Source file '{file_path}' is already in '{fmt_clean}' format. Skipping conversion.")
        return

    # Read content from source file
    docs = read_txt_database(file_path = file_path, split_strings = False, doc_separator = doc_separator)
    content = docs[0] if len(docs) > 0 else ""

    # Export to target format
    export_as_pdf = (fmt_clean == 'pdf')
    create_txt_db(
        file_path = exported_file_path,
        strings_to_save = content,
        doc_separator = doc_separator,
        export_as_pdf = export_as_pdf
    )

    if ControlVars.show_results:
        print(f"Converted database from '{in_ext}' to '{fmt_clean}' saved at '{exported_file_path}'.")


def text_extraction(
    file_paths,
    doc_separator = '\n\n-----\n\n',
    output_text_path = None,
    output_meta_path = None,
    previous_text_database_path = None,
    previous_metadata_database_path = None,
    previous_filenames_database_path = None,
    export_as_pdf = False
):
    """
    text_extraction:
    Extracts text and metadata across supported file formats (PDF, CSV, TXT, HTML, DOCX).
    Supports incremental database updates and exporting as either TXT or PDF.

    : param: file_paths: str or list of str containing full paths of files to process.
    : param: doc_separator: delimiter between documents.
    : param: output_text_path: target path for extracted text database.
    : param: output_meta_path: target path for extracted metadata.
    : param: export_as_pdf: bool (default False), export as PDF if True.
    : return: tuple (texts, metadata, file_names).
    """
    if isinstance(file_paths, str):
        file_paths = [file_paths]

    if output_text_path is None:
        output_text_path = 'extracted_text.pdf' if export_as_pdf else 'extracted_text.txt'
    if output_meta_path is None:
        output_meta_path = 'metadata.txt'

    if ControlVars.show_results:
        print(f"Processing {len(file_paths)} files for text extraction.\n")

    metadata = []
    texts = []
    file_names = []

    for file_path in file_paths:
        if not os.path.exists(file_path):
            continue

        base_name = os.path.basename(file_path)
        ext = os.path.splitext(file_path)[1].lower().strip('.')
        file_names.append(base_name)

        doc_text = ""
        doc_meta = {"source": file_path, "filename": base_name}

        try:
            if ext == "pdf":
                doc_text = _read_pdf_file(file_path)
            elif ext in ["csv", "txt"]:
                with open(file_path, 'r', encoding = 'utf-8', errors = 'ignore') as f:
                    doc_text = f.read()
            elif ext == "html":
                with open(file_path, 'r', encoding = 'utf-8', errors = 'ignore') as f:
                    raw_html = f.read()
                doc_text = re.sub(r'<[^>]+>', ' ', raw_html)
            elif ext in ["docx", "doc"]:
                try:
                    from langchain_community.document_loaders import Docx2txtLoader
                    loader = Docx2txtLoader(file_path)
                    data = loader.load()
                    doc_text = "\n".join([page.page_content for page in data])
                except Exception:
                    doc_text = f"[DOCX document: {base_name}]"
            else:
                doc_text = f"[Unsupported format: {ext}]"

            texts.append(doc_text)
            metadata.append(doc_meta)
        except Exception as e:
            texts.append(f"[Error reading file: {e}]")
            metadata.append(doc_meta)

    # Incorporate previous databases if provided
    if previous_text_database_path is not None and os.path.exists(previous_text_database_path):
        prev_texts = read_txt_database(previous_text_database_path, split_strings = True, doc_separator = doc_separator)
        texts = prev_texts + texts

    if previous_metadata_database_path is not None and os.path.exists(previous_metadata_database_path):
        prev_meta = read_txt_database(previous_metadata_database_path, split_strings = True, doc_separator = doc_separator)
        metadata = prev_meta + metadata

    if previous_filenames_database_path is not None and os.path.exists(previous_filenames_database_path):
        prev_names = read_txt_database(previous_filenames_database_path, split_strings = True, doc_separator = doc_separator)
        file_names = prev_names + file_names

    # Export results
    create_txt_db(
        file_path = output_text_path,
        strings_to_save = texts,
        doc_separator = doc_separator,
        export_as_pdf = export_as_pdf
    )

    create_txt_db(
        file_path = output_meta_path,
        strings_to_save = [str(m) for m in metadata],
        doc_separator = doc_separator,
        export_as_pdf = False
    )

    create_txt_db(
        file_path = 'file_names.txt',
        strings_to_save = file_names,
        doc_separator = doc_separator,
        export_as_pdf = False
    )

    if ControlVars.show_results:
        print(f"Text extraction complete. {len(texts)} documents stored in database.")

    return texts, metadata, file_names


def convert_str_to_dicts(text_to_convert):
    """
    convert_str_to_dicts:
    Parses string representations of Python dictionary literals into actual dictionaries.
    """
    import ast

    def _convert_single(s):
        try:
            res = ast.literal_eval(s)
            return res if isinstance(res, dict) else {"raw_value": res}
        except Exception:
            return {"raw_string": s}

    if isinstance(text_to_convert, str):
        return [_convert_single(text_to_convert)]
    return [_convert_single(t) for t in text_to_convert]
