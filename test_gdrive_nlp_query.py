import os
import sys
from unittest.mock import MagicMock, patch

import pytest

from gdrive_nlp_query import (download_document, get_query, get_service,
                              process_document)


@pytest.fixture
def sample_document_path(tmpdir):
    content = "This is a sample document.\nIt contains a query string."
    file_path = os.path.join(tmpdir, "sample_document.txt")
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(content)
    return file_path


@pytest.fixture
def mock_drive_service(mocker):
    return mocker.patch("gdrive_nlp_query.build", return_value=MagicMock())


def test_get_service(mock_drive_service):
    credentials = MagicMock()
    service = get_service(credentials)
    assert service is not None
    mock_drive_service.assert_called_once_with("drive", "v3", credentials=credentials)


def test_get_query():
    with patch.object(sys, "argv", ["gdrive_nlp_query.py", "word1", "word2"]):
        query = get_query()
        assert query == ["word1", "word2"]


def test_download_document(sample_document_path, mock_drive_service, mocker):
    mock_drive_service.files().export_media().execute = MagicMock(
        return_value="Mock document content".encode("utf-8")
    )
    download_document("file_id", sample_document_path, mock_drive_service)
    assert os.path.exists(sample_document_path)
    with open(sample_document_path, "r", encoding="utf-8") as file:
        assert file.read() == "Mock document content"


def test_process_document(sample_document_path, capsys):
    query = ["query", "string"]
    process_document(sample_document_path, query)
    captured = capsys.readouterr()
    assert "Matches in document" in captured.out
    assert "It contains a query string." in captured.out


def test_process_document_no_match(sample_document_path, capsys):
    query = ["nonexistent", "query"]
    process_document(sample_document_path, query)
    captured = capsys.readouterr()
    assert "No matches found in document" in captured.out
