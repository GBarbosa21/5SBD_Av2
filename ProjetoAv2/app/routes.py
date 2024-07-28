from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from .models import Carga, Clientes, Produtos, ItensPedidos, Pedidos, Estoque, Entregas
from .database import SessionLocal
from typing import List
from pydantic import BaseModel
from datetime import date, timedelta
import logging


router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/cargas")
def get_cargas(db: Session = Depends(get_db)):
    try:
        cargas = db.query(Carga).all()
        return cargas
    except Exception as e:
        return {"error": f"Erro ao buscar cargas: {str(e)}"}

@router.get("/cargas/{id}")
def get_carga(id: int, db: Session = Depends(get_db)):
    carga = db.query(Carga).filter(Carga.Id_cargas == id).first()
    if carga is None:
        raise HTTPException(status_code=404, detail="Carga not found")
    return carga

# Função para verificar e inserir clientes
def insert_client_from_carga(db: Session, cliente_email: str, cliente_nome: str, cliente_cpf: int):
    try:
        # Verifica se o cliente já existe na tabela Clientes
        cliente_existente = db.query(Clientes).filter_by(email_cl=cliente_email).first()

        # Se não existir, insere o cliente
        if not cliente_existente:
            novo_cliente = Clientes(
                nome_cl=cliente_nome,
                email_cl=cliente_email,
                Cpf_cl=cliente_cpf
            )
            db.add(novo_cliente)
            db.commit()
            print(f"Cliente inserido: {cliente_nome}")

    except IntegrityError as e:
        db.rollback()
        print(f"Erro de integridade: {e}")

    except Exception as e:
        db.rollback()
        print(f"Erro ao inserir cliente: {e}")

@router.post("/inserir_clientes")
def inserir_clientes(db: Session = Depends(get_db)):
    try:
        # Busca todas as cargas
        cargas = db.query(Carga).all()

        #Procura sobre as cargas e insere os clientes que ainda não estiverem cadastrados
        for carga in cargas:
            insert_client_from_carga(db, carga.email, carga.nomeComprador, carga.Cpf)

        return {"message": "Dados inseridos com sucesso!"}

    except Exception as e:
        db.rollback()
        return {"error": f"Erro ao inserir dados: {e}"}

    finally:
        db.close()

@router.get("/clientes")
def get_clientes(db: Session = Depends(get_db)):
    clientes = db.query(Clientes).all()
    return clientes

@router.get("/clientes/{id}")
def get_cliente(id: int, db: Session = Depends(get_db)):
    cliente = db.query(Clientes).filter(Clientes.Id_cliente == id).first()
    if cliente is None:
        raise HTTPException(status_code=404, detail="Cliente not found")
    return cliente
    
def insert_Produto_from_carga(db: Session, nome_produto: str, preco_produto: float, sku: int, upc: int):
    try:
        # Verifica se o produto já existe na tabela Produtos
        produto_existente = db.query(Produtos).filter_by(SKU=sku).first()

        # Se não existir, insere o produto
        if not produto_existente:
            novo_produto = Produtos(
                nome_produto=nome_produto,
                preco_produto=preco_produto,
                SKU=sku,
                UPC=upc,
            )
            db.add(novo_produto)
            db.commit()
            print(f"Produto inserido: {nome_produto}")

    except IntegrityError as e:
        db.rollback()
        print(f"Erro de integridade: {e}")

    except Exception as e:
        db.rollback()
        print(f"Erro ao inserir produto: {e}")

@router.post("/inserir_produtos")
def inserir_produtos(db: Session = Depends(get_db)):
    try:
        # Busca todas as cargas
        cargas = db.query(Carga).all()

        #Procura sobre as cargas e insere os clientes que ainda não estiverem cadastrados
        for carga in cargas:
            insert_Produto_from_carga(db, carga.nome_produto, carga.preco_produto, carga.SKU, carga.UPC)

        return {"message": "Dados inseridos com sucesso!"}

    except Exception as e:
        db.rollback()
        return {"error": f"Erro ao inserir dados: {e}"}

    finally:
        db.close()

