from typing import List

from google import genai
from google.genai.types import HttpOptions, Part
from pydantic import BaseModel


PROJECT_ID = "ai-document-intelligence-2026"
LOCATION = "global"

PDF_URI = "gs://ai-document-intelligence-2026-documents/VIGNESHWARAN_Resume.pdf"


# --------------------------------------------------
# Response schema
# --------------------------------------------------

class DocumentAnalysis(BaseModel):
    title: str
    summary: str
    topics: List[str]
    entities: List[str]
    key_points: List[str]
    dates: List[str]
    important_numbers: List[str]


# --------------------------------------------------
# Vertex AI client
# --------------------------------------------------

client = genai.Client(
    vertexai=True,
    project=PROJECT_ID,
    location=LOCATION,
    http_options=HttpOptions(api_version="v1"),
)


# --------------------------------------------------
# Gemini request
# --------------------------------------------------

response = client.models.generate_content(
    model="gemini-2.5-flash",

    contents=[
        Part.from_uri(
            file_uri=PDF_URI,
            mime_type="application/pdf",
        ),

        """
        Analyze the provided document.

        Extract:

        - Document title
        - Short summary
        - Main topics
        - Important entities
        - Key points
        - Important dates
        - Important numbers

        Return only information that is actually present
        in the document.
        """
    ],

    config={
        "response_mime_type": "application/json",
        "response_schema": DocumentAnalysis,
    },
)


# --------------------------------------------------
# Parse Gemini response
# --------------------------------------------------

analysis = DocumentAnalysis.model_validate_json(response.text)


# --------------------------------------------------
# Display result
# --------------------------------------------------

print("\nDocument Analysis")
print("=================")

print(f"\nTitle:\n{analysis.title}")

print(f"\nSummary:\n{analysis.summary}")

print("\nTopics:")
for topic in analysis.topics:
    print(f"  - {topic}")

print("\nEntities:")
for entity in analysis.entities:
    print(f"  - {entity}")

print("\nKey Points:")
for point in analysis.key_points:
    print(f"  - {point}")

print("\nDates:")
for date in analysis.dates:
    print(f"  - {date}")

print("\nImportant Numbers:")
for number in analysis.important_numbers:
    print(f"  - {number}")