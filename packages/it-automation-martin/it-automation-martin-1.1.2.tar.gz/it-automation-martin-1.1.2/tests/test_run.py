from it_automation.run import read_description_directory, post_description
import os
import pytest
from unittest import mock


def test_read_description_directory():
    file_path = os.path.dirname(os.path.realpath(__file__))
    test_description_directory = os.path.join(
        file_path,
        'test_data',
        'read_data'
    )

    test_dic = [{'name': 'Avocado',
                 'weight': 200,
                 'description': 'Avocado contains large amount of oleic acid, '
                                'a type of monounsaturated fat that can replace '
                                'saturated fat in the diet, which is very '
                                'effective in reducing cholesterol levels. '
                                'Avocado is also high in fiber. Its soluble '
                                'fiber can remove excess cholesterol from the '
                                'body, while its insoluble fiber helps keep '
                                'the digestive system functioning and prevent '
                                'constipation. ',
                 'image_name': '002.jpeg'},
                {'name': 'Apple',
                 'weight': 500,
                 'description': 'Apple is one of the most nutritious and '
                                'healthiest fruits. It is very rich in '
                                'antioxidants and dietary fiber. Moderate '
                                'consumption can not only increase satiety, '
                                'but also help promote bowel movements. '
                                'Apple also contains minerals such as '
                                'calcium and magnesium, which can help prevent '
                                'and delay bone loss and maintain bone health. '
                                'It is good for young and old. ',
                 'image_name': '001.jpeg'}
                ]
    test_dic = sorted(test_dic, key=lambda d: d['name'], reverse=True)
    dic = read_description_directory(test_description_directory)
    dic = sorted(dic, key=lambda d: d['name'], reverse=True)
    assert dic == test_dic


@pytest.mark.parametrize(
    "_input, expected",
    [(201, "Success"), (400, "POST error status=400")]
)
@mock.patch("it_automation.run.requests.post")
def test_post_description(mock_requests_post, _input, expected):
    mock_requests_post.return_value = mock.Mock(**{"status_code": _input})

    data_list = ["test data 1", "test data 2"]
    test_url = "test url"

    if _input != 201:
        with pytest.raises(Exception, match=expected):
            post_description(test_url, data_list)
    else:
        post_description(test_url, data_list)

    mock_requests_post.assert_called()