@router.get("/produtos")
def get_produtos(db: Session = Depends(get_db)):
    produtos = db.query(Produtos).all()
    return produtos

@router.get("/produtos/{id}")
def get_produto(id: int, db: Session = Depends(get_db)):
    produto = db.query(Produtos).filter(Produtos.Id_produto == id).first()
    if produto is None:
        raise HTTPException(status_code=404, detail="Produto not found")
    return produto

def insert_item_pedido_from_carga(db: Session, carga):
    try:
        produto = db.query(Produtos).filter_by(SKU=carga.SKU).first()
        if not produto:
            raise HTTPException(status_code=404, detail=f"Produto com SKU {carga.SKU} não encontrado")

        novo_item_pedido = ItensPedidos(
            cod_pedido=carga.cod_pedido,
            id_produto=produto.Id_produto,
            Qntd_produto=carga.Qntd_produto
        )
        db.add(novo_item_pedido)
        db.commit()
        print(f"Item de pedido inserido para o pedido {carga.cod_pedido}")
    except IntegrityError as e:
        db.rollback()
        print(f"Erro de integridade: {e}")
    except Exception as e:
        db.rollback()
        print(f"Erro ao inserir item de pedido: {e}")

@router.post("/inserir_itens_pedido")
def inserir_itens_pedido(db: Session = Depends(get_db)):
    try:
        cargas = db.query(Carga).all()
        for carga in cargas:
            insert_item_pedido_from_carga(db, carga)
        return {"message": "Itens de pedido inseridos com sucesso!"}
    except Exception as e:
        db.rollback()
        return {"error": f"Erro ao inserir itens de pedido: {e}"}
    finally:
        db.close()

@router.get("/itensPedidos")
def get_ItensPedido(db: Session = Depends(get_db)):
    itens = db.query(ItensPedidos).all()
    return itens

@router.get("/ItensPedido/{cod_pedido}")
def get_produto(cod_pedido: int, db: Session = Depends(get_db)):
    item = db.query(ItensPedidos).filter(ItensPedidos.cod_pedido == cod_pedido).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Produto not found")
    return item

@router.get("/Pedidos")
def get_Pedido(db: Session = Depends(get_db)):
    pedidos = db.query(Pedidos).all()
    return pedidos

def insert_pedido_from_carga(db: Session, carga: Carga):
    try:
        # Verifica se o cliente existe pelo email na carga
        cliente = db.query(Clientes).filter(Clientes.email_cl == carga.email).first()
        if not cliente:
            raise HTTPException(status_code=404, detail=f"Cliente com email {carga.email} não encontrado")

        # Cria um novo pedido
        novo_pedido = Pedidos(
            data_pedido=carga.data_pedido,
            id_cliente=cliente.Id_cliente,
            total_pedido=0.0  # Inicializa com 0, será atualizado depois
        )
        db.add(novo_pedido)
        db.commit()

        # Adiciona os itens do pedido
        itemPedido = db.query(ItensPedidos).filter_by(cod_pedido=carga.cod_pedido).first()
        if not itemPedido:
            raise HTTPException(status_code=404, detail=f"Itens de pedido não encontrados para o pedido {carga.cod_pedido}")

        novo_item_pedido = ItensPedidos(
            cod_pedido=novo_pedido.cod_pedido,
            id_produto=itemPedido.id_produto,
            Qntd_produto=carga.Qntd_produto
        )
        db.add(novo_item_pedido)

        # Calcula e atualiza o total do pedido
        novo_pedido.total_pedido = calcular_total_pedido(novo_pedido.cod_pedido, db)
        db.commit()

        print(f"Pedido {novo_pedido.cod_pedido} inserido com sucesso.")
    except IntegrityError as e:
        db.rollback()
        print(f"Erro de integridade ao inserir pedido: {e}")
        raise HTTPException(status_code=400, detail="Erro de integridade ao inserir pedido")
    except Exception as e:
        db.rollback()
        print(f"Erro ao inserir pedido: {e}")
        raise HTTPException(status_code=500, detail="Erro ao inserir pedido")

