from flask import Flask, render_template, request, jsonify, redirect, url_for
import sqlite3
import base64

# POSSÍCEIS ATUALIZAÇÕES

# mudar a cor das atividades que tiver com o ID = 1, to pensando  numa maneira
# que acho que vai da certo.

# ideia nova: e se o ADM só quiser ver algumas colunas específicas da tabela
# sem necessariamente precisar visualizar ela por inteiro

# Na tabela 'atividades' na coluna 'status' mudar para o sistema binário 0 / 1
# 0 = não realizado, 1 = realizado, isso ajudaria na coontagem de atividades realizadas,
# atividades não realizadas, ajudaria a ter um total de atividades

# sistema estatístico: um painél montando o total de cada 'informação' talvez
# ou um quadro como se fosse um gráfico.



# administrativo
# seguranca
# eletrica
# mecanica
# pintura
# telhado


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






def tabelaRegistro():
    conectar = conectar_db()
    cursor = conectar.cursor()
    cursor.execute('''
CREATE TABLE IF NOT EXISTS registro (
  id_registro INTEGER PRIMARY KEY AUTOINCREMENT,
  id_atividade TEXT,
  legenda TEXT,
  img BLOB
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
  STATUS TEXT VARCHAR(255) DEFAULT '0'
);
''')
    conectar.commit()
    conectar.close()



def criar_tabela_frequencia():
    conectar = conectar_db()
    cursor = conectar.cursor()
    cursor.execute('''
CREATE TABLE IF NOT EXISTS frequencia (
    id_frequencia INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT VARCHAR(40),
    data TEXT VARCHAR(20),
    hora TEXT VARCHAR(12),
    funcao TEXT VARCHAR(20)
);
''')
    conectar.commit()
    conectar.close()






@app.route('/')
def index():
    print(')')
    print(')')
    print(')')
    print('FUNÇÃO >>> / <<<')
    print(')')
    print(')')
    print(')')
    return render_template('index.html')

@app.route('/registro_das_atividades_adm', methods=['POST'])
def exibir_registros():
    print(')(')
    print(')(')
    print(')(')
    print(')(')
    print('  FUNÇÃO EXIBIR REGISTRO NO ADM')

    conectar = conectar_db()
    cursor = conectar.cursor()
    cursor.execute("SELECT * FROM registro ORDER BY id_atividade;")
    tabela = cursor.fetchall()
    lista_json = []
    # futuramente colocar a hora exatada de cada foto, da pra fazer isso, para nos informar a hora exatada que foi tirada a foto

    for registro in tabela:
        dicionario = {
            'id_registro':registro[0],
            'id_atividade':registro[1],
            'legenda':registro[2],
            'foto': f"data:image/jpeg;base64,{base64.b64encode(registro[3]).decode('utf-8')}"
        }
        lista_json.append(dicionario)

    conectar.commit()
    conectar.close()
    return jsonify(lista_json), 200


    # return jsonify({
    #     'msg':'por enquanto só mensagem'
    # }), 200
    
    print(')(')
    print(')(')
    print(')(')



@app.route('/album_de_fotos_das_atividades', methods=['POST'])
def album():
    dados = request.get_json()
    print('()')
    print('()')
    print('()')
    print('()')
    print('()')
    print('()')
    print(' FUNÇÃO /ALBUM DE FOTOS DAS ATIVIDADES')
    print('()')
    print('()')
    print('()')
    print('()')
    print('()')

    tabelaRegistro()
    conectar = conectar_db()
    cursor = conectar.cursor()

    for a in dados:
        print('')
        print(f' - ID: {a["id"]}')
        print(f' - LEGENDA: {a["legenda"]}')
        # id = int(a['id'])
        id = a['id']
    
        # legenda = str(a["legenda"])
        legenda = a['legenda']

        imagem_base64_com_prefixo = a['imagemData']
        _, encoded_image = imagem_base64_com_prefixo.split(',', 1)
        imagem_bytes = base64.b64decode(encoded_image) #imagem em formato binário

        cursor.execute("INSERT INTO registro (id_atividade, legenda, img) VALUES (?, ?, ?);", (id, legenda, imagem_bytes))
        print('')

    conectar.commit()
    conectar.close()


    print('()')
    print('()')
    print('()')
    print('()')
    print('()')
    print('()')
    print('()')
    print('()')
    print('()')
    print('()')
    print('()')




@app.route('/exibir_tabela_frequencia', methods=['POST'])
def exibir_tabela_frequencia():
    dados = request.get_json()

    conectar = conectar_db()
    cursor = conectar.cursor()
    cursor.execute("SELECT * FROM frequencia")
    tabela = cursor.fetchall()

    nova_lista = []
    for a in tabela:
        dicionario = {
            'id':a[0],
            'nome':a[1],
            'data':a[2],
            'tempo':a[3],
            'funcao':a[4]
        }
        nova_lista.append(dicionario)
    conectar.commit()
    conectar.close()
    return jsonify(nova_lista), 200



