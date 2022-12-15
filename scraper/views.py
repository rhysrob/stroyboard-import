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
                if 'Language'.lower() in table.rows[0].cells[0].text.lower():
                    if "Lesson".lower() in table.rows[1].cells[0].text.lower():
                        try:
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

                            if "Lesson".lower() in table.rows[1].cells[1].text.lower():
                                messages.error(
                                    request, f' Lesson {lesson_number} tile is not correct -> {table.rows[1].cells[1].text}')
                                continue
                        except IndexError:
                            messages.error(
                                request, f'LESSON: {lesson_number}, screen: {screen_number} need to be added')

                        # adding screens
                        if "Screen".lower() in table.rows[2].cells[0].text.lower():
                            try:
                                dic['lessons'][lesson_number - 1]['subLessons'].append(
                                    {
                                        "title": {
                                            "en": table.rows[2].cells[1].text,
                                            "cy": table.rows[2].cells[2].text,
                                        },
                                        "slug": "slug",
                                        "cards": []
                                    }

                                )
                                screen_number += 1
                                if table.rows[2].cells[1].text == '':
                                    messages.error(
                                        request, f'{lesson_number}, {screen_number} is empty,  {table.rows[2].cells[0].text}')
                                continue
                            except IndexError:
                                messages.error(
                                    request, f'Screen in lesson: {lesson_number}, screen: {screen_number} need to be added')

                    elif "Screen".lower() in table.rows[1].cells[0].text.lower():
                        try:
                            dic['lessons'][lesson_number - 1]['subLessons'].append(
                                {
                                    "title": {
                                        "en": table.rows[1].cells[1].text,
                                        "cy": table.rows[1].cells[2].text,
                                    },
                                    "slug": "slug",
                                    "cards": []
                                },

                            )
                            screen_number += 1
                            continue
                        except IndexError:
                            messages.error(
                                request, f'Screen title in lesson: {lesson_number}, screen: {screen_number} need to be added')

                if 'LESSON OBJECTIVES'.lower() in table.rows[0].cells[0].text.lower():
                    try:
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
                        continue
                    except IndexError:
                        messages.error(
                            request, f'LESSON OBJECTIVES card in lesson: {lesson_number}, screen: {screen_number} need to be added ')

                 # adding reading cards
                if "reading".lower() in table.rows[0].cells[0].text.lower():
                    try:
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
                        continue
                    except IndexError:
                        messages.error(
                            request, f' Reading card in Lesson {lesson_number}, Screen {screen_number} need to be added')

                # adding WRITING cards
                if "WRITING".lower() in table.rows[0].cells[0].text.lower():
                    try:
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
                        continue
                    except IndexError:
                        messages.error(
                            request, f'WRITING Card in lesson: {lesson_number}, screen: {screen_number} need to be added')

                # Adding CASE STUDY cards
                if "case study" in table.rows[0].cells[0].text.lower():
                    try:
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
                        continue
                    except IndexError:
                        messages.error(
                            request, f'Case study card in lesson: {lesson_number}, screen: {screen_number} need to be added ')

                # Adding SPEAKING cards
                if "speaking" in table.rows[0].cells[0].text.lower():
                    try:
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
                        continue
                    except IndexError:
                        messages.error(
                            request, f'Speaking card in lesson: {lesson_number}, screen: {screen_number} need to be added ')

                # Adding SUMMARY cards
                if "summary" in table.rows[0].cells[0].text.lower():
                    try:
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
                        continue
                    except IndexError:
                        messages.error(
                            request, f'summary card in lesson: {lesson_number}, screen: {screen_number} need to be added ')

                # Adding MCQ cards
                if "MCQ" in table.rows[0].cells[0].text:
                    try:
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
                        continue
                    except IndexError:
                        messages.error(
                            request, f'MCQ card in lesson: {lesson_number}, screen: {screen_number} need to be added ')

              # Spot the mistake card
                if "Spot the mistake" in table.rows[0].cells[0].text:
                    try:
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
                            messages.error(
                                request, f'You need to add the Mistake manually in "spot the mistake activity" located in  lesson number: {lesson_number}, and screen {screen_number}')
                            continue
                    except IndexError:
                        messages.error(
                            request, f'Spot the mistake card in lesson: {lesson_number}, screen: {screen_number} need to be added ')

                # video card
                if 'Video block' in table.rows[0].cells[0].text:
                    # print(table.rows[2].cells[0].text.split('/')[0].strip())
                    try:
                        dic['lessons'][lesson_number - 1]['subLessons'][screen_number - 1]['cards'].append(
                            {
                                "type": "look",
                                "data": {
                                    "title": {
                                        "en": "",
                                        "cy": ""
                                    },
                                    "content": {
                                        "en": f"\n<div class=\"video-container\"><iframe src=\"https://www.youtube.com/embed/{table.rows[2].cells[0].text}?rel=0&start=0&end=\" allowfullscreen></iframe></div>",
                                        "cy": f"\n<div class=\"video-container\"><iframe src=\"https://www.youtube.com/embed/{table.rows[2].cells[0].text}?rel=0&start=0&end=\" allowfullscreen></iframe></div>",
                                        "_editorEn": "code"
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
                        continue
                    except IndexError:
                        messages.error(
                            request, f'Video block card in lesson: {lesson_number}, screen: {screen_number} need to be addded ')

                # Sortable into Columns
                # ------------------------------------------------------------------------------------------------------ loop through the content
                if 'Sortable into Columns' in table.rows[0].cells[0].text:
                    try:
                        for i in range(3, len(table.rows)):
                            dic['lessons'][lesson_number - 1]['subLessons'][screen_number - 1]['cards'].append(
                                {
                                    "type": "sortableColumns",
                                    "data": {
                                        "title": {
                                            "en": table.rows[2].cells[0].text,
                                            "cy": table.rows[2].cells[1].text,
                                        },
                                        "content": {
                                            "en": "",
                                            "cy": ""
                                        },
                                        "dragItems": [
                                            {
                                                "id": "item-1637836143496.374",
                                                "text": {
                                                    "en": "Banana",
                                                    "cy": "Banana CY"
                                                },
                                                "answer": "col-1637836109525.1797"
                                            },
                                            {
                                                "id": "item-1637836146182.3167",
                                                "text": {
                                                    "en": "Beer",
                                                    "cy": "Beer CY"
                                                },
                                                "answer": "col-1637836109379.3835"
                                            },
                                            {
                                                "id": "item-1637836149848.6738",
                                                "text": {
                                                    "en": "Sunday Roast",
                                                    "cy": "Sunday Roast CY"
                                                },
                                                "answer": "col-1637836109525.1797"
                                            }
                                        ],
                                        "dropItems": [
                                            {
                                                "id": "col-1637836109525.1797",
                                                "title": {
                                                    "en": 'headings column here',
                                                    "cy": "Food CY"
                                                }
                                            },
                                            {
                                                "id": "col-1637836109379.3835",
                                                "title": {
                                                    "en": 'headings column here',
                                                    "cy": "Drinks CY"
                                                }
                                            }
                                        ]
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
                            continue
                    except IndexError:
                        messages.error(
                            request, f'Sortable into Columns card in lesson: {lesson_number}, screen: {screen_number} need to be added')

                # 'REFLECTION card'
                if 'REFLECTION' in table.rows[0].cells[0].text:
                    try:
                        dic['lessons'][lesson_number - 1]['subLessons'][screen_number - 1]['cards'].append(
                            {
                                "type": "reflection",
                                "data": {
                                    "title": {
                                        "en": "",
                                        "cy": ""
                                    },
                                    "content": {
                                        "en": table.rows[2].cells[0].text,
                                        "cy": table.rows[2].cells[1].text,
                                    }
                                }
                            }

                        )
                        continue
                    except IndexError:
                        messages.error(
                            request, f'REFLECTION card in Lesson {lesson_number}, Screen {screen_number}, need to be added')

              # Question carousel card
              #   need to loop for the tables
                if 'Question Carousel'.lower() in table.rows[0].cells[0].text.lower():
                    try:
                        dic['lessons'][lesson_number - 1]['subLessons'][screen_number - 1]['cards'].append(
                            {
                                "type": "carousel",
                                "data": {
                                        "scrollBar": False,
                                        "indicator": True,
                                        "loop": True,
                                        "content": {
                                            "en": table.rows[1].cells[0].text,
                                            "cy": table.rows[1].cells[1].text,
                                        }
                                }
                            },
                        )
                        continue
                    except IndexError:
                        messages.error(
                            request, f' Question carousel card in lesson: {lesson_number}, screen: {screen_number} need to be added ')

                 # OPINION
                if 'OPINION'.lower() in table.rows[0].cells[0].text.lower():
                    try:
                        dic['lessons'][lesson_number - 1]['subLessons'][screen_number - 1]['cards'].append(
                            {
                                "type": "opinionOpen",
                                "data": {
                                    "title": {
                                        "en": "",
                                        "cy": ""
                                    },
                                    "content": {
                                        "en": table.rows[2].cells[0].text,
                                        "cy": table.rows[2].cells[1].text, }
                                }
                            }
                        )
                        continue
                    except IndexError:
                        messages.error(
                            request, f'OPINION card in lesson: {lesson_number}, screen: {screen_number} need to be added')

                # Multi-choice
                if 'Multi-choice with 1 correct answer'.lower() in table.rows[0].cells[0].text.lower():
                    try:
                        dic['lessons'][lesson_number - 1]['subLessons'][screen_number - 1]['cards'].append(
                            {
                                "type": "mcq",
                                "data": {
                                        "title": {
                                            "en": "",
                                            "cy": ""
                                        },
                                    "content": {
                                            "en": "Click on the answer you think is correct.",
                                            "cy": "Cliciwch ar yr ateb rydych chi'n credu sy'n gywir."
                                    },
                                    "question": {
                                            "en": table.rows[2].cells[0].text,
                                            "cy": table.rows[2].cells[1].text,
                                    },
                                    "choices": [
                                            {
                                                "answer": {
                                                    "en": "Blue",
                                                    "cy": "Glas"
                                                },
                                                "correct": True
                                            },
                                            {
                                                "answer": {
                                                    "en": "Red",
                                                    "cy": "Coch"
                                                },
                                                "correct": False
                                            },
                                            {
                                                "answer": {
                                                    "en": "Yellow",
                                                    "cy": "Melyn"
                                                },
                                                "correct": False
                                            }
                                    ],
                                    "feedback": {
                                            "en": "Optional <span data-glossary='something abour something.'>Word</span>",
                                            "cy": "Adborth opsiynol"
                                    }
                                }
                            }

                        )
                        continue
                    except IndexError:
                        messages.error(
                            request, f'Multi-choice with 1 correct answer card in lesson: {lesson_number}, screen: {screen_number} need to be added')

                # ------------------------------------------------------------------------------------------------------ loop through the content
                # Fill the gaps drodown cards
                if 'Fill the gaps – dropdown'.lower() in table.rows[0].cells[0].text.lower():
                    try:
                        dic['lessons'][lesson_number - 1]['subLessons'][screen_number - 1]['cards'].append(
                            {
                                "type": "fillBlankDropdown",
                                "data": {
                                    "title": {
                                        "en": "Fill in the blanks (Dropdown)",
                                        "cy": "cy_Fill in the blanks (Dropdown)"
                                    },
                                    "content": {
                                        "en": "<p>Select your answers from the dropdowns to fill the gaps.</p>",
                                        "cy": "<p>cy_Select your answers from the dropdowns to fill the gaps.</p>"
                                    },
                                    "options": {
                                        "en": [
                                            [
                                                "were",
                                                "war",
                                                "army"
                                            ],
                                            [
                                                "one",
                                                "two",
                                                "three"
                                            ],
                                            [
                                                "1",
                                                "2",
                                                "3"
                                            ]
                                        ],
                                        "cy": [
                                            [
                                                "cy_were",
                                                "cy_war",
                                                "cy_army"
                                            ],
                                            [
                                                "cy_un",
                                                "cy_dai",
                                                "cy_tri"
                                            ],
                                            [
                                                "cy_1",
                                                "cy_2",
                                                "cy_3"
                                            ]
                                        ]
                                    },
                                    "activityContent": {
                                        "en": table.rows[2].cells[0].text,
                                        "cy": table.rows[2].cells[1].text
                                    }
                                }
                            }
                        )
                        messages.error(
                            request, f'Fill the gaps – dropdown card in lesson: {lesson_number}, screen: {screen_number}')
                        continue
                    except IndexError:
                        messages.error(
                            request, f'Fill the gaps – dropdown card in lesson: {lesson_number}, screen: {screen_number} need to be added')

                 # Fill the gaps typing card
                # ------------------------------------------------------------------------------------------------------ loop through the content
                if 'Fill the gaps – Typing'.lower() in table.rows[0].cells[0].text.lower():
                    try:
                        dic['lessons'][lesson_number - 1]['subLessons'][screen_number - 1]['cards'].append(
                            {
                                "type": "fillBlankText",
                                "data": {
                                    "title": {
                                        "en": "Fill in the blanks (Text)",
                                        "cy": "cy_Fill in the blanks (Text)"
                                    },
                                    "content": {
                                        "en": "<p>Type your answers into the gaps.</p>",
                                        "cy": "<p>cy_Type your answers into the gaps.</p>"
                                    },
                                    "activityContent": {
                                        "en": "<p>The recruits <input type=\"text\" class=\"blank-input\" data-answer=\"were\" /> mostly <input type=\"text\" class=\"blank-input\" data-answer=\"war\" /> veterans and junior <input type=\"text\" class=\"blank-input\" data-answer=\"army\" /> officers, who were violently anti-communist.</p>",
                                        "cy": "<p>The recruits <input type=\"text\" class=\"blank-input\" data-answer=\"were\" /> mostly <input type=\"text\" class=\"blank-input\" data-answer=\"war\" /> veterans and junior <input type=\"text\" class=\"blank-input\" data-answer=\"army\" /> officers, who were violently anti-communist.</p>"
                                    }
                                }
                            }
                        )
                        continue
                    except IndexError:
                        messages.error(
                            request, f'Fill the gaps – Typing card in lesson: {lesson_number}, screen: {screen_number} need to be added')

                 # Question & Answer card
                if 'Question & Answer'.lower() in table.rows[0].cells[0].text.lower():
                    try:
                        dic['lessons'][lesson_number - 1]['subLessons'][screen_number - 1]['cards'].append(
                            {
                                "type": "questionAndAnswer",
                                        "data": {
                                            "title": {
                                                "en": "",
                                                "cy": ""
                                            },
                                            "content": {
                                                "en": "Additional content",
                                                "cy": "CY_Aditional content"
                                            },
                                            "question": {
                                                "en": table.rows[2].cells[0].text,
                                                "cy": table.rows[2].cells[1].text,
                                            },
                                            "answer": {
                                                "en": table.rows[3].cells[0].text,
                                                "cy": table.rows[3].cells[1].text,
                                            },
                                            "feedback": {
                                                "en": "Feedback",
                                                "cy": "CY_Feedback"
                                            }
                                        }
                            }
                        )
                        continue
                    except IndexError:
                        messages.error(
                            request, f'Question & Answer card in lesson: {lesson_number}, screen: {screen_number} need to be added')

                # Random question generator with answer
                # ------------------------------------------------------------------------------------------------------ loop through the content
                if 'Random question generator with answer'.lower() in table.rows[0].cells[0].text.lower():
                    try:
                        dic['lessons'][lesson_number - 1]['subLessons'][screen_number - 1]['cards'].append(
                            {
                                "type": "randomGenerator",
                                "data": {
                                    "title": {
                                        "en": "Random Question Generator - Answers",
                                        "cy": "Random Question Generator - Answers CY"
                                    },
                                    "showAnswers": True,
                                    "questions": [
                                        {
                                            "question": {
                                                "en": table.rows[2].cells[0].text,
                                                "cy": table.rows[2].cells[1].text,
                                            },
                                            "answer": {
                                                "en": table.rows[3].cells[0].text,
                                                "cy": table.rows[3].cells[1].text,
                                            }
                                        },
                                    ]
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
                            }
                        )
                        continue
                    except IndexError:
                        messages.error(
                            request, f'Random question generator with answer card in lesson: {lesson_number}, screen: {screen_number} need to be added')

                # Random question generator -no answer
                # ------------------------------------------------------------------------------------------------------ loop through the content
                if 'Random question generator - no answer'.lower() in table.rows[0].cells[0].text.lower():
                    try:
                        dic['lessons'][lesson_number - 1]['subLessons'][screen_number - 1]['cards'].append(
                            {
                                "type": "randomGenerator",
                                "data": {
                                    "title": {
                                        "en": "Random Question Generator - Answers",
                                        "cy": "Random Question Generator - Answers CY"
                                    },
                                    "content": {
                                        "en": f"<p>{table.rows[2].cells[0].text}</p>",
                                        "cy": f"<p>{table.rows[2].cells[1].text}</p>",
                                    },
                                    "showAnswers": True,
                                    "questions": [
                                        {
                                            "question": {
                                                "en": "<p>Question one</p>",
                                                "cy": "<p>Cwestiwn un</p>"
                                            },
                                            "answer": {
                                                "en": "Answer one",
                                                "cy": "Ateb un"
                                            }
                                        },
                                        {
                                            "question": {
                                                "en": "<p>Question two</p>",
                                                "cy": "<p>Cwestiwn dau</p>"
                                            },
                                            "answer": {
                                                "en": "Answer two",
                                                "cy": "Ateb dau"
                                            }
                                        },
                                        {
                                            "question": {
                                                "en": "<p>Question three</p>",
                                                "cy": "<p>Cwestiwn tri</p>"
                                            },
                                            "answer": {
                                                "en": "Answer three",
                                                "cy": "Ateb tri"
                                            }
                                        }
                                    ]
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
                            }
                        )
                        continue
                    except IndexError:
                        messages.error(
                            request, f'Random question generator - no answer card in lesson: {lesson_number}, screen: {screen_number} need to be added')

                # Image Carousel block
                if 'Image Carousel block'.lower() in table.rows[0].cells[0].text.lower():
                    try:
                        dic['lessons'][lesson_number - 1]['subLessons'][screen_number - 1]['cards'].append(
                            {
                                "type": "carousel",
                                "data": {
                                    "scrollBar": False,
                                    "indicator": True,
                                    "loop": True,
                                    "slides": [
                                        {
                                            "en": f"<p>{table.rows[2].cells[0].text}</p>",
                                            "cy": f"<p>{table.rows[2].cells[1].text}</p>",
                                        }
                                    ]
                                }
                            },
                        )
                        continue
                    except IndexError:
                        messages.error(
                            request, f'Image Carousel block card in lesson: {lesson_number}, screen: {screen_number} need to be added')

                # Sound block
                if 'Sound block'.lower() in table.rows[0].cells[0].text.lower():
                    try:
                        dic['lessons'][lesson_number - 1]['subLessons'][screen_number - 1]['cards'].append(
                            {
                                "type": "sound",
                                "data": {
                                    "title": {
                                        "en": "Sound/Audio",
                                        "cy": "_Sound/Audio"
                                    },
                                    "content": {
                                        "en": f"<a href='{table.rows[2].cells[0].text}' target='_blank'><img src='https://resource.download.wjec.co.uk/vtc/2020-21/bl20-21_4-26/bbc-audio.jpg' class='img-block'></a>",
                                        "cy": f"<a href='{table.rows[2].cells[1].text} target='_blank'><img src='https://resource.download.wjec.co.uk/vtc/2020-21/bl20-21_4-26/bbc-audio.jpg' class='img-block'></a>"
                                    }
                                }
                            }
                        )
                        continue
                    except IndexError:
                        messages.error(
                            request, f'Sound block in lesson: {lesson_number}, screen: {screen_number} need to be added')

                # Download block
                # ------------------------------------------------------------------------------------------------------ Json errror
                if 'Download block'.lower() in table.rows[0].cells[0].text.lower():
                    try:
                        dic['lessons'][lesson_number - 1]['subLessons'][screen_number - 1]['cards'].append(
                            {
                                "type": "download",
                                "data": {
                                    "title": {
                                        "en": "Download",
                                        "cy": "cy_Download"
                                    },
                                    "content": {
                                        "en": "Text content",
                                        "cy": "_Text content"
                                    },
                                    "link": {
                                        "en": table.rows[2].cells[0].text,
                                        "cy": table.rows[2].cells[1].text
                                    }
                                }
                            }
                        )
                        continue
                    except IndexError:
                        messages.error(
                            request, f'Download block card in lesson: {lesson_number}, screen: {screen_number} need to be added')


                # GLOSSARY
                # ------------------------------------------------------------------------------------------------------ loop through the content
                if 'GLOSSARY'.lower() in table.rows[0].cells[0].text.lower():
                    try:
                        dic['lessons'][lesson_number - 1]['subLessons'][screen_number - 1]['cards'].append(
                            {
                                "type": "read",
                                "downloadFiles": [
                                    {
                                        "fileName": {
                                            "en": "",
                                            "cy": ""
                                        },
                                        "url": {
                                            "en": "",
                                            "cy": ""
                                        }
                                    }
                                ],
                                "data": {
                                    "title": {
                                        "en": "",
                                        "cy": ""
                                    },
                                    "content": {
                                        "en": table.rows[2].cells[0].text,
                                        "cy": table.rows[2].cells[1].text
                                }
                                }
                            }
                        )
                        continue
                    except IndexError:
                        messages.error(
                            request, f'GLOSSARY card with answer in Lesson {lesson_number}, Screen {screen_number}, need to be check')
                        

                # TEST YOURSELF
                if 'Static text – TEST YOURSELF (for past paper questions only)'.lower() in table.rows[0].cells[0].text.lower():
                    try:
                        dic['lessons'][lesson_number - 1]['subLessons'][screen_number - 1]['cards'].append(

                            {
                                "type": "testYourself",
                                        "data": {
                                            "title": {
                                                "en": "Test Yourself Title",
                                                "cy": "_Test Yourself Title"
                                            },
                                            "content": {
                                                "en": table.rows[2].cells[0].text,
                                                "cy": table.rows[2].cells[1].text
                                            },
                                            "link": {
                                                "en": "https://resource.download.wjec.co.uk/vtc/2020-21/bl20-21_2-1/Pages%20from%20s18-3110-01.pdf",
                                                "cy": "https://resource.download.wjec.co.uk/vtc/2020-21/bl20-21_2-1/Pages%20from%20s18-3110-51.pdf"
                                            }
                                        }
                            }
                        )
                        continue
                    except IndexError or TypeError:
                        messages.error(
                            request, f'Static text – TEST YOURSELF (for past paper questions only) card in lesson: {lesson_number}, screen: {screen_number} need to be added')

                # MARK YOURSELF
                if 'Static text – MARK YOURSELF  (for past paper questions only)'.lower() in table.rows[0].cells[0].text.lower():
                    try:
                        dic['lessons'][lesson_number - 1]['subLessons'][screen_number - 1]['cards'].append(

                            {
                                "type": "markYourself",
                                "data": {
                                    "title": {
                                        "en": "Mark Yourself Title",
                                        "cy": "_Mark Yourself Title"
                                    },
                                    "content": {
                                        "en": table.rows[2].cells[0].text,
                                        "cy": table.rows[2].cells[1].text
                                    },
                                    "link": {
                                        "en": "https://resource.download.wjec.co.uk/vtc/2020-21/bl20-21_2-1/Pages%20from%20s18-geography1-ms.pdf",
                                        "cy": "https://resource.download.wjec.co.uk/vtc/2020-21/bl20-21_2-1/Pages%20from%20s18-3110n10-1-gcse-geography-u1-ms.pdf"
                                    }
                                }
                            }

                        )
                        continue
                    except IndexError:
                        messages.error(
                            request, f'Static text – MARK YOURSELF  (for past paper questions only) card in lesson: {lesson_number}, screen: {screen_number} need to be added')

                 # True or False
                # ------------------------------------------------------------------------------------------------------ loop through the content
                if 'True or False'.lower() in table.rows[0].cells[0].text.lower():
                    try:
                        dic['lessons'][lesson_number - 1]['subLessons'][screen_number - 1]['cards'].append(
                            {
                                "type": "trueFalse",
                                "data": {
                                    "title": {
                                        "en": table.rows[1].cells[0].text,
                                        "cy": table.rows[1].cells[1].text}
                                    },
                                    "content": {
                                        "en": table.rows[3].cells[0].text,
                                        "cy": table.rows[3].cells[1].text

                                    },
                                    "activityContent": [
                                        [
                                            {
                                                "str": {
                                                    "en": "A1",
                                                    "cy": "A1_CY"
                                                },
                                                "correct": True
                                            },
                                            {
                                                "str": {
                                                    "en": "A2",
                                                    "cy": "A2_CY"
                                                }
                                            }
                                        ],
                                        [
                                            {
                                                "str": {
                                                    "en": "B1",
                                                    "cy": "B1_Cy"
                                                },
                                                "correct": True
                                            },
                                            {
                                                "str": {
                                                    "en": "B2",
                                                    "cy": "B2_CY"
                                                }
                                            }
                                        ],
                                        [
                                            {
                                                "str": {
                                                    "en": "C1",
                                                    "cy": "C1_CY"
                                                },
                                                "correct": True
                                            },
                                            {
                                                "str": {
                                                    "en": "C2",
                                                    "cy": "C2_CY"
                                                }
                                            }
                                        ],
                                        [
                                            {
                                                "str": {
                                                    "en": "D1",
                                                    "cy": "D1_Cy"
                                                },
                                                "correct": True
                                            },
                                            {
                                                "str": {
                                                    "en": "D2",
                                                    "cy": "D2_CY"
                                                }
                                            }
                                        ]
                                    ]
                                }

                        )
                        continue
                    except IndexError:
                        messages.error(
                            request, f'True or False in lesson: {lesson_number}, screen: {screen_number} need to be added')

                 # Structured Framework
                 # ------------------------------------------------------------------------------------------------------ check this activity
                if 'Structured Framework'.lower() in table.rows[0].cells[0].text.lower():
                    try:
                        dic['lessons'][lesson_number - 1]['subLessons'][screen_number - 1]['cards'].append(
                            {
                                "type": "sortable",
                                "data": {
                                    "title": {
                                        "en": "Structured Framework",
                                        "cy": "CY Structured Framework"
                                    },
                                    "content": {
                                        "en": "<p>Reorder the items in to the correct order.</p>",
                                        "cy": "<p>CY Reorder the items in to the correct order.</p>"
                                    },
                                    "doCheck": True,
                                    "activityContent": [
                                        {
                                            "title": {
                                                "en": "Introduction",
                                                "cy": "Cyflwyniad"
                                            },
                                            "str": {
                                                "en": "Many were sharecroppers and were forced to give up their farms.",
                                                "cy": "Roedd llawer ohonyn nhw'n gyfran-gnydwyr (<em>sharecroppers</em>) ac fe gawson nhw eu gorfodi i roi'r gorau i'w ffermydd."
                                            }
                                        },
                                        {
                                            "title": {
                                                "en": "Section 1",
                                                "cy": "Rhan 1"
                                            },
                                            "str": {
                                                "en": "Many picked cotton, which was not in as much demand.",
                                                "cy": "Roedd llawer yn casglu cotwm, a doedd dim cymaint o alw amdano."
                                            }
                                        },
                                        {
                                            "title": {
                                                "en": "Section 2",
                                                "cy": "Rhan 2"
                                            },
                                            "str": {
                                                "en": "They had the lowest paid jobs.",
                                                "cy": " Nhw oedd â'r swyddi a oedd yn talu'r lleiaf."
                                            }
                                        },
                                        {
                                            "title": {
                                                "en": "Section 3",
                                                "cy": "Rhan 3"
                                            },
                                            "str": {
                                                "en": "They were not educated.",
                                                "cy": "Doedden nhw ddim wedi cael eu haddysgu."
                                            }
                                        },
                                        {
                                            "title": {
                                                "en": "Section 4",
                                                "cy": "Rhan 4"
                                            },
                                            "str": {
                                                "en": "They were subject to prejudice and discrimination.",
                                                "cy": "Roedden nhw'n profi rhagfarn a gwahaniaethu."
                                            }
                                        },
                                        {
                                            "title": {
                                                "en": "Conclusion",
                                                "cy": "Diweddglo"
                                            },
                                            "str": {
                                                "en": "Many were farm labourers who lost their jobs.",
                                                "cy": "Roedd llawer ohonyn nhw'n weithwyr fferm a gollodd eu swyddi."
                                            }
                                        }
                                    ]
                                }
                            }
                        )
                        continue
                    except IndexError:
                        messages.error(
                            request, f'Structured Framework(sortable) card in lesson: {lesson_number}, screen: {screen_number} need to be added')

                # Thought shower
                if 'Thought shower'.lower() in table.rows[0].cells[0].text.lower():
                    try:
                        dic['lessons'][lesson_number - 1]['subLessons'][screen_number - 1]['cards'].append(
                            {
                                "type": "thoughtShower",
                                "data": {
                                    "title": {
                                        "en": "",
                                        "cy": ""
                                    },
                                    "content": {
                                        "en": f"\n<p>{table.rows[2].cells[0].text}</p>\n",
                                        "cy": f"\n<p>{table.rows[2].cells[1].text}</p>\n"
                                    },
                                    "question": {
                                        "en": "\n<p>What to Think About!</p>\n",
                                        "cy": "\n<p>What to Think About!CY</p>\n"
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
                            }
                        )
                        continue
                    except IndexError:
                        messages.error(
                            request, f'Thought shower in lesson: {lesson_number}, screen: {screen_number} need to be added')

                # Video with Question
                if 'Video with Question'.lower() in table.rows[0].cells[0].text.lower():
                    try:
                        dic['lessons'][lesson_number - 1]['subLessons'][screen_number - 1]['cards'].append(
                            {
                                "type": "videoQuestion",
                                "downloadFiles": [],
                                "hint": {},
                                "extension": {},
                                "answer": {},
                                "data": {
                                    "title": {
                                        "en": "Video with Question - Source",
                                        "cy": "_Read Title"
                                    },
                                    "content": {
                                        "en": "<p>Take a look at the following video and asnwer the questions that appear.</p>",
                                        "cy": "<p>Cymerwch olwg ar y fideo ac yna ateb y cewsitynau sy'n ymddangos.</p>"
                                    },
                                    "isYouTube": False,
                                    "path": f"{table.rows[2].cells[0].text}",
                                    "questions": [
                                        {
                                            "time": 3,
                                            "comment": {
                                                "en": "What do you think of this statement?",
                                                "cy": "Beth ydych yn meddwl o'r hyn?"
                                            }
                                        },
                                        {
                                            "time": 6,
                                            "comment": {
                                                "en": "Can you think of any other like this?",
                                                "cy": ""
                                            }
                                        },
                                        {
                                            "time": 9,
                                            "comment": {
                                                "en": "What do you think is missing here?",
                                                "cy": ""
                                            }
                                        }
                                    ]
                                }
                            },
                        )
                        continue
                    except IndexError:
                        messages.error(
                            request, f'Video with Question card with answer in Lesson {lesson_number}, Screen {screen_number}, add content {table.rows[0].cells[0].text}')

                # Gallery Card"
                # ------------------------------------------------------------------------------------------------------ check this activity
                if 'Gallery Card'.lower() in table.rows[0].cells[0].text.lower():
                    try:
                        dic['lessons'][lesson_number - 1]['subLessons'][screen_number - 1]['cards'].append(
                            {
                                "type": "gallery",
                                "data": {
                                    "title": {
                                        "en": "Gallery",
                                        "cy": "Galeri"
                                    },
                                    "content": {
                                        "en": table.rows[2].cells[0].text,
                                        "cy": table.rows[2].cells[1].text
                                    },
                                    "photos": [
                                        {
                                            "title": {
                                                "en": "Image 1 title",
                                                "cy": "_Image 1 title"
                                            },
                                            "content": {
                                                "en": "Caption 1",
                                                "cy": "_Caption"
                                            },
                                            "source": "https://resource.download.wjec.co.uk/vtc/2020-21/bL20-21_1-1/allegorical-portrait.jpg"
                                        },
                                        {
                                            "title": {
                                                "en": "Image 2 title",
                                                "cy": "_Image 2 title"
                                            },
                                            "content": {
                                                "en": "Caption 2",
                                                "cy": "_Caption"
                                            },
                                            "source": "https://resource.download.wjec.co.uk/vtc/2020-21/bL20-21_1-1/armada-portrait.jpg"
                                        },
                                    ]
                                }
                            }
                        )
                        continue
                    except IndexError:
                        messages.error(
                            request, f'Gallery Card in lesson: {lesson_number}, screen: {screen_number} need to be added')

            messages.success(request, 'File converted succesfully')
    dic = json.dumps(dic, indent=4)
    context = {'dic': dic}
    return render(request, 'scraper.html', context)


                        # HINT/SUPPORT
                    # if 'HINT/SUPPORT'.lower() in table.rows[0].cells[0].text.lower():

                    #     )
                    #     messages.error(
                    #         request, f'HINT/SUPPORT  card with answer in Lesson {lesson_number}, Screen {screen_number}, add content {table.rows[0].cells[0].text}')

                    # EXTENSION
                    # if 'EXTENSION'.lower() in table.rows[0].cells[0].text.lower():

                    #     messages.error(
                    #         request, f'EXTENSION card with answer in Lesson {lesson_number}, Screen {screen_number}, add content {table.rows[0].cells[0].text}')

                    # ANSWER
                    # if 'ANSWER'.lower() in table.rows[0].cells[0].text.lower():

                    #     messages.error(
                    #         request, f'ANSWER card with answer in Lesson {lesson_number}, Screen {screen_number}, add content {table.rows[0].cells[0].text}')

                    #  if the uopload is successful

