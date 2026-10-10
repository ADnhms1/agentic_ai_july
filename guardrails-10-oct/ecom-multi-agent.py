
def extract(orders):
    return [row for row in orders if "price" in row]

def validate(rows):
    return [
        row for row in rows
        if row.get("quantity", 0) > 0 and row.get("price") >= 0
    ]

def report(rows):
    revenue = sum(row["quantity"] * row["price"] for row in rows)
    return {"valid_rows": len(rows), "revenue": revenue}


orders = [
    {"quantity": 2, "price": 500},
    {"quantity": 1, "price": 1000},
    {"quantity": 3, "price": 200},
    {"quantity": 2, "price": 500},
    {"quantity": 1, "price": 0},
    {"quantity": 0, "price": 200},
]

extractedData = extract(orders)
validatedData = validate(extractedData)
reportData = report(validatedData)

print("Report Data:", reportData)