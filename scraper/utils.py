from django.contrib import messages
# add content to static cards
def add_static_card_content(dic,lesson_number,screen_number,card_number,table, content='content'):
    try:
        dic['lessons'][lesson_number - 1]['subLessons'][screen_number - 1]['cards'][card_number -
                                                                                    1]['data'][content]['en'] += table.rows[2].cells[0].text
        dic['lessons'][lesson_number - 1]['subLessons'][screen_number - 1]['cards'][card_number -1]['data'][content]['cy'] += table.rows[2].cells[1].text
    except IndexError:
        print('')


# loop though table contents
def loop_though_table_content(row_number, dic,lesson_number,screen_number,card_number,table, content= "content"):
    try:
        if table.rows[row_number].cells[0].text:
            for i in range(row_number, len(table.rows)):
                dic['lessons'][lesson_number - 1]['subLessons'][screen_number - 1]['cards'][card_number -
                                                                                            1]['data'][content]['en'] += f'<p>{table.rows[i].cells[0].text}</p>\n'
                dic['lessons'][lesson_number - 1]['subLessons'][screen_number - 1]['cards'][card_number -
                                                                                            1]['data'][content]['cy'] += f'<p>{table.rows[i].cells[1].text}</p>\n'
    except IndexError:
        print('')

def loop_through_tables_in_cells(row_number, dic,lesson_number,screen_number,card_number,table, content= "content"):
        try:
            for table in table.rows[row_number].cells[0].tables:
                for i in range(0, len(table.columns)):
                    dic['lessons'][lesson_number - 1]['subLessons'][screen_number - 1]['cards'][card_number - 1]['data'][content]['en'] += f'<th>{table.columns[i].cells[0].text}</th>'
                    for j in range(1, len(table.rows)):
                        dic['lessons'][lesson_number - 1]['subLessons'][screen_number - 1]['cards'][card_number - 1]['data'][content]['en'] += f'<td>{table.rows[j].cells[i].text}</td>'
        except IndexError:
            print('')
        except AttributeError:
            print('')

        try:
            for table in table.rows[row_number].cells[1].tables:
                for i in range(0, len(table.columns)):
                    dic['lessons'][lesson_number - 1]['subLessons'][screen_number - 1]['cards'][card_number - 1]['data'][content]['cy'] += f'<th>{table.columns[i].cells[0].text}</th>'
                    for j in range(1, len(table.rows)):
                        dic['lessons'][lesson_number - 1]['subLessons'][screen_number - 1]['cards'][card_number - 1]['data'][content]['cy'] += f'<td>{table.rows[j].cells[i].text}</td>'
        except IndexError:
                  print('')
        except AttributeError:
            print('')



def append_table_to_answer_hint_extension(row_number, dic,lesson_number,screen_number,card_number,table, content= "answer"):
        try:
            for table in table.rows[row_number].cells[0].tables:
                for i in range(0, len(table.columns)):
                    dic['lessons'][lesson_number - 1]['subLessons'][screen_number - 1]['cards'][card_number - 1][content]['en'] += f'<th>{table.columns[i].cells[0].text}</th>'
                    for j in range(1, len(table.rows)):
                        dic['lessons'][lesson_number - 1]['subLessons'][screen_number - 1]['cards'][card_number - 1][content]['en'] += f'<td>{table.rows[j].cells[i].text}</td>'
        except IndexError:
            print('')
        except AttributeError:
            print('')

        try:
            for table in table.rows[row_number].cells[1].tables:
                for i in range(0, len(table.columns)):
                    dic['lessons'][lesson_number - 1]['subLessons'][screen_number - 1]['cards'][card_number - 1][content]['cy'] += f'<th>{table.columns[i].cells[0].text}</th>'
                    for j in range(1, len(table.rows)):
                        dic['lessons'][lesson_number - 1]['subLessons'][screen_number - 1]['cards'][card_number - 1][content]['cy'] += f'<td>{table.rows[j].cells[i].text}</td>'
        except IndexError:
                  print('')
        except AttributeError:
            print('')
