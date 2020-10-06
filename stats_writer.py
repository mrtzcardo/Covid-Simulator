import xlsxwriter

def xlsx_stats(y1, y2, y3, y4):

    workbook = xlsxwriter.Workbook('Covid.xlsx')
    worksheet = workbook.add_worksheet("covid")

    worksheet.write(0, 0, "Infected")
    worksheet.write(0, 1, "Healthy")
    worksheet.write(0, 2, "Recovered")
    worksheet.write(0, 3, "Dead")

    row = 1
    col = 0

    # Iterates over the data and writes it out row by row.
    for value in y1:
        worksheet.write(row, col, value)
        row += 1

    row = 1
    for value in y2:
        worksheet.write(row, col+1, value)
        row += 1

    row = 1
    for value in y3:
        worksheet.write(row, col+2, value)
        row += 1

    row = 1
    for value in y4:
        worksheet.write(row, col+3, value)
        row += 1

    workbook.close()
