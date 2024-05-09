import uvicorn

from fastapi import FastAPI, Header,Request,File, UploadFile,status,Form
from fastapi.responses import StreamingResponse,FileResponse,Response
from typing import Dict,List,Any,Union
from CaesarSQLDB.caesarcrud import CaesarCRUD
from CaesarSQLDB.caesarhash import CaesarHash
from fastapi.responses import StreamingResponse
from fastapi import WebSocket,WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from CaesarJWT.caesarjwt import CaesarJWT
from CaesarSQLDB.caesar_create_tables import CaesarCreateTables

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


caesarcrud = CaesarCRUD()
maturityjwt = CaesarJWT(caesarcrud)
caesarcreatetables = CaesarCreateTables()
caesarcreatetables.create(caesarcrud)

JSONObject = Dict[Any, Any]
JSONArray = List[Any]
JSONStructure = Union[JSONArray, JSONObject]

@app.get('/')# GET # allow all origins all methods.
async def index():
    return "Welcome to CaesarAI Template. Hello"
@app.post('/sendmessage')# GET # allow all origins all methods.
async def sendmessage(data: JSONStructure = None):
    try:
        data = dict(data)
        
        message = data.get("message")
        if message:
            return {"message":message}
        return {"error":"make message as key."}
    except Exception as ex:
        return {"error":f"{type(ex)},{ex}"}



if __name__ == "__main__":
    uvicorn.run("main:app",port=8080,log_level="info")
