import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

from src.loaders.pdf_loader import load_pdf, load_pdfs_from_folder


# =========================
# Test load_pdf
# =========================

def test_load_pdf_success(tmp_path):
    # Tạo file PDF giả
    fake_pdf = tmp_path / "test.pdf"
    fake_pdf.write_text("dummy")

    mock_docs = [MagicMock(metadata={})]

    with patch("src.loaders.pdf_loader.PyMuPDFLoader") as MockLoader:
        instance = MockLoader.return_value
        instance.load.return_value = mock_docs

        docs = load_pdf(fake_pdf)

        assert len(docs) == 1
        assert docs[0].metadata["source"] == str(fake_pdf)
        assert docs[0].metadata["filename"] == "test.pdf"


def test_load_pdf_file_not_found():
    with pytest.raises(FileNotFoundError):
        load_pdf("not_exist.pdf")


# =========================
# Test load_pdfs_from_folder
# =========================

def test_load_pdfs_from_folder_success(tmp_path):
    # Tạo 2 file PDF giả
    pdf1 = tmp_path / "a.pdf"
    pdf2 = tmp_path / "b.pdf"
    pdf1.write_text("a")
    pdf2.write_text("b")

    mock_docs = [MagicMock(metadata={})]

    with patch("src.loaders.pdf_loader.load_pdf") as mock_load_pdf:
        mock_load_pdf.return_value = mock_docs

        docs = load_pdfs_from_folder(tmp_path)

        # 2 file → mỗi file trả 1 doc
        assert len(docs) == 2
        assert mock_load_pdf.call_count == 2


def test_load_pdfs_from_folder_not_found():
    with pytest.raises(FileNotFoundError):
        load_pdfs_from_folder("not_exist_folder")


def test_load_pdfs_from_folder_empty(tmp_path):
    docs = load_pdfs_from_folder(tmp_path)
    assert docs == []