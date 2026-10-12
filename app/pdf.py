from pathlib import Path
import img2pdf # type: ignore
import shutil

def convert_to_pdf(dir: Path, file_name: str)-> None:
   jpg_files = sorted(list(dir.glob("*.jpg")))

   if not jpg_files:
      print(f"No JPG files found in {dir}. Skipping PDF conversion.")
      return
   
   output_pdf = dir.parent / f"{file_name}.pdf"

   with open(output_pdf,"wb") as pdf:
        pdf.write(img2pdf.convert(jpg_files))

   shutil.rmtree(dir)
   print(f"PDF created: {output_pdf}")