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
                   cpf TEXT VARCHAR(255),
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
  id_atividade INTEGER,
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



@app.route('/excluirRegistro', methods=['POST'])
def excluirRegistro():

    conectar = None
    
    try:
        dados = request.get_json()
        print(f'Dados: {dados}')
        alt = int(dados['alt'])
        conectar = conectar_db()
        cursor = conectar.cursor()
        cursor.execute('DELETE FROM registro WHERE id_registro = ?', (alt, ))
        conectar.commit()
        # conectar.close()
        print('REGISTRO DELETADO')
        return jsonify({
            'success':True,
            'msg':'REGISTRO DELETADO COM SUCESSO'
        }), 200

    except Exception as erro:
        if conectar:
            conectar.rollback()

        print('ERRO DETECTADO FUNÇÃO: FUNÇÃO EXCLUIR REGISTRO')
        print(f'o Tipo de erro: {type(erro)}')
        print(f'Descrição do erro: {str(erro)}')

        return jsonify({
            'success':False,
            'msg':'ERRO ao tentar excluir o registro'
        }), 500
    
    finally:
        if conectar:
            conectar.close()


    


@app.route('/registro_das_atividades_adm', methods=['GET'])
def exibir_registros():
    conectar = None
    
    try: 
        conectar = conectar_db()
        cursor = conectar.cursor()
        cursor.execute("SELECT * FROM registro ORDER BY id_atividade;")
        tabela = cursor.fetchall()
        lista_json = []

        for registro in tabela:
            dicionario = {
                'id_registro':registro[0],
                'id_atividade':registro[1],
                'legenda':registro[2],
                'foto':f"data:image/jpeg;base64,{base64.b64encode(registro[3]).decode('utf-8')}"
            }
            lista_json.append(dicionario)
        # return jsonify(lista_json), 200
        return jsonify({
            'success':True,
            'dados':lista_json,
            'msg':'Comunicação realizada com a API'
        }), 200
    
    except Exception as erro:
        if conectar:
            conectar.rollback()

        print(f'ERRO DETECTADO, FUNÇÃO: REGISTRO DAS ATIVIDADES ADM')
        print(f'TIPO DO ERRO: {type(erro)}')
        print(f'DESCRIÇÃO: {str(erro)}')

        return jsonify({
            'msg':'ERRO ao exibir os registros',
            'success':False
        }), 500
    
    finally:
        if conectar:
            conectar.close()




@app.route('/album_de_fotos_das_atividades', methods=['POST'])
def album():
    conectar = None
    
    try:
        dados = request.get_json()
        tabelaRegistro() #caso ela n exista vai ser criada essa tabela
        conectar = conectar_db()
        cursor = conectar.cursor()
        
        for a in dados:
            print(f'ID: {a["id"]}')
            print(f'LEGENDA: {a["legenda"]}')
            print('=')
            id = int(a['id'])
            legenda = str(a['legenda'])

            imagem_base64_com_prefixo = a['imagemData']
            _, encoded_image = imagem_base64_com_prefixo.split(',', 1)
            imagem_bytes = base64.b64decode(encoded_image) #imagem em formato binário

            cursor.execute("INSERT INTO registro (id_atividade, legenda, img) VALUES (?, ?, ?);", (id, legenda, imagem_bytes))
        conectar.commit()

        return jsonify({
            'success':True,
            'msg':'FUNÇÃO DE ADICIONAR A IMAGEM NO BANCO DE DADOS = OK'
        }), 200
    
    except Exception as erro:
        if conectar:
            conectar.rollback()

        print(f'ERRO DETECTADO, FUNÇÃO: ALBUM')
        print(f'TIPO DO ERRO: {type(erro)}')
        print(f'DESCRIÇÃO: {str(erro)}')

        return jsonify({
            'success':False,
            'msg':'ERRO AO GUARDAR AS IMAGEM NO BANCO DE DADOS = ERRO'
        }), 500
    
    finally:
        if conectar:
            conectar.close()

        

@app.route('/exibir_tabela_frequencia', methods=['GET'])
def exibir_tabela_frequencia():
    conectar = None

    try:
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
        return jsonify({
            'success':True,
            'msg':'Frequência coletada',
            'dados':nova_lista
        }), 200
    
    except Exception as erro:
        if conectar:
            conectar.rollback()
        
        print(f'ERRO DETECTADO, FUNÇÃO: EXIBIR A TABELA FREQUÊNCIA')
        print(f'TIPO DO ERRO: {type(erro)}')
        print(f'DESCRIÇÃO: {str(erro)}')
        print('=')

        return jsonify({
            'success': False,
            'msg':'Erro ao coletar a frequência da tabela'
        }), 500

    finally:
        if conectar:
            conectar.close()




