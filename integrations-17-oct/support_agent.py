# HelpdeskAPI: to handle to the ticket management
class HelpdeskAPI:
    def __init__(self):
        self.tickets = []
        self.next_id = 1

    def create_ticket(self, customer, subject, description, priority):
        ticket = {
            "id": self.next_id,
            "customer": customer,
            "subject": subject,
            "description": description,
            "priority": priority,
            "status": "open"
        }

        self.tickets.append(ticket)
        self.next_id += 1

        return {
            "success": True,
            "ticket_id": ticket["id"],
            "status": ticket["status"]
        }


# support agent: customer info and message, create a ticket using the info

def support_agent(customer, message):
    print("Analyzing customer complaint...")

    subject = "Duplicate premium payment"
    priority = "high"

    api = HelpdeskAPI()

    result = api.create_ticket(
        customer=customer,
        subject=subject,
        description=message,
        priority=priority
    )

    if result["success"]:
        print(f"Ticket created : #{result['ticket_id']}")
        print(f"Status: {result['status']}")
        print("Customer response: Your complaint has been registered")
    else:
        print("Ticket creation is failed!")

    print("\n Tickets stored in the helpdesk.")
    for ticket in api.tickets:
        print(ticket)

    
support_agent(customer="Aarav shah", message="My insurance premium was deducted twice.")