# Issue tracker, create_issue

class IssueTracker:
    def __init__(self):
        self.issues = []
    
    def create_issue(self, title, severity):
        issue = {
            "id": len(self.issues) + 1,
            "title": title,
            "severity": severity
        }

        self.issues.append(issue)

        return {
            "success": True,
            "issue": issue
        }

# function processing the issue
def process_alert(alert, tracker):
    if alert["severity"] not in ("high", "critical"):
        return {
            "success": False,
            "action": "skipped",
            "reason": "Severity is too low"
        }

    return tracker.create_issue(title=alert["title"], severity=alert["severity"])

tracker = IssueTracker()

alerts = [
    {"title": "Minor image loading delay", "severity": "low"},
    {"title": "Payment latency is increased", "severity": "high"},
    {"title": "Checkout unavailable", "severity": "critical"}
]

for alert in alerts:
    result = process_alert(alert, tracker)
    print(alert["severity"], " -> ", result)

print("\nTotal issues created : ", len(tracker.issues))