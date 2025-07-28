import json
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.datamodel.base_models import InputFormat

def extract_headings_and_body(source_path: str):
    pdf_opt = PdfFormatOption(pipeline_options=PdfPipelineOptions(do_table_structure=True))
    converter = DocumentConverter(format_options={InputFormat.PDF: pdf_opt})
    doc = converter.convert(source_path).document
    data = doc.model_dump()

    all_texts = data.get("texts", [])
    sections = []

    idx = 0
    while idx < len(all_texts):
        t = all_texts[idx]

        label = t.get("label", "")
        text = t.get("text", "").strip()

        # Skip empty blocks, tables, and figures
        if not text or label in ["table", "figure"]:
            idx += 1
            continue

        if label == "section_header":
            heading_parts = [text]
            page = t.get("prov", [{}])[0].get("page_no", -1)

            body_parts = []
            next_idx = idx + 1

            while next_idx < len(all_texts):
                next_t = all_texts[next_idx]
                next_label = next_t.get("label", "")
                next_text = next_t.get("text", "").strip()

                # Skip empty blocks, tables, and figures
                if not next_text or next_label in ["table", "figure"]:
                    next_idx += 1
                    continue

                if next_label == "section_header":
                    if body_parts:
                        break
                    else:
                        heading_parts.append(next_text)
                        next_idx += 1
                        continue

                body_parts.append(next_text)
                next_idx += 1

            heading = "##".join(heading_parts)
            body = " ".join(body_parts)

            sections.append({
                "heading": heading,
                "body": body,
                "page": page,
                "source": source_path.split("\\")[-1]
            })

            idx = next_idx
        else:
            idx += 1

    return sections
