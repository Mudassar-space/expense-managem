import imp
from typing import List
from fastapi import Depends, FastAPI, Response, status
from sqlalchemy.orm import Session

from . import models, schemas
from .database import SessionLocal, engine
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
app=FastAPI()


models.Base.metadata.create_all(engine)
def get_db():

    db=SessionLocal()

    try:

        yield db

    finally:
        db.close()
        

@app.post('/categories', tags=['categories'], status_code=status.HTTP_201_CREATED, response_model=schemas.Cate_response_model,
                           responses={
                           status.HTTP_400_BAD_REQUEST: {"model":  schemas.Responses},
                           status.HTTP_422_UNPROCESSABLE_ENTITY: {"model":  schemas.Responses},
                           status.HTTP_500_INTERNAL_SERVER_ERROR: {"model":  schemas.Responses}})
def create(request:schemas.Categories,db:Session=Depends(get_db)):
    new_category=models.CategoriesTableSchema(created_on=request.created_on, name=request.name, user_id=request.user_id)
    try:
        db.add(new_category)
        db.commit()
        db.refresh(new_category)
        return JSONResponse(status_code=status.HTTP_201_CREATED, content =jsonable_encoder(new_category))
    except Exception:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content =jsonable_encoder(schemas.Responses))


@app.get('/categories/{Id}',tags=['categories'], responses={status.HTTP_200_OK: {"model": schemas.Cate_response_model},
                           status.HTTP_404_NOT_FOUND: {"model": schemas.Responses},
                           status.HTTP_422_UNPROCESSABLE_ENTITY: {"model":  schemas.Responses},
                           status.HTTP_500_INTERNAL_SERVER_ERROR: {"model":  schemas.Responses}})
def show(Id:int,db:Session=Depends(get_db)):
    category=db.query(models.CategoriesTableSchema).filter(models.CategoriesTableSchema.category_Id==Id).first()
    if not category:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content = jsonable_encoder(schemas.Responses(status=False, message="Not found")))
    try:
        return JSONResponse(status_code=status.HTTP_200_OK, content = jsonable_encoder(category))
    except Exception:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content =jsonable_encoder(schemas.Responses))


@app.get('/categories',tags=['categories'], responses={status.HTTP_200_OK: {"model": List[schemas.Cate_response_model]},
                           status.HTTP_422_UNPROCESSABLE_ENTITY: {"model":  schemas.Responses},
                           status.HTTP_500_INTERNAL_SERVER_ERROR: {"model":  schemas.Responses}})
def all(db:Session=Depends(get_db)):
    categories=db.query(models.CategoriesTableSchema).all()
    try:
        return JSONResponse(status_code=status.HTTP_200_OK, content = jsonable_encoder(categories))
    except Exception:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content =jsonable_encoder(schemas.Responses))


@app.put('/categories/{id}', tags=['categories'], responses={status.HTTP_200_OK: {"model": schemas.Categories},
                           status.HTTP_404_NOT_FOUND: {"model": schemas.Responses},
                           status.HTTP_400_BAD_REQUEST: {"model": schemas.Responses},
                           status.HTTP_422_UNPROCESSABLE_ENTITY: {"model":  schemas.Responses},
                           status.HTTP_500_INTERNAL_SERVER_ERROR: {"model":  schemas.Responses}})
def update(id:str, ques:schemas.Categories, db:Session=Depends(get_db)):
    data = ques.dict()
    result = db.query(models.CategoriesTableSchema).filter(models.CategoriesTableSchema.category_Id==id).update(data)
    db.commit()
    if not result:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=jsonable_encoder(schemas.Responses(status=False, message="Not found")))
    try:
        if result==1:
            return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(data))
    except Exception:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content =jsonable_encoder(schemas.Responses))
    


@app.delete('/categories/{id}',tags=['categories'], status_code= status.HTTP_204_NO_CONTENT, responses={
                           status.HTTP_404_NOT_FOUND: {"model": schemas.Responses},
                           status.HTTP_400_BAD_REQUEST: {"model": schemas.Responses},
                           status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": schemas.Responses},
                           status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": schemas.Responses}})
def Destroy(id,db:Session=Depends(get_db)):
    deleted=db.query(models.CategoriesTableSchema).filter(models.CategoriesTableSchema.category_Id==id).delete(synchronize_session=False)
    db.commit()
    if not deleted:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content = jsonable_encoder(schemas.Responses(status=False, message="Not found")))
    try:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except Exception:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content =jsonable_encoder(schemas.Responses))


@app.post('/users',status_code=201,tags=['users'], response_model=schemas.User_response, responses={
                           status.HTTP_400_BAD_REQUEST: {"model":  schemas.Responses},
                           status.HTTP_422_UNPROCESSABLE_ENTITY: {"model":  schemas.Responses},
                           status.HTTP_500_INTERNAL_SERVER_ERROR: {"model":  schemas.Responses}})
def create(user:schemas.User,db:Session=Depends(get_db)):
    new_user=models.User(name=user.name,email=user.email,created_at=user.created_at)
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return JSONResponse(status_code=status.HTTP_201_CREATED, content =jsonable_encoder(new_user))
    except Exception:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content =jsonable_encoder(schemas.Responses))
    

