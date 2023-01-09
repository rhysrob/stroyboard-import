
# add content to static cards
def add_static_card_content(dic,lesson_number,screen_number,card_number,table, content='content'):
    try:
        dic['lessons'][lesson_number - 1]['subLessons'][screen_number - 1]['cards'][card_number -
                                                                                    1]['data'][content]['en'] += table.rows[2].cells[0].text
        dic['lessons'][lesson_number - 1]['subLessons'][screen_number - 1]['cards'][card_number -1]['data']['content']['cy'] += table.rows[2].cells[1].text
    except IndexError:
        print('')


# loop though table contents
def loop_though_table_content(row_number, dic,lesson_number,screen_number,card_number,table):
    try:
        if table.rows[row_number].cells[0].text:
            for i in range(row_number, len(table.rows)):
                dic['lessons'][lesson_number - 1]['subLessons'][screen_number - 1]['cards'][card_number -
                                                                                            1]['data']['content']['en'] += f'<p>{table.rows[i].cells[0].text}</p>\n'
                dic['lessons'][lesson_number - 1]['subLessons'][screen_number - 1]['cards'][card_number -
                                                                                            1]['data']['content']['cy'] += f'<p>{table.rows[i].cells[1].text}</p>\n'
    except IndexError:
        print('')

