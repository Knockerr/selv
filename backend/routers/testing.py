from fastapi import APIRouter, HTTPException

# Create routeur
router = APIRouter()


@router.post("/sendError/httpException")
async def sendErrorHttp():
    raise HTTPException(500, "[TEST] Internal server error.. / httpException")


@router.post("/sendError/exception")
async def sendErrorException():
    def raiseException():
        raise Exception("[TEST] Internal server error.. / Exception")

    raiseException()
