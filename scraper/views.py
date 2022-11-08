from django.shortcuts import redirect, render
from django.contrib import messages
from docx import Document
import json


# Create your views here.

def scraper(request):
   files = request.FILES.getlist('filename')
   dic = {}
   if request.POST:
      if  not files:
         messages.error(request, 'The input is empy, please add a file')
      else:
         document = Document(files[0])
         tables = document.tables
         # code
         dic['code'] = tables[0].rows[0].cells[1].text.lower().replace('.', '-').strip()
         # This project name
         if "|" in tables[0].rows[1].cells[1].text:
            dic['resourceTitle'] = {
               "en": tables[0].rows[1].cells[1].text.split('|')[0].strip(),
               "cy": tables[0].rows[1].cells[1].text.split('|')[1].strip()
            }
         else:
             dic['resourceTitle'] = {
               "en": tables[0].rows[1].cells[1].text.strip(),
               "cy": ''
         }
         # Subject name
         if "|" in tables[0].rows[2].cells[1].text:
            dic['subject'] = {
               "en": tables[0].rows[2].cells[1].text.split('|')[0].strip(),
               "cy": tables[0].rows[2].cells[1].text.split('|')[1].strip()
            }
         else:
             dic['subject'] = {
               "en": tables[0].rows[2].cells[1].text.strip(),
               "cy": ''
         }
         # show bar
         dic['showSidebar'] = True
         # lessons
         dic['lessons'] = []

         for i in tables:
            if 'Language' in i.rows[0].cells[0].text:
               if "Lesson" in i.rows[1].cells[0].text:
                     dic['lessons'].append(
                  {
                     "title": {
                     "en": i.rows[1].cells[1].text.strip(),
                     "cy": i.rows[1].cells[2].text.strip(),
                     },
                     "active": False,
                     "heroImage": "https://resource.download.wjec.co.uk/vtc/2022-23/el22-23_2-6/images/shakespeare-book.png",
                     "progress": 0,
                     "subLessons": []
                  }
               )


         messages.success(request, 'File converted succesfully')
   dic = json.dumps(dic, indent=4)
   context = {'dic':dic}
   return render(request, 'scraper.html', context)

















# def scraper(request):
#    files = request.FILES.getlist('filename')
#    dic = {}
#    if request.POST:
#       if  not files:
#          messages.error(request, 'the input is empy, please add a file')
#       else:
#          document = Document(files[0])
#          tables = document.tables[0]
#          row = tables.rows[0].cells[0].text
#          columns = tables.rows[0].cells[1].text
#          dic[row] = columns
#          messages.success(request, 'file converted succesfully')
#    context = {'dic':dic}
#    return render(request, 'scraper.html', context)



   # def scraper(request):
   # files = request.FILES.getlist('filename')
   # array = {}
   # if request.POST:
   #    if  not files:
   #       messages.error(request, 'the input is empy, please add a file')
   #    else:
   #       document = Document(files[0])
   #       print('paragraphs', document.tables)
   #       for table in document.tables:
   #          for row in table.rows:
   #             for cell in row.cells:
   #                for paragraph in cell.paragraphs:
   #                   array['docs'] = paragraph.text

   #       messages.success(request, 'file converted succesfully')
   # context = {'array':array}
   # return render(request, 'scraper.html', context)



   #  document = Document(files[0])
   #       tables = document.tables[0]
   #       row = tables.rows[0]
   #       column = tables.columns[0]
   #       row_cell = row.cells[0]
   #       row_column = column.cells[0]
   #       row_cell_paragraphs = row_cell.paragraphs[0]
   #       row_column_paragraphs = row_column.paragraphs[0]
   #       text_row_cell_paragraphs = row_cell_paragraphs.text
   #       text_row_column_paragraphs = row_column_paragraphs.text
   #       print(text_row_cell_paragraphs, text_row_column_paragraphs)


   # def scraper(request):
   # files = request.FILES.getlist('filename')
   # array = {}
   # if request.POST:
   #    if  not files:
   #       messages.error(request, 'the input is empy, please add a file')
   #    else:
   #       document = Document(files[0])
   #       tables = document.tables[0]
   #       row = tables.rows[0].cells[0].text
   #       columns = tables.rows[0].cells[1].text
   #       # column = tables.columns[0].cells[1].text
   #       # row_cell = row.cells[0]
   #       # row_column = column.cells[0]
   #       # row_cell_paragraphs = row_cell.paragraphs[0]
   #       # row_column_paragraphs = row_column.paragraphs[0]
   #       # text_row_cell_paragraphs = row_cell_paragraphs.text
   #       # text_row_column_paragraphs = row_column_paragraphs.text
   #       print(row, columns)
   #       # print('text-->', text)
   #       messages.success(request, 'file converted succesfully')
   # return render(request, 'scraper.html')



# "---------------------------------------------------------latest"

# def scraper(request):
#    files = request.FILES.getlist('filename')
#    dic = {}
#    if request.POST:
#       if  not files:
#          messages.error(request, 'the input is empy, please add a file')
#       else:
#          document = Document(files[0])
#          # This is the first table
#          tables = document.tables[0]
#          project_code  = tables.rows[0].cells[1].text
#          project_name  = tables.rows[1].cells[1].text[11:]
#          Subject = tables.rows[2].cells[1].text
#          dic['code'] = project_code
#          dic['resourceTitle'] = {
#             "en":project_name,
#          }
#          dic['Subject'] = {
#             "en":Subject
#          }
#          dic['showSidebar'] = True
#          # This is the second table
#          tables = document.tables[3]
#          Lesson_1 = tables.rows[1].cells[1].text.split("\n")[1]
#          dic['lessons'] = {
#               "title": {
#                   "en": Lesson_1,
#                   "cy": "cy " + Lesson_1,
#                   }
#          }
                
#          messages.success(request, 'file converted succesfully')
#          dic = json.dumps(dic, indent=4)
#    context = {'dic':dic}
#    return render(request, 'scraper.html', context)




# getting the table names 

#   document = Document(files[0])
#          # This is the first table
#          tables = document.tables
#          for i in tables:
#             dic[i.rows[0].cells[0].text] = i.rows[0].cells[0].text





   #  # screens
   #       for i in tables:
   #          if 'Language' in i.rows[0].cells[0].text:
   #             if "Screen" in i.rows[2].cells[0].text:
   #                print("yes")
   #             #       dic['subLessons'].append(
   #             #    {
   #             #       "title": {
   #             #       "en": i.rows[2].cells[1].text.strip(),
   #             #       "cy": i.rows[2].cells[2].text.strip(),
   #             #       },
   #             #    }
   #             # )