@app.route('/limparFrequencia', methods=['POST'])
def limparFrequencia():
    
    conectar = None
    try:
        conectar = conectar_db()
        cursor = conectar.cursor()
        cursor.execute("DELETE FROM frequencia")
        conectar.commit()

        return jsonify({
            "success":True,
            "msg":"Frequência Limpa com successo"
        }), 200

    except Exception as erro:
        if conectar:
            conectar.rollback()

        print('=============================================')
        print(f'ERRO DETECTADO, FUNÇÃO: LIMPAR FREQUÊNCIA')
        print(f'TIPO DO ERRO: {type(erro)}')
        print(f'DESCRIÇÃO: {str(erro)}')
        print('=============================================')

        return jsonify({
            "success":False,
            "msg":"Erro ao Limpar a frequência"
        }), 500


    finally:
        if conectar:
            conectar.close()



       

@app.route('/frequencia', methods=['POST'])
def frequencia():
    
    conectar = None

    try:
        print('caso de certo')
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

        return jsonify({
            "success":True,
            "msg":"Frequência registrada com successo"
        }), 200

    except Exception as erro:
        if conectar:
            conectar.rollback()

        print('=============================================')
        print(f'ERRO DETECTADO, FUNÇÃO: FREQUÊNCIA')
        print(f'TIPO DO ERRO: {type(erro)}')
        print(f'DESCRIÇÃO: {str(erro)}')
        print('=============================================')

        return jsonify({
            "success": False,
            "msg":"Falha ao registrar a frequência"
        }), 500

    finally:
        if conectar:
            conectar.close()






@app.route('/recuperar-senha', methods=['GET'])
def recuperar():
    conectar = None

    try:
        # dados = request.get_json()
        # cpf = dados.get('cpff')
        cpf = request.args.get('cpf')

        if not cpf:
            return jsonify({
                "success":False,
                "msg":"CPF é obrigatório para recuperação. Por favor forneça um CPF"
            }), 400 # FOI ENVIADA UMA REQUISIÇÃO INVÁLIDA

        conectar = conectar_db()
        cursor = conectar.cursor()
        cursor.execute("SELECT * FROM funcionarios_cadastrados WHERE cpf = ?", (cpf, ))
        registro = cursor.fetchone()
        print(f'Registro: {registro}')

        if registro is None:
            return jsonify({
                "success":False,
                "msg":"CPF não encontrado em nossos registros. Verifique o CPF novamente"
            }), 404 # O RECURSO NÃO EXISTE
        
        else:
            return jsonify({
                "success":True,
                "msg":"Registro localizado. Seu nome de usuário foi preenchido",
                "nome":registro[1]
            }), 200

    except Exception as erro:
        if conectar:
            conectar.rollback()

        print('=============================================')
        print(f'ERRO DETECTADO, FUNÇÃO: RECUPERAR SENHA')
        print(f'TIPO DO ERRO: {type(erro)}')
        print(f'DESCRIÇÃO: {str(erro)}')
        print('=============================================')

        return jsonify({
            "success":False,
            "msg":"Erro ao executar a função"
        }), 500

    finally:
        if conectar:
            conectar.close()



    
    

# aqui uma função importante, pós ela vai ser o referêncial para login, recuperação e consulta;
@app.route('/cadastrar_funcionario', methods=['POST'])
def cadastrar_funcionario():
    conectar = None

    try:
        dados = request.get_json()
        criar_tabela()
        conectar = conectar_db()
        cursor = conectar.cursor()

        if type(dados.get('nome')) is not str or not dados.get('nome').strip():
            return jsonify({
                "success":False,
                "msg":"Campo nome vázio ou tipo de dado inválido"
            }), 400
        
        
        if type(dados.get('senhaa')) is not str or not dados.get('senhaa').strip():
            return jsonify({
                "success":False,
                "msg":"Campo senha vázio ou tipo de dado inválido"
            }), 400
        
        
        cpf = dados.get('cpf')
        if type(cpf) is not str:
            return jsonify({
                "success":False,
                "msg":"tipo de dado inválido"
            }), 400
        cpf_limpo = cpf.replace('.','').replace('-','').replace(' ','')
        

        if not cpf_limpo.strip():
            return jsonify({
                "success":False,
                "msg":"CPF não pode ser vazio"
            }), 400
        
        
        if not cpf_limpo.isdigit():
            return jsonify({
                "success":False,
                "msg":"O CPF deve conter apenas números"
            }), 400
        

        if len(cpf_limpo) != 11:
            return jsonify({
                "success":False,
                "msg":"Quantidade inválida de dígitos"
            }), 400

        
        if type(dados.get('funcao')) is not str or not dados.get('funcao').strip():
            return jsonify({
                "success":False,
                "msg":"Campo FUNÇÃO vázio ou tipo de dado inválido"
            }), 400

        cursor.execute('INSERT INTO funcionarios_cadastrados (nome, senha, cpf, funcao) VALUES (?, ?, ?, ?)', (dados['nome'], dados['senhaa'], cpf_limpo, dados['funcao']))
        conectar.commit()

        return jsonify({
            "success":True,
            "msg":"Dados processados e guardados com Success"
        }), 200

    except Exception as erro:
        if conectar:
            conectar.rollback()

        print('=============================================')
        print(f'ERRO DETECTADO, FUNÇÃO: CADASTRAR FUNCIONÁRIO')
        print(f'TIPO DO ERRO: {type(erro)}')
        print(f'DESCRIÇÃO: {str(erro)}')
        print('=============================================')

        return jsonify({
            "success":False,
            "msg":"Erro ao executar a função"
        }), 500

    finally:
        if conectar:
            conectar.close()






