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
                if 'Language' in table.rows[0].cells[0].text:
                    if "Lesson" in table.rows[1].cells[0].text:
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

                            if "Lesson" in table.rows[1].cells[1].text:
                                messages.error(
                                    request, f' Lesson {lesson_number} tile is not correct -> {table.rows[1].cells[1].text}')
                                continue
                        except IndexError:
                            messages.error(request, f'LESSON: {lesson_number}, screen: {screen_number} need to be added')

                        # adding screens
                        if "Screen" in table.rows[2].cells[0].text:
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
                                    messages.error(request, f'{lesson_number}, {screen_number} is empty,  {table.rows[2].cells[0].text}')
                                continue
                            except IndexError:
                                messages.error(request, f'Screen in lesson: {lesson_number}, screen: {screen_number} need to be added')


                    elif "Screen" in table.rows[1].cells[0].text:
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
                        messages.error(request, f'LESSON OBJECTIVES card in lesson: {lesson_number}, screen: {screen_number} need to be added ')


                 # adding reading cards
                if "reading" in table.rows[0].cells[0].text.lower():
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
                        messages.error(request, f' Reading card in Lesson {lesson_number}, Screen {screen_number} need to be added')

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
                        messages.error(request, f'Case study card in lesson: {lesson_number}, screen: {screen_number} need to be added ')


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
                        messages.error(request, f'Speaking card in lesson: {lesson_number}, screen: {screen_number} need to be added ')


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
                        messages.error(request, f'summary card in lesson: {lesson_number}, screen: {screen_number} need to be added ')


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
                        messages.error(request, f'MCQ card in lesson: {lesson_number}, screen: {screen_number} need to be added ')

                    

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
                        messages.error(request, f'Spot the mistake card in lesson: {lesson_number}, screen: {screen_number} need to be added ')


                # video card
                if 'Video block' in table.rows[0].cells[0].text:
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
                                        "en": f"\n<div class=\"video-container\"><iframe src=\"https://www.youtube.com/embed/{table.rows[2].cells[0].text.split('/')[0].strip()}?rel=0&start=0&end=\" allowfullscreen></iframe></div>",
                                        "cy": f"\n<div class=\"video-container\"><iframe src=\"https://www.youtube.com/embed/{table.rows[2].cells[1].text.split('/')[0].strip()}?rel=0&start=0&end=\" allowfullscreen></iframe></div>",
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
                        messages.error(request, f' There is a video in Lesson {lesson_number}, Screen {screen_number}, make sure is the right link')
                        continue
                    except IndexError:
                        messages.error(request, f'Video block card in lesson: {lesson_number}, screen: {screen_number} need to be addded ')

                # Sortable into Columns
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
                        messages.error(request, f'Sortable into Columns card in lesson: {lesson_number}, screen: {screen_number} need to be added')

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

                # carousel card
                if 'carousel' in table.rows[0].cells[0].text.lower():
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
                                                "en": "<h2>Lorem ipsum dolor sit amet consectetur adipisicing elit.</h2>",
                                                "cy": "<h2>cy_Lorem ipsum dolor sit amet consectetur adipisicing elit.</h2>"
                                            },
                                            {
                                                "en": "<h2 class=\"text-center\">Magnam natus unde iure voluptatem eos est cum earum provident non laboriosam!</h2>",
                                                "cy": "<h2 class=\"text-center\">CY_ Magnam natus unde iure voluptatem eos est cum earum provident non laboriosam!</h2>"
                                            },
                                            {
                                                "en": "<img class='img-block' src=\"https://source.unsplash.com/1600x900/?nature,water\" /></div>",
                                                "cy": "<img class='img-block' src=\"https://source.unsplash.com/1600x900/?nature,water\" /></div>"
                                            },
                                            {
                                                "en": "<img class='img-block img-right w-50' src='http://placehold.it/600x600'/><h1>Heading One</h1><h2>Heading Two</h2><h3>Heading Thrre</h3><h4>Heaiing Four</h4><p>Lorem ipsum dolor sit amet consectetur adipisicing elit.Ex sapiente quibusdam consectetur quae tenetur enimcupiditate voluptas, quod ea ut hicdolorum deserunt perferendis temporibus consequunturincidunt eos eligendi reiciendis.</p><ul><li>Lorem ipsum dolor sit.</li><li>Fuga fugit veniam sint.</li><li>Quasi magnam saepe consectetur!</li><li>Ipsum adipisci dolorem veniam?</li></ul><blockquote><p>Lorem ipsum dolor sit amet consectetur adipisicing elit.<br />Dolorum animi accusantium est illo iste quasmollitiaquidem facilis veniam voluptatem.</p></blockquote>",
                                                "cy": "<h1>CY</h1><img class='img-block img-right w-50' src='http://placehold.it/600x600'/><h1>Heading One</h1><h2>Heading Two</h2><h3>Heading Thrre</h3><h4>Heaiing Four</h4><p>Lorem ipsum dolor sit amet consectetur adipisicing elit.Ex sapiente quibusdam consectetur quae tenetur enimcupiditate voluptas, quod ea ut hicdolorum deserunt perferendis temporibus consequunturincidunt eos eligendi reiciendis.</p><ul><li>Lorem ipsum dolor sit.</li><li>Fuga fugit veniam sint.</li><li>Quasi magnam saepe consectetur!</li><li>Ipsum adipisci dolorem veniam?</li></ul><blockquote><p>Lorem ipsum dolor sit amet consectetur adipisicing elit.<br />Dolorum animi accusantium est illo iste quasmollitiaquidem facilis veniam voluptatem.</p></blockquote>"
                                            },
                                            {
                                                "en": "<p>The well known Pythagorean theorem \\(x^2 + y^2 = z^2\\) was \n proved to</p><ul><li>one term</li><li>Term two</li><li>three things</li></ul><p>be invalid for other exponents.</p><p>he well known Pythagorean theorem $(x^2 + y^2 = z^2)$ was \n proved to be invalid for other exponents.</p>",
                                                "cy": "CY_<p>The well known Pythagorean theorem $$(x^2 + y^2 = z^2)$$ was \n proved to</p><ul><li>one term</li><li>Term two</li><li>three things</li></ul><p>be invalid for other exponents.</p><p>he well known Pythagorean theorem $(x^2 + y^2 = z^2)$ was \n proved to be invalid for other exponents.</p>"
                                            }
                                        ]
                                }
                            },

                        )
                        continue
                    except IndexError:
                        messages.error(request, f'carousel card in lesson: {lesson_number}, screen: {screen_number} need to be added ')


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
                        messages.error(request, f'OPINION card in lesson: {lesson_number}, screen: {screen_number} need to be added')

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
                        messages.error(request, f'Multi-choice with 1 correct answer card in lesson: {lesson_number}, screen: {screen_number} need to be added')


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
                                        "en": "<p>The recruits <select class=\"blank-dropdown\" data-answer=\"were\"></select> mostly <select class=\"blank-dropdown\" data-answer=\"two\"></select> veterans and junior <select class=\"blank-dropdown\" data-answer=\"1\"></select> officers, who were violently anti-communist.</p>",
                                        "cy": "<p>The recruits <select class=\"blank-dropdown\" data-answer=\"cy_were\"></select> mostly <select class=\"blank-dropdown\" data-answer=\"cy_dai\"></select> veterans and junior <select class=\"blank-dropdown\" data-answer=\"cy_1\"></select> officers, who were violently anti-communist.</p>"
                                    }
                                }
                            }
                        )
                        continue
                    except IndexError:
                        messages.error(request, f'Fill the gaps – dropdown card in lesson: {lesson_number}, screen: {screen_number} need to be added')


                 # Fill the gaps typing card
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
                        messages.error(request, f'Fill the gaps – Typing card in lesson: {lesson_number}, screen: {screen_number} need to be added')

                 # Question & Answer card
                if 'Question & Answer'.lower() in table.rows[0].cells[0].text.lower():
                    try:
                        dic['lessons'][lesson_number - 1]['subLessons'][screen_number - 1]['cards'].append(
                            {
                                "title": {
                                    "en": "Question and Answer",
                                    "cy": "Question and Answer CY"
                                },
                                "slug": "question and answer",
                                "cards": [
                                    {
                                        "type": "questionAndAnswer",
                                        "data": {
                                            "title": {
                                                "en": "Question and Answer Card",
                                                "cy": "Question and Answer Card"
                                            },
                                            "content": {
                                                "en": "Additional content",
                                                "cy": "CY_Aditional content"
                                            },
                                            "question": {
                                                "en": "Which city is the capital of Wales?",
                                                "cy": "Pa ddinas yw prif ddinas Cymru?"
                                            },
                                            "answer": {
                                                "en": "Cardiff",
                                                "cy": "Caerdydd"
                                            },
                                            "feedback": {
                                                "en": "Feedback",
                                                "cy": "CY_Feedback"
                                            }
                                        }
                                    }
                                ]
                            },
                        )
                        continue
                    except IndexError:
                        messages.error(request, f'Question & Answer card in lesson: {lesson_number}, screen: {screen_number} need to be added')


                # Random question generator with answer
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
                                    "content": {
                                        "en": "<p>This statement will tell you what the questions are about.<br>\nThis is an individual activity. user answers are checked so they can compare.</p>",
                                        "cy": "<p>This statement will tell you what the questions are about. CY<br>\nThis is an individual activity. user answers are checked so they can compare. CY</p>"
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
                        messages.error(request, f'Random question generator with answer card in lesson: {lesson_number}, screen: {screen_number} need to be added')

                # Random question generator -no answer
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
                                        "en": "<p>This statement will tell you what the questions are about.<br>\nThis is an individual activity. user answers are checked so they can compare.</p>",
                                        "cy": "<p>This statement will tell you what the questions are about. CY<br>\nThis is an individual activity. user answers are checked so they can compare. CY</p>"
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
                        messages.error(request, f'Random question generator - no answer card in lesson: {lesson_number}, screen: {screen_number} need to be added')

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
                                            "en": "<h2>Lorem ipsum dolor sit amet consectetur adipisicing elit.</h2>",
                                            "cy": "<h2>cy_Lorem ipsum dolor sit amet consectetur adipisicing elit.</h2>"
                                        },
                                        {
                                            "en": "<h2 class=\"text-center\">Magnam natus unde iure voluptatem eos est cum earum provident non laboriosam!</h2>",
                                            "cy": "<h2 class=\"text-center\">CY_ Magnam natus unde iure voluptatem eos est cum earum provident non laboriosam!</h2>"
                                        },
                                        {
                                            "en": "<img class='img-block' src=\"https://source.unsplash.com/1600x900/?nature,water\" /></div>",
                                            "cy": "<img class='img-block' src=\"https://source.unsplash.com/1600x900/?nature,water\" /></div>"
                                        },
                                        {
                                            "en": "<img class='img-block img-right w-50' src='http://placehold.it/600x600'/><h1>Heading One</h1><h2>Heading Two</h2><h3>Heading Thrre</h3><h4>Heaiing Four</h4><p>Lorem ipsum dolor sit amet consectetur adipisicing elit.Ex sapiente quibusdam consectetur quae tenetur enimcupiditate voluptas, quod ea ut hicdolorum deserunt perferendis temporibus consequunturincidunt eos eligendi reiciendis.</p><ul><li>Lorem ipsum dolor sit.</li><li>Fuga fugit veniam sint.</li><li>Quasi magnam saepe consectetur!</li><li>Ipsum adipisci dolorem veniam?</li></ul><blockquote><p>Lorem ipsum dolor sit amet consectetur adipisicing elit.<br />Dolorum animi accusantium est illo iste quasmollitiaquidem facilis veniam voluptatem.</p></blockquote>",
                                            "cy": "<h1>CY</h1><img class='img-block img-right w-50' src='http://placehold.it/600x600'/><h1>Heading One</h1><h2>Heading Two</h2><h3>Heading Thrre</h3><h4>Heaiing Four</h4><p>Lorem ipsum dolor sit amet consectetur adipisicing elit.Ex sapiente quibusdam consectetur quae tenetur enimcupiditate voluptas, quod ea ut hicdolorum deserunt perferendis temporibus consequunturincidunt eos eligendi reiciendis.</p><ul><li>Lorem ipsum dolor sit.</li><li>Fuga fugit veniam sint.</li><li>Quasi magnam saepe consectetur!</li><li>Ipsum adipisci dolorem veniam?</li></ul><blockquote><p>Lorem ipsum dolor sit amet consectetur adipisicing elit.<br />Dolorum animi accusantium est illo iste quasmollitiaquidem facilis veniam voluptatem.</p></blockquote>"
                                        },
                                        {
                                            "en": "<p>The well known Pythagorean theorem \\(x^2 + y^2 = z^2\\) was \n proved to</p><ul><li>one term</li><li>Term two</li><li>three things</li></ul><p>be invalid for other exponents.</p><p>he well known Pythagorean theorem $(x^2 + y^2 = z^2)$ was \n proved to be invalid for other exponents.</p>",
                                            "cy": "CY_<p>The well known Pythagorean theorem $$(x^2 + y^2 = z^2)$$ was \n proved to</p><ul><li>one term</li><li>Term two</li><li>three things</li></ul><p>be invalid for other exponents.</p><p>he well known Pythagorean theorem $(x^2 + y^2 = z^2)$ was \n proved to be invalid for other exponents.</p>"
                                        }
                                    ]
                                }
                            },
                        )
                        continue
                    except IndexError:
                        messages.error(request, f'Image Carousel block card in lesson: {lesson_number}, screen: {screen_number} need to be added')

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
                                        "en": "<a href='https://www.bbc.co.uk/sounds/play/p03m0hxr' target='_blank'><img src='https://resource.download.wjec.co.uk/vtc/2020-21/bl20-21_4-26/bbc-audio.jpg' class='img-block'></a>",
                                        "cy": "<a href='https://www.bbc.co.uk/sounds/play/p03m0hxr' target='_blank'><img src='https://resource.download.wjec.co.uk/vtc/2020-21/bl20-21_4-26/bbc-audio.jpg' class='img-block'></a>"
                                    }
                                }
                            }
                        )
                        continue
                    except IndexError:
                        messages.error(request, f'Sound block in lesson: {lesson_number}, screen: {screen_number} need to be added')

                # Download block
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
                                        "en": "https://avatars2.githubusercontent.com/u/5277598?v=4",
                                        "cy": "https://avatars2.githubusercontent.com/u/5277598?v=4"
                                    }
                                }
                            }
                        )
                        continue
                    except IndexError:
                        messages.error(request, f'Download block card in lesson: {lesson_number}, screen: {screen_number} need to be added')

                # GLOSSARY
                if 'GLOSSARY'.lower() in table.rows[0].cells[0].text.lower():
                    try:
                        dic['lessons'][lesson_number - 1]['subLessons'][screen_number - 1]['cards'].append(
                            {
                                "type": "read",
                                "downloadFiles": [
                                    {
                                        "fileName": {
                                            "en": "test custom file name",
                                            "cy": "test custom file name CY"
                                        },
                                        "url": {
                                            "en": "https://resource.download.wjec.co.uk/vtc/2020-21/bl20-21_3-7/downloads/s18-3122-06-Q1c.pdf",
                                            "cy": "https://resource.download.wjec.co.uk/vtc/2020-21/bl20-21_3-7/downloads/s18-3122-06-Q1c.pdf"
                                        }
                                    }
                                ],
                                "data": {
                                    "title": {
                                        "en": "Read Title",
                                        "cy": "_Read Title"
                                    },
                                    "content": {
                                        "en": "<p class='text-center'>The Bible is <span data-glossary=\"Able to be trusted as accurate or true and should be obeyed.\">authoritative</span> for Catholics because as <strong><span data-glossary=\"The holy writings contained in the Bible.\">Sacred Scripture</span></strong>, it is divinely inspired or God-breathed (2 Tim 3:16).  Catholics live good <span data-glossary=\"Standards of behaviour; principles of right or wrong. \">moral</span> lives by being obedient to the Bible. For Catholics, the Bible reveals the <span data-glossary=\"The law that comes from God and is revealed in the Bible. \">Divine Law</span> for humanity. This means that the Bible is God’s Law. All other forms of law, natural and human should uphold the Divine Law and this in turn satisfies the <span data-glossary=\"The laws that govern the entire universe and can be knowable only by God.\">Eternal Law</span> which is fully known by God. </p>\n<blockquote class=\"blockquote\">\n  <p class=\"mb-1\">Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed quis quam leo. Nunc egestas tempus commodo. Integer et felis a sapien laoreet condimentum. Nunc commodo iaculis nibh, a pellentesque nisi. Etiam a urna vehicula, efficitur dui sed, placerat arcu. Donec tincidunt felis mi, a lacinia leo mollis vehicula. Donec auctor condimentum leo ac tristique. Quisque bibendum quis dolor in consectetur. Pellentesque suscipit dignissim ex id tempor.</p>\n<p class=\"mb-1\">Suspendisse dolor nibh, rhoncus sit amet tincidunt non, ullamcorper non augue. Ut nec enim dui. Duis consequat ac est at rutrum. Duis ut iaculis mi, et vehicula tellus. Fusce lacinia id sapien vitae facilisis. Fusce aliquet rhoncus nisi, auctor congue diam mollis ac. Aenean in tortor mollis, cursus enim at, convallis mi. Aliquam at condimentum metus, sit amet posuere diam. Sed sed ullamcorper nunc, consequat semper purus. Aenean nec justo posuere ligula rutrum tristique sit amet id lacus. Quisque auctor non metus id interdum. Etiam sit amet urna vehicula, sodales nulla sed, suscipit mauris.</p>\n  <footer class=\"blockquote-footer\">Someone famous in <cite title=\"Source Title\">Source Title</cite></footer>\n</blockquote>\n<div class='col-6'><img src=\"https://source.unsplash.com/1600x900/?food\" class=\"mx-auto d-block img-block\"></div><p>The Bible is important because it is the revealed Word of God.  The Bible was inspired by the Holy Spirit.  Catholic Christians believe that God continues to communicate with people today through the Bible. Therefore, Catholics are encouraged to read the Bible for themselves as well as listen to Church teaching about it. </p><p>In the Bible, we find important rules on how to live one’s life such as the 10 Commandments and the Sermon on the Mount. Teachings in the Bible guide Catholics about what is right and wrong, and the Bible gives advice on how to treat people and how to <span data-glossary=\"Give great respect to someone or something.\">honour</span> God through <span data-glossary=\"Looking after something because it is given by God.\">stewardship</span> of one’s life.</p><p>However, Catholics believe that as well as through the Bible, God reveals himself to humanity in other ways. </p><p>‘Dei Verbum’, one of the four key documents that emerged from the <span data-glossary=\"The most recent council (assembly) of all Catholic Bishops which met between 1962 and 1965 to discuss issues from the modern world that affected the Catholic Church.\">Second Vatican Council</span> claims that the Word of God is communicated through Sacred Scripture, <span data-glossary=\"The faith and practices that have been passed down from the early Christians and adhered to by the Catholic Church.\">Tradition</span>, and the teaching authority of the Church (<span data-glossary=\"The inspired teaching role of the Catholic Church.\">Magisterium</span>). All three are linked together and guided by God’s Holy Spirit. </p>    <p>Watch the following video and answer the questions that follow. </p>",
                                        "cy": "<p>ô â Â, ê Ê, î Î, ô Ô, û Û, ŵ and ŷ Mae’r Beibl yn <span data-glossary=\"Rhywbeth y gellir ymddiried ynddo fel rhywbeth cywir neu wir ac y dylid ufuddhau iddo.\">awdurdod</span> i Gatholigion gan ei fod, fel <span data-glossary=\"Ysgrifeniadau sanctaidd yn y Beibl.\">Ysgrythur Sanctaidd</span>, wedi’i ysbrydoli’n ddwyfol neu wedi’i anadlu gan Dduw (2 Timotheus 3:16). Mae Catholigion yn byw bywydau <span data-glossary=\"Safonau ymddygiad; egwyddorion o ran y da a’r drwg. \">moesol</span> da drwy ufuddhau i’r Beibl. I Gatholigion, mae'r Beibl yn datgelu’r <span data-glossary=\"Y gyfraith a ddaw gan Dduw ac a ddatgelir yn y Beibl.\">Gyfraith Ddwyfol</span> ar gyfer y ddynoliaeth. Mae hyn yn golygu mai Cyfraith Duw yw’r Beibl. Dylai pob math arall o gyfraith, yn naturiol ac yn ddynol ategu’r Gyfraith Ddwyfol ac, yn ei dro, mae hyn yn bodloni <span data-glossary=\"Y cyfreithiau sy’n llywodraethu’r bydysawd, na all neb ond Duw wybod amdanynt. \">Cyfraith Dragwyddol</span> Duw. </p>\n<blockquote class=\"blockquote\">\n  <p class=\"mb-1\">Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed quis quam leo. Nunc egestas tempus commodo. Integer et felis a sapien laoreet condimentum. Nunc commodo iaculis nibh, a pellentesque nisi. Etiam a urna vehicula, efficitur dui sed, placerat arcu. Donec tincidunt felis mi, a lacinia leo mollis vehicula. Donec auctor condimentum leo ac tristique. Quisque bibendum quis dolor in consectetur. Pellentesque suscipit dignissim ex id tempor.</p>\n<p class=\"mb-1\">Suspendisse dolor nibh, rhoncus sit amet tincidunt non, ullamcorper non augue. Ut nec enim dui. Duis consequat ac est at rutrum. Duis ut iaculis mi, et vehicula tellus. Fusce lacinia id sapien vitae facilisis. Fusce aliquet rhoncus nisi, auctor congue diam mollis ac. Aenean in tortor mollis, cursus enim at, convallis mi. Aliquam at condimentum metus, sit amet posuere diam. Sed sed ullamcorper nunc, consequat semper purus. Aenean nec justo posuere ligula rutrum tristique sit amet id lacus. Quisque auctor non metus id interdum. Etiam sit amet urna vehicula, sodales nulla sed, suscipit mauris.</p>\n  <footer class=\"blockquote-footer\">Someone famous in <cite title=\"Source Title\">Source Title</cite></footer>\n</blockquote><img src=\"https://source.unsplash.com/1600x900/?food\" class=\"img-right\"><p>Mae’r Beibl yn bwysig gan mai Gair datguddiedig Duw ydyw.   Cafodd y Beibl ei ysbrydoli gan yr Ysbryd Glân.  Mae Cristnogion Catholig yn credu bod Duw yn parhau i gyfathrebu â phobl heddiw drwy’r Beibl. Felly, mae Catholigion yn cael eu hannog i ddarllen y Beibl eu hunain yn ogystal â gwrando ar ddysgeidiaeth yr Eglwys amdano. </p><p>Yn y Beibl, cawn reolau ar sut i fyw ein bywyd megis y Deg Gorchymyn a’r Bregeth ar y Mynydd. Mae dysgeidiaethau yn y Beibl yn rhoi arweiniad i Gatholigion ar yr hyn sy’n dda a’r hyn sy’n ddrwg, ac mae’r Beibl yn rhoi cyngor ar sut i drin pobl a sut i <span data-glossary=\"Dangos parch mawr at rywun neu rywbeth.\">anrhydeddu</span> Duw drwy <span data-glossary=\"Gofalu am rywbeth am ei fod yn rhodd gan Dduw.\">stiwardiaeth</span> ein bywyd. </p><p>Fodd bynnag, mae Catholigion yn credu bod Duw yn datgelu ei hun i’r ddynoliaeth drwy ffyrdd eraill, yn ogystal â thrwy’r Beibl. </p><p>Mae ‘Dei Verbum’, sef un o’r bedair dogfen allweddol a gyhoeddwyd gan Ail Gyngor y Fatigan, yn honni bod Gair Duw yn cael ei gyfleu drwy Ysgrythur Sanctaidd, Traddodiad, ac awdurdod dysgeidiaeth yr Eglwys (y Magisterium). Mae’r tri pheth yn gysylltiedig â’i gilydd ac yn cael eu llywio gan Ysbryd Glân Duw. </p><p>Mae ‘Dei Verbum’, sef un o’r bedair dogfen allweddol a gyhoeddwyd gan <span data-glossary=\"Cyngor (cynulliad) diweddaraf yr holl Esgobion Catholig a gyfarfu rhwng 1962 ac 1965 i drafod materion yn y byd modern a oedd yn effeithio ar yr Eglwys Gatholig. \">Ail Gyngor y Fatigan</span>, yn honni bod Gair Duw yn cael ei gyfleu drwy Ysgrythur Sanctaidd, <span data-glossary=\"Ffydd ac arferion a drosglwyddwyd gan y Cristnogion cynnar ac a ddilynir gan yr Eglwys Gatholig.  \">Traddodiad</span>, ac awdurdod dysgeidiaeth yr Eglwys (<span data-glossary=\"Rôl addysgu ysbrydoledig yr Eglwys Gatholig.\">y Magisterium</span>). Mae’r tri pheth yn gysylltiedig â’i gilydd ac yn cael eu llywio gan Ysbryd Glân Duw. </p><p>Gwyliwch y fideo canlynol ac atebwch y cwestiynau sy’n dilyn.</p>"
                                    }
                                }
                            }
                        )
                        continue
                    except IndexError:
                        messages.error(request, f'GLOSSARY card with answer in Lesson {lesson_number}, Screen {screen_number}, need to be check')

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
                                                "en": "<p>PAST PAPER QUESTION – PAPER 1 2018 Question 1C (i – iii)</p><img src=\"https://resource.download.wjec.co.uk/vtc/2020-21/bl20-21_2-1/Pages%20from%20s18-3110-01_Page_1.png\" class=\"img-block\"/><img src=\"https://resource.download.wjec.co.uk/vtc/2020-21/bl20-21_2-1/Pages%20from%20s18-3110-01_Page_2.png\" class=\"img-block\"/>",
                                                "cy": "<p>CWESTIWN O BAPUR BLAENOROL – PAPUR 1 2018 Cwestiwn 1C (i – iii)</p><img src=\"https://resource.download.wjec.co.uk/vtc/2020-21/bl20-21_2-1/Pages%20from%20s18-3110-51_Page_1.png\" class=\"img-block\"/><img src=\"https://resource.download.wjec.co.uk/vtc/2020-21/bl20-21_2-1/Pages%20from%20s18-3110-51_Page_2.png\" class=\"img-block\"/>"
                                            },
                                            "link": {
                                                "en": "https://resource.download.wjec.co.uk/vtc/2020-21/bl20-21_2-1/Pages%20from%20s18-3110-01.pdf",
                                                "cy": "https://resource.download.wjec.co.uk/vtc/2020-21/bl20-21_2-1/Pages%20from%20s18-3110-51.pdf"
                                            }
                                        }
                            }
                        )
                        continue
                    except IndexError:
                        messages.error(request, f'Static text – TEST YOURSELF (for past paper questions only) card in lesson: {lesson_number}, screen: {screen_number} need to be added')

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
                                        "en": "<p>Now use the marking scheme to assess your answer. Can you do anything to improve your score?</p><img src=\"https://resource.download.wjec.co.uk/vtc/2020-21/bl20-21_2-1/Pages%20from%20s18-geography1-ms_Page_1.png\" class=\"img-block\"/><img src=\"https://resource.download.wjec.co.uk/vtc/2020-21/bl20-21_2-1/Pages%20from%20s18-geography1-ms_Page_2.png\" class=\"img-block\"/>",
                                        "cy": "<p>Nawr defnyddiwch y cynllun marcio i asesu eich ateb. Allwch chi wneud unrhyw beth i wella eich sgôr?</p><img src=\"https://resource.download.wjec.co.uk/vtc/2020-21/bl20-21_2-1/Pages%20from%20s18-3110n10-1-gcse-geography-u1-ms-2_Page_1.png\" class=\"img-block\"/><img src=\"https://resource.download.wjec.co.uk/vtc/2020-21/bl20-21_2-1/Pages%20from%20s18-3110n10-1-gcse-geography-u1-ms-2_Page_2.png\" class=\"img-block\"/>"
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
                        messages.error(request, f'Static text – MARK YOURSELF  (for past paper questions only) card in lesson: {lesson_number}, screen: {screen_number} need to be added')

                 # True or False
                if 'True or False'.lower() in table.rows[0].cells[0].text.lower():
                    try:
                        dic['lessons'][lesson_number - 1]['subLessons'][screen_number - 1]['cards'].append(
                            {
                                "type": "trueFalse",
                                "data": {
                                    "title": {
                                        "en": "True or False",
                                        "cy": "True or False"
                                    },
                                    "content": {
                                        "en": "<p>Click on the statement that you think is <strong>True</strong>.",
                                        "cy": "<p>cy_Click on the statement that you think is <strong>True</strong>."
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
                            }

                        )
                        continue
                    except IndexError:
                        messages.error(request, f'True or False in lesson: {lesson_number}, screen: {screen_number} need to be added')

                 # Structured Framework
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
                        messages.error(request, f'Structured Framework(sortable) card in lesson: {lesson_number}, screen: {screen_number} need to be added')

                # Thought shower
                if 'Thought shower'.lower() in table.rows[0].cells[0].text.lower():
                    try:
                        dic['lessons'][lesson_number - 1]['subLessons'][screen_number - 1]['cards'].append(
                            {
                                "type": "thoughtShower",
                                "data": {
                                    "title": {
                                        "en": "Thought Shower Example",
                                        "cy": "Thought Shower Example CY"
                                    },
                                    "content": {
                                        "en": "\n<p>Add as many thoughts as you have about the topic below.</p>\n",
                                        "cy": "\n<p>Add as many thoughts as you have about the topic below. CY</p>\n"
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
                        messages.error(request, f'Thought shower in lesson: {lesson_number}, screen: {screen_number} need to be added')

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
                                    "path": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4",
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
                        messages.error(request, f'Video with Question card with answer in Lesson {lesson_number}, Screen {screen_number}, add content {table.rows[0].cells[0].text}')

                # Gallery Card"
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
                                        "en": "Text Content",
                                        "cy": "_Text Content"
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
                        messages.error(request, f'Gallery Card in lesson: {lesson_number}, screen: {screen_number} need to be added')

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
            messages.success(request, 'File converted succesfully')
    dic = json.dumps(dic, indent=4)
    context = {'dic': dic}
    return render(request, 'scraper.html', context)
