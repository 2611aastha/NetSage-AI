# NetSage AI — Evidence-Backed Network Troubleshooting Dashboard

**Author:** Aastha Deep  
**Roll Number:** 102303283  
**Email:** adeep_be23@thapar.edu  
**Institution:** Thapar Institute of Engineering & Technology  

## Demo Video Link
- **Watch System Walkthrough (Loom):** 
https://www.loom.com/share/48d50e8eb0fa41a4937648d1ebc447e2

---

## 1. Project Overview
NetSage AI is an evidence-backed network diagnostic and decision-support platform designed for Cisco Packet Tracer environments. It pairs a deterministic Layer 1–3 rule verification engine with a structured AI diagnostic pipeline. 

To comply with strict Responsible AI principles:
- The AI acts strictly in an advisory capacity and **never** auto-configures routers or switches.
- Every diagnostic suggestion requires mandatory human operator approval (**Human Review Gate**).
- All operator actions (accept/reject/override) are recorded to an immutable audit trail (`data/audit_log.csv`).

---

## 2. System Architecture & Tech Stack
- **Backend Framework:** FastAPI (Python 3.13)
- **Frontend Dashboard:** React 18, Vite, Tailwind CSS, Lucide React Icons
- **Deterministic Rule Engine:** Python (Regex CLI parser for Cisco `show` commands)
- **Automated Testing:** Pytest
- **Dataset:** 32 pre-configured synthetic network failure scenarios (`data/cases.csv`)

---

## 3. How to Run the Application

### Prerequisites
- **Python:** 3.10 or higher
- **Node.js:** v18 or higher

---

### Step A: Start the Backend API Server (Terminal 1)
Open a terminal in the project root folder (`NetSage-AI`):

```powershell
# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Install Python dependencies (if first time running)
pip install -r requirements.txt

# Launch FastAPI server
python -m uvicorn backend.main:app --reload --port 8000

### Step B: Launch the React Dashboard (Terminal 2)
Open a second terminal tab in VS Code and navigate to the frontend folder:

# Change directory to frontend
cd frontend

# Install Node dependencies (if first time running)
npm install

# Launch Vite development server
npm run dev

### Step C: Execute Automated Unit Tests (Terminal 3)
To verify deterministic rules and rule engine integrity:

# Run from project root directory
pytest tests/

### 4. Key Diagnostic Workflow
Select a synthetic test case (or enter custom Cisco CLI outputs).

Click Run Diagnostics to execute deterministic Layer 1–3 checks.

Review the AI-generated diagnosis and confidence score.

Click Accept Recommendation or Reject / Manual Override to record the decision in the audit log.

Here is how to create the `README.md` file directly in your root directory and the exact contents to put inside it.

---

### Step 1: Create the File in VS Code

1. In VS Code, look at your left Explorer panel at the top root directory (`NetSage-AI`).
2. Click the **New File** icon (or right-click in the empty space below your folders) and name it **`README.md`**.
3. Open `README.md`, paste the content below, and press **`Ctrl + S`** to save.

---

### Step 2: Content for `README.md`

```markdown
# NetSage AI — Evidence-Backed Network Troubleshooting Dashboard

**Author:** Aastha Deep  
**Roll Number:** 102303283  
**Email:** adeep_be23@thapar.edu  
**Institution:** Thapar Institute of Engineering & Technology  

---

## 1. Project Overview
NetSage AI is an evidence-backed network diagnostic and decision-support platform designed for Cisco Packet Tracer environments. It pairs a deterministic Layer 1–3 rule verification engine with a structured AI diagnostic pipeline. 

To comply with strict Responsible AI principles:
- The AI acts strictly in an advisory capacity and **never** auto-configures routers or switches.
- Every diagnostic suggestion requires mandatory human operator approval (**Human Review Gate**).
- All operator actions (accept/reject/override) are recorded to an immutable audit trail (`data/audit_log.csv`).

---

## 2. System Architecture & Tech Stack
- **Backend Framework:** FastAPI (Python 3.13)
- **Frontend Dashboard:** React 18, Vite, Tailwind CSS, Lucide React Icons
- **Deterministic Rule Engine:** Python (Regex CLI parser for Cisco `show` commands)
- **Automated Testing:** Pytest
- **Dataset:** 32 pre-configured synthetic network failure scenarios (`data/cases.csv`)

---

## 3. How to Run the Application

### Prerequisites
- **Python:** 3.10 or higher
- **Node.js:** v18 or higher

---

### Step A: Start the Backend API Server (Terminal 1)
Open a terminal in the project root folder (`NetSage-AI`):

```powershell
# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Install Python dependencies (if first time running)
pip install -r requirements.txt

# Launch FastAPI server
python -m uvicorn backend.main:app --reload --port 8000

```

*Backend server confirmation:* `http://localhost:8000`

---

### Step B: Launch the React Dashboard (Terminal 2)

Open a **second terminal tab** in VS Code and navigate to the frontend folder:

```powershell
# Change directory to frontend
cd frontend

# Install Node dependencies (if first time running)
npm install

# Launch Vite development server
npm run dev

```

*Dashboard UI link:* Open `http://localhost:5173` in your browser.

---

### Step C: Execute Automated Unit Tests (Terminal 3)

To verify deterministic rules and rule engine integrity:

```powershell
# Run from project root directory
pytest tests/

```

---

## 4. Key Diagnostic Workflow

1. Select a synthetic test case (or enter custom Cisco CLI outputs).
2. Click **Run Diagnostics** to execute deterministic Layer 1–3 checks.
3. Review the AI-generated diagnosis and confidence score.
4. Click **Accept Recommendation** or **Reject / Manual Override** to record the decision in the audit log.


---

### Step 3: Update Submission Packages

Once saved, close Word (if open) and run `python package_project.py` in your root PowerShell terminal. This will automatically include the newly created `README.md` inside your final `NetSage_AI_Submission.zip` archive!

