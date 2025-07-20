from cv_model import CVUpload, session

records = session.query(CVUpload).all()

print("📄 Uploaded CVs:")
for record in records:
    print(f"🆔 ID: {record.id}")
    print(f"📁 Filename: {record.filename}")
    print(f"📍 Path: {record.filepath}")
    print(f"⏰ Uploaded at: {record.upload_time}")
    print("—" * 40)
