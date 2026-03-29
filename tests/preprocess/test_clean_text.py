from langchain_core.documents import Document

from src.preprocess.clean_text import clean_text, clean_documents


def test_clean_text_returns_empty_string_for_none():
    assert clean_text(None) == ""


def test_clean_text_returns_empty_string_for_empty_input():
    assert clean_text("") == ""


def test_normalize_newlines():
    raw = "line1\rline2\r\nline3\nline4"
    expected = "line1\nline2\nline3\nline4"
    assert clean_text(raw) == expected


def test_remove_special_invisible_characters():
    raw = "\ufeffhello\u200b\xa0world"
    expected = "hello world"
    assert clean_text(raw) == expected


def test_normalize_bullet_characters_to_standard_bullet():
    raw = " item 1\n◦ item 2\n▪ item 3\n■ item 4\n‣ item 5\n• item 6"
    expected = "• item 1\n• item 2\n• item 3\n• item 4\n• item 5\n• item 6"
    assert clean_text(raw) == expected


def test_strip_and_collapse_spaces_per_line():
    raw = "   hello    world   \n\tfoo\t\tbar\t"
    expected = "hello world\nfoo bar"
    assert clean_text(raw) == expected


def test_collapse_multiple_blank_lines_into_single_blank_line():
    raw = "line1\n\n\n\nline2\n\n\nline3"
    expected = "line1\n\nline2\n\nline3"
    assert clean_text(raw) == expected


def test_keep_basic_line_structure():
    raw = "Title\nSubtitle\n\nParagraph line"
    expected = "Title\nSubtitle\n\nParagraph line"
    assert clean_text(raw) == expected


def test_trim_leading_and_trailing_blank_lines():
    raw = "\n\n  line1  \n\nline2\n\n\n"
    expected = "line1\n\nline2"
    assert clean_text(raw) == expected


def test_clean_documents_cleans_page_content():
    docs = [
        Document(page_content="hello\r\n\r\nworld", metadata={"page": 1}),
        Document(page_content="\ufefffoo\u200b\xa0bar", metadata={"page": 2}),
    ]

    cleaned = clean_documents(docs)

    assert cleaned[0].page_content == "hello\n\nworld"
    assert cleaned[1].page_content == "foo bar"


def test_clean_documents_copies_metadata():
    original_metadata = {"page": 1, "source": "file.pdf"}
    docs = [Document(page_content="text", metadata=original_metadata)]

    cleaned = clean_documents(docs)

    assert cleaned[0].metadata == original_metadata
    assert cleaned[0].metadata is not original_metadata


def test_clean_documents_returns_new_document_objects():
    docs = [Document(page_content="text", metadata={"page": 1})]

    cleaned = clean_documents(docs)

    assert cleaned[0] is not docs[0]