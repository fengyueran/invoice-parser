import re
import pdfplumber
import os
import pandas as pd

PATTERNS = {
    '票号': re.compile(r'\d{10}'),
    '案号': re.compile(r'\(\d{4}\)[\u4e00-\u9fa5]{1,3}\d{4}.*\d+号'),
    '费用': re.compile(r'费 .*? ([\d,]+\.\d{2})'),
    '开票日期': re.compile(r'\b\d{4}-\d{2}-\d{2}\b'),
}

DEFAULT_NO_MATCH = '未匹配到'


def extract_data_from_page(text, patterns=PATTERNS, no_match_default=DEFAULT_NO_MATCH):
    result = {}
    for key, pattern in patterns.items():
        matches = pattern.findall(text) if text else []
        if not matches:
            result[key] = no_match_default
        elif len(matches) > 1:
            result[key] = '; '.join(matches)
        else:
            result[key] = matches[0]
    return result


def extract_data_from_pdf(pdf_file_path, patterns=PATTERNS, no_match_default=DEFAULT_NO_MATCH):
    results = {key: [] for key in patterns}
    try:
        with pdfplumber.open(pdf_file_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                page_data = extract_data_from_page(text, patterns, no_match_default)
                for key, value in page_data.items():
                    results[key].append(value)
    except Exception as e:
        print(f"Error processing file {pdf_file_path}: {e}")
        for key in patterns:
            results[key].append(no_match_default)
    return results


def extract_from_directory(directory_path, patterns=PATTERNS, no_match_default=DEFAULT_NO_MATCH):
    all_data = {
        '文件': [],
        '票号': [],
        '案号': [],
        '费用': [],
        '开票日期': []
    }

    for filename in os.listdir(directory_path):
        if filename.lower().endswith('.pdf'):
            pdf_file_path = os.path.join(directory_path, filename)
            print(f"Processing file: {filename}")
            pdf_data = extract_data_from_pdf(pdf_file_path, patterns, no_match_default)
            all_data['文件'].append(filename)
            for key in patterns:
                all_data[key].append('; '.join(pdf_data[key]))
    return all_data


def save_to_excel(data, output_file):
    df = pd.DataFrame(data)
    df.to_excel(output_file, index=False)
    print(f"Data saved to {output_file}")


directory_path = './pdfs'
output_file = 'output.xlsx'

all_data = extract_from_directory(directory_path)

print(f"all_data: {all_data}")

save_to_excel(all_data, output_file)