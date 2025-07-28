import os
from src.extractor import extract_headings_and_body
from src.embedder import MiniLMRemoteEmbedder
from src.faiss_indexer import FaissIndex
from src.query_generator import generate_multiple_queries
from src.refiner import refine_sections
from datetime import datetime

# remove it later
import json

def run_pipeline(input_json, llm):
    persona = input_json["persona"]["role"]
    job = input_json["job_to_be_done"]["task"]
    docs = input_json["documents"]

    all_sections = []
    input_doc_names = []

    for doc in docs:
        path = os.path.join("documents", doc["filename"])
        input_doc_names.append(doc["filename"])
        sections = extract_headings_and_body(path)
        all_sections.extend(sections)
    
    print("loara_pipe")
    with open("deb.txt", "a") as f:
        f.write(f"Extracted {len(all_sections)} sections from {len(docs)} documents.\n")
        f.write(f"Documents: {', '.join(input_doc_names)}\n")
        f.write(f"Sections: {json.dumps(all_sections, indent=2)}\n")

    with open("deb.txt", "a") as f:
        f.write(timestamp := f"Timestamp_Start: {datetime.now()}\n")

    embedder = MiniLMRemoteEmbedder()
    faiss_index = FaissIndex()
    faiss_index.add_sections(all_sections, embedder)
    print("loara_pipe__2")

    with open("deb.txt", "a") as f:
        f.write(timestamp := f"Timestamp_after_indexing: {datetime.now()}\n")

    query = f"As a {persona}, I want to {job}.".format(
        persona=persona,
        job=job
    )

    # Debugging: Save generated querie
    # Run each query through FAISS
    
    with open("deb.txt", "a") as f:
        f.write(timestamp := f"Timestamp_before_multiple_query_retrival: {datetime.now()}\n")

    matched_query_map = {}
    retrieved_sections = []
    seen_titles = set()
    for sec in faiss_index.search(query, embedder, k=5):  # reduce k to 3 per query
        title = sec['heading'].split("##")[0] + sec.get('source', '')
        if title not in seen_titles:
            retrieved_sections.append(sec)
            matched_query_map[title] = query
            seen_titles.add(title)












    with open("deb.txt", "a") as f:
        f.write(timestamp := f"Timestamp_after_multiple_query_retrival: {datetime.now()}\n")

    print("loara_pipe__3")
    
    with open("deb.txt", "a") as f:
        json.dump(matched_query_map, f, indent=2)


    # for debugging johar sahab isko hatadena baad mai
    with open("deb.txt", "a") as f:
        json.dump(retrieved_sections, f, indent=2)

    
    
    # work to done  
    refined = refine_sections(retrieved_sections, persona, job, llm)

    # final JSON
    output = {
        "metadata": {
            "input_documents": input_doc_names,
            "persona": persona,
            "job_to_be_done": job
        },
        "extracted_sections": [
            {
                "document": sec["source"],
                "section_title": sec["heading"],
                "importance_rank": idx + 1,
                "page_number": sec["page"]
            } for idx, sec in enumerate(retrieved_sections)
        ],
        "subsection_analysis": [
            {
                "document": sec["document"],
                "refined_text": sec["refined_text"],
                "page_number": sec["page_number"]
            } for sec in refined
        ]
    }

    return output
