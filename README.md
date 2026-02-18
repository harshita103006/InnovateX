# InnovateX

VajraAI – AI-Powered Email Fraud Detection (Phase 1)

🚀 Overview

VajraAI is an AI-driven fraud detection platform designed to combat emerging AI-generated threats.
Currently, the platform implements the Email Fraud Detection Module, which analyzes suspicious emails using a hybrid NLP-based approach to detect phishing, AI-generated text, and credential exposure patterns.
This is Phase 1 implementation of the larger VajraAI system.


✅ Implemented Features (Current Working System)

📧 Email Analyzer Module

The Email Analyzer performs:

>AI-generated text detection
>Phishing intent detection
>Urgency & manipulation pattern detection
>Suspicious link pattern detection
>Credential request detection
>Named Entity Recognition (NER) for sensitive data masking

🎯 Output Includes:

>Risk Score (0–100%)
>Risk Level (Low / Medium / High / Critical)
>Flagged Indicators
>Masked Email Preview


🏗 Current Architecture

>FastAPI Backend
>Modular Email Detection Engine
>Risk Scoring Logic (Email module only)
>Web-based Frontend Interface


🛠 Tech Stack

Backend:

>Python
>FastAPI
>NLP Models (BERT / RoBERTa or equivalent)
>Perplexity Scoring
>Regex + NER

Frontend:

>HTML
>CSS
>JavaScript


📌 Development Status

Module	Status

>Email Analyzer	✅ Completed
>Attachment Sandbox	🔄 Planned
>URL & Website Analyzer	🔄 Planned
>Deepfake Voice Detection	🔄 Planned
>Central Multi-Module Risk Engine	🔄 Planned


🔮 Future Expansion

VajraAI is designed as a modular microservices platform. Future phases will include:

>Attachment malware sandbox
>URL & phishing website detection
>Deepfake voice scam detection
>Prompt injection testing sandbox
>Enterprise-grade deployment & scaling
