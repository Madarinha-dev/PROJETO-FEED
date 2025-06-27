from flask import Flask, render_template, request, jsonify, redirect, url_for
import sqlite3

# POSSÍCEIS ATUALIZAÇÕES

# ideia nova: e se o ADM só quiser ver algumas colunas específicas da tabela
# sem necessariamente precisar visualizar ela por inteiro

# Na tabela 'atividades' na coluna 'status' mudar para o sistema binário 0 / 1
# 0 = não realizado, 1 = realizado, isso ajudaria na coontagem de atividades realizadas,
# atividades não realizadas, ajudaria a ter um total de atividades

# sistema estatístico: um painél montando o total de cada 'informação' talvez
# ou um quadro como se fosse um gráfico.


app = Flask(__name__)
lista = []



def conectar_db():
    conectar = sqlite3.connect("banco.db")
    return conectar



def criar_tabela():
    conectar = conectar_db()
    cursor = conectar.cursor()
    cursor.execute('''
CREATE TABLE IF NOT EXISTS funcionarios_cadastrados (
                   id_funcionario INTEGER PRIMARY KEY AUTOINCREMENT,
                   nome TEXT VARCHAR(255),
                   senha TEXT VARCHAR(255),
                   cpf int varchar(255),
                   funcao varchar(255) 
                   );
''')
    conectar.commit()
    conectar.close()



def criar_tabela_atividade():
    conectar = conectar_db()
    cursor = conectar.cursor()
    cursor.execute('''
CREATE TABLE IF NOT EXISTS atividades (
  id_atividade INTEGER PRIMARY KEY AUTOINCREMENT,
  tipo_de_servico TEXT VARCHAR(255),
  descricao TEXT VARCHAR(255),
  quem TEXT VARCHAR(255),
  armazenna TEXT VARCHAR(255),
  empresa TEXT VARCHAR(255),
  data TEXT VARCHAR(255),
  STATUS TEXT VARCHAR(255) DEFAULT 'N Realizado'
);
''')
    conectar.commit()
    conectar.close()






@app.route('/')
def index():
    return render_template('index.html')





@app.route('/frequencia', methods=['POST'])
def frequencia():
    registro = request.get_json()
    
    r = {
        "nome": registro.get('nome'), 
        "funcao": registro.get('funcao'),
        "dia":registro.get('dia'),
        "mes":registro.get('mes'),
        "ano":registro.get('ano'),
        "hora":registro.get('hora'),
        "minuto":registro.get('minuto'),
        "segundo":registro.get('segundo')
        }
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")

    lista.append(r)


    # contador = 0
    # se fosse banco de dados mesmo:
    # nome = r["nome"]
    # for x in lista:
    #  if nome == x:
    #   contador = contador + 1

    sid = 0
    fhellype = 0
    bruno = 0
    julio = 0
    c = 0

    for elemento in lista:
        print("")
        print(f'O C: {c}')
        print("")
        # print(f'Elemento: {elemento}')
        print(f'Data: {elemento["dia"]}/{elemento["mes"]}/{elemento["ano"]} | Hora: {elemento["hora"]}:{elemento["minuto"]}:{elemento["segundo"]} | {elemento["nome"]} - {elemento["funcao"]}')
        if elemento["nome"] == 'sid':
            sid = sid + 1
            if sid > 1:
                print("eliminando..")
                lista.pop(c)
                

        elif elemento["nome"] == 'julio':
            julio = julio + 1
            if julio > 1:
                print("eliminando..")
                lista.pop(c)
                

        elif elemento["nome"] == 'bruno':
            bruno = bruno + 1
            if bruno > 1:
                print("eliminando..")
                lista.pop(c)
                

        elif elemento["nome"] == 'fhellype':
            fhellype = fhellype + 1
            if fhellype > 1:
                print("eliminando..")
                lista.pop(c)
        c = c + 1
                
    print("")
    print("")
    print("LISTA:")
    for i in lista:
        print(f'Data: {i["dia"]}/{i["mes"]}/{i["ano"]} | Hora: {i["hora"]}:{i["minuto"]}:{i["segundo"]} | {i["nome"]} - {i["funcao"]}')

    # print(f'Fhellype: {fhellype}, Sid: {sid}, Julio: {julio}, Bruno: {bruno}')
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")

    




