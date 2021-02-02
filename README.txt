O programa em questão é responsável por receber o body de uma requisição http e armazená-la em um arquivo CSV.

Os campos obrigatórios do body são:

    id: int
    save_type: str
    data: dict
    consult_data: bool

Os campos id, save_type e data serão armazenados cada um em sua respectiva coluna no arquivo CSV. Já o campo consult_data
recebe os valores True ou False e responsável pela consulta dos dados da tabela.

A função create_item é chamada toda vez que uma nova requisição é enviada. Nela o arquivo .csv é criado caso ele não exista ainda,
e ocorre a inclusão de novos itens no aquivo caso ele ja exista. Para que o item seja adicionado na tabela, é necessário que o id dele ainda não
esteja contido nela. Para isso, tem-se a função verify_id, que é responsável por verificar se o novo id recebido pela nova requisição
ainda não existe na tabela. Caso o novo id não exista, os dados serão armazenados no arquivo .csv, caso o novo id já exista a função id_erro
será chamada, o que gerará uma resposta de 422 na requisição e os dados não serão armazenados.

Caso o usuário queira consultar algum dado na tabela, basta passar o campo consult_data como true. Dessa forma a função consult_file
será chamada, solicitando que o usuário	informe se deseja consultar apenas uma linha, uma linha e coluna específica ou a tabela completa. 
Após o usuário informar os dados necessários ele poderá escolher se deseja realizar uma nova consulta ou se deseja modificar algum dado específico.
É importante ressaltar que caso consult_data esteja como true, os dados contidos nos outros campos não serão adicionados na tabela.

Caso o usuário deseje modificar algum dado, a função change_data_in_file será chamada e solicitará que o usuário informe a linha e a
coluna do dado que deseja modificar e em seguida o que será colocado nessa posição.

Para rodar o código é necessário executar o seguinte comando no terminal linux

uvicorn main:app --reload

Para fazer as requisições basta adicionar o url informado na primeira linha de excecução do comando uvicorn adicionado de um "/items"
("http://127.0.0.1:8000/items") além disso é preciso adicionar o bloco de código abaixo no body da requisição:

{
    "id": "1",
    "save_type": "csv",
    "data": {"key1" : "value"},
    "consult_data": "false"
}

Além disso, para rodar o programa é necessário que se tenha instalado:
 
pandas - pip install pandas
pydantic - pip install pydantic
fastapi - pip install fastapi
uvicorn - pip install uvicorn
