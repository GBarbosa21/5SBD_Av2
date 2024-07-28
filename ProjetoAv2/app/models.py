from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from .database import Base

class Carga(Base):
    __tablename__ = 'cargas'

    Id_cargas = Column(Integer, primary_key=True, nullable=False)
    cod_pedido = Column(Integer, nullable=False)
    Id_itemPedido = Column(Integer, nullable=False)
    data_pedido = Column(Date, nullable=False)
    email = Column(String(120), nullable=False)
    nomeComprador = Column(String(150), nullable=False)
    Cpf = Column(Integer, nullable=False)
    SKU = Column(Integer, nullable=False)
    UPC = Column(Integer, nullable=False)
    nome_produto = Column(String(50), nullable=False)
    preco_produto = Column(Float, nullable=False)
    Qntd_produto = Column(Integer, nullable=False)
    Frete = Column(Float, nullable=False)  
    endereco = Column(String(200), nullable=False)
    CEP = Column(String(12), nullable=False)
    Pais = Column(String(20), nullable=False)

class Clientes(Base):
    __tablename__ = 'clientes'

    Id_cliente = Column(Integer, primary_key=True, nullable=False)
    nome_cl = Column(String(150), nullable=False)
    email_cl = Column(String(120), nullable=False)
    Cpf_cl = Column(Integer, nullable=False)

    pedidos = relationship("Pedidos", back_populates="cliente")

class Produtos(Base):
    __tablename__ = 'produtos'

    Id_produto = Column(Integer, primary_key=True, nullable=False, index=True)
    nome_produto = Column(String(50), nullable=False)
    preco_produto = Column(Integer, nullable=False)
    SKU = Column(Integer, nullable=False, unique=True, index=True)
    UPC = Column(Integer, nullable=False, unique=True, index=True)

    itens_pedidos = relationship("ItensPedidos", back_populates="produto", overlaps="itens_pedido")

class ItensPedidos(Base):
    __tablename__ = 'itens_pedidos'

    id_itemPedido = Column(Integer, primary_key=True, nullable=False)
    cod_pedido = Column(Integer, ForeignKey('pedidos.cod_pedido'), nullable=False)
    id_produto = Column(Integer, ForeignKey('produtos.Id_produto'), nullable=False)
    Qntd_produto = Column(Integer, nullable=False)

    produto = relationship("Produtos", back_populates="itens_pedidos")
    pedido = relationship("Pedidos", back_populates="itens_pedidos")

class Pedidos(Base):
    __tablename__ = 'pedidos'

    cod_pedido = Column(Integer, primary_key=True, nullable=False)
    data_pedido = Column(Date, nullable=False)
    id_cliente = Column(Integer, ForeignKey('clientes.Id_cliente'), nullable=False)
    itens_pedidos = Column(Integer, ForeignKey('pedidos.id_itemPedido'), nullable=False)
    total_pedido = Column(Float, nullable=False, default=0.0)
    status = Column(Integer, nullable=True, default=0) # 1: Disponível, 2: Não disponível

    itens_pedidos = relationship("ItensPedidos", back_populates="pedido")
    cliente = relationship("Clientes", back_populates="pedidos")
    entregas = relationship("Entregas", back_populates="pedido")

class Estoque(Base):
    __tablename__ = 'estoque'

    id_estoque = Column(Integer, primary_key=True, nullable=False)
    id_produto = Column(Integer, ForeignKey('produtos.Id_produto'), nullable=False)
    nome_produto = Column(String(50), nullable=False)
    qntd_estoque = Column(Integer, nullable=False)

class Entregas(Base):
    __tablename__ = 'entregas'

    id_entrega = Column(Integer, primary_key=True, autoincrement=True)
    cod_pedido = Column(Integer, ForeignKey('pedidos.cod_pedido'), nullable=False)
    nome_comprador = Column(String(150), nullable=False)
    endereco = Column(String(200), nullable=False)
    data_entrega = Column(Date, nullable=False)
    status_entrega = Column(String(50), nullable=False)

    pedido = relationship("Pedidos", back_populates="entregas")

