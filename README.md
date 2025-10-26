1. Strategy (Estratégia)

Problema: o sistema era todo engessado — se eu quisesse mudar a forma de pagamento ou o tipo de frete, tinha que mexer no código inteiro.

Solução:
Criei um “jeito” de trocar essas partes sem precisar reescrever tudo.
Agora o sistema entende diferentes estratégias de pagamento (como Pix, cartão ou até “mana” 😄) e de frete (normal, expresso ou até teletransporte 🚀).

O legal é que posso mudar o tipo de pagamento ou o frete sem alterar o resto do código, só trocando a “estratégia”.

👉 É como escolher o modo de entrega ou o método de pagamento num app de compras: o sistema se adapta ao que você escolher.

2. Decorator (Decorador)

Problema: os cálculos de desconto e taxas estavam misturados no meio do código principal. Virava uma bagunça toda vez que precisava mudar algo.

Solução:
Criei uma forma de “empilhar” funcionalidades.
Por exemplo:

Um decorador que dá desconto pra pedidos grandes.

Outro que adiciona taxa de embalagem de presente.

Agora posso usar um, outro, ou os dois ao mesmo tempo — sem precisar mexer nas regras principais.

👉 É como montar um sanduíche: você escolhe o que quer adicionar (desconto, taxa, etc.), sem precisar refazer o pão toda vez. 🥪

3. Facade (Fachada)

Problema: pra finalizar um pedido era preciso chamar várias partes do sistema — estoque, nota fiscal, pagamento… uma confusão.

Solução:
Criei uma “fachada” que faz tudo isso de uma vez.
O cliente só chama um comando e o sistema cuida do resto por baixo dos panos (registra o pedido, emite nota, etc).

👉 É como apertar um botão de “Finalizar compra”: o usuário vê só isso, mas o sistema resolve tudo nos bastidores.

🚀 O resultado final

Com essa nova estrutura:

O código ficou mais organizado e fácil de entender

É super simples de adicionar coisas novas

Cada parte pode ser testada separadamente, sem quebrar o resto

E o sistema ficou muito mais flexível e profissional

Em resumo: deixei um código que era um emaranhado cheio de “se isso, faz aquilo” virar um sistema limpo, modular e pronto pra crescer sem dores de cabeça. 😎💻