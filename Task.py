from typing import TypedDict, List
import asyncio

from semantic_kernel import Kernel
from semantic_kernel.functions import kernel_function
from langgraph.graph import StateGraph


# ----------------------------
# 1) State schema (required by LangGraph)
# ----------------------------
class TaskState(TypedDict):
    user: str
    tasks: str

# ----------------------------
# 2) Semantic Kernel plugin (new API)
# ----------------------------
class TaskPlugin:
    @kernel_function(name="prioritize_tasks", description="Classify tasks into P1/P2/P3")
    def prioritize_tasks(self, tasks: str) -> str:
        """
        Input: semicolon-separated tasks
        Heuristic:
          - P1: contains 'client', 'escalation', 'prod'
          - P2: contains 'bug', 'review', 'sla'
          - Else: P3
        Output: human-readable text block
        """
        P = {"P1": [], "P2": [], "P3": []}
        for raw in [t.strip() for t in tasks.split(";") if t.strip()]:
            t = raw.lower()
            if "client" in t or "escalation" in t or "prod" in t:
                P["P1"].append(raw)
            elif "bug" in t or "review" in t or "sla" in t:
                P["P2"].append(raw)
            else:
                P["P3"].append(raw)

        def block(k): return f"\n{k}:\n" + "\n".join(f"• {x}" for x in P[k]) if P[k] else ""
        return (block("P1") + block("P2") + block("P3")).lstrip() or "No tasks."


# ----------------------------
# 3) Helper (local) — for interactive selection
# ----------------------------
def classify_local(tasks_list: List[str]):
    P = {"P1": [], "P2": [], "P3": []}
    for raw in tasks_list:
        t = raw.lower()
        if any(k in t for k in ["client", "escalation", "prod"]):
            P["P1"].append(raw)
        elif any(k in t for k in ["bug", "review", "sla"]):
            P["P2"].append(raw)
        else:
            P["P3"].append(raw)
    return P


# ----------------------------
# 4) Nodes
# ----------------------------
def greet(state: TaskState):
    user = state.get("user", "there")
    print(f"\n Hi {user}! Good morning — looks like a busy day.")
    return state


def load_tasks(state: TaskState):
    sample = [
        "Resolve client escalation on Firefighter",
        "Fix Sales360 development bug",
        "Review PR #23",
        "provision new cluster in production",
        "Close BI Migration activity",
    ]
    print("Task Priyanka added to your bucket:")
    for t in sample:
        print("–", t)
    state["tasks"] = "; ".join(sample)
    return state


async def prioritize(state: TaskState):
    # 1) Ask SK to propose priorities (async call; result is FunctionResult)
    result = await kernel.invoke(task_plugin["prioritize_tasks"], tasks=state["tasks"])
    suggested_text = getattr(result, "value", str(result))
    print("\n Suggested priority (SK):\n" + suggested_text)

    # 2) Show a numbered list & let user pick P1 and P2; rest auto P3
    tasks_list = [t.strip() for t in state["tasks"].split(";") if t.strip()]
    print("\n  Your tasks (choose P1 and P2 by number, comma-separated):")
    for i, t in enumerate(tasks_list, start=1):
        print(f"  {i}. {t}")

    # Defaults from heuristic if user hits Enter
    P = classify_local(tasks_list)
    default_p1 = P["P1"][0] if P["P1"] else tasks_list[0] if tasks_list else ""
    # pick a P2 default that's not the same as default P1
    default_p2 = None
    for t in (P["P2"] + tasks_list):
        if t and t != default_p1:
            default_p2 = t
            break

    raw = input(
        f"\n Pick P1,P2 (e.g., 1,2). Press Enter for defaults "
        f"[P1='{default_p1 or '-'}', P2='{default_p2 or '-'}']: "
    ).strip()

    if raw:
        try:
            chosen = [int(x) for x in raw.split(",") if x.strip()]
            p1 = tasks_list[chosen[0] - 1] if len(chosen) >= 1 else default_p1
            p2 = tasks_list[chosen[1] - 1] if len(chosen) >= 2 else default_p2
        except Exception:
            print(" Invalid input. Using defaults.")
            p1, p2 = default_p1, default_p2
    else:
        p1, p2 = default_p1, default_p2

    # Build final assignment: P1, P2, rest P3
    final_p1 = p1 if p1 else ""
    final_p2 = p2 if p2 else ""
    final_p3 = [t for t in tasks_list if t not in {final_p1, final_p2}]

    print("\nFinal plan for today:")
    if final_p1:
        print(f"  P1: {final_p1}")
    if final_p2:
        print(f"  P2: {final_p2}")
    if final_p3:
        print("  P3:")
        for t in final_p3:
            print(f"   • {t}")

    return state


# ----------------------------
# 5) Wire up SK + LangGraph
# ----------------------------
kernel = Kernel()
task_plugin = kernel.add_plugin(TaskPlugin(), plugin_name="task")

g = StateGraph(TaskState)          # pass the schema (required)
g.add_node("greet", greet)
g.add_node("load", load_tasks)
g.add_node("prioritize", prioritize)  # async node is fine
g.set_entry_point("greet")
g.add_edge("greet", "load")
g.add_edge("load", "prioritize")
graph = g.compile()


# ----------------------------
# 6) Run
# ----------------------------
if __name__ == "__main__":
    username = input("Enter your name: ") or "Akshata"
    asyncio.run(graph.ainvoke({"user": username, "tasks": ""}))
