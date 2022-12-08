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
                                messages.error(
                                    request, f'{lesson_number}, {screen_number} is empty,  {table.rows[2].cells[0].text}')

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
                            messages.error(
                                request, f'{lesson_number}, {screen_number} is empty', {table.rows[1].cells[0].text})
                            # request, f'{lesson_number}, {screen_number} is empty, {table.rows[1].cells[0].text}')

                if 'LESSON OBJECTIVES'.lower() in table.rows[0].cells[0].text.lower():
                    dic['lessons'][lesson_number - 1]['subLessons'][screen_number - 1]['cards'].append(
                        {
                            "type": "read",
                            "data": {
                                "title": {
                                    "en": "",
                                    "cy": ""
                                },
                                "content": {
                                    # "en": table.rows[2].cells[0].text,
                                    # "cy": table.rows[2].cells[1].text,
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

                 # adding reading cards
                if "reading" in table.rows[0].cells[0].text.lower():
                    print(table.rows[0].cells[0].text.lower())
                    dic['lessons'][lesson_number - 1]['subLessons'][screen_number - 1]['cards'].append(
                        {
                            "type": "read",
                            "data": {
                                "title": {
                                    "en": "",
                                    "cy": ""
                                },
                                "content": {
                                    # "en": table.rows[2].cells[0].text,
                                    # "cy": table.rows[2].cells[0].text,
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
                    messages.error(
                        request, f' Reading card needs content in Lesson {lesson_number}, Screen {screen_number}')

                # adding WRITING cards
                if "WRITING".lower() in table.rows[0].cells[0].text.lower():
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

              # Spot the mistake card
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
                    messages.error(
                        request, f'You need to add the Mistake manually in "spot the mistake activity" located in  lesson number: {lesson_number}, and screen {screen_number}')

                # video card
                if 'Video block' in table.rows[0].cells[0].text:
                    # print(table.rows[2].cells[0].text.split('/')[0].strip())
                    dic['lessons'][lesson_number - 1]['subLessons'][screen_number - 1]['cards'].append(
                        {
                            "type": "look",
                            "data": {
                                "title": {
                                    "en": "",
                                    "cy": ""
                                },
                                "content": {
                                    "en": f"\n<div class=\"video-container\"><iframe src=\"https://www.youtube.com/embed/{table.rows[0].cells[0].text}?rel=0&start=0&end=\" allowfullscreen></iframe></div>",
                                    "cy": "",
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
                    messages.error(
                        request, f' There is a video in Lesson {lesson_number}, Screen {screen_number}, make sure is the right link')

                # Sortable into Columns
                if 'Sortable into Columns' in table.rows[0].cells[0].text:
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
                    messages.error(
                        request, f' Sortable Columns in Lesson {lesson_number}, Screen {screen_number}, make sure is correct', )

                # 'REFLECTION card'
                if 'REFLECTION' in table.rows[0].cells[0].text:
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
                                    "cy": table.rows[2].cells[1].text, }
                            }
                        }

                    )
                    messages.error(
                        request, f'REFLECTION Lesson {lesson_number}, Screen {screen_number}, make sure is correct', )

                # carousel card
                if 'carousel' in table.rows[0].cells[0].text.lower():
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
                    messages.error(
                        request, f'carousel Lesson {lesson_number}, Screen {screen_number}, make sure is correct {table.rows[0].cells[0].text}', )

                 # OPINION
                if 'OPINION'.lower() in table.rows[0].cells[0].text.lower():
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
                        })
                    messages.error(
                        request, f'Opinion card in Lesson {lesson_number}, Screen {screen_number}, make sure is correct {table.rows[0].cells[0].text}', )

                # Multi-choice
                if 'Multi-choice with 1 correct answer'.lower() in table.rows[0].cells[0].text.lower():
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
                    messages.error(
                        request, f'Multi-choice card in Lesson {lesson_number}, Screen {screen_number}, make sure is correct {table.rows[0].cells[0].text}')

            messages.success(request, 'File converted succesfully')
    dic = json.dumps(dic, indent=4)
    context = {'dic': dic}
    return render(request, 'scraper.html', context)
