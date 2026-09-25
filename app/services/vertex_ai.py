from google import genai
from google.genai.types import HttpOptions, Part

from app.schemas import DocumentAnalysis


PROJECT_ID = "ai-document-intelligence-2026"
LOCATION = "global"


client = genai.Client(
    vertexai=True,
    project=PROJECT_ID,
    location=LOCATION,
    http_options=HttpOptions(api_version="v1"),
)


def analyze_document(pdf_uri: str) -> DocumentAnalysis:

    response = client.models.generate_content(
        model="gemini-2.5-flash",

        contents=[
            Part.from_uri(
                file_uri=pdf_uri,
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

            Return only information that is actually
            present in the document.

            If information is not present,
            return an empty array where appropriate.
            """
        ],

        config={
            "response_mime_type": "application/json",
            "response_schema": DocumentAnalysis,
        },
    )

    return DocumentAnalysis.model_validate_json(
        response.text
    )