from __future__ import annotations

import json
import shutil
import sys
import tempfile
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse
import cgi

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from thesis_formatter import analyze_template, apply_template_format


class ThesisRequestHandler(BaseHTTPRequestHandler):
    server_version = "ThesisFormatterAPI/0.1"

    def _send_json(self, status: int, payload: dict) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_error(self, status: int, message: str) -> None:
        self._send_json(status, {"error": message})

    def _read_multipart(self) -> cgi.FieldStorage:
        return cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={
                "REQUEST_METHOD": "POST",
                "CONTENT_TYPE": self.headers.get("Content-Type", ""),
                "CONTENT_LENGTH": self.headers.get("Content-Length", "0"),
            },
        )

    def _save_upload(self, form: cgi.FieldStorage, field_name: str, directory: Path) -> Path:
        field = form[field_name] if field_name in form else None
        if field is None or not getattr(field, "filename", ""):
            raise ValueError(f"Missing upload field: {field_name}")

        filename = Path(field.filename).name
        if not filename.lower().endswith(".docx"):
            raise ValueError(f"{field_name} must be a .docx file")

        destination = directory / filename
        with destination.open("wb") as output:
            shutil.copyfileobj(field.file, output)
        return destination

    def do_GET(self) -> None:
        path = urlparse(self.path).path
        if path == "/api/health":
            self._send_json(HTTPStatus.OK, {"ok": True})
            return
        self._send_error(HTTPStatus.NOT_FOUND, "Not found")

    def do_POST(self) -> None:
        path = urlparse(self.path).path
        try:
            if path == "/api/analyze":
                self._handle_analyze()
                return
            if path == "/api/apply":
                self._handle_apply()
                return
            self._send_error(HTTPStatus.NOT_FOUND, "Not found")
        except ValueError as exc:
            self._send_error(HTTPStatus.BAD_REQUEST, str(exc))
        except Exception as exc:
            self._send_error(HTTPStatus.INTERNAL_SERVER_ERROR, f"Failed: {exc}")

    def _handle_analyze(self) -> None:
        form = self._read_multipart()
        with tempfile.TemporaryDirectory(prefix="thesis-analyze-") as tmp:
            template_path = self._save_upload(form, "template", Path(tmp))
            profile = analyze_template(template_path)
            self._send_json(HTTPStatus.OK, profile.to_dict())

    def _handle_apply(self) -> None:
        form = self._read_multipart()
        with tempfile.TemporaryDirectory(prefix="thesis-apply-") as tmp:
            tmp_path = Path(tmp)
            template_path = self._save_upload(form, "template", tmp_path)
            thesis_path = self._save_upload(form, "thesis", tmp_path)
            output_path = tmp_path / "formatted-thesis.docx"
            apply_template_format(template_path, thesis_path, output_path)

            body = output_path.read_bytes()
            self.send_response(HTTPStatus.OK)
            self.send_header(
                "Content-Type",
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )
            self.send_header("Content-Disposition", 'attachment; filename="formatted-thesis.docx"')
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)


def main() -> None:
    server = ThreadingHTTPServer(("127.0.0.1", 8765), ThesisRequestHandler)
    print("Thesis Formatter API listening on http://127.0.0.1:8765")
    server.serve_forever()


if __name__ == "__main__":
    main()
