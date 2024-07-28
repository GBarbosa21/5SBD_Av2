from sqlalchemy import create_engine, Column, Integer, String, Float, Date
from sqlalchemy.orm import declarative_base, sessionmaker
import random

# Configurações do banco de dados
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:@localhost/bazar_temtudo"

# Criando a engine de conexão
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Criando uma sessão para interagir com o banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para criação das tabelas
Base = declarative_base()

# Modelo da tabela Carga
class Carga(Base):
    __tablename__ = 'cargas'

    Id_cargas = Column(Integer, primary_key=True, nullable=False)
    cod_Pedido = Column(Integer, nullable=False)
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

#Modelo da tabela Produto
class Produtos(Base):
    __tablename__ = 'produtos'

    Id_produto = Column(Integer, primary_key=True, nullable=False)
    nome_produto = Column(String(50), nullable=False)
    preco_produto = Column(Float, nullable=False)
    SKU = Column(Integer, nullable=False)
    UPC = Column(Integer, nullable=False)

# Modelo da tabela Estoque
class Estoque(Base):
    __tablename__ = 'estoque'

    id_estoque = Column(Integer, primary_key=True, nullable=False)
    id_produto = Column(Integer, nullable=False)
    nome_produto = Column(String(50), nullable=False)
    qntd_estoque = Column(Integer, nullable=False)

# Criando a tabela no banco de dados
Base.metadata.create_all(bind=engine)

# Função para popular a tabela Carga
def popular_tabela():
    # Inicia uma sessão
    session = SessionLocal()

    # Dados de exemplo para inserir na tabela Carga
    cargas_exemplo = [
        # Pedido 1 com 1 produto
        {
            "cod_Pedido": 1,
            "Id_itemPedido": 101,
            "data_pedido": '2024-01-01',
            "email": "clienteA@example.com",
            "nomeComprador": "Cliente A",
            "Cpf": 12345678901,
            "SKU": 12345,
            "UPC": 67890,
            "nome_produto": "Produto A",
            "preco_produto": 100.00,
            "Qntd_produto": 10,
            "Frete": 15.50,
            "endereco": "Rua A, 123",
            "CEP": "12345-678",
            "Pais": "Brasil"
        },
        # Pedido 2 com 1 produto
        {
            "cod_Pedido": 2,
            "Id_itemPedido": 102,
            "data_pedido": '2024-02-01',
            "email": "clienteB@example.com",
            "nomeComprador": "Cliente B",
            "Cpf": 10987654321,
            "SKU": 54321,
            "UPC": 98765,
            "nome_produto": "Produto B",
            "preco_produto": 200.00,
            "Qntd_produto": 5,
            "Frete": 20.00,
            "endereco": "Avenida B, 456",
            "CEP": "87654-321",
            "Pais": "Brasil"
        },
        # Pedido 3 com 2 produtos
        {
            "cod_Pedido": 3,
            "Id_itemPedido": 103,
            "data_pedido": '2024-03-01',
            "email": "clienteC@example.com",
            "nomeComprador": "Cliente C",
            "Cpf": 11223344556,
            "SKU": 67890,
            "UPC": 12345,
            "nome_produto": "Produto C",
            "preco_produto": 150.00,
            "Qntd_produto": 8,
            "Frete": 10.00,
            "endereco": "Rua C, 789",
            "CEP": "45678-123",
            "Pais": "Brasil"
        },
        {
            "cod_Pedido": 4,
            "Id_itemPedido": 104,
            "data_pedido": '2024-03-01',
            "email": "clienteC@example.com",
            "nomeComprador": "Cliente C",
            "Cpf": 11223344556,
            "SKU": 67891,
            "UPC": 12346,
            "nome_produto": "Produto D",
            "preco_produto": 180.00,
            "Qntd_produto": 3,
            "Frete": 10.00,
            "endereco": "Rua C, 789",
            "CEP": "45678-123",
            "Pais": "Brasil"
        }
    ]

    # Inserindo os dados na tabela Carga
    for carga_data in cargas_exemplo:
        carga = Carga(**carga_data)
        session.add(carga)

    # Comitando as transações
    session.commit()

    # Fechando a sessão
    session.close()

def populate_estoque():
    session = SessionLocal()
    try:
        # Exemplo de inserção de produtos no estoque
        produtos = session.query(Produtos).all()

        for produto in produtos:
            # Simular alguns produtos ausentes nos pedidos
            if random.random() < 0.5:  # 50% de chance de estar ausente
                continue
            
            # Simular uma quantidade de estoque aleatória entre 0 e 100
            qntd_estoque = random.randint(0, 100)

            novo_registro = Estoque(
                id_produto=produto.Id_produto,
                nome_produto=produto.nome_produto,
                qntd_estoque=qntd_estoque,
            )
            session.add(novo_registro)
        
        session.commit()
        print("População de estoque concluída com sucesso.")
    except Exception as e:
        session.rollback()
        print(f"Erro ao popular estoque: {e}")
    finally:
        session.close()

# Populando a tabela
if __name__ == "__main__":
    popular_tabela()
    print("Tabela Carga populada com sucesso!")
    populate_estoque()
    print("Tabela Estoque populada com sucesso!")