@app.route('/adicionarAtividade', methods=['POST'])
def adicionarAtividade():
    conectar = None

    try:
        dados = request.get_json()
        criar_tabela_atividade()
        conectar = conectar_db()
        cursor = conectar.cursor()

        if type(dados.get('tipoDeservico')) is not str or not dados.get('tipoDeservico').strip():
            return jsonify({
                "success":False,
                "msg":"o Input do tipo de serviço tem que ser do tipo texto"
            }), 400
        
        if type(dados.get('descricao')) is not str or not dados.get('descricao').strip():
            return jsonify({
                "success":False,
                "msg":"o Input descrição tem que ser do tipo TEXT"
            }), 400
        
        if type(dados.get('quem')) is not str or not dados.get('quem').strip():
            return jsonify({
                "success":False,
                "msg":"o Input QUEM tem que ser do tipo TEXT"
            }), 400
        
        if type(dados.get('armazenna')) is not str or not dados.get('armazenna').strip():
            return jsonify({
                "success":False,
                "msg":"o Input armazenna tem que ser do tipo TEXT"
            }), 400
        
        if type(dados.get('empresa')) is not str or not dados.get('empresa').strip():
            return jsonify({
                "success":False,
                "msg":"o Input Empresa tem que ser do tipo TEXT"
            }), 400
        
        if type(dados.get('data')) is not str or not dados.get('data').strip():
            return jsonify({
                "success":False,
                "msg":"o Input Data tem que ser do tipo Text ou convertido para texto"
            }), 400


        cursor.execute('INSERT INTO atividades (tipo_de_servico, descricao, quem, armazenna, empresa, data) VALUES (?, ?, ?, ?, ?, ?)', (dados.get('tipoDeServico'), dados.get('descricao'), dados.get('quem'), dados.get('armazenna'), dados.get('empresa'), dados.get('data')))
        conectar.commit()

        return jsonify({
            "success":True,
            "msg":"Função adicionar atividade realizada com success"
        }), 200

    except Exception as erro:
        if conectar:
            conectar.rollback()

        print('=============================================')
        print(f'ERRO DETECTADO, FUNÇÃO: ADICIONAR ATIVIDADE')
        print(f'TIPO DO ERRO: {type(erro)}')
        print(f'DESCRIÇÃO: {str(erro)}')
        print('=============================================')

        return jsonify({
            "success":False,
            "msg":"Erro ao executar a função"
        }), 500


    finally:
        if conectar:
            conectar.close()




@app.route('/excluirFuncionario', methods=['POST'])
def excluirFuncionario():
    
    conectar = None

    try:
        dados = request.get_json()
        id = dados.get('id')

        if id is None:
            return jsonify({
                "success":False,
                "msg":"o ID não foi fornecido"
            }), 400

        
        try:
            id_convertido = int(id)

        except ValueError:
            return jsonify({
                "success":False,
                "msg":"ID do funcionário inválido, Deve ser um número inteiro"
            }), 400

        
        conectar = conectar_db()
        cursor = conectar.cursor()
        cursor.execute("SELECT id_funcionario FROM funcionarios_cadastrados WHERE id_funcionario = ?", (id_convertido,))
        funcionario = cursor.fetchone()

        if funcionario is None:
            return jsonify({
                "success":False,
                "msg":f"Funcionário com o ID: ${id} não foi encontrado."
            }), 404
        
        
        cursor.execute("DELETE FROM funcionarios_cadastrados WHERE id_funcionario = ?", (id_convertido,))
        conectar.commit()


        return jsonify({
            "success":True,
            "msg":"Registro do funcionário localizado e deletado com success"
        }), 200
        

    except Exception as erro:
        if conectar:
            conectar.rollback()

        print('=============================================')
        print(f'ERRO DETECTADO, FUNÇÃO: EXCLUIR FUNCIONÁRIO')
        print(f'TIPO DO ERRO: {type(erro)}')
        print(f'DESCRIÇÃO: {str(erro)}')
        print('=============================================')

        return jsonify({
            "success":False,
            "msg":"Erro ao executar a função EXCLUIR FUNCIONÁRIO"
        }), 500

    finally:
        if conectar:
            conectar.close()
    




