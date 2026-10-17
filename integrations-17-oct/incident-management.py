# EngineeringAPI: allow us to create and issue.
class EngineeringAPI:
    def __init__(self):
        self.issues = []
        self.next_id = 101
    
    def create_issue(self, title, body, labels):
        issue = {
            "id": self.next_id,
            "title": title,
            "body": body,
            "labels": labels,
            "url": f"https://www.github.example/acme/app/issues/{self.next_id}"
        }

        self.issues.append(issue)
        self.next_id += 1

        return {
            "success": True,
            "issue_id": issue["id"],
            "url": issue["url"]
        }

# function analayze incident, this will be responsible for analyzing the issue and then create that issue.

def analyze_incident(alert):
    print("Analyzing monitoring alert...")

    if alert["error_rate"] < 20:
        return {
            "action": "skip",
            "reason": "Error rate is below threshold"
        }

    api = EngineeringAPI()

    result = api.create_issue(
        title=f"[CRITICAL] {alert["service"]} error rate is high",
        body=(
            f"Service: {alert['service']}\n"
            f"Error rate: {alert['error_rate']}%\n"
            f"Investigate immediately"
        ),
        labels=["incident", "automated"]
    )

    return result

alert = {
    "service": "checkout-api",
    "error_rate": 18
}

result = analyze_incident(alert)
print("Final result:", result)