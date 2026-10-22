# 🚚 Shipment Exception Desk

**An LLM-powered shipment exception triage system built with LangChain, Python, and Gradio.**

Shipment Exception Desk automates the processing of shipment exception reports for Northwind Logistics. It classifies incidents, calculates compensation using deterministic business rules, decides whether human intervention is required, and generates appropriate communications.

The application combines **LLM-powered classification and message generation** with **rule-based decision-making** to make exception handling more consistent, transparent, and efficient.

It also provides an interactive Gradio interface with a running triage log and a daily summary of compensation costs and escalation rates.

---

## 📌 Problem Statement

Logistics companies handle shipment exceptions such as delayed deliveries, damaged goods, and lost shipments.

Traditionally, operations analysts manually review every report to:

* Identify the type of shipment exception.
* Calculate compensation according to company policy.
* Decide whether the issue can be resolved automatically.
* Escalate high-value or unclear cases to a manager.
* Draft customer-facing emails or internal escalation notes.

This manual process can be slow and inconsistent.

**Shipment Exception Desk automates this workflow while keeping compensation calculations and escalation decisions under explicit Python business rules.**

---

## ✨ Key Features

### 1. AI-Powered Exception Classification

Uses a LangChain LLM chain to classify incoming reports into four categories:

* **Delayed:** The shipment arrived later than expected.
* **Damaged:** The shipment or its contents were damaged.
* **Lost:** The shipment is missing or cannot be located.
* **Unknown:** The report is ambiguous, garbled, or insufficient for reliable classification.

### 2. Rule-Based Compensation Calculation

Calculates compensation using dedicated Python functions for delayed, damaged, and lost shipments.

Each calculator returns a structured dictionary containing the category, shipment value, compensation amount, currency, and policy description.

Compensation is calculated deterministically rather than delegated to the LLM.

### 3. Intelligent Escalation

Routes exceptions according to compensation thresholds and customer tier.

* Premium customers have a lower escalation threshold than standard customers.
* High-value exceptions are routed to a manager when the applicable threshold is exceeded.
* Unclassifiable reports always require human review, regardless of shipment value or compensation.

### 4. Automated Message Drafting

Uses separate LangChain chains to generate:

* Customer-facing emails for automatically resolved exceptions.
* Internal escalation notes for cases requiring managerial review.

### 5. Daily Triage Summary

Aggregates the results of processed exceptions, including:

* Total reports processed.
* Total compensation calculated.
* Number of escalated exceptions.
* Escalation rate.
* Compensation totals by exception category.
* Costliest category by aggregate compensation.

The costliest category is determined by summing compensation across all reports in each category, not by selecting the largest individual payout.

### 6. Interactive Gradio Interface

Provides a user-friendly interface for analysts to:

* Submit shipment exception reports.
* Enter shipment value and customer tier.
* View classification and compensation results.
* Inspect the processing steps and escalation decision.
* Read generated messages.
* Review the running triage log.
* Generate the daily summary.

---

## 🏗️ Architecture

The application uses a straightforward pipeline architecture.

```text
                  ┌─────────────────────────┐
                  │     Gradio Interface    │
                  │         app.py          │
                  └────────────┬────────────┘
                               │
                               ▼
                  ┌─────────────────────────┐
                  │   Exception Pipeline    │
                  │       pipeline.py       │
                  └────────────┬────────────┘
                               │
                               ▼
                  ┌─────────────────────────┐
                  │    classify_chain       │
                  │   LangChain + LLM       │
                  └────────────┬────────────┘
                               │
                               ▼
                  ┌─────────────────────────┐
                  │  Python Business Rules  │
                  │        tools.py         │
                  └────────────┬────────────┘
                               │
                               ▼
                  ┌─────────────────────────┐
                  │   Escalation Decision   │
                  │   Customer Tier + Cost  │
                  └────────────┬────────────┘
                               │
                    ┌──────────┴──────────┐
                    │                     │
                    ▼                     ▼
           ┌────────────────┐   ┌─────────────────┐
           │ Automatic      │   │ Human Review    │
           │ Resolution     │   │ Required        │
           └───────┬────────┘   └────────┬────────┘
                   │                     │
                   ▼                     ▼
           ┌────────────────┐   ┌─────────────────┐
           │ Customer Email │   │ Manager Note    │
           │ draft_email_   │   │ escalate_chain  │
           │ chain          │   │                 │
           └───────┬────────┘   └────────┬────────┘
                   │                     │
                   └──────────┬──────────┘
                              │
                              ▼
                  ┌─────────────────────────┐
                  │   Daily Triage Session  │
                  │       session.py        │
                  └────────────┬────────────┘
                               │
                               ▼
                  ┌─────────────────────────┐
                  │ Daily Log and Summary   │
                  └─────────────────────────┘
```

