def get_payment_status(payment_id: str):
    return f"Payment status for {payment_id}: Pending"

def get_fraud_signals(payment_id: str):
    return f"Fraud signals for {payment_id}: No suspicious activity detected"

def issue_refund(payment_id: str):
    return f"Refund issued for {payment_id}"

billing_tools = {
    "get_payment_status": get_payment_status
}

fraud_tools = {
    "get_fraud_signals": get_fraud_signals
}

def execute_tool(allowed_tools, tool_name, argument):
    if tool_name not in allowed_tools:
        raise PermissionError(f"Tool '{tool_name}' is not allowed for this agent.")
    
    return allowed_tools[tool_name](argument)

print(execute_tool(billing_tools, "get_payment_status", "PAY-12345"))

try:
    execute_tool(billing_tools, "get_fraud_signals", "PAY-12345")
except PermissionError as e:
    print(e)  # Should raise a permission error since fraud tools are not allowed for billing agent