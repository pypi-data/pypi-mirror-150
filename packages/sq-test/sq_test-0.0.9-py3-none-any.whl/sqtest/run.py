
import pytest
import os



def test_run():
    pytest.main([os.path.join(os.path.dirname(os.path.abspath(__file__)),'test_template.py'),'-sv', '--alluredir', 'report/tmp'])
    os.system('allure serve report/tmp')

