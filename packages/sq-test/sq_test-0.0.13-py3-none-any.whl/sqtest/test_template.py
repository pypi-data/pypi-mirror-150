import sys
import allure
import pytest
from .exec import Exec
from .utils.handle_excel import get_excel_data




filepath = sys.argv[1]
filesheet = sys.argv[2]

all_data = get_excel_data(filepath,filesheet)


@pytest.mark.parametrize('data',all_data[0])
@allure.epic(f'{all_data[1]}')
@allure.feature(f'{filesheet}')
@allure.title('{data[1][name]}')
def test_temp(data):
        exe = Exec(data)
        list_dict = {
            'goto':exe.goto,
            'input':exe.input,
            'click':exe.click,
            'assert':exe.def_assert,
            'save_text':exe.save_text
        }
        for one in data:
            for k  in list(one.keys()):
                if k in list_dict:
                    if k == 'save_text':
                        res = list_dict[k]()
                    elif k == 'assert':
                        list_dict[k](res)
                    else:
                        list_dict[k]()
                else:
                    continue

