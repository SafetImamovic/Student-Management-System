from fastapi.responses import JSONResponse
from app.utils.enums import ErrorType, Location


def pydantic_error_response(errors: list[dict]) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content={"detail": errors}
    )


def add_error(errors: list[dict], loc: list[Location | str], msg: str, error_type: ErrorType = ErrorType.VALUE_ERROR):
    errors.append({"loc": loc, "msg": msg, "type": error_type.value})