@app.get('/users/{Id}', tags=['users'], responses={status.HTTP_200_OK: {"model": schemas.User_response},
                           status.HTTP_404_NOT_FOUND: {"model": schemas.Responses},
                           status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": schemas.Responses},
                           status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": schemas.Responses}})
def show(Id:int, db:Session=Depends(get_db)):
    user=db.query(models.User).filter(models.User.user_id==Id).first()
    if not user:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content = jsonable_encoder(schemas.Responses(status=False, message="Not found")))
    try:
        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(user)) 
    except Exception:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content =jsonable_encoder(schemas.Responses))
    


@app.get('/users', tags=['users'], responses={status.HTTP_200_OK: {"model": List[schemas.User_response]},
                           status.HTTP_422_UNPROCESSABLE_ENTITY: {"model":  schemas.Responses},
                           status.HTTP_500_INTERNAL_SERVER_ERROR: {"model":  schemas.Responses}})
def all(db:Session=Depends(get_db)):
    user=db.query(models.User).all()
    try:
        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(user))
    except Exception:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content =jsonable_encoder(schemas.Responses))


@app.put('/users/{id}',tags=['users'], responses={status.HTTP_200_OK: {"model": schemas.User},
                           status.HTTP_404_NOT_FOUND: {"model": schemas.Responses},
                           status.HTTP_400_BAD_REQUEST: {"model": schemas.Responses},
                           status.HTTP_422_UNPROCESSABLE_ENTITY: {"model":  schemas.Responses},
                           status.HTTP_500_INTERNAL_SERVER_ERROR: {"model":  schemas.Responses}})
def update(id: int, ques: schemas.User, db: Session=Depends(get_db)):
    data = ques.dict()
    user = db.query(models.User).filter(models.User.user_id==id).update(data)
    db.commit()
    if not user:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=jsonable_encoder(schemas.Responses(status=False, message="Not found")))
    try:
        if user==1:
            return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(data))
    except Exception:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content =jsonable_encoder(schemas.Responses))


@app.delete('/users/{id}',tags=['users'],status_code= status.HTTP_204_NO_CONTENT, responses={
                           status.HTTP_404_NOT_FOUND: {"model": schemas.Responses},
                           status.HTTP_400_BAD_REQUEST: {"model": schemas.Responses},
                           status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": schemas.Responses},
                           status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": schemas.Responses}})
def Destroy(id,db:Session=Depends(get_db)):

    deleted=db.query(models.User).filter(models.User.user_id==id).delete(synchronize_session=False)
    db.commit()
    if not deleted:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content = jsonable_encoder(schemas.Responses(status=False, message="Not found")))
    try:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except Exception:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content =jsonable_encoder(schemas.Responses))


@app.post('/accounts',status_code=201,tags=['accounts'],  response_model=schemas.Account_response,
                        responses={
                           status.HTTP_400_BAD_REQUEST: {"model":  schemas.Responses},
                           status.HTTP_422_UNPROCESSABLE_ENTITY: {"model":  schemas.Responses},
                           status.HTTP_500_INTERNAL_SERVER_ERROR: {"model":  schemas.Responses}})
def create(account:schemas.Account,db:Session=Depends(get_db)):
    new_account=models.Account(account_name=account.account_name, initial_balance=account.initial_balance, type=account.type, user_id=account.user_id, created_at=account.created_at)
    try:
        db.add(new_account)
        db.commit()
        db.refresh(new_account)
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=jsonable_encoder(new_account))
    except Exception:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=jsonable_encoder(schemas.Responses))


@app.get('/accounts', tags=['accounts'], responses={status.HTTP_200_OK: {"model": List[schemas.Account_response]},
                           status.HTTP_422_UNPROCESSABLE_ENTITY: {"model":  schemas.Responses},
                           status.HTTP_500_INTERNAL_SERVER_ERROR: {"model":  schemas.Responses}})
def all(db:Session=Depends(get_db)):
    account=db.query(models.Account).all()
    try:
        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(account))
    except Exception:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=jsonable_encoder(schemas.Responses))


@app.get('/accounts/{Id}',tags=['accounts'],responses={status.HTTP_200_OK: {"model": schemas.Account_response},
                           status.HTTP_404_NOT_FOUND: {"model": schemas.Responses},
                           status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": schemas.Responses},
                           status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": schemas.Responses}})
def show(Id:int,db:Session=Depends(get_db)):
    account=db.query(models.Account).filter(models.Account.account_id==Id).first()
    if not account:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content = jsonable_encoder(schemas.Responses(status=False, message="Not found")))
    try:
        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(account)) 
    except Exception:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=jsonable_encoder(schemas.Responses))


@app.put('/accounts{id}',tags=['accounts'],responses={status.HTTP_200_OK: {"model": schemas.Account},
                           status.HTTP_404_NOT_FOUND: {"model": schemas.Responses},
                           status.HTTP_400_BAD_REQUEST: {"model": schemas.Responses},
                           status.HTTP_422_UNPROCESSABLE_ENTITY: {"model":  schemas.Responses},
                           status.HTTP_500_INTERNAL_SERVER_ERROR: {"model":  schemas.Responses}})