#  REFAZER ESSA ESTRUTURA DEPOIS QUE O BANCO DE DADOS COMEÇAR A SER INSTALADO;
@app.route('/recuperar-senha', methods=['POST'])
def recuperar():

    dados = request.get_json()
    cpf = dados.get('cpff')
    
    # BANCO DE SIMULAÇÃO, SOFRER ALTERAÇÃO QUANDO O REAL VIER;
    pessoas = [ 
        {"nome":"FHELLYPE","senha":"1984","funcao": "pintura", "cpf":"16811949457"},
        {"nome":"JULIO","senha":"2025","funcao":"telhado", "cpf":"01"},
        {"nome":"BRUNO","senha":"1984", "funcao":"eletrica", "cpf":"02"},
        {"nome":"SID", "senha":"2025", "funcao":"adm", "cpf":"03"}
        ]
    
    for r in pessoas:
        # print(r)
        if cpf == r['cpf']:
            nome = r['nome']
            senha = r['senha']
            dado = 1

    if dado == 1:
        return jsonify({
            "recado":"Dados-localizados",
            "nome":nome,
            "senha":senha
        }), 200
    else:
        return jsonify({
            "recado":"nao-localizado"
        }), 200
    





# aqui uma função importante, pós ela vai ser o referêncial para login, recuperação e consulta;
@app.route('/cadastrar_funcionario', methods=['POST'])
def cadastrar_funcionario():
    dados = request.get_json()
    criar_tabela()
    conectar = conectar_db()
    cursor = conectar.cursor()

    cursor.execute('INSERT INTO funcionarios_cadastrados (nome, senha, cpf, funcao) VALUES (?, ?, ?, ?)', (dados['nome'], dados['senhaa'], dados['cpf'], dados['funcao']))
    conectar.commit()
    conectar.close()

    return jsonify({
        'msg':'01'
    }), 200



@app.route('/adicionarAtividade', methods=['POST'])
def adicionarAtividade():
    dados = request.get_json()
    criar_tabela_atividade()
    conectar = conectar_db()
    cursor = conectar.cursor()
    cursor.execute('INSERT INTO atividades (tipo_de_servico, descricao, quem, armazenna, empresa, data) VALUES (?, ?, ?, ?, ?, ?)', (dados['tipoDeservico'], dados['descricao'], dados['quem'], dados['armazenna'], dados['empresa'], dados['data']))
    conectar.commit()
    conectar.close()
    return jsonify({
        'msg':'01'
    }), 200






@app.route('/excluirFuncionario', methods=['POST'])
def excluirFuncionario():
    dados = request.get_json()
    id = dados['id']

    conectar = conectar_db()
    cursor = conectar.cursor()
    cursor.execute("SELECT id_funcionario FROM funcionarios_cadastrados WHERE id_funcionario = ?", (id,))
    funcionario = cursor.fetchone()
    
    if funcionario is None:
        conectar.commit()
        conectar.close()

        return jsonify({
            'msg':"0"
        }), 200
    
    else:
        cursor.execute("DELETE FROM funcionarios_cadastrados WHERE id_funcionario = ?", (id,))
        conectar.commit()
        conectar.close()

        return jsonify({
            "msg":'1'
        }), 200
    
@app.route('/excluiratividade', methods=['POST'])
def excluiratividade():
    dados = request.get_json()
    id = dados['id_atividade']
    conectar = conectar_db()
    cursor = conectar.cursor()
    cursor.execute("SELECT id_atividade FROM atividades WHERE id_atividade = ?", (id,))
    atividade = cursor.fetchone()

    if atividade is None:
        conectar.commit()
        conectar.close()
        return jsonify({
            "msg":"0"
        }), 200
    
    else:
        cursor.execute("DELETE FROM atividades WHERE id_atividade = ?", (id, ))
        conectar.commit()
        conectar.close()
        return jsonify({
            "msg":"1"
        }), 200



