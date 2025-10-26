# ==========================================================
# FLEXORDER - SISTEMA REFATORADO COM DESIGN PATTERNS
# Padrões: Strategy, Decorator, Facade
# ==========================================================

from abc import ABC, abstractmethod
from typing import List, Dict

# ==========================================================
# PADRÃO STRATEGY - PAGAMENTO
# ==========================================================

class EstrategiaPagamento(ABC):
    """Interface abstrata para estratégias de pagamento."""
    
    @abstractmethod
    def processar(self, valor: float) -> bool:
        """Processa o pagamento com o valor especificado.
        
        Args:
            valor: O valor a ser pago
            
        Returns:
            bool: True se pagamento aprovado, False caso contrário
        """
        pass
    
    @abstractmethod
    def get_desconto(self) -> float:
        """Retorna o percentual de desconto desta forma de pagamento.
        
        Returns:
            float: Percentual de desconto (ex: 0.05 para 5%)
        """
        pass


class PagamentoPix(EstrategiaPagamento):
    """Estratégia concreta para pagamento via PIX."""
    
    def processar(self, valor: float) -> bool:
        print(f"Processando R${valor:.2f} via PIX...")
        print("   -> Pagamento com PIX APROVADO (QR Code gerado).")
        return True
    
    def get_desconto(self) -> float:
        return 0.05  # 5% de desconto


class PagamentoCredito(EstrategiaPagamento):
    """Estratégia concreta para pagamento via Cartão de Crédito."""
    
    def __init__(self, limite: float = 1000.0):
        self.limite = limite
    
    def processar(self, valor: float) -> bool:
        print(f"Processando R${valor:.2f} via Cartão de Crédito...")
        if valor < self.limite:
            print("   -> Pagamento com Credito APROVADO.")
            return True
        else:
            print("   -> Pagamento com Credito REJEITADO (limite excedido).")
            return False
    
    def get_desconto(self) -> float:
        return 0.0  # Sem desconto


class PagamentoMana(EstrategiaPagamento):
    """Estratégia concreta para pagamento via Transferência de Mana."""
    
    def processar(self, valor: float) -> bool:
        print(f"Processando R${valor:.2f} via Transferência de Mana...")
        print("   -> Pagamento com Mana APROVADO (requer 10 segundos de espera).")
        return True
    
    def get_desconto(self) -> float:
        return 0.0  # Sem desconto


# ==========================================================
# PADRÃO STRATEGY - FRETE
# ==========================================================

class EstrategiaFrete(ABC):
    """Interface abstrata para estratégias de frete."""
    
    @abstractmethod
    def calcular(self, valor_pedido: float) -> float:
        """Calcula o custo do frete baseado no valor do pedido.
        
        Args:
            valor_pedido: O valor total do pedido
            
        Returns:
            float: O custo do frete
        """
        pass


class FreteNormal(EstrategiaFrete):
    """Estratégia concreta para frete normal."""
    
    def calcular(self, valor_pedido: float) -> float:
        custo = valor_pedido * 0.05
        print(f"Frete Normal: R${custo:.2f}")
        return custo


class FreteExpresso(EstrategiaFrete):
    """Estratégia concreta para frete expresso."""
    
    def calcular(self, valor_pedido: float) -> float:
        custo = valor_pedido * 0.10 + 15.00
        print(f"Frete Expresso (com taxa): R${custo:.2f}")
        return custo


class FreteTeletransporte(EstrategiaFrete):
    """Estratégia concreta para frete via teletransporte."""
    
    def calcular(self, valor_pedido: float) -> float:
        custo = 50.00
        print(f"Frete Teletransporte: R${custo:.2f}")
        return custo


# ==========================================================
# PADRÃO DECORATOR - COMPONENTE BASE
# ==========================================================

class ComponentePedido(ABC):
    """Interface base para o pedido e seus decoradores."""
    
    @abstractmethod
    def calcular_valor(self) -> float:
        """Calcula o valor do pedido.
        
        Returns:
            float: O valor calculado
        """
        pass
    
    @abstractmethod
    def get_descricao(self) -> str:
        """Retorna a descrição do pedido.
        
        Returns:
            str: Descrição textual
        """
        pass


