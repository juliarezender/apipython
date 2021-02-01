from fastapi import FastAPI, Response, status
from pydantic import BaseModel
import csv
import pandas as pd
            
class Item(BaseModel):
    id: int
    save_type: str
    data: dict
    consult_data: bool

def change_data_in_file(response):
    df_open = pd.read_csv('data.csv')
    df_open.drop(df_open.filter(regex="Unnamed"),axis=1, inplace=True)

    row = int(input("Digite o número da linha que deseja alterar: "))
    column = input("Digite o nome da coluna que deseja alterar (ID, TYPE, DATA): ")
    column = column.upper()
    new_value = input("Digite o que quer colocar no lugar: ")
    if column == "ID":
        if not verify_id(new_value):
            id_erro(response)
    old_value = df_open.loc[row][column]
    df_open[column] = df_open[column].replace([old_value], new_value)          

    df_open.to_csv('data.csv')

def consult_file(response):
    new_consult = 1
    while new_consult:
        try:
            df_open = pd.read_csv('data.csv')
            df_open.drop(df_open.filter(regex="Unnamed"),axis=1, inplace=True)

            consult = int(input("Digite 1 se deseja consultar uma linha completa, 2 se deseja " 
                                + "consultar uma linha e coluna ou 3 se deseja visualizar a tabela completa: "))
            if consult == 1:
                row = int(input("Digite o número da linha que deseja consultar: "))
                print(df_open.loc[row])
            elif consult == 2:
                row = int(input("Digite o número da linha que deseja consultar: "))
                column = input("Digite o nome da coluna que deseja alterar (ID, TYPE, DATA):  ")
                print(df_open.loc[row][column])
            elif consult == 3:
                print(df_open)

            new_consult = int(input("Fazer nova consulta? 1 para sim 0 para não. "))
            if not new_consult:
                change_data = int(input("Deseja modificar algum dados? 1 para sim 0 para não. "))
                if change_data:
                    change_data_in_file(response)
        except FileNotFoundError:
            response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY

def verify_id(id):
    df_open = pd.read_csv('data.csv')
    df_open.drop(df_open.filter(regex="Unnamed"),axis=1, inplace=True)
    for row in df_open.iterrows():
        if row[1][0] == id:
            return False
    return True

def id_erro(response):
    print("ID já existente, informe outro ID")
    response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        
app = FastAPI()

@app.post("/items/")
async def create_item(item: Item, response: Response):
    if item.consult_data:
        consult_file(response)
    
    else:
        data = [item.id, item.save_type, item.data]

        columns = ('ID', 'TYPE', 'DATA')
        try:
            df_open = pd.read_csv('data.csv')
            df_open.drop(df_open.filter(regex="Unnamed"),axis=1, inplace=True)
            if df_open.empty: 
                first_data_frame = pd.DataFrame(data=data, index=columns).T
                first_data_frame.to_csv('data.csv')

            else:
                if verify_id(item.id):
                    df_intermediate = pd.DataFrame(data=data, index=columns).T
                    df = pd.concat([df_open, df_intermediate])
                    df.to_csv('data.csv')
                else: 
                    id_erro(response)     

        except FileNotFoundError:
            first_data_frame = pd.DataFrame(data=data, index=columns).T
            first_data_frame.to_csv('data.csv')
    



    return item
