# 🚀 LoanWise : Smart Loans, Smarter Decision

## 🏆 The Great Bengaluru Hackathon Project

A centralized, AI-driven conversational assistant designed to help users with loan eligibility checks, loan applications, and financial literacy through intelligent multi-agent architecture.

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![React Version](https://img.shields.io/badge/react-18.0+-61DAFB.svg?logo=react)](https://reactjs.org/)

## ✨ Features

- 💬 **Multilingual Support**: Text and speech interactions in multiple regional languages backed by SARVAM AI
- 🤖 **AI-Driven Conversations**: Personalized financial advice using advanced LLMs techniques like RAG, Similarity Search
- 📊 **Real-time Analysis**: Live assessment of loan eligibility and market offers using Web Scrapping
- 🔐 **Intent Recognition**: Non hard coded intent recognition, the model increases in acuraccy with training and time
- 📚 **Financial Literacy**: Built-in educational resources

## 📋 Table of Contents

- [System Architecture](#-system-architecture)
- [Workflow](#-workflow)
- [Setup and Installation](#-setup-and-installation)
- [Usage](#-usage)
- [Team](#-team)
- [License](#-license)

## 🏗 System Architecture

Our solution employs a multi-agent architecture to provide comprehensive loan advisory services:

![System Architecture Diagram](/architecture.jpeg)

### Key Components

#### A. KYC Agent
- Builds and maintains user knowledge graphs
- Tracks financial history and preferences
- Implements sentiment analysis for context-aware responses
- Personalizes recommendations based on user profiles

#### B. Loan Advisor Agent
- Suggests optimal loan options based on user data
- Implements real-time web scraping for market offers
- Compares interest rates and eligibility criteria
- Provides proactive financial insights

#### C. FAQ/Helper Agent
- Utilizes Retrieval-Augmented Generation (RAG)
- Delivers precise answers from financial knowledge base
- Supports multi-turn conversations
- Clarifies loan terms and eligibility criteria

#### D. Logger Agent
- Manages inter-agent communication
- Detects system failures and anomalies
- Generates detailed logs for analytics

#### E. Multilingual Text + Speech Pipeline
- Supports regional languages via NLLB/Google Translate
- Integrates STT and TTS capabilities
- Adapts to user language preferences

#### F. Frontend Interfaces
- WhatsApp integration via Twilio/Meta Business API
- React-based web application
- Document upload functionality
- Application tracking

## 🔄 Workflow

<div align="center">
  <img src="https://via.placeholder.com/700x400" alt="User Journey Flowchart">
</div>

1. **User Initiation**: Conversation begins via WhatsApp or web app
2. **KYC Engagement**: System collects and processes financial data
3. **Intent Recognition**: AI determines user needs and routes accordingly
4. **Loan Advisory**: Personalized loan options based on real-time data
5. **Query Resolution**: RAG-based system answers financial questions
6. **System Monitoring**: Logger ensures stability and performance
7. **Language Processing**: Seamless multilingual support
8. **Application Submission**: Guided documentation and submission process

## 🛠 Setup and Installation

### Prerequisites

- Python 3.8+
- React.js
- flask-python
- Neo4js

### Backend Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/bubblesort-team/loan-advisory-system.git
   cd loan-advisory-system
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and configurations
   ```

5. Start the server:
   ```bash
   python server.py
   ```

### Frontend Setup

1. Navigate to the client directory:
   ```bash
   npm create-react-app client  # If not already created
   cd client
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```

## 📱 Usage

<div align="center">
  <img src"1.jpeg" alt="Application Demo">
</div>

<div align="center">
  <img src"2.jpeg" alt="Application Demo">
</div>

<div align="center">
  <img src"3.jpeg" alt="Application Demo">
</div>


1. Send a message to begin the conversation

### Web Application

1. Navigate to [https://bubblesort-loans.example.com](https://bubblesort-loans.example.com)
2. Create an account or log in
3. Complete your financial profile
4. Start exploring loan options or ask questions

## 👥 Team

The Bubble Sort team consists of:

- **Siddartha A Y** - Architecture & Backend
- **Kushal B Gowda** - AI Models & Integration
- **Aaron Sabu** - Frontend & UX
- **Rainhan N** - Data Engineering & Analytics

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<div align="center">
  <p>Built with ❤️ by Team Bubble Sort</p>
  <p>The Great Bengaluru Hackathon 2023</p>
</div>
