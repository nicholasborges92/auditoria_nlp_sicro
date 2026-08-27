Auditoria e Classificação de Insumos SICRO segundo a ABNT NBR 15965
Este repositório contém o conjunto de dados analíticos, o pipeline de Machine Learning e as rotinas de auditoria desenvolvidas para o artigo científico "AUDITORIA E AVALIAÇÃO PRELIMINAR DE CLASSIFICAÇÃO TEXTUAL DE INSUMOS DE TERRAPLENAGEM RODOVIÁRIA SEGUNDO A NBR 15965"
, submetido ao 23º Congresso Rio de Transportes (RDT 2026)
.
O objetivo do estudo é auditar a correspondência semântica e avaliar os limites práticos de classificadores lexicais baseados em Processamento de Linguagem Natural (NLP) ao relacionar composições e insumos de terraplenagem do Sistema de Custos Referenciais de Obras (SICRO) à estrutura hierárquica da ABNT NBR 15965
.
📌 Visão Geral do Projeto
A interoperabilidade entre bases de custos (SICRO) e padrões semânticos de modelagem da informação da construção (série NBR 15965) é um pilar fundamental para a viabilização de fluxos de trabalho em BIM 5D (orçamentação automatizada)
.
Este trabalho realiza um benchmark estatístico e lógico, demonstrando de forma crítica que os elevados índices de acerto comumente reportados em modelos de classificação textual de insumos decorrem, em grande parte, da repetição de padrões textuais (vazamento lexical) e da dependência de registros, e não de uma efetiva generalização semântica das classes da norma
.
📊 Conjunto de Dados (DATASET_NLP)
A base analítica foi estruturada a partir da identificação de insumos tecnicamente representativos em composições do SICRO associadas a serviços de terraplenagem rodoviária
.
Registros Brutos: 274 composições/serviços
Classes Iniciais (Rótulos NBR 15965): 13 classes
Desbalanceamento de Classes: Severo, com 82,5% de representação de uma única classe majoritária (2Q 66 10 02 00 00 00 - Caminhões basculantes)
.
Filtro Experimental: Remoção de classes unitárias (com apenas uma ocorrência) para viabilizar o particionamento estratificado, resultando em um subconjunto de 268 registros e 7 classes ativas
.
======================================================================================================
Rótulo (NBR 15965)     Descrição do Grupo de Insumos                  Ocorrências   Participação
======================================================================================================
2Q 66 10 02 00 00 00   Veículos e Equipamentos de Carga e Transporte          226          82,5%
2Q 62 30 02 14 00 00   Tratores de Esteiras com Lâmina                         18           6,6%
2Q 62 50 10 00 00 00   Rompedores Hidráulicos e Ponteiros                       9           3,3%
2Q 62 26 00 00 00 00   Motoscrapers / Escavadeiras                              7           2,6%
2Q 42 06 18 02 02 00   Equipamentos de Perfuração e Sondas                      3           1,1%
2Q 58 10 10 02 06 00   Perfuratrizes / Rompedores Manuais                       3           1,1%
2Q 62 34 54 02 06 00   Rolos e Equipamentos de Compactação                      2           0,7%
======================================================================================================