@app.route('/limparFrequencia', methods=['POST'])
def limparFrequencia():
    conectar = conectar_db()
    cursor = conectar.cursor()
    cursor.execute("DELETE FROM frequencia")
    conectar.commit()
    conectar.close()

    return jsonify({
        'msg':'comando eliminar comfirmado'
    }), 200




@app.route('/frequencia', methods=['POST'])
def frequencia():
    print(')')
    print(')')
    print(')')
    print('FUNÇÃO FREQUÊNCIA')
    print(')')
    print(')')
    print(')')
    registro = request.get_json()

    nome = registro.get('nome')
    data = (f"{str(registro.get('dia'))}/{str(registro.get('mes'))}/{str(registro.get('ano'))}")
    tempo = (f"{str(registro.get('hora'))}:{str(registro.get('minuto'))}:{str(registro.get('segundo'))}")
    funcao = registro.get('funcao')
    

    criar_tabela_frequencia()
    conectar = conectar_db()
    cursor = conectar.cursor()
    cursor.execute("INSERT INTO frequencia (nome, data, hora, funcao) VALUES (?, ?, ?, ?)", (nome, data, tempo, funcao))
    conectar.commit()
    conectar.close()


@app.route('/recuperar-senha', methods=['POST'])
def recuperar():
    print(')')
    print(')')
    print(')')
    print('FUNÇÃO RECUPERAR SENHA')
    print(')')
    print(')')
    print(')')

    dados = request.get_json()
    cpf = dados.get('cpff')
    
    conectar = conectar_db()
    cursor = conectar.cursor()
    cursor.execute("SELECT * FROM funcionarios_cadastrados WHERE cpf = ?", (cpf, ))
    registro = cursor.fetchone()
    print(f'registro {registro}')

    if registro is None:
        return jsonify({
            'recado':'nao-localizado'
        }), 200
    
    else:
        return jsonify({
            'recado':'Dados-localizados',
            'nome':registro[1],
            'senha':registro[2]
        }), 200
    
    


# aqui uma função importante, pós ela vai ser o referêncial para login, recuperação e consulta;
@app.route('/cadastrar_funcionario', methods=['POST'])
def cadastrar_funcionario():
    print(')')
    print(')')
    print(')')
    print('FUNÇÃO CADASTRAR FUNCIONARIO')
    print(')')
    print(')')
    print(')')
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
    print(')')
    print(')')
    print(')')
    print('FUNÇÃO ADICIONAR ATIVIDADE')
    print(')')
    print(')')
    print(')')
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
    print(')')
    print(')')
    print(')')
    print('FUNÇÃO EXCLUIR FUNCIONÁRIO')
    print(')')
    print(')')
    print(')')
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
    print(')')
    print(')')
    print(')')
    print('FUNÇÃO EXCLUIR ATIVIDADE')
    print(')')
    print(')')
    print(')')
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
    print(')')
    print(')')
    print(')')
    print('FUNÇÃO ALTERAR FUNCIONÁRIO')
    print(')')
    print(')')
    print(')')

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
    conectar.commit()
    conectar.close()

    return jsonify({
        'msg':'1'
    }), 200

@app.route('/alterarAtividade', methods=['POST'])
def alterarAtividade():
    print(')')
    print(')')
    print(')')
    print('FUNÇÃO ALTERAR ATIVIDADE')
    print(')')
    print(')')
    print(')')

   
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


    if tabela is None:
        conectar.commit()
        conectar.close()
        
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
            print('Armazenna vazio')
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
            
        cursor.execute("UPDATE atividades SET id_atividade = ?, tipo_de_servico = ?, descricao = ?, quem = ?, armazenna = ?, empresa = ?, data = ?, STATUS = ? WHERE id_atividade = ?", (id, servico, descricao, pessoa, armazenna, empresa, data, status, id))
        conectar.commit()
        conectar.close()
        
    return jsonify({
        'msg':'ignore',
        'texto':'ignora esse return, se der errado, vai mostrar de outra forma, obg...'
    }), 200

