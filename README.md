# Project Title: Document Processing Application

## Overview
This project is designed to process and extract information from PDF documents related to the South of France. It utilizes various machine learning models and techniques to enhance the extraction and querying of data.

## Project Structure
```
.
├── src/
│   ├── extractor.py
│   ├── embedder.py
│   ├── faiss_indexer.py
│   ├── llm_handler.py
│   ├── pipeline.py
│   ├── refiner.py
│   └── utils.py
├── models/
│   ├── qwen2.5/
│   │   └── qwen2.5-0.5b-instruct-q4_k_m.gguf
│   └── nomic-ai/
│       └── nomic-embed-text-v1.5.f16.gguf
├── input/
│   ├── Collection_1/
│   ├── Collection_2/
│   └── Collection_3/
├── run.py
├── start_llm_server.py
├── startup.sh
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
│   ├── South of France - Cities.pdf
│   └── South of France - Cuisine.pdf
├── run.py
├── input.json
├── output.json
└── README.md
```

## Components
- **src/extractor.py**: Functions for extracting headings and body content from documents using Docling.
- **src/embedder.py**: Wrapper for the MiniLM model to embed text data.
- **src/faiss_indexer.py**: Builds and retrieves indices using the FAISS library for similarity search.
- **src/llm_handler.py**: Wrapper for the LlamaCpp model (Qwen2.5) for language model interactions.
- **src/query_generator.py**: Generates contextual queries based on user persona and task.
- **src/refiner.py**: Refines and scores text sections based on specified persona.
- **src/pipeline.py**: Main logic for orchestrating the application components.
- **src/utils.py**: Utility functions supporting other modules.

## Input and Output
- **Input Files**: 
  - `documents/South of France - Cities.pdf`
  - `documents/South of France - Cuisine.pdf`
  - `input.json`: Contains input data in JSON format.
  
- **Output Files**: 
  - `output.json`: Stores the final output data in JSON format.

## Running the Application
To run the application, execute the `run.py` script. Ensure that all dependencies are installed and the necessary input files are available in the specified directories.

## License
This project is licensed under the MIT License.