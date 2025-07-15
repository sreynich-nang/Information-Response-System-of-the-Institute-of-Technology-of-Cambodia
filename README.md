---

# AI-Powered Academic & Career Guidance Chatbot

## Project Overview

This thesis project presents the design, development, and evaluation of an AI-powered chatbot aimed at assisting students with academic and career guidance. The chatbot is built to accurately retrieve and generate relevant information from complex institutional documents using advanced Retrieval-Augmented Generation (RAG) architecture.

By leveraging state-of-the-art components such as MPNet embeddings, OpenChat generation, and vector databases, the system enhances semantic understanding and response accuracy. The project involved meticulous data cleaning, chunking, and retrieval configuration to optimize the chatbot’s performance.

Evaluation metrics including MRR\@3, MAP, Recall\@3, ROUGE-L, and Cosine Similarity demonstrated the system’s effectiveness in providing document-grounded and relevant answers. Compared to general-purpose AI models like ChatGPT and DeepSeek, this chatbot uniquely succeeded in retrieving specific institutional data (e.g., tuition fees), confirming its value for academic applications. The study also identifies technical limitations and proposes directions for future improvements.

---

## Executive Summary

This project delivers a cutting-edge AI chatbot system powered by Retrieval-Augmented Generation (RAG), combining large language models (LLMs) with an external, dynamically updated knowledge base to answer user queries with contextual accuracy.

The architecture employs:

* **FastAPI** as a stateless backend to handle API requests,
* **Next.js** for a user-friendly frontend interface,
* **LangChain** to orchestrate the RAG pipeline including chunking, embedding, retrieval, and prompt formatting,
* **ChromaDB** as a scalable vector database for efficient semantic search.

Users can upload documents in PDF or TXT formats, which the system parses, chunks, and embeds to enrich the chatbot’s knowledge base. To optimize performance and scalability, an MD5 hashing mechanism prevents redundant processing of duplicate documents.

---

## Key Features

### 1. LLM-Powered Chatbot with RAG Framework

* Converts user queries into embedding vectors.
* Searches the ChromaDB vector store for semantically relevant document chunks.
* Constructs context-aware prompts using retrieved information.
* Generates accurate, document-grounded answers with the LLM.

### 2. Document Upload and Knowledge Base Expansion

* Supports PDF and TXT document uploads.
* Parses and splits documents into meaningful text chunks.
* Embeds chunks into vectors stored in ChromaDB.
* Uses MD5 file hashing to detect duplicates and avoid redundant processing.

### 3. Modular Backend and Frontend Architecture

* **Backend:** FastAPI-based, stateless API handling uploads, hashing, processing, and querying.
* **Frontend:** Next.js interface for seamless user interactions and real-time chatbot responses.
* **Orchestration:** LangChain manages document chunking, embeddings, retrieval, and prompt formatting.

### 4. Performance Optimization & Scalability

* Redundancy checks using hashing to save computation and storage.
* Efficient semantic search with vector embeddings and cosine similarity.
* Scalable vector storage using ChromaDB.
* Stateless backend architecture enables horizontal scaling for high-demand usage.

---

## Project Impact and Applications

This AI chatbot system empowers users and organizations by providing:

* **Education:** Students receive summarized, context-aware academic guidance tailored to their institution.
* **Legal & Compliance:** Professionals can quickly navigate complex regulatory documents.
* **Customer Support:** Support teams access internal documentation to reduce response times.
* **Enterprise Knowledge Management:** Employees query company documents naturally, enhancing productivity.

By bridging the gap between static document knowledge bases and dynamic user queries, this system facilitates informed decision-making and improves accessibility to critical information.

---

## Technologies Used

* **Language Models:** OpenChat LLM integrated via RAG
* **Embeddings:** MPNet for semantic representation
* **Backend:** FastAPI
* **Frontend:** Next.js
* **Orchestration:** LangChain
* **Vector Database:** ChromaDB
* **File Handling:** MD5 hashing for duplicate detection

---

## How to Use

1. **Upload documents** (PDF/TXT) via the frontend interface to expand the chatbot’s knowledge base.
2. **Ask questions** related to the uploaded documents.
3. The chatbot retrieves relevant chunks and generates precise, context-aware answers.
4. Duplicate document uploads are automatically detected and skipped for efficiency.

---

## Evaluation Metrics

The system was evaluated using multiple metrics:

* **MRR\@3** (Mean Reciprocal Rank)
* **MAP** (Mean Average Precision)
* **Recall\@3**
* **ROUGE-L** (Recall-Oriented Understudy for Gisting Evaluation)
* **Cosine Similarity**

Results show the chatbot consistently provides relevant and accurate answers grounded in the uploaded documents.

---

## Future Directions

* Enhance multi-lingual support and domain adaptation.
* Integrate additional vector databases for scalability.
* Improve UI/UX for better user engagement.
* Optimize backend for even faster response times.
* Expand evaluation to more diverse datasets and real-world user feedback.

---
