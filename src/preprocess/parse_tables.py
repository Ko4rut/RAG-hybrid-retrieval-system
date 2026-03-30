import re
from langchain_core.documents import Document


class TableParser:
    def __init__(self, replace_br_with: str = " "):
        self.replace_br_with = replace_br_with

    def parse_document(self, doc: Document) -> Document:
        return Document(
            page_content=self.parse_text(doc.page_content),
            metadata=doc.metadata
        )

    def parse_text(self, text: str) -> str:
        blocks = self.detect_table_blocks(text)
        parsed_text = text

        for block_info in blocks:
            block = block_info["block"]
            title = block_info["section_title"]

            if not self.is_clean_table_block(block):
                continue

            normalized = self.parse_table_block(block, section_title=title)
            parsed_text = parsed_text.replace(block, normalized, 1)

        return parsed_text

    def detect_table_blocks(self, text: str) -> list[dict]:
        lines = text.splitlines()
        blocks = []
        i = 0

        while i < len(lines) - 1:
            if self.is_table_row(lines[i]) and self.is_separator_row(lines[i + 1]):
                start = i
                block_lines = [lines[i], lines[i + 1]]
                i += 2

                while i < len(lines) and self.is_table_row(lines[i]):
                    block_lines.append(lines[i])
                    i += 1

                block = "\n".join(block_lines)
                section_title = self.find_previous_section_title(lines, start)

                blocks.append({
                    "block": block,
                    "section_title": section_title
                })
            else:
                i += 1

        return blocks

    def is_table_row(self, line: str) -> bool:
        stripped = line.strip()
        return stripped.startswith("|") and stripped.count("|") >= 2

    def is_separator_row(self, line: str) -> bool:
        stripped = line.strip()
        if not stripped.startswith("|"):
            return False

        parts = [p.strip() for p in stripped.strip("|").split("|")]
        if not parts:
            return False

        return all(re.fullmatch(r":?-{3,}:?", p) for p in parts)

    def is_clean_table_block(self, block: str) -> bool:
        lines = [line for line in block.splitlines() if line.strip()]
        if len(lines) < 3:
            return False

        header_cols = self.count_columns(lines[0])
        if header_cols == 0:
            return False

        if not self.is_separator_row(lines[1]):
            return False

        for row in lines[2:]:
            if self.is_separator_row(row):
                return False
            if self.count_columns(row) != header_cols:
                return False

        return True

    def count_columns(self, line: str) -> int:
        return len(self.split_row(line))

    def split_row(self, line: str) -> list[str]:
        return [cell.strip() for cell in line.strip().strip("|").split("|")]

    def clean_cell(self, cell: str) -> str:
        cell = cell.replace("<br>", self.replace_br_with)
        cell = re.sub(r"\*\*(.*?)\*\*", r"\1", cell)
        cell = re.sub(r"\s+", " ", cell).strip()
        return cell

    def parse_table_block(self, block: str, section_title: str | None = None) -> str:
        lines = [line for line in block.splitlines() if line.strip()]

        header = [self.clean_cell(c) for c in self.split_row(lines[0])]
        data_rows = lines[2:]

        output = []

        if section_title:
            output.append(f"Section: {section_title}")

        output.append(f"Columns: {' | '.join(header)}")

        for idx, row in enumerate(data_rows, start=1):
            cells = [self.clean_cell(c) for c in self.split_row(row)]

            pairs = []
            for h, c in zip(header, cells):
                pairs.append(f"{h}: {c}")

            output.append(f"Row {idx}: " + " | ".join(pairs))

        return "\n".join(output)

    def find_previous_section_title(self, lines: list[str], start_idx: int) -> str | None:
        for i in range(start_idx - 1, -1, -1):
            line = lines[i].strip()
            if line.startswith("##"):
                title = re.sub(r"^#+\s*", "", line)
                title = re.sub(r"\*\*(.*?)\*\*", r"\1", title).strip()
                return title
        return None