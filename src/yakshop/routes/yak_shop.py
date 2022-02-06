import os.path
from fastapi import APIRouter, status, HTTPException
import logging
from yakshop.yak_ops.yak_operator import YakOperator
from yakshop.utils.config import get_root_path
from yakshop.utils.schemas import YakStock, Herd, YakOrder
from yakshop.utils.config import read_yaml

config = read_yaml(root_path=get_root_path())
yak_op = YakOperator.init_herd(os.path.join(get_root_path(), config["data_path"]))
router = APIRouter()
classifier_route_logger = logging.getLogger("classifier.classifier")


@router.get(path="/stock/{dt}", tags=["Stock"], response_model=YakStock)
async def get_stock(dt: int) -> dict:
    """
    This GET endpoint returns the available stock amount of wool skin and milk produced based on the elapsed time.
    Args:
        dt (int): Elapsed time.

    Returns (dict): Returns YakStock response body.

    """
    return yak_op.calculate_stock(dt=dt)


@router.get(path="/herd/{dt}", tags=["Herd"], response_model=Herd)
async def get_herd(dt: int) -> dict:
    """
    This GET endpoint returns the name, age and the last shaved time for yaks over a given period of elapsed time given
    as a parameter.
    Args:
        dt (int): Elapsed time.

    Returns (dict): Herd response body.

    """
    return {"herd": yak_op.herd_state_after_t_days(dt=dt)}


@router.post(path="/order/{t}", tags=["Order"])
async def order_from_stock(req: YakOrder, t: int):
    """
    This POST request handles the order and returns the deliverable amount. It either return 201, 206 or 404.
    Args:
        req (YakOrder): Request body schema
        t (int): Day of the order.

    Returns (dict): Returns the deliverable milk or status code.

    """
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
