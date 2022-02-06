import os.path

from yakshop.yak_ops.yak_operator import YakOperator
from yakshop.utils.config import get_root_path

test_yak_op = YakOperator.init_herd(
    path=os.path.join(get_root_path(), "fake_db/herd.xml")
)


def test_calculate_stock():
    dt_1 = 13
    dt_2 = 14

    res_1 = test_yak_op.calculate_stock(dt=dt_1)
    res_2 = test_yak_op.calculate_stock(dt=dt_2)

    assert type(res_1) == dict
    assert res_1["wool"] == 3
    assert res_1["milk"] == 1104.48

    assert type(res_2) == dict
    assert res_2["wool"] == 4
    assert res_2["milk"] == 1188.81


def test_herd_state_after_t_days():
    dt = 13
    res = test_yak_op.herd_state_after_t_days(dt=dt)
    assert type(res) == list
    assert len(res) > 0
    assert res[0]["age"] == 4.13


def test_pack_order():
    dt = 14
    res = test_yak_op.pack_order(milk_ordered=100, wool_ordered=5, dt=dt)

    assert type(res) == tuple
    assert res[0] == 100
    assert res[1] == 0
