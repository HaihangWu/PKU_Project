import zipfile
import pathlib

folder=pathlib.Path("/root/autodl-tmp/data/7 scenes/pumpkin/")

for zip_path in folder.glob("*.zip"):
    print(f"Extracting {zip_path} -> {folder}")
    try:
        with zipfile.ZipFile(zip_path, 'r') as zf:
            for member in zf.namelist():
                try:
                    zf.extract(member, folder)
                except zipfile.BadZipFile:
                    # If it's a Thumbs.db causing the CRC error, delete it
                    if member.endswith("Thumbs.db"):
                        thumbs_path = folder / member
                        if thumbs_path.exists():
                            thumbs_path.unlink()
                            print(f"Deleted corrupted file: {thumbs_path}")
                    else:
                        print(f"Skipped corrupted file: {member}")

    except zipfile.BadZipFile:
        print(f"Skipped corrupted archive: {zip_path}")

    # Remove the zip file after processing
    try:
        zip_path.unlink()
        print(f"Deleted zip archive: {zip_path}")
    except Exception as e:
        print(f"Failed to delete {zip_path}: {e}")