@app.route('/ordenarAtividades', methods=['POST'])
def ordenarAtividades():
    dados = request.get_json()
    orde = dados['ordenar_por']
    print(')')
    print(')')
    print(')')
    print('FUNÇÃO ORDENAR ATIVIDADES')
    print(')')
    print(')')
    print(f'dados: {dados}')
    print('')
    print(f'Ordenar por: {orde}')
    print('aqui vou montar a lógica para ordenar os dados e mandar para o FRONT END')

    conectar = conectar_db()
    cursor = conectar.cursor()

    if orde == 'id_atividade':
        cursor.execute("SELECT * FROM atividades ORDER BY id_atividade")

    elif orde == 'tipo_de_servico':
        cursor.execute("SELECT * FROM atividades ORDER BY tipo_de_servico")

    elif orde == 'descricao':
        cursor.execute("SELECT * FROM atividades ORDER BY descricao")

    elif orde == 'quem':
        cursor.execute("SELECT * FROM atividades ORDER BY quem")

    elif orde == 'armazenna':
        cursor.execute("SELECT * FROM atividades ORDER BY armazenna")

    elif orde == 'empresa':
        cursor.execute("SELECT * FROM atividades ORDER BY empresa")

    elif orde == 'data':
        cursor.execute("SELECT * FROM atividades ORDER BY data")

    elif orde == 'STATUS':
        cursor.execute("SELECT * FROM atividades ORDER BY STATUS")
    else:
        cursor.execute("SELECT * FROM atividades ORDER BY id_atividade") 

    ordenado = cursor.fetchall()
    nova_lista = []
    for a in ordenado:
        dicionario = {
            'id_atividade':a[0],
            'tipo_de_servico':a[1],
            'descricao':a[2],
            'quem':a[3],
            'armazenna':a[4],
            'empresa':a[5],
            'data':a[6],
            'status':a[7]
        }
        nova_lista.append(dicionario)

    return jsonify(nova_lista), 200
        


@app.route('/ordenarfuncionarios', methods=['POST'])
def ordenarfuncionarios():
    dados = request.get_json()
    print(")")
    print(")")
    print('FUNção /ordernarFuncionarios')
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

    return jsonify(dados_para_json), 200
    

@app.route('/mostrar_atividades', methods=['POST'])
def mostrar_tabela_eletrica():
    dados = request.get_json()
    print(')(')
    print(')(')
    print(')(')
    # print(f'DADOS: {dados}')
    # DADOS: {'msg': 'atividades de elétrica'}

    conectar = conectar_db()
    cursor = conectar.cursor()


    dados_para_json = []

    if dados['msg'] == 'atividades de elétrica':
        cursor.execute("SELECT id_atividade, descricao, quem, armazenna, empresa, data, STATUS FROM atividades WHERE tipo_de_servico = 'ELÉTRICA'")
        resultado = cursor.fetchall()
        
        
    elif dados['msg'] == 'atividades de mecanica':
        cursor.execute("SELECT id_atividade, descricao, quem, armazenna, empresa, data, STATUS FROM atividades WHERE tipo_de_servico = 'MECÂNICA'" )
        resultado = cursor.fetchall()


    elif dados['msg'] == 'atividades de pintura':
        cursor.execute("SELECT id_atividade, descricao, quem, armazenna, empresa, data, STATUS FROM atividades WHERE tipo_de_servico = 'PINTURA'")
        resultado = cursor.fetchall()


    elif dados['msg'] == 'atividades de telhado':
        cursor.execute("SELECT id_atividade, descricao, quem, armazenna, empresa, data, STATUS FROM atividades WHERE tipo_de_servico = 'TELHADO'")
        resultado = cursor.fetchall()


    # caso especial pós eu preciso de todas as áreas
    # elif dados['msg'] == 'atividades de relatório':
    #     cursor.execute("")

    elif dados['msg'] == 'atividades de montagem':
        cursor.execute("SELECT id_atividade, descricao, quem, armazenna, empresa, data, STATUS FROM atividades WHERE tipo_de_servico = 'MONTAGEM'")
        resultado = cursor.fetchall()

    for a in resultado:
        dicionario = {
            'id':a[0],
            'descricao':a[1],
            'quem':a[2],
            'armazenna':a[3],
            'empresa':a[4],
            'data':a[5],
            'status':a[6]
        }
        dados_para_json.append(dicionario)
    return jsonify(dados_para_json), 200




# rota que vai receber os dados la da tela de login
@app.route('/receber_dados', methods=['POST'])
def receber_dados():
    dados_recebidos = request.get_json()

    nome = dados_recebidos.get('nome')
    senha = dados_recebidos.get('senhar')
    conectar = conectar_db()
    cursor = conectar.cursor()
    cursor.execute("SELECT * FROM funcionarios_cadastrados WHERE nome = ? AND senha = ?", (nome, senha))
    funcionarios = cursor.fetchone()
    print(f'Funcionários: {funcionarios}')
    
    if nome == 'none' and senha == 'none':
        funcao = 'adm'
        return jsonify({
            "status":"sucesso",
            "texto":"001",
            "funcao":funcao
        }), 200
    
    elif funcionarios is None:
        print(')')
        print("vazio ou dados inválidos")
        print(')')
        return jsonify({
            "status":"errado 647 - pyton"
        }), 200
    
    else:
        print(')')
        print(f'Dados: {funcionarios}')
        print(')')
        funcao = funcionarios[4]
        
        return jsonify({
            "status":"sucesso",
            "texto":"001",
            "funcao":funcao
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
