class IncidentWorkflow:
    def __init__(self):
        self.created_issues = []

    def run(self, service, severity, finding):
        state = {
            "service": service,
            "severity": severity,
            "finding": finding,
            "github_draft": None,
            "github_issue_url": None
        }

        if severity not in ("high", "critical"):
            return {
                "success": True,
                "action": "no_write",
                "state": state,
                "response": (
                    f"We reviewed the {service} alert. "
                    "No engineering issue was needed."
                )
            }
        
        draft = {
            "title": f"[{severity.upper()}] {service} incident",
            "body": finding
        }

        issue_id = len(self.created_issues) + 1
        url = f"https://github.example/issues/{issue_id}"

        self.created_issues.append({
            **draft,
            "url": url
        })

        state["github_draft"] = draft
        state["github_issue_url"] = url

        return {
            "success": True,
            "action": "issue_created",
            "state": state,
            "response": f"Engineering issue : {url}"
        }

workflow = IncidentWorkflow()

for severity in ("low", "high", "critical"):
    result = workflow.run(
        service="search-api",
        severity=severity,
        finding="Request latency execeeded the normal baseline"
    )

    print(f"\nSeverity : {severity}")
    print("Action : ", result["action"])
    print("Response : ", result["response"])

print("\nTotal issues : ", len(workflow.created_issues))