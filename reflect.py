import sqlite3
import json
import os
import sys
sys.path.append(r"C:\agent")
from logger import get_recent_actions, get_user_patterns

DB_PATH = r"C:\agent\agent_memory.db"

def reflect():
    print("\n=== SELF REFLECTION STARTED ===\n")

    # Pull recent actions
    actions = get_recent_actions(20)
    patterns = get_user_patterns()

    if not actions:
        print("[INFO] No actions logged yet.")
        return

    # Score performance
    total = len(actions)
    successes = sum(1 for a in actions if a[3] == 1)
    failures = total - successes
    success_rate = (successes / total) * 100

    print(f"Total actions reviewed : {total}")
    print(f"Successful             : {successes}")
    print(f"Failed                 : {failures}")
    print(f"Success rate           : {success_rate:.1f}%")

    # Identify failure patterns
    print("\n--- Failed actions ---")
    failed_actions = [a for a in actions if a[3] == 0]
    if failed_actions:
        for a in failed_actions:
            print(f"  [{a[0]}] {a[1]} → {a[2]}")
    else:
        print("  None! All recent actions succeeded.")

    # Identify most common user patterns
    print("\n--- User behaviour patterns ---")
    if patterns:
        for p in patterns[:5]:
            print(f"  Pattern : {p[0]}")
            print(f"  Count   : {p[1]} times")
            print(f"  Time    : {p[2] or 'varies'}")
            print(f"  Context : {p[3] or 'general'}")
            print()
    else:
        print("  No patterns detected yet.")

    # Save reflection to database
    summary = f"Reviewed {total} actions. Success rate: {success_rate:.1f}%."
    mistakes = "; ".join([a[1] for a in failed_actions]) if failed_actions else "None"
    improvements = "Retry failed actions with different approach." if failures > 0 else "Maintain current performance."

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO reflections (summary, mistakes, improvements, confidence_score)
        VALUES (?, ?, ?, ?)
    ''', (summary, mistakes, improvements, success_rate / 100))
    conn.commit()
    conn.close()

    print("--- Reflection saved to memory ---")
    print(f"Summary      : {summary}")
    print(f"Mistakes     : {mistakes}")
    print(f"Improvements : {improvements}")
    print(f"Confidence   : {success_rate / 100:.2f}")
    print("\n=== REFLECTION COMPLETE ===")

reflect()