@app.route('/alterarfuncionario', methods=['POST'])
def alterarfuncionario():
    novosdados = request.get_json()

    id = novosdados['id']
    nomenovo = novosdados['nome']
    senhanovo = novosdados['senha']
    cpfnovo = novosdados['cpf']
    funcaonovo = novosdados['funcao']

    conectar = conectar_db()
    cursor = conectar.cursor()
    cursor.execute("SELECT id_funcionario, nome, senha, cpf, funcao FROM funcionarios_cadastrados WHERE id_funcionario = ?", (id,))

    velhosdados = cursor.fetchone()
    nomevelho = velhosdados[1]
    senhavelho = velhosdados[2]
    cpfvelho = velhosdados[3]
    funcaovelho = velhosdados[4]

    if nomenovo == '':
        print("nome vazio")
    else:
        nomevelho = nomenovo

    if senhanovo == '':
        print("senha vazia")
    else:
        senhavelho = senhanovo

    if cpfnovo == '':
        print("CPF vazio")
    else:
        cpfvelho = cpfnovo

    if funcaonovo == '':
        print("Função vazio")
    else:
        funcaovelho = funcaonovo

    
    cursor.execute("UPDATE funcionarios_cadastrados SET nome = ?, senha = ?, cpf = ?, funcao = ? WHERE id_funcionario = ?", (nomevelho, senhavelho, cpfvelho, funcaovelho, id))
    # select * from funcionarios_cadastrados order by cpf
    # cursor.execute("SELECT * FROM funcionarios_cadastrados ORDER BY ?", (cpfvelho,))
    conectar.commit()
    conectar.close()

    return jsonify({
        'msg':'1'
    }), 200

@app.route('/alterarAtividade', methods=['POST'])
def alterarAtividade():
    print("(")
    print("(")
    print("(")
    print("(")
    print("(")
    print("(")
    print("(")
    print("(")
    print("(")
    print("(")
    # dados: {'id': '4', 'servico': '', 'descricao': '', 'pessoas': 'BERG e IVO', 'armazenna': 'armazenna01', 'empresa': '', 'data': '', 'status': ''}
    dadosnovos = request.get_json()
    id = dadosnovos['id']
    servicoatual = dadosnovos['servico']
    desscricaoatual = dadosnovos['descricao']
    pessoaatual = dadosnovos['pessoas']
    armazennaatual = dadosnovos['armazenna']
    empresaatual = dadosnovos['empresa']
    dataatual = dadosnovos['data']
    statusatual = dadosnovos['status']

    conectar = conectar_db()
    cursor = conectar.cursor()
    cursor.execute("SELECT * FROM atividades WHERE id_atividade = ?", (id, ))
    tabela = cursor.fetchone()
    print(f'atualizar: {dadosnovos}')
    print('')
    print(f'dados atuais: {tabela}')
    print('')

    if tabela is None:
        print('vazio')
    else:
        id = tabela[0]
        servico = tabela[1]
        descricao = tabela[2]
        pessoa = tabela[3]
        armazenna = tabela[4]
        empresa = tabela[5]
        data = tabela[6]
        status = tabela[7]
        
        if servicoatual == '':
            print('serviço vazio')
        else:
            servico = servicoatual
        
        if desscricaoatual == '':
            print('descrição vazio')
        else:
            descricao = desscricaoatual
        
        if pessoaatual == '':
            print('pessoa vazio')
        else:
            pessoa = pessoaatual
        
        if armazennaatual == '':
            print('armazenna vazio')
        else:
            armazenna = armazennaatual

        if empresaatual == '':
            print('empresa vazio')
        else:
            empresa = empresaatual
        
        if dataatual == '':
            print('data vazio')
        else:
            data = dataatual

        if statusatual == '':
            print('status vazio')
        else:
            status = statusatual
        # cursor.execute("UPDATE funcionarios_cadastrados SET nome = ?, senha = ?, cpf = ?, funcao = ? WHERE id_funcionario = ?", (nomevelho, senhavelho, cpfvelho, funcaovelho, id))
        cursor.execute("UPDATE atividades SET id_atividade = ?, tipo_de_servico = ?, descricao = ?, quem = ?, armazenna = ?, empresa = ?, data = ?, STATUS = ? WHERE id_atividade = ?", (id, servico, descricao, pessoa, armazenna, empresa, data, status, id))
        conectar.commit()
        conectar.close()
        print(f'dados atualizado PORRAAAAAA')
    # [(4, 'mecanica', 'Tomada queimada ', 'Bruno, Janderson', 'armazenna02', 'XXXX', '2025-07-08', 'N Realizado')]
    
    

    return jsonify({
        'msg':'0',
        'texto':'ID não localizado...'
    }), 200
        


