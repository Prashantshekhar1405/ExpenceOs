import re
from datetime import datetime


def extract_amount(text):

    patterns = [
        r"(?:total|grand total|amount payable)\s*[:\-]?\s*[₹$]?\s*([\d,]+(?:\.\d{1,2})?)",
        r"[₹$]\s*([\d,]+(?:\.\d{1,2})?)"
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:
            return match.group(1).replace(",", "")

    return None

def extract_merchant(text):

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    if not lines:
        return None

    return lines[0]

def extract_date(text):

    patterns = [
        r"\b(\d{2}[/-]\d{2}[/-]\d{4})\b",
        r"\b(\d{4}[/-]\d{2}[/-]\d{2})\b"
    ]

    for pattern in patterns:

        match = re.search(pattern, text)

        if match:
            return match.group(1)

    return None

def parse_date(date_string):
    if not date_string:
        return None
    
    formats = [
        "%d/%m/%Y",
        "%d-%m-%Y",
        "%Y/%m/%d",
        "%Y-%m-%d",
    ]
    for date_format in formats:
        try:
            return datetime.strptime(
                date_string,
                date_format
            ).date()

        except ValueError:
            continue

    return None

def extract_tax_amount(text):

    patterns = [
        # GST / Tax / VAT / Sales Tax
        r"(?:gst|tax|vat|sales\s*tax)\s*[:\-]?\s*[₹$]?\s*([\d,]+(?:\.\d{1,2})?)",

        # CGST / SGST / IGST
        r"(?:cgst|sgst|igst)\s*[:\-]?\s*[₹$]?\s*([\d,]+(?:\.\d{1,2})?)",
    ]

    for pattern in patterns:

        matches = re.findall(
            pattern,
            text,
            re.IGNORECASE
        )

        if matches:
            # If there are multiple taxes such as
            # CGST + SGST, add them together.
            total_tax = sum(
                float(amount.replace(",", ""))
                for amount in matches
            )

            return total_tax

    return None

def extract_invoice_number(text):

    patterns = [
        r"(?:invoice\s*(?:no|number|#)?|inv\s*(?:no|#)?)\s*[:\-]?\s*([A-Z0-9][A-Z0-9\-/]*)",
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:
            return match.group(1)

    return None

def parse_receipt(text):

    return {
        "merchant": extract_merchant(text),
        "receipt_amount": extract_amount(text),
        "receipt_date": parse_date(extract_date(text)),
        "tax_amount": extract_tax_amount(text),
        "invoice_number": extract_invoice_number(text),
    }