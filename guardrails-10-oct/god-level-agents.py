tools = [
    "check_payment",
    "issue_refund",
    "check_fraud_signals",
    "reset_password",
    "search_knowledge_base",
    "create_github_issue",
    "deploy_application",
    "check_inventory",
]


def god_agent(request):
    print("Request received:", request)
    print("Available tools:", tools)
    print("Problem: every request recieves the same tool list!")


god_agent("Please check the payment status for order #12345.")
god_agent("I need to issue a refund for order #67890.")
god_agent("Can you check for any fraud signals on my account?")