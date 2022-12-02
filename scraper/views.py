from django.shortcuts import redirect, render
from django.contrib import messages
from docx import Document
import json


# Create your views here.

def scraper(request):
    files = request.FILES.getlist('filename')
    dic = {}
    lesson_number = 0
    screen_number = 0

    cards = [
        'READING', 'True or False',
        'WRITING',
        'Fill the gap',
        'Video block',
        'REFLECT',
        'Download block ',
        'HINT/SUPPORT',
        'OPINION',
        'GLOSSARY',
        'CASE STUDY',
        'ANSWER',
        'Sortable into Columns',
        'Thought Shower',
        'EXTENSION',
        'SUMMARY',
        'Fill the gaps – Typing',
        'Ranking no correct answer',
    ]
    if request.POST:
        if not files:
            messages.error(request, 'The input is empy, please add a file')
        else:
            document = Document(files[0])
            tables = document.tables
            # code
            dic['code'] = tables[0].rows[0].cells[1].text.lower().replace('.',
                                                                          '-').strip()
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

            for table in tables:
                if 'Language' in table.rows[0].cells[0].text:
                    if "Lesson" in table.rows[1].cells[0].text:

                        dic['lessons'].append(
                            {
                                "title": {
                                    "en": table.rows[1].cells[1].text.strip(),
                                    "cy": table.rows[1].cells[2].text.strip(),
                                },
                                "active": False,
                                "heroImage": "https://resource.download.wjec.co.uk/vtc/2022-23/el22-23_2-6/images/shakespeare-book.png",
                                "progress": 0,
                                "subLessons": []
                            }
                        )

                        lesson_number += 1
                        screen_number = 0
                        # adding screens
                        if "Screen" in table.rows[2].cells[0].text:
                            dic['lessons'][lesson_number - 1]['subLessons'].append(
                                {
                                    "title": {
                                        "en": table.rows[2].cells[1].text,
                                        "cy": '',
                                    },
                                    "slug": "slug",
                                    "cards": []
                                }

                            )
                            screen_number += 1 
                            if table.rows[2].cells[1].text == '':
                                messages.error(request,f'{lesson_number}, {screen_number} is empty,  {table.rows[2].cells[0].text}')

                            

                

                    elif "Screen" in table.rows[1].cells[0].text:
                        dic['lessons'][lesson_number - 1]['subLessons'].append(
                            {
                                "title": {
                                    "en": table.rows[1].cells[1].text,
                                    "cy": '',
                                },
                                "slug": "slug",
                                "cards": []
                            },

                        )
                        screen_number += 1
                        if table.rows[1].cells[1].text == '':
                            messages.error(request,f'{lesson_number}, {screen_number} is empty, {table.rows[1].cells[0].text}')
                        

             # adding reading cards
                if "Static text – READING " in table.rows[0].cells[0].text or 'Static text – LESSON OBJECTIVES' in table.rows[0].cells[0].text:
                    dic['lessons'][lesson_number - 1]['subLessons'][screen_number - 1]['cards'].append(
                        {
                            "type": "read",
                            "data": {
                                "title": {
                                    "en": "",
                                    "cy": ""
                                },
                                "content": {
                                    "en": table.rows[2].cells[0].text,
                                    "cy": table.rows[2].cells[1].text,
                                    "_editorEn": "visual"
                                }
                            },
                            "answer": {
                                "en": "",
                                "cy": ""
                            },
                            "hint": {
                                "en": "",
                                "cy": ""
                            },
                            "extension": {
                                "en": "",
                                "cy": ""
                            },
                            "downloadFiles": []
                        },
                    )

                # adding WRITING cards
                if "WRITING" in table.rows[0].cells[0].text:
                    dic['lessons'][lesson_number - 1]['subLessons'][screen_number - 1]['cards'].append(
                        {
                            "type": "write",
                            "data": {
                                "title": {
                                    "en": "",
                                    "cy": ""
                                },
                                "content": {
                                    "en": table.rows[2].cells[0].text,
                                    "cy": table.rows[2].cells[1].text,
                                    "_editorEn": "visual"
                                }
                            },
                            "answer": {
                                "en": "",
                                "cy": ""
                            },
                            "hint": {
                                "en": "",
                                "cy": ""
                            },
                            "extension": {
                                "en": "",
                                "cy": ""
                            },
                            "downloadFiles": []
                        },
                    )

                # Adding CASE STUDY cards
                if "case study" in table.rows[0].cells[0].text.lower():
                    dic['lessons'][lesson_number - 1]['subLessons'][screen_number - 1]['cards'].append(
                        {
                            "type": "caseStudy",
                            "data": {
                                "title": {
                                    "en": "",
                                    "cy": ""
                                },
                                "content": {
                                    "en": table.rows[2].cells[0].text,
                                    "cy": table.rows[2].cells[1].text,
                                    "_editorEn": "visual"
                                }
                            },
                        },
                    )

                # Adding SPEAKING cards
                if "speaking" in table.rows[0].cells[0].text.lower():
                    dic['lessons'][lesson_number - 1]['subLessons'][screen_number - 1]['cards'].append(
                        {
                            "type": "speaking",
                            "data": {
                                "title": {
                                    "en": "",
                                    "cy": ""
                                },
                                "content": {
                                    "en": table.rows[2].cells[0].text,
                                    "cy": table.rows[2].cells[1].text,
                                    "_editorEn": "visual"
                                }
                            },
                        },
                    )

                # Adding SUMMARY cards
                if "summary" in table.rows[0].cells[0].text.lower():
                    dic['lessons'][lesson_number - 1]['subLessons'][screen_number - 1]['cards'].append(
                        {
                            "type": "summary",
                            "data": {
                                "title": {
                                    "en": "",
                                    "cy": ""
                                },
                                "content": {
                                    "en": table.rows[2].cells[0].text,
                                    "cy": table.rows[2].cells[1].text,
                                    "_editorEn": "visual"
                                }
                            },
                        },
                    )

                # Adding MCQ cards
                if "MCQ" in table.rows[0].cells[0].text:
                    dic['lessons'][lesson_number - 1]['subLessons'][screen_number - 1]['cards'].append(
                        {
                            "type": "mcq",
                            "data": {
                                "title": {
                                    "en": "",
                                    "cy": ""
                                },
                                "content": {
                                    "en": table.rows[2].cells[0].text,
                                    "cy": table.rows[2].cells[1].text,
                                    "_editorEn": "visual"
                                }
                            },
                        },
                    )

                if "Spot the mistake" in table.rows[0].cells[0].text:

                    for i in range(3, len(table.rows)):
            
                        dic['lessons'][lesson_number - 1]['subLessons'][screen_number - 1]['cards'].append(
                            {
                                "type": "spotMistake",
                                "data": {
                                    "title": {
                                        "en": "",
                                        "cy": ""
                                    },
                                    "content": {
                                        "en": "<p>Spot the mistake in the sentence and then insert the correction.</p>",
                                        "cy": "<p>Ceisiwch ddod o hyd i’r camgymeriad yn y frawddeg yna ewch ati i’w chywiro.</p>\n"
                                    },
                                    "question": {
                                        "en": table.rows[i].cells[0].text,
                                        "cy": table.rows[i].cells[2].text,
                                    },
                                    "answer": {
                                        "en": table.rows[i].cells[1].text,
                                        "cy": table.rows[i].cells[1].text,
                                    },
                                    "mistake": {
                                        "en": "Banquo",
                                        "cy": ""
                                    },
                                    "feedback": {
                                        "en": "",
                                        "cy": ""
                                    }
                                },
                                "answer": {
                                    "en": "",
                                    "cy": ""
                                },
                                "hint": {
                                    "en": "",
                                    "cy": ""
                                },
                                "extension": {
                                    "en": "",
                                    "cy": ""
                                },
                                "downloadFiles": []
                            },
                        )
                        print(i)
                    messages.error(request, f'You need to add the Mistake manually in "spot the mistake activity" located in  lesson number: {lesson_number}, and screen {screen_number}' )

            messages.success(request, 'File converted succesfully')
    dic = json.dumps(dic, indent=4)
    context = {'dic': dic}
    return render(request, 'scraper.html', context)