def calcular_total_pedido(pedido_id: int, db: Session):
    itens = db.query(ItensPedidos).filter(ItensPedidos.cod_pedido == pedido_id).all()
    if not itens:
        logging.warning(f"No itens found for pedido ID {pedido_id}")
        return 0.0
    total = sum(item.Qntd_produto * item.produto.preco_produto for item in itens)
    return total

@router.post("/inserir_pedido")
def inserir_pedido(db: Session = Depends(get_db)):
    try:
        cargas = db.query(Carga).all()
        for carga in cargas:
            insert_pedido_from_carga(db, carga)
        return {"message": "Pedidos inseridos com sucesso!"}
    except Exception as e:
        db.rollback()
        return {"error": f"Erro ao inserir pedido: {e}"}
    finally:
        db.close()

@router.get("/estoque")
def get_Estoque(db: Session = Depends(get_db)):
    estoque = db.query(Estoque).all()
    return estoque

@router.get("/entregas")
def get_Entregas(db: Session = Depends(get_db)):
    entregas = db.query(Entregas).all()
    return entregas
        
# Função para inserir entregas a partir de cargas e verificar estoque
def insert_entregas_from_carga(db: Session, carga: Carga):
    try:
        # Verifica se o pedido existe pelo id na Pedidos
        pedido = db.query(Pedidos).filter(Pedidos.cod_pedido == carga.cod_pedido).first()
        if not pedido:
            raise HTTPException(status_code=404, detail=f"Pedido com código {carga.cod_pedido} não encontrado")

        # Calcula a data de entrega
        data_entrega = pedido.data_pedido + timedelta(days=7)

        # Verifica e atualiza o estoque
        produtos_disponiveis = True
        itens_carga = db.query(Carga).filter(Carga.cod_pedido == carga.cod_pedido).all()
        
        for item in itens_carga:
            produto = db.query(Produtos).filter(Produtos.SKU == item.SKU).first()
            estoque = db.query(Estoque).filter(Estoque.id_produto == produto.SKU).first()
            if not estoque or estoque.qntd_estoque < item.qntd:
                produtos_disponiveis = False
                break

        if produtos_disponiveis:
            for item in itens_carga:
                produto = db.query(Produtos).filter(Produtos.SKU == item.SKU).first()
                estoque = db.query(Estoque).filter(Estoque.id_produto == produto.SKU).first()
                estoque.qntd_estoque -= item.qntd
            status_entrega = "1"  # Sucesso
        else:
            status_entrega = "2"  # Falha

        # Cria uma nova entrega
        nova_entrega = Entregas(
            cod_pedido=pedido.cod_pedido,
            nome_comprador=carga.nomeComprador,  # Ajustar para o campo correto do modelo Pedidos
            endereco=carga.endereco,
            data_entrega=data_entrega,
            status_entrega=status_entrega
        )
        db.add(nova_entrega)
        db.commit()

        print(f"Pedido {nova_entrega.cod_pedido} inserido com sucesso.")
    except IntegrityError as e:
        db.rollback()
        print(f"Erro de integridade ao inserir pedido: {e}")
        raise HTTPException(status_code=400, detail="Erro de integridade ao inserir pedido")
    except Exception as e:
        db.rollback()
        print(f"Erro ao inserir pedido: {e}")
        raise HTTPException(status_code=500, detail="Erro ao inserir pedido")

# Endpoint para processar todos os pedidos
@router.post("/Inserir_entregas")
def criar_entrega(db: Session = Depends(get_db)):
    cargas = db.query(Carga).all()
    for carga in cargas:
        insert_entregas_from_carga(db, carga)
    return {"message": "Entregas criadas com sucesso"}