import hashlib

class ReliableIncidentAgent:
    def __init__(self):
        self.issue_by_key = {}
        self.tracker_available = False

    def create_issue(self, thread_id, title, body):
        key = hashlib.sha256(f"{thread_id}::{title}::{body}".encode()).hexdigest()

        # check for an already comfirmed result
        if key in self.issue_by_key:
            return {
                "success": True,
                **self.issue_by_key[key],
                "reused_previous_result": True
            }

        if not self.tracker_available:
            return {
                "success": False,
                "error_type": "service is not available",
                "error": "Issue tracker unavailable"
            }

        issue_id = len(self.issue_by_key) + 1

        issue = {
            "issue_id": issue_id,
            "url": f"https://github.example/issues/{issue_id}"
        }

        self.issue_by_key[key] = issue

        return {
            "success": True,
            **issue,
            "reused_previous_result": False
        }

    def run(self, thread_id, service, severity, finding):
        title = f"[{severity.upper()}] {service} incident"
        body = finding

        result = self.create_issue(
            thread_id,
            title,
            body
        )

        if result["success"]:
            return {
                "success": True,
                "issue_url": result["url"],
                "response": (
                    f"The incident is being tracked at "
                    f"{result['url']}"
                )
            }

        return {
            "success": False,
            "error_type": result["error_type"],
            "response": (
                f"We detected an incident affecting {service}. "
                "Automated tracking temporily unavailable",
                "manual engineering follow-up is required"
            )
        }

agent = ReliableIncidentAgent()

arguments = {
    "thread_id": "INC_1200",
    "service": "payment-api",
    "severity": "critical",
    "finding": "The service is returning request HTTP 503 errors."
}

print("ATTEMPT 1 - Tracker available")
print(agent.run(**arguments))

agent.tracker_available = True

print("ATTEMPT 2 - Tracker recovered")
print(agent.run(**arguments))

print("ATTEMPT 3 - Workflow replay")
print(agent.run(**arguments))

print("ATTEMPT 4 - Workflow replay")
print(agent.run(**arguments))


print("ATTEMPT 5 - Workflow replay")
print(agent.run(**arguments))


print("ATTEMPT 6 - Workflow replay")
print(agent.run(**arguments))


print("ATTEMPT 7 - Workflow replay")
print(agent.run(**arguments))

print("ATTEMPT 8 - Workflow replay")
print(agent.run(**arguments))

print("ATTEMPT 9 - Workflow replay")
print(agent.run(**arguments))

print("ATTEMPT 10 - Workflow replay")
print(agent.run(**arguments))

print("\n Confirmed issues stored : ", len(agent.issue_by_key))
