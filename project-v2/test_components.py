import json
import os
from src.llm_handler import LLMWrapper
from src.embedder import MiniLMRemoteEmbedder
from src.extractor import extract_headings_and_body
from src.faiss_indexer import FaissIndex
from src.refiner import refine_sections, format_messages

def test_llm():
    print("\n=== Testing LLM Wrapper ===")
    llm = LLMWrapper()
    try:
        response = llm.generate("Tell me a short joke.")
        print("✅ LLM Test Passed")
        print(f"Response: {response}")
    except Exception as e:
        print(f"❌ LLM Test Failed: {str(e)}")

def test_embedder():
    print("\n=== Testing Embedder ===")
    embedder = MiniLMRemoteEmbedder()
    try:
        embedding = embedder.get_embedding("Test sentence")
        print("✅ Embedder Test Passed")
        print(f"Embedding shape: {embedding.shape}")
    except Exception as e:
        print(f"❌ Embedder Test Failed: {str(e)}")

def test_extractor():
    print("\n=== Testing Extractor ===")
    try:
        test_pdf = os.path.join("documents", os.listdir("documents")[0])
        sections = extract_headings_and_body(test_pdf)
        print("✅ Extractor Test Passed")
        print(f"Extracted {len(sections)} sections")
    except Exception as e:
        print(f"❌ Extractor Test Failed: {str(e)}")

def test_faiss():
    print("\n=== Testing FAISS Indexer ===")
    embedder = MiniLMRemoteEmbedder()
    index = FaissIndex()
    try:
        # Create test sections
        test_sections = [
            {"heading": "Test 1", "body": "This is a test section"},
            {"heading": "Test 2", "body": "Another test section"}
        ]
        index.add_sections(test_sections, embedder)
        results = index.search("test", embedder, k=2)
        print("✅ FAISS Test Passed")
        print(f"Search returned {len(results)} results")
    except Exception as e:
        print(f"❌ FAISS Test Failed: {str(e)}")

def test_refiner():
    print("\n=== Testing Refiner ===")
    llm = LLMWrapper()
    try:
        test_sections = [
            {
                "body": "Paris is the capital of France",
                "source": "test.pdf",
                "page": 1
            }
        ]
        refined = refine_sections(test_sections, "Travel Guide", "Plan a trip", llm)
        print("✅ Refiner Test Passed")
        print(f"Refined text: {refined[0]['refined_text'][:100]}...")
    except Exception as e:
        print(f"❌ Refiner Test Failed: {str(e)}")

if __name__ == "__main__":
    print("🔍 Starting Component Tests")
    print("Make sure the LLM server is running!")
    
    test_llm()
    test_embedder()
    test_extractor()
    test_faiss()
    test_refiner()