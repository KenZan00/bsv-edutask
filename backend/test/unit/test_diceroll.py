import pytest
from unittest.mock import patch
from src.util.helpers import diceroll

@pytest.mark.dice
@pytest.mark.parametrize('num, expected', [
    (3, False),
    (4, False),
    (5, True),
])
def test_diceroll_fixed(num, expected):
    with patch('src.util.helpers.random.randint') as randint_mock:
        randint_mock.return_value = num
        
        result = diceroll()
        assert result is expected

# Number 4 is not correct from documentation as it should be >4 and not >=4