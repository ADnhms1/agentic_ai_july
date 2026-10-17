# IncidentAgent: analyze -> create issue -> run
class IncidentAgent:
    def __init__(self):
        self.issues = []
        self.next_id = 1001
    
    def analyze(self, service, error_rate):
        severity = "critical" if error_rate >= 40 else "high"

        return {
            "service": service,
            "error_rate": error_rate,
            "severity": severity
        }

    def create_issue(self, analysis):
        issue_id = self.next_id
        self.next_id += 1

        issue = {
            "id": issue_id,
            "title": (
                f"[{analysis['severity'].upper()}] "
                f"{analysis["service"]} outage"
            ),
            "body": (
                f"Observed error rate: "
                f"{analysis['error_rate']}%"
            ),
            "url": f"https://github.example/issues/{issue_id}"
        }

        self.issues.append(issue)

        return {
            "success": True,
            "issue_id": issue_id,
            "url": issue["url"]
        }

    def run(self, service, error_rate):
        state = {
            "github_draft": None,
            "github_issue_url": None
        }

        analysis = self.analyze(service, error_rate)

        if analysis["severity"] not in ("high", "critical"):
            return {
                "success": True,
                "action": "skipped",
                "reason": "Severity below threshold"
            }

        state["github_draft"] = {
            "title": (
                f"[{analysis['severity'].upper()}] "
                f"{service} outage"
            ),
            "body": f"Error rate: {error_rate}%"
        }
        
        result = self.create_issue(analysis)

        if result["success"]:
            state["github_issue_url"] = result["url"]

        return {
            "analysis": analysis,
            "state": state,
            "customer_response": (
                f"We detected an incident affecting {service}. "
                f"Engineering tracking link : {state['github_issue_url']}"
            )
        }

agent = IncidentAgent()

result = agent.run(service="checkout-api", error_rate = 42)

print("Final workflow result : ")
print(result)