### Design Principles

* **LLMs handle language tasks:** Classification and message generation.
* **Python handles business decisions:** Compensation calculations and escalation rules.
* **Structured outputs support reliable processing:** Classification returns a defined category, while compensation calculators return dictionaries.
* **The pipeline coordinates the workflow:** Conditional logic connects the individual components.
* **The session maintains operational statistics:** Every successfully processed report contributes to the daily aggregation.

---

## 🛠️ Technology Stack

| Technology    | Purpose                                         |
| ------------- | ----------------------------------------------- |
| Python        | Application logic and business rules            |
| LangChain     | LLM chains and prompt orchestration             |
| OpenAI API    | Exception classification and message generation |
| Gradio        | Interactive web interface                       |
| Pydantic      | Structured classification output                |
| python-dotenv | Environment variable management                 |

---

## 📂 Project Structure

```text
shipment-exception-desk/
│
├── chains.py
│   └── LangChain classification and drafting chains
│
├── tools.py
│   └── Compensation calculation functions
│
├── pipeline.py
│   └── Exception processing and escalation logic
│
├── session.py
│   └── Session records and daily aggregation
│
├── app.py
│   └── Gradio user interface
│
├── triage_check.py
│   └── Automated triage verification
│
├── requirements.txt
│   └── Python dependencies
│
├── .env
│   └── Local API configuration
│
├── .gitignore
│   └── Files excluded from version control
│
└── README.md
    └── Project documentation
```

---

## ⚙️ Installation and Setup

### Prerequisites

Make sure you have:

* Python 3.10 or later.
* An OpenAI API key.
* Internet connectivity for API requests.
* Git, if you want to clone the repository.

### Step 1: Clone the Repository

```bash
git clone <your-repository-url>
cd shipment-exception-desk
```

Replace `<your-repository-url>` with your actual repository URL.

Alternatively, download the project and open its directory in your terminal.

### Step 2: Create a Virtual Environment

**Windows PowerShell**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Linux or macOS**

```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-4.1-mini
```

Replace `your_openai_api_key` with your actual API key.

The application loads the environment variables using `python-dotenv`. `ChatOpenAI` reads the API key from the environment.

**Security:** Never commit your `.env` file or expose your API key in source code, screenshots, or public repositories.

### Step 5: Launch the Application

```bash
python app.py
```

After the application starts, open the local Gradio URL displayed in your terminal. It is typically:

```text
http://127.0.0.1:7860
```

The Shipment Exception Desk interface is now ready to use.

---

## 🚀 How to Use the Application

### Step 1: Submit an Exception Report

Enter a description of the shipment problem.

Example:

> The shipment was supposed to arrive yesterday, but it has still not been delivered.

### Step 2: Enter Shipment Details

Provide:

* Shipment value in INR.
* Customer tier: `standard` or `premium`.

### Step 3: Process the Exception

Click **Process Exception**.

The system will:

1. Validate the input.
2. Classify the exception.
3. Calculate compensation.
4. Evaluate escalation conditions.
5. Generate a customer email or manager note.
6. Update the session's triage log.

### Step 4: Review the Result

The interface displays:

* Exception category.
* Shipment value.
* Calculated compensation.
* Escalation status and reason.
* Generated message.
* Individual processing steps.

### Step 5: Review the Daily Summary

Click **Generate Daily Summary** to see aggregated statistics for the current application session.

---

## 💰 Compensation and Escalation Rules

The following values are illustrative defaults in the example implementation. They are not verified Northwind Logistics policies.

### Compensation Rules

| Exception | Calculation            |        Maximum Compensation |
| --------- | ---------------------- | --------------------------: |
| Delayed   | 5% of shipment value   |                      ₹1,000 |
| Damaged   | 20% of shipment value  |                      ₹5,000 |
| Lost      | 100% of shipment value |                     ₹10,000 |
| Unknown   | Manual review          | ₹0 automatically calculated |

The example calculators use the following formulas:

```python
# Delayed
compensation = min(shipment_value * 0.05, 1000)

# Damaged
compensation = min(shipment_value * 0.20, 5000)

# Lost
compensation = min(shipment_value, 10000)
```

### Escalation Rules

| Customer Tier | Escalation Threshold |
| ------------- | -------------------: |
| Premium       |               ₹2,000 |
| Standard      |               ₹5,000 |

