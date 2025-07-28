import faiss

class FaissIndex:
    def __init__(self, embed_dim=768):
        self.index = faiss.IndexFlatL2(embed_dim)
        self.sections = []
        
    def add_sections(self, sections, embedder):
        for sec in sections:
            text = "heading -> " + sec['heading'] + "\ncontent -> " + sec['body'][:512]
            emb = embedder.get_embedding(text).reshape(1, -1)
            self.index.add(emb)
            self.sections.append(sec)

    def search(self, query, embedder, k=5):
        qvec = embedder.get_embedding(query).reshape(1, -1)
        D, I = self.index.search(qvec, k)
        return [self.sections[i] for i in I[0]]
