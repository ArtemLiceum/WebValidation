from fastapi import APIRouter, Request
from pydantic import BaseModel
from pymongo.collection import Collection
from typing import Dict
from app.services.field_utils import detect_field_type

router = APIRouter()

db_client = None  # Placeholder for database client, to be initialized externally

def get_templates_collection() -> Collection:
    """Helper to get the MongoDB collection."""
    global db_client
    if db_client is None:
        raise RuntimeError("Database client is not initialized.")
    print("Accessing templates collection...")
    return db_client.form_templates.templates

class Template(BaseModel):
    name: str
    fields: Dict[str, str]

@router.post("/add_template/")
def add_template(template: Template):
    """Add a form template to the database."""
    collection = get_templates_collection()
    print(f"Adding template: {template}")
    collection.insert_one(template.dict())
    return {"message": "Template added successfully."}

@router.post("/get_form/")
async def get_form(request: Request):
    """Get the matching form template or suggest field types."""
    form_data = await request.form()
    form_dict = {key: value for key, value in form_data.items()}
    print(f"Received form data: {form_dict}")
    detected_types = {key: detect_field_type(value) for key, value in form_dict.items()}
    print(f"Detected field types: {detected_types}")

    collection = get_templates_collection()

    # Search for a matching template
    for template in collection.find():
        print(f"Checking template: {template}")
        template_fields = template["fields"]
        if all(
            field_name in form_dict and detect_field_type(form_dict[field_name]) == field_type
            for field_name, field_type in template_fields.items()
        ):
            print(f"Match found: {template['name']}")
            return {"matched_template": template["name"]}

    print("No matching template found.")
    return detected_types
