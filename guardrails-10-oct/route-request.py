def route_request(text):
    text = text.lower()

    if any(word in text for word in ["payment", "refund", "transaction", "invoice"]):
        return "billing"

    if any(word in text for word in ["fraud", "suspicious", "account compromise"]):
        return "fraud"
    
    if any(word in text for word in ["crash", "error", "bug", "issue", "not working"]):
        return "technical_support"

    return "human_support"

print(route_request("Please check the payment status for order #12345."))
print(route_request("I need to issue a refund for order #67890."))