"""
GLiNER2 base-v1 — JSON structured extraction demo
Model: fastino/gliner2-base-v1
Requires: pip install gliner2[local]
"""

import json
from gliner2 import GLiNER2

# ---------------------------------------------------------------------------
# Load model (downloads on first run, cached afterward)
# ---------------------------------------------------------------------------
extractor = GLiNER2.from_pretrained("fastino/gliner2-base-v1")

# ---------------------------------------------------------------------------
# Sample texts
# ---------------------------------------------------------------------------
NEWS_TEXT = (
    "Apple CEO Tim Cook unveiled the iPhone 16 Pro for $999 at the Steve Jobs "
    "Theater in Cupertino on September 9, 2024."
)

INVOICE_TEXT = (
    "Invoice #INV-2024-0891 from Acme Corp to DataSystems Ltd. "
    "Amount due: $14,500.00. Due date: 2024-08-15. "
    "Line items: Cloud hosting x3 months @ $3,500, Professional services @ $4,000."
)

MEDICAL_TEXT = (
    "Patient: John Doe, 45. Presenting symptoms: chest pain, shortness of breath. "
    "Prescribed: Aspirin 100mg daily, Atorvastatin 20mg nightly. "
    "Follow-up in 2 weeks with Dr. Sarah Miller at City General Hospital."
)

# # ---------------------------------------------------------------------------
# # 1. Named Entity Recognition — returns JSON-serialisable dict
# # ---------------------------------------------------------------------------
# print("=" * 60)
# print("1. NAMED ENTITY RECOGNITION")
# print("=" * 60)

# ner_result = extractor.extract_entities(
#     NEWS_TEXT,
#     {
#         "person":   "Full name of a person or executive",
#         "company":  "Company or organisation name",
#         "product":  "Product or service name",
#         "location": "City, venue, or geographic place",
#         "price":    "Monetary amount or price",
#         "date":     "Specific date or time reference",
#     },
#     include_confidence=True,
#     include_spans=True,
# )

# print(json.dumps(ner_result, indent=2))

# ---------------------------------------------------------------------------
# 2. Structured Data Extraction (extract_json) — invoice
# ---------------------------------------------------------------------------
print("\n" + "=" * 60)
print("2. STRUCTURED DATA EXTRACTION — INVOICE")
print("=" * 60)

invoice_result = extractor.extract_json(
    INVOICE_TEXT,
    {
        "response": [
            "title::str::Full product name and model",
            "storage::str::Storage capacity",
            "processor::str::Chip or processor information",
            "price::str::Product price with currency"
        ]
    },
    # include_confidence=True,
)

print(json.dumps(invoice_result, indent=2))

# # ---------------------------------------------------------------------------
# # 3. Structured Data Extraction — medical record
# # ---------------------------------------------------------------------------
# print("\n" + "=" * 60)
# print("3. STRUCTURED DATA EXTRACTION — MEDICAL RECORD")
# print("=" * 60)

# medical_result = extractor.extract_json(
#     MEDICAL_TEXT,
#     {
#         "patient_info": [
#             "name::str::Patient full name",
#             "age::str::Patient age",
#             "symptoms::list::Reported symptoms or complaints",
#         ],
#         "prescriptions": [
#             "medication::str::Drug or medication name",
#             "dosage::str::Dosage amount",
#             "frequency::str::How often to take the medication",
#         ],
#         "follow_up": [
#             "timeframe::str::When the follow-up is scheduled",
#             "doctor::str::Attending physician name",
#             "facility::str::Hospital or clinic name",
#         ],
#     },
# )

# print(json.dumps(medical_result, indent=2))

# # ---------------------------------------------------------------------------
# # 4. Multi-task schema: entities + classification + relations
# # ---------------------------------------------------------------------------
# print("\n" + "=" * 60)
# print("4. MULTI-TASK SCHEMA (entities + classification + relations)")
# print("=" * 60)

# schema = (
#     extractor.create_schema()
#     .entities(
#         {
#             "person":   "Names of people or executives",
#             "company":  "Organisation or corporation names",
#             "product":  "Products or services mentioned",
#             "location": "Geographic locations",
#         }
#     )
#     .classification("sentiment", ["positive", "negative", "neutral"])
#     .classification(
#         "category",
#         ["technology", "business", "finance", "healthcare"],
#     )
#     .relations(
#         {
#             "works_for":   "Employment — person works at organisation",
#             "located_in":  "Geographic — entity is in a location",
#             "announced":   "Announcement — person or company announced product",
#         }
#     )
# )

# multi_result = extractor.extract(NEWS_TEXT, schema, include_confidence=True)
# print(json.dumps(multi_result, indent=2))

# # ---------------------------------------------------------------------------
# # 5. Batch entity extraction
# # ---------------------------------------------------------------------------
# print("\n" + "=" * 60)
# print("5. BATCH ENTITY EXTRACTION")
# print("=" * 60)

# batch_texts = [NEWS_TEXT, INVOICE_TEXT, MEDICAL_TEXT]
# batch_results = extractor.batch_extract_entities(
#     batch_texts,
#     ["person", "company", "product", "location", "date"],
#     batch_size=4,
# )

# for idx, result in enumerate(batch_results, start=1):
#     print(f"\n--- Text {idx} ---")
#     print(json.dumps(result, indent=2))
