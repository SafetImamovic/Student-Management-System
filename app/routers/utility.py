from typing import Annotated

from sqlalchemy.engine.result import Result

from fastapi import APIRouter, Depends

from app.controllers.utility_controller import UtilityController, seed

router = APIRouter()


@router.delete(
    '/truncate_db/',
    responses={

    },
    response_model=None,
    tags=["TRUNCATE DATABASE"]
)
def truncate_db(
    controller: Annotated[UtilityController, Depends(UtilityController)]
):
    """
    :param controller:
    :return:
    """

    # TODO: Better logging
    result: Result = controller.truncate()

    if result:
        return {"msg": "Database Tables truncated successfully."}


@router.post(
    '/re_seed_db/',
    responses={

    },
    response_model=None,
    tags=["RE-SEED DATABASE"]
)
def re_seed_database(
    controller: Annotated[UtilityController, Depends(UtilityController)]
):
    """
    This function re-seeds some tables in the database based on the default values
    :param controller:
    :return: The re-seeded database
    """

    seed(controller)

    return {"msg": "Database Tables re-seeded successfully."}
