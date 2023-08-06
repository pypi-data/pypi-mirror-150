import os
from it_automation.report_email import read_data, summary_data


def test_read_data():
    file_path = os.path.dirname(os.path.realpath(__file__))
    test_description_directory = os.path.join(
        file_path,
        'test_data',
        'read_data'
    )

    name_list, weight_list = read_data(test_description_directory)
    name_list = set(name_list)
    weight_list = set(weight_list)
    test_name_list = {'Avocado', 'Apple'}
    test_weight_list = {'200 lbs', '500 lbs'}
    assert name_list == test_name_list
    assert weight_list == test_weight_list


def test_summary_data():
    name_list = ['Avocado', 'Apple']
    weight_list = ['200 lbs', '500 lbs']
    test_summary = 'name: Avocado <br /> weight: 200 lbs <br /><br />name: ' \
                   'Apple <br /> weight: 500 lbs <br /><br />'
    summary = summary_data(name_list, weight_list)
    assert test_summary == summary
