from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Union


class Wafer(BaseModel):
    wafer_id: str
    description: Union[str, None] = None
    lot_id: str


router = APIRouter(
    prefix="/wafers",
    tags=["wafers"],
    # dependencies=[Depends(get_tsmc_uid)],
    responses={404: {"description": "Wafer not found"}}
)
wafers = [Wafer(wafer_id=f"N12345.{i:02d}", lot_id="N12345.00") for i in range(1, 26)]


@router.get("/{wafer_id}", response_model=Wafer, response_model_exclude_unset=True)
async def get_wafer(wafer_id: str):
    """
    Get one wafer
    :param wafer_id:
    :return:
    """
    ws = [w for w in wafers if w.wafer_id == wafer_id]
    if len(ws) > 0:
        return ws[0]
    else:
        raise HTTPException(status_code=404, detail=f"Wafer[{wafer_id}] not found")


@router.get("/", response_model=Wafer, response_model_exclude_unset=True)
async def list_wafers():
    """
    List all wafers
    :return:
    """
    return wafers


@router.delete("/{wafer_id}")
async def delete_wafer(wafer_id: str):
    ws = [w for w in wafers if w.wafer_id == wafer_id]
    if len(ws) > 0:
        wafers.remove(ws[0])
        return {"message": f"Wafer[{wafer_id}] deleted successfully."}
    else:
        raise HTTPException(status_code=404, detail=f"Wafer[{wafer_id}] not found")


@router.put("/{wafer_id}", response_model=Wafer, response_model_exclude_unset=True)
async def update_wafer(wafer_id: str, description: Optional[str] = None):
    ws = [w for w in wafers if w.wafer_id == wafer_id]
    if len(ws) > 0:
        w = ws[0]
        w.description = description
        return w
    else:
        raise HTTPException(status_code=404, detail=f"Wafer[{wafer_id}] not found")

## No router
# @router.get("/wafers/", tags=["wafers"])
# async def read_wafers():
#     return [{"wafer_id": "N12345.01"}, {"wafer_id": "N12345.02"}]
#
#
# @router.get("/wafers/{wafer_id}", tags=["wafers"])
# async def read_wafers(wafer_id: str):
#     return {"wafer_id": wafer_id}

