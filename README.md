

````markdown
# VeriFlow AI

### A Replayable Verification Oracle for AI-Generated Outputs and Code Migrations

VeriFlow AI is an AI-powered verification layer for developers that evaluates whether AI-generated answers are supported by reliable evidence and whether migrated code preserves the behavior of the original implementation.

Instead of trusting an AI-generated response based only on confidence scores or citations, VeriFlow breaks the output into verifiable units, retrieves evidence from multiple sources, applies Natural Language Inference (NLI), compares behavioral outputs, and produces an auditable verification result.

---

## Problem

AI-generated answers and code migrations can appear convincing while containing:

- Unsupported or incorrect claims
- Contradictory information
- Low-quality evidence
- Hidden reasoning errors
- Behavioral differences after code migration

Existing approaches such as citations, model confidence, compilation, and manually written tests do not provide a complete verification layer.

VeriFlow AI addresses this by combining evidence retrieval, NLI-based verification, behavioral testing, failure localization, and auditability.

---

## Solution

VeriFlow AI processes an AI-generated artifact through a multi-phase verification pipeline:

```text
User Input
    |
    v
Phase 1: Claim / Code Decomposition
    |
    v
Phase 2: Multi-Source Evidence Retrieval
    |
    v
Phase 3: Verification Oracle
    |
    +---- NLI Verification
    |
    +---- Behavioral Equivalence
    |
    v
Phase 4: Failure Localization
    |
    v
Phase 5: Audit Trail Generation
    |
    v
Verification Report
````

---

## Key Features

### 1. Claim Decomposition

For text inputs, VeriFlow extracts atomic claims and classifies them as:

* Factual
* Inferential
* Normative

For code inputs, the system identifies functions, control flow, and data transformations.

### 2. Multi-Source Evidence Retrieval

VeriFlow retrieves supporting evidence from external web sources.

The retrieval layer records:

* Source title
* URL
* Evidence text
* Source reliability
* Matched evidence

The system is designed to prioritize authoritative sources while preserving evidence from multiple sources.

### 3. NLI-Based Verification

VeriFlow uses a DeBERTa-v3 Natural Language Inference model to compare:

```text
Evidence → Premise
Claim    → Hypothesis
```

The NLI model produces:

* Entailment probability
* Neutral probability
* Contradiction probability

These results are used by the verification oracle.

### 4. Behavioral Equivalence Testing

For legacy and migrated code, VeriFlow compares outputs for the same test inputs.

It detects:

* Matching outputs
* Different fields
* Legacy values
* Migrated values

This allows compilation success to be distinguished from actual behavioral equivalence.

### 5. Consensus Aggregation

Evidence from multiple sources is combined using:

* NLI confidence
* Source reliability
* Multi-source agreement

The resulting score contributes to the claim-level verification verdict.

### 6. Failure Localization

VeriFlow is designed to go beyond:

```text
Verification Failed
```

and identify why verification failed, including:

* Missing evidence
* Contradictory evidence
* Low source reliability
* Consensus mismatch
* Behavioral divergence

### 7. Auditability

The system includes an audit layer for producing reproducible verification information such as:

* Artifact information
* Claim verdicts
* Evidence
* NLI probabilities
* Test results
* Equivalence confidence
* Trust Index
* Divergence information

---

## Technology Stack

### Backend

* Python
* FastAPI
* PyTorch
* Hugging Face Transformers
* DeBERTa-v3 NLI
* BeautifulSoup
* Requests
* Pytest

### Frontend

* React
* Vite
* JavaScript
* CSS

### Retrieval

* External web search
* Web page content extraction
* Multi-source evidence collection

### Development

* Git
* GitHub
* Docker support

---

## Project Structure

```text
veriflow/
│
├── backend/
│   ├── app/
│   │   ├── phase1/
│   │   ├── phase2/
│   │   ├── phase3/
│   │   ├── phase4/
│   │   ├── phase5/
│   │   ├── models/
│   │   ├── api/
│   │   ├── services/
│   │   ├── core/
│   │   ├── main.py
│   │   └── verification_pipeline.py
│   │
│   └── tests/
│
├── frontend/
│   ├── src/
│   ├── public/
│   └── package.json
│
├── data/
│   ├── sample_inputs/
│   ├── sample_evidence/
│   └── golden_tests/
│
├── docs/
│
├── .gitignore
├── README.md
└── LICENSE
```

---

## Verification Pipeline

### Phase 1 — Input Processing & Claim Decomposition

```text
AI Generated Text
        |
        v
Sentence Splitting
        |
        v
Atomic Claim Extraction
        |
        v
Claim Classification
        |
        v
Structured Claims
```

For code:

```text
Legacy + Migrated Code
        |
        v
AST / Code Analysis
        |
        v
Functions + Control Flow
        |
        v
