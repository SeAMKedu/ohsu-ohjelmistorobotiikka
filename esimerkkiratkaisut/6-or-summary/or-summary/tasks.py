from robocorp.tasks import task
from RPA.Excel.Files import Files as Excel
from RPA.Word.Application import Application as Word

@task
def create_summary():
    # Open Excel file and get rows
    excel = Excel()
    excel.open_workbook("./output/challenge.xlsx")
    rows = excel.read_worksheet_as_table("Sheet1", header=True)

    # Parse number of persons and distinct companies
    num_persons, companies = parse_Excel_data(rows)

    # Create Word    
    word = Word()
    word.open_application()

    # Add content to the template and new Woed file
    create_Word_summary(word, num_persons, companies)

def parse_Excel_data(rows) -> tuple:
    num_persons = len(rows)
    companies = []

    for row in rows:
        company = str(row["Company Name"])
        if (company not in companies):
            companies.append(company)
    
    return (num_persons, companies)

def create_Word_summary(word, num_persons, companies):
    word.open_file("./output/template.docx")
    #word.create_new_document()

    companies.sort()
    companies_text = ""
    for company in range(0, len(companies)):
        if (company == 0):
            companies_text = companies[company]
        elif (company == (len(companies) - 1)):
            companies_text = companies_text + ", and " + companies[company]
        else:        
            companies_text = companies_text + ", " + companies[company]


    word.write_text(f"During the follow up period, we have used " + \
                    f"{num_persons} external consultants. They " + \
                    f"represented the following companies: " + \
                    f"{companies_text}.")
    
    #word.save_document_as("./output/summary.docx")
    word.save_document_as("C:/temp/summary.docx")
    word.quit_application()