def update(id:int,para:schemas.Account,db:Session=Depends(get_db)):
    data=para.dict()
    account=db.query(models.Account).filter(models.Account.account_id==id).update(data)
    db.commit()
    if not account:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=jsonable_encoder(schemas.Responses(status=False, message="Not found")))
    try:
        if account==1:
            return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(data))
    except Exception:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=jsonable_encoder(schemas.Responses))


@app.delete('/accounts{id}',tags=['accounts'],status_code= status.HTTP_204_NO_CONTENT, responses={
                           status.HTTP_404_NOT_FOUND: {"model": schemas.Responses},
                           status.HTTP_400_BAD_REQUEST: {"model": schemas.Responses},
                           status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": schemas.Responses},
                           status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": schemas.Responses}})
def delete(id,db:Session=Depends(get_db)):
    deleted=db.query(models.Account).filter(models.Account.account_id==id).delete(synchronize_session=False)
    db.commit()
    if not deleted:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content = jsonable_encoder(schemas.Responses(status=False, message="Not found")))
    try:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except Exception:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=jsonable_encoder(schemas.Responses))


@app.post('/ledgers',status_code=201,tags=['ledgers'],  response_model=schemas.Ledger,
                        responses={
                           status.HTTP_400_BAD_REQUEST: {"model":  schemas.Responses},
                           status.HTTP_422_UNPROCESSABLE_ENTITY: {"model":  schemas.Responses},
                           status.HTTP_500_INTERNAL_SERVER_ERROR: {"model":  schemas.Responses}})
def create(ledger:schemas.Ledger,db:Session=Depends(get_db)):
    new_ledger=models.Ledger(amount=ledger.amount, account_id=ledger.account_id, category_Id=ledger.category_Id, user_id=ledger.user_id, transaction=ledger.transaction, transfer_to=ledger.transfer_to, created_at=ledger.created_at)
    try:
        db.add(new_ledger)
        db.commit()
        db.refresh(new_ledger)
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=jsonable_encoder(new_ledger))
    except Exception:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=jsonable_encoder(schemas.Responses))
    

@app.get('/ledgers/{Id}', tags=['ledgers'], responses={status.HTTP_200_OK: {"model": schemas.Ledger},
                           status.HTTP_404_NOT_FOUND: {"model": schemas.Responses},
                           status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": schemas.Responses},
                           status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": schemas.Responses}})
def show(Id:int, db:Session=Depends(get_db)):
    ledger=db.query(models.Ledger).filter(models.Ledger.ledger_id==Id).first()
    if not ledger:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content = jsonable_encoder(schemas.Responses(status=False, message="Not found")))
    try:
        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(ledger)) 
    except Exception:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content =jsonable_encoder(schemas.Responses))



@app.get('/ledgers', tags=['ledgers'], responses={status.HTTP_200_OK: {"model": List[schemas.Ledger]},
                           status.HTTP_422_UNPROCESSABLE_ENTITY: {"model":  schemas.Responses},
                           status.HTTP_500_INTERNAL_SERVER_ERROR: {"model":  schemas.Responses}})
def all(db:Session=Depends(get_db)):
    ledgers=db.query(models.Ledger).all()
    try:
        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(ledgers))
    except Exception:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=jsonable_encoder(schemas.Responses))
    


@app.put('/ledgers{id}',tags=['ledgers'],responses={status.HTTP_200_OK: {"model": schemas.Ledger},
                           status.HTTP_404_NOT_FOUND: {"model": schemas.Responses},
                           status.HTTP_400_BAD_REQUEST: {"model": schemas.Responses},
                           status.HTTP_422_UNPROCESSABLE_ENTITY: {"model":  schemas.Responses},
                           status.HTTP_500_INTERNAL_SERVER_ERROR: {"model":  schemas.Responses}})
def update(id:int,para:schemas.Ledger,db:Session=Depends(get_db)):
    data=para.dict()
    ledger=db.query(models.Ledger).filter(models.Ledger.ledger_id==id).update(data)
    db.commit()
    if not ledger:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=jsonable_encoder(schemas.Responses(status=False, message="Not found")))
    try:
        if ledger==1:
            return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(data))
    except Exception:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=jsonable_encoder(schemas.Responses))



@app.delete('/ledgers{id}',tags=['ledgers'],status_code= status.HTTP_204_NO_CONTENT, responses={
                           status.HTTP_404_NOT_FOUND: {"model": schemas.Responses},
                           status.HTTP_400_BAD_REQUEST: {"model": schemas.Responses},
                           status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": schemas.Responses},
                           status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": schemas.Responses}})
def delete(id,db:Session=Depends(get_db)):
    deleted=db.query(models.Ledger).filter(models.Ledger.ledger_id==id).delete(synchronize_session=False)
    db.commit()
    if not deleted:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content = jsonable_encoder(schemas.Responses(status=False, message="Not found")))
    try:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except Exception:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=jsonable_encoder(schemas.Responses))