class PedidoBase(ComponentePedido):
    """Implementação concreta do pedido base."""
    
    def __init__(self, itens: List[Dict]):
        self.itens = itens
        self.valor_base = sum(item['valor'] for item in itens)
    
    def calcular_valor(self) -> float:
        return self.valor_base
    
    def get_descricao(self) -> str:
        return f"Pedido com {len(self.itens)} itens"


# ==========================================================
# PADRÃO DECORATOR - DECORADORES CONCRETOS
# ==========================================================

class DecoradorPedido(ComponentePedido):
    """Decorador abstrato base."""
    
    def __init__(self, pedido: ComponentePedido):
        self._pedido = pedido
    
    def calcular_valor(self) -> float:
        return self._pedido.calcular_valor()
    
    def get_descricao(self) -> str:
        return self._pedido.get_descricao()


class DescontoPedidoGrande(DecoradorPedido):
    """Decorador que aplica desconto para pedidos acima de R$500."""
    
    def calcular_valor(self) -> float:
        valor = self._pedido.calcular_valor()
        if valor > 500:
            print("Aplicando 10% de desconto para pedidos grandes.")
            return valor * 0.90
        return valor
    
    def get_descricao(self) -> str:
        valor = self._pedido.calcular_valor()
        if valor > 500:
            return self._pedido.get_descricao() + " + Desconto Pedido Grande (10%)"
        return self._pedido.get_descricao()


class TaxaEmbalagemPresente(DecoradorPedido):
    """Decorador que adiciona taxa de embalagem para presente."""
    
    def __init__(self, pedido: ComponentePedido, taxa: float = 5.00):
        super().__init__(pedido)
        self.taxa = taxa
    
    def calcular_valor(self) -> float:
        valor = self._pedido.calcular_valor()
        print(f"Adicionando R${self.taxa:.2f} de Embalagem de Presente.")
        return valor + self.taxa
    
    def get_descricao(self) -> str:
        return self._pedido.get_descricao() + f" + Embalagem Presente (R${self.taxa:.2f})"


# ==========================================================
# CONTEXTO DO STRATEGY - CLASSE PEDIDO
# ==========================================================

class Pedido:
    """Classe contexto que usa as estratégias de pagamento e frete."""
    
    def __init__(self, 
                 componente_pedido: ComponentePedido,
                 estrategia_pagamento: EstrategiaPagamento,
                 estrategia_frete: EstrategiaFrete):
        self.componente_pedido = componente_pedido
        self.estrategia_pagamento = estrategia_pagamento
        self.estrategia_frete = estrategia_frete
    
    def calcular_valor_com_desconto_pagamento(self) -> float:
        """Calcula o valor aplicando desconto do método de pagamento."""
        valor = self.componente_pedido.calcular_valor()
        desconto = self.estrategia_pagamento.get_desconto()
        
        if desconto > 0:
            print(f"Aplicando {desconto*100:.0f}% de desconto do método de pagamento.")
            return valor * (1 - desconto)
        return valor
    
    def calcular_frete(self) -> float:
        """Calcula o custo do frete."""
        valor_com_desconto = self.calcular_valor_com_desconto_pagamento()
        return self.estrategia_frete.calcular(valor_com_desconto)
    
    def calcular_valor_final(self) -> float:
        """Calcula o valor final do pedido (com frete)."""
        valor_com_desconto = self.calcular_valor_com_desconto_pagamento()
        custo_frete = self.calcular_frete()
        return valor_com_desconto + custo_frete
    
    def processar_pagamento(self) -> bool:
        """Processa o pagamento usando a estratégia definida."""
        valor_final = self.calcular_valor_final()
        return self.estrategia_pagamento.processar(valor_final)
    
    def get_descricao(self) -> str:
        """Retorna a descrição completa do pedido."""
        return self.componente_pedido.get_descricao()


# ==========================================================
# PADRÃO FACADE - SUBSISTEMAS
# ==========================================================

class SistemaEstoque:
    """Subsistema responsável pelo controle de estoque."""
    
    def registrar_pedido(self, pedido: Pedido) -> None:
        print("Pedido registrado no sistema de estoque.")
        print(f"   Descrição: {pedido.get_descricao()}")


