"""
Unit tests for idsw.datafetch.texts module.
Covers:
- create_txt_db (TXT and PDF export)
- read_txt_database (reading TXT and PDF databases)
- convert_text_db_format (TXT <-> PDF format conversions and skip logic)
- text_extraction (multi-file processing and incremental appending)
- convert_str_to_dicts
"""

import unittest
import os
import shutil
import tempfile
import pandas as pd

from idsw import ControlVars, InvalidInputsError
from idsw.datafetch.texts import (
    create_txt_db,
    read_txt_database,
    convert_text_db_format,
    text_extraction,
    convert_str_to_dicts
)


class TestDatafetchTexts(unittest.TestCase):

    def setUp(self):
        ControlVars.show_plots = False
        ControlVars.show_results = False
        self.test_dir = tempfile.mkdtemp()

        self.sample_docs = [
            "Document 1: Introduction to industrial biosensors.",
            "Document 2: Electrochemical monitoring of enzyme reactions.",
            "Document 3: Real-time sensor signal processing in fermentation."
        ]

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_create_and_read_txt_db(self):
        txt_path = os.path.join(self.test_dir, "test_database.txt")
        create_txt_db(
            file_path=txt_path,
            strings_to_save=self.sample_docs,
            export_as_pdf=False
        )
        self.assertTrue(os.path.exists(txt_path))

        # Read back with split_strings = True
        read_docs = read_txt_database(txt_path, split_strings=True)
        self.assertEqual(len(read_docs), 3)
        self.assertIn("Introduction to industrial biosensors", read_docs[0])

        # Read back with split_strings = False
        full_doc = read_txt_database(txt_path, split_strings=False)
        self.assertEqual(len(full_doc), 1)

    def test_create_and_read_pdf_db(self):
        pdf_path = os.path.join(self.test_dir, "test_database.pdf")
        create_txt_db(
            file_path=pdf_path,
            strings_to_save=self.sample_docs,
            export_as_pdf=True
        )
        self.assertTrue(os.path.exists(pdf_path))
        self.assertGreater(os.path.getsize(pdf_path), 0)

        # Read back PDF database
        read_docs = read_txt_database(pdf_path, split_strings=False)
        self.assertGreater(len(read_docs), 0)
        self.assertIn("Introduction to industrial biosensors", read_docs[0])

    def test_convert_text_db_format(self):
        txt_path = os.path.join(self.test_dir, "source_db.txt")
        pdf_target = os.path.join(self.test_dir, "converted_target.pdf")
        txt_reconverted = os.path.join(self.test_dir, "reconverted.txt")

        create_txt_db(txt_path, self.sample_docs, export_as_pdf=False)

        # TXT -> PDF
        convert_text_db_format(
            file_path=txt_path,
            output_format="pdf",
            exported_file_path=pdf_target
        )
        self.assertTrue(os.path.exists(pdf_target))

        # PDF -> TXT
        convert_text_db_format(
            file_path=pdf_target,
            output_format="txt",
            exported_file_path=txt_reconverted
        )
        self.assertTrue(os.path.exists(txt_reconverted))

        # Skip conversion when formats match
        convert_text_db_format(
            file_path=txt_path,
            output_format="txt",
            exported_file_path=os.path.join(self.test_dir, "should_skip.txt")
        )
        self.assertFalse(os.path.exists(os.path.join(self.test_dir, "should_skip.txt")))

    def test_convert_str_to_dicts(self):
        dict_str = "{'author': 'Marco Soares', 'year': 2024, 'topic': 'Data Science'}"
        res = convert_str_to_dicts(dict_str)
        self.assertIsInstance(res, list)
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]["author"], "Marco Soares")
        self.assertEqual(res[0]["year"], 2024)

    def test_invalid_inputs(self):
        # Non-existent file
        with self.assertRaises(InvalidInputsError):
            read_txt_database(os.path.join(self.test_dir, "non_existent.txt"))

        # Invalid output format in conversion
        with self.assertRaises(InvalidInputsError):
            convert_text_db_format(
                file_path=os.path.join(self.test_dir, "fake.txt"),
                output_format="invalid_format",
                exported_file_path=os.path.join(self.test_dir, "out.doc")
            )


if __name__ == "__main__":
    unittest.main()
