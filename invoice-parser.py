import re
import pdfplumber

def extract_ticket_and_bill(pdf_file_path):
    tickets = []
    billes = []

    ticket_pattern = re.compile(r'\d{10}')  # 票号：10位数字
    bill_pattern = re.compile(r'\(\d{4}\)[\u4e00-\u9fa5]{1,3}\d{4}.*\d+号')  #(2024)渝0106民初21686号


    no_match_default = ['未匹配到']  

    with pdfplumber.open(pdf_file_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            # print("text:", text)
            if text:
                # 匹配票据号码
                found_tickets = re.findall(ticket_pattern, text)
                if len(found_tickets) == 0:
                    tickets += no_match_default
                elif len(found_tickets) > 1:
                    tickets += ['; '.join(found_tickets)]  
                else:
                    tickets += found_tickets

                # 匹配案号（同样的逻辑应用于案号）
                found_billes = re.findall(bill_pattern, text)
                if len(found_billes) == 0:
                    billes += no_match_default
                elif len(found_billes) > 1:
                    billes += ['; '.join(found_billes)]  
                else:
                    billes += found_billes

    return tickets, billes






import os

def extract_from_multiple_pdfs(directory_path):
    all_pdfs = []
    all_tickets = []
    all_billes = []

    for filename in os.listdir(directory_path):
        if filename.endswith('.pdf') or filename.endswith('.PDF'):
            pdf_file_path = os.path.join(directory_path, filename)
            tickets, billes = extract_ticket_and_bill(pdf_file_path)
            all_pdfs.append(filename)
            all_tickets.extend(tickets)
            all_billes.extend(billes)

    return all_pdfs, all_tickets, all_billes


directory_path = './pdfs'
all_pdfs, all_tickets, all_billes = extract_from_multiple_pdfs(directory_path)

print("所有文件:", all_pdfs)
print("所有票号:", all_tickets)
print("所有案号:", all_billes)

import pandas as pd

def save_to_excel(tickets, billes, output_file):
    df = pd.DataFrame({
        '文件': all_pdfs,
        '票号': tickets,
        '案号': billes
    })
    df.to_excel(output_file, index=False)

save_to_excel(all_tickets, all_billes, 'output.xlsx')