@app.route('/excluiratividade', methods=['POST'])
def excluiratividade():
    conectar = None

    try:
        dados = request.get_json()
        id = dados.get('id_atividade')

        if id is None:
            return jsonify({
                "success":False,
                "msg":"O ID não foi fornecido"
            }), 400
        
        try: 
            id_convertido = int(id)

        except ValueError:
            return jsonify({
                "success":False,
                "msg":"ID da atividade são inválidos, Deve ser um número do tipo inteiro"
            }), 400
        
        conectar = conectar_db()
        cursor = conectar.cursor()
        cursor.execute("SELECT id_atividade FROM atividades WHERE id_atividade = ?", (id_convertido,))
        atividade = cursor.fetchone()

        if atividade is None:
            return jsonify({
                "success":False,
                "msg":f'Atividade com o ID: {id} não encontrado.'
            }), 400
        
        cursor.execute("DELETE FROM atividades WHERE id_atividade = ?", (id_convertido, ))
        conectar.commit()

        return jsonify({
            "success":True,
            "msg":f"Atividade de ID: {id} deletada com sucesso"
        }), 200
        
    except Exception as erro:
        if conectar:
            conectar.rollback()

        print('=============================================')
        print(f'ERRO DETECTADO, FUNÇÃO: EXCLUIR ATIVIDADE')
        print(f'TIPO DO ERRO: {type(erro)}')
        print(f'DESCRIÇÃO: {str(erro)}')
        print('=============================================')

        return jsonify({
            "success":False,
            "msg":"Erro ao executar a função EXCLUIR ATIVIDADE"
        }), 500

    finally:
        if conectar:
            conectar.close()













































# @app.route('/alterarfuncionario', methods=['POST'])
# def alterarfuncionario():
#     novosdados = request.get_json()
#     print(')')
#     print(')')
#     print(')')
#     print('FUNÇÃO ALTERAR FUNCIONÁRIO')
#     print(')')
#     print(')')
#     print(')')

#     id = novosdados['id']
#     nomenovo = novosdados['nome']
#     senhanovo = novosdados['senha']
#     cpfnovo = novosdados['cpf']
#     funcaonovo = novosdados['funcao']

#     conectar = conectar_db()
#     cursor = conectar.cursor()
#     cursor.execute("SELECT id_funcionario, nome, senha, cpf, funcao FROM funcionarios_cadastrados WHERE id_funcionario = ?", (id,))

#     velhosdados = cursor.fetchone()
#     nomevelho = velhosdados[1]
#     senhavelho = velhosdados[2]
#     cpfvelho = velhosdados[3]
#     funcaovelho = velhosdados[4]

#     if nomenovo == '':
#         print("nome vazio")
#     else:
#         nomevelho = nomenovo

#     if senhanovo == '':
#         print("senha vazia")
#     else:
#         senhavelho = senhanovo

#     if cpfnovo == '':
#         print("CPF vazio")
#     else:
#         cpfvelho = cpfnovo

#     if funcaonovo == '':
#         print("Função vazio")
#     else:
#         funcaovelho = funcaonovo

    
#     cursor.execute("UPDATE funcionarios_cadastrados SET nome = ?, senha = ?, cpf = ?, funcao = ? WHERE id_funcionario = ?", (nomevelho, senhavelho, cpfvelho, funcaovelho, id))
#     conectar.commit()
#     conectar.close()

#     return jsonify({
#         'msg':'1'
#     }), 200






















































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

    conectar = None
    try:
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
                "success":True,
                "msg":"ACESSO EMERGÊNCIAL",
                "texto":"001",
                "funcao":funcao
            }), 200
        
        elif funcionarios is None:
            return jsonify({
                "success":False,
                "msg":"Dados Inválidos ou campo vazio, tente novamente"
            }), 401
        
        else:
            funcao = funcionarios[4]
            return jsonify({
                "success":True,
                "msg":"LOGIN CONCEDIDO",
                "texto":"001",
                "funcao":funcao
            }), 200
        
        

    except Exception as erro:
        if conectar:
            conectar.rollback()

        print('=============================================')
        print(f'ERRO DETECTADO, FUNÇÃO: RECEBER DADOS')
        print(f'TIPO DO ERRO: {type(erro)}')
        print(f'DESCRIÇÃO: {str(erro)}')
        print('=============================================')

        return jsonify({
            "success":False,
            "msg":"Erro ao processar os dados"
        }), 500


    finally:
        if conectar:
            conectar.close()


    


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
