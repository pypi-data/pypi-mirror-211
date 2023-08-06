import pandas as pd
from jinja2 import Environment, FileSystemLoader
import pdfkit
import time
from PyPDF2 import PdfMerger
import math
import os

def generate():
    # Import JSON data from file # to read new added json make changes here
    json_file = r'C:\Users\Jigya\Downloads\New folder\actualData.json'

    with open(json_file, 'r', encoding='utf-8') as file:
        json_text = file.read()

    # Convert JSON to DataFrame
    df = pd.read_json(json_text)

    # Convert DataFrame to list of dictionaries
    data = df.to_dict(orient='records')

    # Load HTML template using Jinja2
    template_file = r'C:\Users\Jigya\Downloads\New folder\template.html'
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template(template_file)

    # Render HTML from the template with dynamic data
    html_content = template.render(data=data)

    html_file = 'output.html'
    with open(html_file, 'w', encoding='utf-8') as file:
        file.write(html_content)
    print(f'Minified HTML file created: {html_file}')

    # Rest of the code...
    start_time = time.time()
    print(start_time)

    # Calculate the total number of lines in the HTML content
    total_lines = len(html_content.split('\n'))
    print(f'Total lines: {total_lines}')

    # Define the number of lines per chunk
    lines_per_chunk = total_lines  # Adjust this value as per your requirement
                    
    # Calculate the number of chunks based on the lines per chunk
    total_chunks = math.ceil(total_lines / lines_per_chunk)
    print(f'Total chunks: {total_chunks}')

    # Generate PDF for each chunk
    pdf_files = []
    for i in range(total_chunks):
        # Calculate the starting and ending line numbers for the current chunk
        start_line = i * lines_per_chunk + 1
        end_line = min((i + 1) * lines_per_chunk, total_lines)

        # Extract the chunk from the HTML content
        chunk = html_content.split('\n')[start_line - 1:end_line]
        chunk_html = '\n'.join(chunk)

        # Configure options for PDF generation (including orientation)
        options = {
            'encoding': 'UTF-8',
            'margin-top': '0px',
            'margin-right': '30px',
            'margin-bottom': '30px',
            'margin-left': '30px',
            'footer-right': "Page [page] of [topage]",
            'footer-font-size': "9",
            'orientation': 'Portrait',
            'page-size': 'A4',
        }

        # Convert HTML chunk to PDF with specified options
        pdf_file = f'output_{i}.pdf'
        pdfkit.from_string(chunk_html, pdf_file, options=options)
        pdf_files.append(pdf_file)

    # Merge the individual PDF files into a single PDF
    merger = PdfMerger()
    for pdf_file in pdf_files:
        merger.append(pdf_file)

    # Output the merged PDF file
    merged_pdf_file = r'C:\Users\Jigya\Downloads\New folder\merged_pdf.pdf'
    merger.write(merged_pdf_file)
    merger.close()

    elapsed_time = time.time() - start_time

    print(f'PDF file created: {merged_pdf_file}')
    print(f'Elapsed time: {elapsed_time / 60} minutes')

    # Delete the individual PDF files (optional)
    for pdf_file in pdf_files:
        os.remove(pdf_file)

generate()