class GeradorNotaFiscal:
    """Subsistema responsável pela geração de notas fiscais."""
    
    def emitir_nota(self, pedido: Pedido, valor_final: float) -> None:
        print("Emitindo nota fiscal...")
        print(f"   Valor Total: R${valor_final:.2f}")


# ==========================================================
# PADRÃO FACADE - FACHADA
# ==========================================================

class CheckoutFacade:
    """Fachada que simplifica o processo de checkout."""
    
    def __init__(self):
        self.sistema_estoque = SistemaEstoque()
        self.gerador_nota = GeradorNotaFiscal()
    
    def concluir_transacao(self, pedido: Pedido) -> bool:
        """Orquestra todo o processo de checkout de forma simplificada.
        
        Args:
            pedido: O pedido a ser processado
            
        Returns:
            bool: True se transação bem-sucedida, False caso contrário
        """
        print("=========================================")
        print("INICIANDO CHECKOUT COM DESIGN PATTERNS...")
        print(f"\nDescrição: {pedido.get_descricao()}")
        
        # Calcula valores
        valor_final = pedido.calcular_valor_final()
        print(f"\nValor a Pagar: R${valor_final:.2f}")
        
        # Processa pagamento
        if pedido.processar_pagamento():
            print("\nSUCESSO: Transação aprovada!")
            self.sistema_estoque.registrar_pedido(pedido)
            self.gerador_nota.emitir_nota(pedido, valor_final)
            return True
        else:
            print("\nFALHA: Transação abortada.")
            return False


# ==========================================================
# DEMONSTRAÇÃO DE USO
# ==========================================================

if __name__ == "__main__":
    # Criar a fachada
    checkout = CheckoutFacade()
    
    # ===== CENÁRIO 1: Pedido com PIX e Frete Normal =====
    print("\n=== CENÁRIO 1: PIX + Frete Normal ===")
    itens1 = [
        {'nome': 'Capa da Invisibilidade', 'valor': 150.0},
        {'nome': 'Poção de Voo', 'valor': 80.0}
    ]
    
    # Criar componente base
    pedido_base1 = PedidoBase(itens1)
    
    # Criar pedido com estratégias
    pedido1 = Pedido(
        componente_pedido=pedido_base1,
        estrategia_pagamento=PagamentoPix(),
        estrategia_frete=FreteNormal()
    )
    
    # Processar via fachada
    checkout.concluir_transacao(pedido1)
    
    # ===== CENÁRIO 2: Pedido Grande com Crédito, Expresso e Embalagem =====
    print("\n\n=== CENÁRIO 2: Crédito + Expresso + Embalagem ===")
    itens2 = [
        {'nome': 'Cristal Mágico', 'valor': 600.0}
    ]
    
    # Criar componente base
    pedido_base2 = PedidoBase(itens2)
    
    # Aplicar decoradores
    pedido_decorado2 = DescontoPedidoGrande(pedido_base2)
    pedido_decorado2 = TaxaEmbalagemPresente(pedido_decorado2)
    
    # Criar pedido com estratégias
    pedido2 = Pedido(
        componente_pedido=pedido_decorado2,
        estrategia_pagamento=PagamentoCredito(),
        estrategia_frete=FreteExpresso()
    )
    
    # Processar via fachada
    checkout.concluir_transacao(pedido2)
    
    # ===== CENÁRIO 3: Demonstrando Flexibilidade - Mana + Teletransporte =====
    print("\n\n=== CENÁRIO 3: Mana + Teletransporte (Novo!) ===")
    itens3 = [
        {'nome': 'Varinha Élfica', 'valor': 300.0},
        {'nome': 'Pergaminho Antigo', 'valor': 120.0}
    ]
    
    pedido_base3 = PedidoBase(itens3)
    pedido_decorado3 = TaxaEmbalagemPresente(pedido_base3)
    
    pedido3 = Pedido(
        componente_pedido=pedido_decorado3,
        estrategia_pagamento=PagamentoMana(),
        estrategia_frete=FreteTeletransporte()
    )
    
    checkout.concluir_transacao(pedido3)
