from fastapi import HTTPException, status


def ItemNotFoundError_404(item_name:str):
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Invalid {item_name.capitalize()}")

def ItemAlreadyExistsError_409(item_name:str):
    return HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"{item_name.capitalize()} already exists")

def InvalidInputError_400(item_name:str):
    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"Invalid {item_name.capitalize()}")
