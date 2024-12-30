def validate_documents(document_paths):
    # Placeholder KYC validation logic
    for path in document_paths:
        if not path.endswith(('.pdf', '.jpg', '.jpeg', '.png')):
            return {"status": "Failed", "reason": f"Invalid format: {path}"}
    return {"status": "Success"}