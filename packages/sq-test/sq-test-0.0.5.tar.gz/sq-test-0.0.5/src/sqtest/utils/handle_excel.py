import xlrd





def get_excel_data(fireDir,sheetName):
    wookBook = xlrd.open_workbook(fireDir,formatting_info=True)
    sheet = wookBook.sheet_by_name(sheetName)
    project_name = sheet.cell_value(0,1)
    keys = sheet.col_values(3)[1:]
    value = sheet.col_values(4)[1:]
    step = sheet.col_values(1)[1:]
    step_text = sheet.col_values(2)[1:]
    reslist = []
    alist = []
    for one in range(len(keys)):
        if one == 0:
            continue
        reslist.append({keys[one]:value[one],step[one]:step_text[one]})
        if keys[one] == 'assert':
            alist.append(reslist)
            reslist = []
            continue
    input_list = [index for index,key in enumerate(keys) if key == 'input']
    click_list = [index for index,key in enumerate(keys) if key == 'click']
    move_on_list =  [index for index,key in enumerate(keys) if key == 'move_on']
    save_text_list = [index for index,key in enumerate(keys) if key == 'save_text']
    save_texts_list = [index for index,key in enumerate(keys) if key == 'save_texts']
    assert_list = [index for index,key in enumerate(keys) if key == 'assert']
    input_idx = 0
    click_idx = 0
    move_on_idx = 0
    save_text_idx = 0
    save_texts_idx = 0
    assert_idx = 0
    for datas in alist:
        for one in datas:
            hand_key = list(one.keys())[0]
            if hand_key == 'input':
                one[hand_key] = [sheet.cell_value(input_list[input_idx]+1 , 4),
                                 sheet.cell_value(input_list[input_idx]+1, 5),
                                 sheet.cell_value(input_list[input_idx]+1, 6)]
                input_idx+=1
            if hand_key == 'click':

                one[hand_key] = [sheet.cell_value(click_list[click_idx]+1 , 4),
                                 sheet.cell_value(click_list[click_idx]+1, 5)]
                click_idx+=1
            if hand_key == 'move_on':
                one[hand_key] = [sheet.cell_value(move_on_list[move_on_idx] + 1, 4),
                                 sheet.cell_value(move_on_list[move_on_idx] + 1, 5)]
                move_on_idx += 1

            if hand_key == 'assert':
                one[hand_key] = [sheet.cell_value(assert_list[assert_idx] + 1, 4),
                                 sheet.cell_value(assert_list[assert_idx] + 1, 5)]
                assert_idx += 1
            if hand_key == 'save_text':
                one[hand_key] = [sheet.cell_value(save_text_list[save_text_idx]+1 , 4),
                                 sheet.cell_value(save_text_list[save_text_idx]+1, 5),
                                 sheet.cell_value(save_text_list[save_text_idx]+1, 6)]
                save_text_idx+=1
            if hand_key == 'save_texts':
                one[hand_key] = [sheet.cell_value(save_texts_list[save_texts_idx]+1 , 4),
                                 sheet.cell_value(save_texts_list[save_texts_idx]+1, 5),
                                 sheet.cell_value(save_texts_list[save_texts_idx]+1, 6)]
                save_texts_idx+=1
    return alist,project_name



if __name__ == '__main__':
    print(get_excel_data('测试用例.xls','登录模块'))


