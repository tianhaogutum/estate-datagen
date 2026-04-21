from weasyprint import HTML

# extract wrapped <HTML>...</HTML> tags and convert to PDF
def extract_html_solutions_and_convert_to_pdf(html_content, filepath):
    solutions = []
    start_tag = "<HTML>"
    end_tag = "</HTML>"

    start_index = 0
    while True:
        start_index = html_content.find(start_tag, start_index)
        if start_index == -1:
            break
        end_index = html_content.find(end_tag, start_index)
        if end_index == -1:
            break

        solution_html = html_content[start_index:end_index + len(end_tag)]
        solutions.append(solution_html)

        start_index = end_index + len(end_tag)

    for i, solution in enumerate(solutions):
        convert_html_to_pdf(solution, filepath + f'_{i+1}.pdf')

def convert_html_to_pdf(html_content, pdf_path):
    try:
        HTML(string=html_content).write_pdf(pdf_path)
        print(f"PDF generated and saved at {pdf_path}")
    except Exception as e:
        print(f"PDF generation failed: {e}")