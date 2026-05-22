import os
import uuid
from supabase import create_client

SUPABASE_URL = "https://puozzecgmmenqeuhxmjr.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InB1b3p6ZWNnbW1lbnFldWh4bWpyIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MTgzODEyMSwiZXhwIjoyMDg3NDE0MTIxfQ.ivlRjzgv_O08XNVcZkD6EjnDsZnyk8kSkLlactLuX5k"   # IMPORTANT: service role key

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

BUCKET_NAME = "receipts"

def upload_receipt(file):
    file_content = file.read()

    # Prevent file overwrite
    unique_filename = f"{uuid.uuid4()}_{file.name}"
    path = f"{unique_filename}"

    supabase.storage.from_(BUCKET_NAME).upload(
        path,
        file_content,
        file_options={"content-type": file.content_type}
    )

    public_url = supabase.storage.from_(BUCKET_NAME).get_public_url(path)

    return public_url