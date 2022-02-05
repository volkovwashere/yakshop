import os.path
from fastapi import APIRouter, status, HTTPException
import logging
from yakshop.yak_ops.yak_operator import YakOperator
from yakshop.utils.config import get_root_path
from yakshop.utils.schemas import YakStock, Herd, YakOrder


yak_op = YakOperator.init_herd(os.path.join(get_root_path(), "fake_db/herd.xml"))
router = APIRouter()
classifier_route_logger = logging.getLogger("classifier.classifier")


@router.get(path="/stock/{dt}", tags=["Stock"], response_model=YakStock)
async def get_stock(dt: int):
    return yak_op.calculate_stock(dt=dt)


@router.get(path="/herd/{dt}", tags=["Herd"], response_model=Herd)
async def get_herd(dt: int):
    return {"herd": yak_op.herd_state_after_t_days(dt=dt)}


@router.post(path="/order/{t}", tags=["Order"])
async def order_from_stock(req: YakOrder, t: int):
    milk, wool = req.order.milk, req.order.wool
    milk_available, wool_available = yak_op.pack_order(
        milk_ordered=milk, wool_ordered=wool, dt=t
    )

    if milk_available > 0 and wool_available > 0:
        return {
            "status_code": status.HTTP_201_CREATED,
            "milk": milk_available,
            "wool": wool_available,
        }
    elif milk_available == 0 and wool_available == 0:
        raise HTTPException(status_code=404, detail="Out of stock.")
    else:
        res = {
            "status_code": status.HTTP_206_PARTIAL_CONTENT,
            "milk": milk_available,
            "wool": wool_available,
        }
        res = {k: v for k, v in res.items() if v != 0}
        return res
