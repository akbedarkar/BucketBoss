# **BucketBoss**  
*Your AI-powered shift planner & task prioritizer*  

---

## 📌 Overview  
**BucketBoss** is a **demo AI assistant** built with **LangGraph** and **Microsoft Semantic Kernel** that:  
- Greets the user when they start their shift.  
- Loads tasks into a “bucket” (sample list or real source).  
- Suggests **priority levels (P1, P2, P3)** automatically based on task content.  
- Lets the user confirm or adjust priorities interactively.  

Perfect for showcasing **AI-powered productivity** in a simple, easy-to-run Python project.  

---

## ✨ Features  
- **Friendly welcome message** personalized for the user.  
- Loads a **sample task list** (can be replaced with Jira/API data).  
- Uses **Semantic Kernel** for automatic prioritization.  
- Interactive step for manual priority adjustment.  
- Modular code design for easy extension.  

---

## 🧱 Tech Stack  
- **Python** 3.10+  
- [**LangGraph**](https://python.langchain.com/docs/langgraph) — to define the AI workflow.  
- [**Microsoft Semantic Kernel**](https://github.com/microsoft/semantic-kernel) — for task prioritization logic.  

---

## 📂 Project Structure  
```
BucketBoss/
│
├── Task.py              # Main application file
├── .gitignore           # Ignored files/folders for Git
└── README.md            # Documentation
```

---

## ⚙️ Setup & Installation  

### **1️⃣ Clone the repository**
```bash
git clone https://github.com/<your-username>/BucketBoss.git
cd BucketBoss
```

### **2️⃣ Create a virtual environment**
```bash
python -m venv .venv
source .venv/bin/activate       # macOS/Linux
.\.venv\Scripts\activate        # Windows
```

## ▶️ Run the Demo
```bash
python Task.py
```

---

## 📌 Example Output  
```
Enter your name: Akshata

👋 Hi Akshata! Good morning — looks like a busy day.
📋 Task Priyanka added to your bucket:
– Resolve client escalation on Firefighter
– Fix Sales360 development issue
– Review PR #104
– Update onboarding status
– Start with BI Migration activity

🧠 Suggested priority:
P1:
• Resolve client escalation on Firefighter

P2:
• Fix Sales360 development issue
• Review PR #104

P3:
• Update onboarding status
• Start with BI Migration activity

👉 Pick P1 and P2 (comma-separated) or press Enter for defaults:
```

---

## 🔍 How It Works  

1. **Workflow (LangGraph)** defines the steps:  
   - `greet` → Welcomes the user.  
   - `load` → Loads sample tasks into the bucket.  
   - `prioritize` → Uses Semantic Kernel to classify tasks.  

2. **Semantic Kernel Plugin**:  
   - A simple rule-based classifier (demo) assigns P1/P2/P3.  
   - Can be swapped for AI model calls for smarter prioritization.  

3. **User Interaction**:  
   - User confirms or overrides suggested P1/P2.  
   - All remaining tasks default to P3.  

---

## 🛠 Customization  
- Change task list in `load_tasks()` function.  
- Modify priority rules in `TaskPlugin`.  
- Integrate with Jira, GitHub Issues, or email for real tasks.  
- Export daily plan to Slack, Teams, or email.  

---

## 📌 Roadmap  
- [ ] Integrate with Slack for daily task updates.  
- [ ] Store plans in a database.  
- [ ] Add natural language task entry.  
- [ ] Include motivational messages.  

---

## 📝 License  
This project is licensed under the **MIT License**.  