@app.route('/ordenarfuncionarios', methods=['POST'])
def ordenarfuncionarios():
    dados = request.get_json()
    print(")")
    print(")")
    print(")")
    print(")")
    print(")")
    print(")")
    print(f'dados informados: {dados}')
    conectar = conectar_db()
    cursor = conectar.cursor()

    if dados['ordenar_por'] == 'nome':
        cursor.execute("SELECT * FROM funcionarios_cadastrados ORDER BY nome")

    elif dados['ordenar_por'] == 'senha':
        cursor.execute("SELECT * FROM funcionarios_cadastrados ORDER BY senha")
    
    elif dados['ordenar_por'] == 'cpf':
        cursor.execute("SELECT * FROM funcionarios_cadastrados ORDER BY cpf")

    elif dados['ordenar_por'] == 'funcao':
        cursor.execute("SELECT * FROM funcionarios_cadastrados ORDER BY funcao")
    else:
        cursor.execute("SELECT * FROM funcionarios_cadastrados ORDER BY id_funcionario")

    orde = cursor.fetchall()
    # print("")
    # print(f'ORDE: {orde}')
    # print("")

    # for a in orde:
    #     print(f'id {a[0]} Nome: {a[1]} Senha: {a[2]} CPF: {a[3]} Função: {a[4]}')
    # print("")

    dados_para_json = []
    for a in orde:

        dicionario = {
            "id": a[0],
            "nome": a[1],
            "senha": a[2],
            "cpf": a[3],
            "funcao": a[4]
        }
        dados_para_json.append(dicionario)

    # print("")
    # print("teste")
    # print(f'DADOS PARA JSON: {dados_para_json}')
    return jsonify(dados_para_json), 200
    




    



# rota que vai receber os dados la da tela de login
@app.route('/receber_dados', methods=['POST'])
def receber_dados():
    dados_recebidos = request.get_json()

    nome = dados_recebidos.get('nome').upper()
    senha = dados_recebidos.get('senhar')

    pessoas = [ 
        {"nome":"FHELLYPE","senha":"1984","funcao": "pintura", "cpf":"16811949457"},
        {"nome":"JULIO","senha":"2025","funcao":"telhado", "cpf":"01"},
        {"nome":"BRUNO","senha":"1984", "funcao":"eletrica", "cpf":"02"},
        {"nome":"SID", "senha":"2025", "funcao":"adm", "cpf":"03"}
        ]
    
    for r in pessoas:
        # print(r)
        if nome == r["nome"] and senha == r["senha"]:
            funcao = r["funcao"]
            dado = 1

    if dado == 1:
        return jsonify({
        "status":"sucesso",
        "texto":"001",
        "funcao":funcao
        }), 200
    else:
        return jsonify({
            "status":"negado",
            "texto":"000",
            "funcao":"vazio"
        }), 200

@app.route('/tela02')
def tela02():
    return render_template('tela02.html')

@app.route('/pintura')
def pintura():
    return render_template('pintura.html')

@app.route('/eletrica')
def eletrica():
    return render_template('eletrica.html')

@app.route('/mecanica')
def mecanica():
    return render_template('mecanica.html')

@app.route('/telhado')
def telhado():
    return render_template('telhado.html')




@app.route('/adm')
def adm():
    return render_template('adm.html')






if __name__ == '__main__':
    app.run(debug=True)