Characterization / Parity Tests
```

---

### Phase 2 — Multi-Source Evidence Retrieval

For each claim, VeriFlow retrieves external evidence and attaches source metadata.

Conceptually:

```text
Claim
 |
 +--> Source 1
 |
 +--> Source 2
 |
 +--> Source 3
 |
 +--> Source 4
 |
 v
Evidence + Reliability Metadata
```

---

### Phase 3 — Verification Oracle

Text verification:

```text
Claim + Evidence
       |
       v
DeBERTa-v3 NLI
       |
       +--> Entailment
       +--> Neutral
       +--> Contradiction
       |
       v
Consensus Aggregation
       |
       v
Claim Verdict
```

Code verification:

```text
Test Input
    |
    +----> Legacy Output
    |
    +----> Migrated Output
                |
                v
        Behavioral Comparison
                |
                v
        PASS / FAIL + Differences
```

---

### Phase 4 — Failure Localization

The system identifies the location and reason for a failed verification.

For example:

```text
Function: calculateTax
Line: 142

Legacy:
ROUND_HALF_UP

Migrated:
ROUND_HALF_EVEN

Result:
Behavioral divergence detected
```

---

### Phase 5 — Audit Trail Generation

A verification run can be represented as an auditable report containing:

```text
Artifact
Claim Results
Evidence
NLI Scores
Test Results
Equivalence Results
Trust Index
Divergence Report
Replay Information
```

---

## Trust and Verification Metrics

### Claim Confidence

The claim confidence combines:

```text
Claim Confidence =
0.5 × NLI Entailment Probability
+ 0.3 × Source Reliability
+ 0.2 × Consensus Score
```

### Source Reliability

```text
Source Reliability =
0.5 × Authority
+ 0.3 × Freshness
+ 0.2 × Citation Score
```

### Behavioral Equivalence

Behavioral verification uses test pass rate and coverage-related factors to estimate equivalence confidence.

### Trust Index

The overall Trust Index combines:

```text
40% Claim Grounding
40% Behavioral Equivalence
20% Non-Hallucination
```

---

## Running the Project

### Backend

Navigate to the backend:

```powershell
cd backend
```

Start FastAPI:

```powershell
python -m uvicorn app.main:app --reload
```

Backend API:

```text
http://127.0.0.1:8000
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

### Frontend

Open a second terminal:

```powershell
cd frontend
npm install
npm run dev
```

Frontend:

```text
http://localhost:5173
```

---

## API

### Health Check

```http
GET /health
```

Example response:

```json
{
  "status": "ok",
  "service": "veriflow-ai"
}
```

### Verify AI Output

```http
POST /api/verify
```

Request:

```json
{
  "content": "Java HashMap allows null keys."
}
```

The response contains results from the verification pipeline, including claims, retrieved evidence, NLI verification, and consensus information.

---

## Example

Input:

```text
Java HashMap allows null keys.
```

VeriFlow:

```text
Phase 1
    ↓
C001: Java HashMap allows null keys.

Phase 2
    ↓
Retrieve external evidence

Phase 3
    ↓
Run NLI verification
    ↓
Calculate confidence
    ↓
Generate verdict
```

The web interface presents these results through a developer-oriented verification dashboard.

---

## Testing

Run the backend test suite with:

```powershell
python -m pytest -q
```

The repository includes tests for:

* Phase 2 web retrieval
* Web content extraction
* Behavioral equivalence
* Consensus aggregation
* Phase 3 verification
* End-to-end verification pipeline
* Phase 5 audit functionality

---

## Security

API keys and environment-specific secrets must not be committed to GitHub.

For example:

```text
.env
```

should remain local and excluded through `.gitignore`.

---

## Current Scope

### Included

* Java-oriented verification workflows
* AI claim verification
* External evidence retrieval
* NLI verification
* Behavioral comparison
* React dashboard
* FastAPI backend
* Verification tests
* Audit and trust-index components

### Out of Scope

* Formal mathematical proof
* Full web-scale fact checking
* Production-grade code sandboxing
* Support for every programming language

---

## Future Improvements

Planned extensions include:

* GitHub Pull Request verification
* More programming languages
* Improved evidence ranking
* Better failure localization
* Signed verification packages
* Active learning for verification models
* Enterprise deployment support

---

## Why VeriFlow AI?

AI systems are becoming increasingly capable of generating code and information, but generation alone does not guarantee correctness.

VeriFlow AI adds a verification layer between generation and human acceptance:

```text
Generate
   ↓
Verify
   ↓
Explain
   ↓
Audit
   ↓
Review with Confidence
```

The goal is not simply to say that an AI output looks correct.

The goal is to provide evidence for **why it should be trusted**.

---

## Team

**Team:** Data Dynamos

**Project:** VeriFlow AI

**Track:** Developer Tools + AI

---

````

### One important thing before you commit

Because your repository currently has **Phase 5 code merged from your teammate**, this README describes the full architecture consistently with that repository state.

Save it as:

```text
VERIFLOW/README.md
````

Then commit and push:

```powershell
git add README.md
git commit -m "Add project README"
git push origin development
```

