## Monday.com Business Intelligence Agent

# Overview

This project implements a production-ready AI-powered Business Intelligence agent that integrates live with Monday.com boards (Deals and Work Orders) to answer founder-level business questions.

The system combines deterministic analytics with LLM-based executive insight generation to ensure both accuracy and interpretability.

Deployed version:  
(https://monday-bi-agent-mslxtrpjugymyaikx8v5le.streamlit.app/)

## Problem Addressed

Founders frequently need quick answers to questions like:

- How is our pipeline looking this quarter?
- What is our mining sector exposure?
- How concentrated is our revenue?
- What is our deal-to-work-order conversion rate?

Business data is often messy and distributed across multiple boards. This agent:

- Fetches live data from Monday.com
- Cleans and normalizes inconsistencies
- Computes deterministic business metrics
- Generates executive-level insights conversationally
- Displays transparent execution traces

## Architecture

The system is designed using a hybrid approach:

### 1️. Deterministic Analytics Layer
Handles:
- Cursor-based pagination
- Data normalization
- Revenue parsing
- Open-only pipeline filtering
- Quarter-based filtering 
- Sector aggregation
- Average deal size calculation
- Top 3 sector concentration %
- Deal → Work Order conversion rate
- Missing data tracking

All business logic is computed deterministically to prevent hallucination.

### 2️. LLM Insight Layer (Gemini)
Responsible for:
- Executive summaries
- Contextual interpretation
- Founder-level communication
- Data caveat explanation

The LLM does not perform calculations.

## Core Features

### 1. Live Monday.com Integration
- GraphQL API integration
- Cursor-based pagination (no record limits)
- No caching (fresh data per query)
- Real-time board state access

### 2. Data Resilience
- Handles null/missing values
- Sanitizes numeric fields
- Normalizes sector labels
- Surfaces data caveats

### 3. Query Understanding
- Interprets founder-level language
- Detects Q1–Q4 and "this quarter"
- Filters by sector
- Asks clarifying questions when query is vague
- Maintains follow-up conversation context using session memory

### 4. Business Intelligence
- Total pipeline value
- Sector-level breakdown
- Average deal size
- Revenue concentration analysis
- Conversion rate (Deals → Work Orders)
- Missing close-date reporting

### 5. Agent Action Visibility

Execution trace displays:
- API fetch counts
- Filtering logic
- Aggregation step
- LLM generation step

## Tech Stack

- Python
- Streamlit
- Monday.com GraphQL API
- Google Gemini API
- Session-based state management

## Deployment

The application is deployed via Streamlit Cloud.

## How to Run Locally

1. Clone repository
2. Create '.env' file:
   
MONDAY_API_KEY="your_key"
GEMINI_API_KEY="your_key"

3. Install dependencies:

pip install -r requirements.txt

4. Run:

streamlit run app.py

## Design Principles

- Deterministic calculations over LLM arithmetic
- Transparent execution tracing
- Live data over caching

## Future Improvements

- Async API calls
- Tool-calling LLM integration (MCP)

## Author
Rahul Kevin
