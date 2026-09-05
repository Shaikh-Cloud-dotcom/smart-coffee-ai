# Smart Coffee AI ☕

Smart Coffee AI is a customer-facing AI coffee shop assistant powered by
Google Gemini and Google ADK.

## Features

- Firebase Authentication
- AI-powered coffee recommendations
- Multi-turn conversations
- Coffee menu search
- Firestore chat storage
- User-specific chat data
- FastAPI backend
- Google Gemini + ADK
- Cloud Run ready

## Technologies

- Python
- FastAPI
- Google Gemini
- Google ADK
- Firebase Authentication
- Cloud Firestore
- Docker
- Google Cloud Run

## Architecture

User
↓
Frontend
↓
Firebase Authentication
↓
FastAPI Backend
↓
Google ADK + Gemini
↓
Coffee Menu Retrieval
↓
Firestore

## Firestore Structure

users
└── {userId}
    └── chats
        └── {chatId}

## Security

Firebase Authentication is used to authenticate users.

Firestore security rules restrict users to their own data.

API keys and environment secrets are stored outside the repository
and must not be committed to GitHub.

## Local Setup

Install dependencies:

```bash
pip install -r requirements.txt