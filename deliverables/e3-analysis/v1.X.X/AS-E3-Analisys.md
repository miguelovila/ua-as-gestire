---
version: 1.0.0
---

# 1.Introdução
    Neste relatório é apresentada a “Gestire”, uma solução de software e hardware que permite que organizações giram facilmente a disponibilidade dos seus espaços e equipamentos por parte dos seus funcionários e utentes.
    A Gestire será composta por uma plataforma multiplataforma acessível em qualquer lugar e em qualquer momento para gerir a requisição de salas e equipamentos, que comunicaria com cacifos inteligentes capazes de oferecer um controlo completo e eficaz sobre os equipamentos.

# 1.1.Sumário Executivo
    Este relatório apresenta os resultados da 2ª iteração (fase de Elaboration, adaptada do método OpenUP), em que se desenvolveu a análise funcional do produto a desenvolver.   O conceito do produto, caracterizado no relatório referente à Visão, serviu como ponto de partida para o trabalho de análise aqui apresentado. Os novos processos de trabalho incidem sobre a forma como se requisita salas e como se requisita e devolve equipamentos.

# 1.2.Controlo de Versões

# 1.3.Estratégia de Determiinação dos Requisitos
    O levantamento de requisitos foi feito pela própria equipa que, como antigos estudantes do DETI (Departamento de Engenharia de Telecomunicações e Informática) da Universidade de Aveiro, sabem as dificuldades que existem quer em requisitar salas, quer em gerir a utilização de equipamentos partilhados, já que, por vezes, passaram por alguns constrangimentos.
    Também foram feitos questionários aos atuais alunos e professores da instituição de modo a perceber quais seriam as funcionalidades de maior interesse e utilidade.

# 1.4.Referências e Recursos Suplementares
    De modo a perceber qual seria a melhor forma para tratar da gestão de equipamentos, efetuou-se a análise do modo de funcionamento dos Cacifos Locky dos CTT.


# 2.Reengenharia dos Processos de Trabalhos

# 2.1.Novos processos de Trabalho
    Nesta secção irá-se apresentar as atividades de reserva de salas, requisição de equipamentos e devolução dos mesmos.

# 2.2.Tecnologias Potenciadoras e Ambiente de Utilização
    A aplicação será constituída por 3 partes fundamentais para o seu funcionamento: um frontend, um backend e hardware (cacifos inteligentes):
        -O frontend será uma aplicação multi-plataforma (Web, Android, Mac, Linux e Windows) desenvolvida em Flutter e Dart;
        -O backend, desenvolvido em python, será responsável por todos os processos de validação e processamento de dados, incluindo o controlo da localização nos cacifos de todos os itens;
        -Os cacifos inteligentes serão o hardware que fará com que a aplicação funcione no mundo real. Estes cacifos serão equipados com sensores e com uma fechadura eletrónica para controlar o acesso dos utilizadores aos equipamentos neles armazenados. O hardware comunicar-se-á com o backend para garantir que todas as operações são válidas.
    
# 3.Modelo do Domínio
# 3.1.Mapa de Conceitos do Domínio
# 3.2.Ciclo de Vida


# 4.Casos de Utilização
# 4.1.Atores
            ATOR                                                    PAPEL NO SISTEMA
           -Aluno              -Um aluno inscrito na Universidade de Aveiro, com número mecanográfico único e login válido.
         -Professor            -Uma professora da Universidade de Aveiro, com número mecanográfico único e login válido.

# 4.2.Casos de Utilização - Visão Geral
# 4.3.Relação


# 5.Aspetos Transversais
# 5.1.Regras do Negócio
        ID                                  Regra                                            Condições
       -BR1                 -Subscrição do serviço mensal/anual                 -Ser um utilizador da Universidade
       -BR2

# 5.2.Requisitos não Funcionais