For known categories, the example pipeline escalates when compensation is **strictly greater than** the applicable threshold.

Unknown classifications always escalate, even when compensation is zero.

For production use, replace these illustrative values with the organization's approved policies.

---

## 📊 Daily Triage Summary

The daily summary calculates statistics across all successfully processed exceptions in the current application session.

### Metrics

**Total reports processed**

The number of exceptions recorded in the session.

**Total compensation**

The sum of the calculated compensation amounts for all recorded reports.

**Escalation rate**

$$
\text{Escalation Rate} =
\frac{\text{Escalated Reports}}{\text{Total Reports}}
\times 100
$$

**Compensation by category**

The system adds together compensation amounts for each category.

**Costliest category**

The category with the highest aggregate compensation is identified using the category totals.

For example:

| Category | Compensation Total |
| -------- | -----------------: |
| Delayed  |             ₹1,500 |
| Damaged  |             ₹4,000 |
| Lost     |             ₹3,000 |

In this example, **damaged** is the costliest category because its aggregate compensation is ₹4,000.

The summary is maintained in memory. Restarting the application clears the session records.

---

## 🧪 Testing

The project includes `triage_check.py` to verify the classification and escalation workflow.

Run:

```bash
python triage_check.py
```

The example test suite covers four scenarios:

| Test Case       | Expected Classification | Expected Outcome     |
| --------------- | ----------------------- | -------------------- |
| Mild delay      | Delayed                 | Automatic resolution |
| High-value loss | Lost                    | Escalation           |
| Minor damage    | Damaged                 | Automatic resolution |
| Garbled report  | Unknown                 | Mandatory escalation |

A successful run should report:

```text
Testing: Mild delay
Result: PASS

Testing: High-value loss
Result: PASS

Testing: Minor damage
Result: PASS

Testing: Garbled report
Result: PASS

Final score: 4/4
```

These are the expected results, not a claim that the tests have already been executed successfully.

Because classification uses an LLM, results can vary. If the instructor supplied a specific `triage_check.py`, use that original file and its expected outcomes.

---

## 🔐 Security and Limitations

### API Key Security

Keep API credentials in environment variables. Add `.env` to `.gitignore`.

### LLM Classification

Classification depends on the quality and clarity of the submitted report. Ambiguous reports should be routed to a human rather than handled automatically.

### Session Storage

The current implementation stores records in application memory. Data is lost when the application process restarts.

### Human Review

Escalation generates an internal note but does not automatically notify a manager or create a ticket in an external system.

### Compensation Policy

The example compensation rates and thresholds must be replaced with the approved policy before the application is used operationally.

### Operational Use

The application is a learning project and demonstration of an LLM-assisted workflow. Production deployment would require additional validation, persistence, monitoring, access controls, and operational safeguards.

---

## 🔮 Future Improvements

Potential extensions include:

* Persistent storage using SQLite or PostgreSQL.
* Daily and monthly historical reporting.
* Exporting triage records to CSV.
* Manager approval and resolution tracking.
* Integration with ticketing or logistics systems.
* Authentication and role-based access control.
* Unit tests for compensation calculations and escalation boundaries.
* Mocked LLM outputs for deterministic pipeline testing.
* Improved error handling and retry logic for API failures.

These features are not required by the current implementation.

---

## 🎯 Learning Outcomes

This project demonstrates practical use of:

* LangChain prompt–model–parser patterns.
* Structured LLM outputs with Pydantic.
* Python functions and conditional branching.
* Separation of LLM tasks from deterministic business logic.
* Workflow orchestration without a graph framework.
* Session-based state management and aggregation.
* Gradio-based interface development.
* Environment variables and API credential management.
* Testing of classification and escalation behavior.

---

## 📄 License

Choose a license appropriate for your project before publishing the repository. For an open-source project, consider the MIT License if its terms fit your intended use.

---

## 👨‍💻 Author

**Aishwary Bajpai**

Built as a hands-on project exploring LangChain, LLM integration, Python business logic, and interactive application development.

---

**Shipment Exception Desk — Turning shipment exception reports into structured, explainable decisions.**


## 🎥 Project Demo

Watch the Shipment Exception Desk in action, demonstrating all four test cases and the Daily Triage Summary.

**The demo covers:**

* 📦 Mild delay — automatic resolution
* 🚚 High-value loss — escalation for human review
* 📦 Minor damage — compensation calculation
* 📊 Daily Triage Summary — aggregate compensation and escalation rate

### Watch the Demo

[▶️ Watch Shipment Exception Desk Demo](https://youtu.be/wE1yufUALlg)
