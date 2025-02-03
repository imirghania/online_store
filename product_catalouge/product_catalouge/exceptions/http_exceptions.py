from fastapi import HTTPException, status


def create_ItemNotFoundError_404(item_name:str):
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Invalid {item_name.capitalize()}")

InvalidInput_400 = HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                                detail="Invalid input")