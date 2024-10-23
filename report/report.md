---
title: Predição de Variáveis Complexas no Modelo de Sznajd
author:
- Vítor Amorim Fróis
abstract: |
  O presente projeto utiliza Aprendizado de Máquina para prever variáveis complexas no modelo de Sznajd em Redes Complexas: o Tempo de Consenso e a Frequência de Troca de Opinião. Ao utilizar medidas topológicas para caracterização de redes e consequentemente como features, podemos prever as variáveis com alta acurácia. Ao explorar a convergência entre estrutura e dinâmica de redes, esse projeto responde dúvidas relacionadas aos mecanismos de polarização em interações sociais.
---


# Introdução
A interação entre componentes de um sistema que possuem regras simples leva a formação de padrões complexos e características como emergência, livre de escala e heterogeneidade. Fenômenos emergentes são presentes em sistemas complexos e caracterizados pelo resultado espontâneo da interação entre os milhares de componentes que constituem o sistema. Um grande exemplo de emergência ocorre durante a noite do sudeste asiático, quando vagalumes da região piscam de acordo ajustam a frequência do piscar de suas luzes de acordo com os vizinhos mais próximos, até que o efeito seja extendido por todo o sistema, de forma que os indivíduos pisquem em sincronia \cite{johnson2002emergence}.

No contexto de dinâmicas sociais, isto é, modelos matemáticos que buscam reproduzir o comportamento humano em redes, a emergência pode ser caracterizada como um fenômeno relacionado a polarização \cite{maia2021emergence}. Aqui e no restante do relatório, definimos polarização como a fragmentação de opiniões, um estado contrário ao consenso. Diversos estudos mostram que a polarização pode ter profunda influência no âmbito político \cite{interian2023polarization,layton2021polarization}. Dessa forma, é de suma importância estudar a polarização para evitar que cenários de discórdia se repitam.

A física estatística desenvolveu ferramentas para o estudo de sistemas de muitas partículas interagentes, os quais são adaptados com facilidade para o estudo de dinâmicas sociais. Ersnt Ising encontrou a solução exata para um modelo de paramagneto, representando materiais que podem alcançar dois estados conflitantes e buscam um estado de mínima energia. O modelo recebeu o nome de Ising e pode ser considerado como um modelo para simples opiniões, onde há uma transição de fase entre os estados de polarização e consenso. O modelo de Sznajd foi inspirado pelo primeiro modelo e busca explorar como opiniões semelhantes são necessárias para influenciar outros. Já o modelo votante ilustra como a maioria pode influenciar vizinhos, explorando por sua vez como a ordem emerge a partir da opinião maioria.

- Sistemas complexos
- Polarização e motivação política
- ising $\rightarrow$ sznajd, voter e q-voter
- topologia pode influenciar na formação de consenso, além disso seria ótimo estudar sistemas complexos com ferramentas como ML
- alguns resultados com o modelo de sznajd
- vamos comparar diferentes abordagens e dinâmicas

# Materiais e Métodos
## Geração de Redes Aleatórias
Seis diferentes topologias das redes foram examinadas. As redes Erdös–Rényi, Barabási–Albert linear, Barabási–Albert não linear com $\alpha=0.5$ and $\alpha=1.5$, Watts–Strogatz e Waxman ~\cite{boccaletti2006complex,costa2007characterization}. Essas topologias buscam abordar diferentes estruturas que sociedades reais possam admitir, considerando a presença de hubs, comunidades e *small*world}. Ou seja, como as redes geradas por esses modelos apresentam diferentes propriedades que podems ser controladas através de seus parâmetros, poderemos gerar um banco de dados com exemplos de topologias diferentes. Assim, os efeitos de propriedades topológicas no processo dinâmico podem ser verificados, visto que muitas propriedades, como distância entre os vértices ou nível de centralidade, sofrerão variações nas bases geradas. Essa variação é importante para oferecermos exemplos diferentes aos modelos de aprendizado que usaremos na fase de predição das variáveis dinâmicas. Para cada uma dessas redes, 100 instâncias foram criadas visando diminuir efeitos da aleatoriedade na construção do modelo.

O modelo de Erdos-Renyi (ER) é um dos mais estudados e detalhados na teoria dos grafos, formando redes ao ligar $N$ nós entre as possíveis arestas com probabilidade $p$. Apesar de não representar com fidelidade cenários do mundo real, possui apelo matemático por possuir características bem definidas. A rede Watts-Strogatz por sua vez, busca garantir que o diâmetro da rede é baixo, conhecido como característica de pequeno mundo, além de um alto agrupamento. As redes Barabási-Álbert, por sua vez, enfatizam a lei de potência na distribuição de probabilidade dos nós através da construção via ligação preferencial. Por fim, a rede de Waxman é construída ao colocar pontos de forma aleatória em um espaço e ligá-los de acordo com sua distância e é conhecida por trazer princípios geográficos, incluindo o aparecimento de comunidades, para os grafos.

## Simulação de Monte Carlo domodelo de Sznajd
O modelo de *spin* de Ising é um dos modelos mais utilizados na mecânica estatística~\cite{castellano2009social}. No artigo \cite{sznajd2000opinion} é proposto o modelo de Sznajd, uma adaptação de Ising para descrever dinâmicas de opinião em uma comunidade.

O modelo original segue uma simulação estocástica implementando o fenômeno de validação social nos agentes $S_i, i=1,2,...,N$ com opiniões $O=\{-1, +1\}$. A cada passo, dois vizinhos são selecionados e o sistema é atualizado de acordo com as seguintes regras dinâmicas:

- Se $SiS_{i+1}=1$, então os vizinhos $S_{i-1}$ e $S_{i+2}$ recebem a opinião do par $S_i, S_{i+1}$ 
- Se $SiS_{i+1}=-1$, então $S_{i-1}=S_{i+1}$ e $S_{i+2}=S_i$

O modelo original foi proposto para um sistema unidimensional. 
% No entanto, a dinâmica foi modificada de forma incluir uma rede complexa~\cite{sanchez2004sznajd}. 
% Nesse trabalho será utilizada a adaptação apresentada em \cite{Bernardes_2002} para implementação do modelo de Sznajd em redes com duas opiniões. 
Considere uma rede de $N$ pessoas, com opiniões $O =\{-1, +1\}$ inicialmente distribuidas de forma aleatória. Cada indivíduo é uma variável dinâmica binária $s(x, t)=O$ de grau $k_x$, em que $x=1,...,N$.  Uma iteração $t$ de uma sequência de iterações até o consenso é descrita abaixo: 

- Uma dupla de nós vizinhos $i$ e $j$ é escolhida aleatoriamente
- Se $s(i, t) \ne s(j, t)$ a iteração termina
- Se $s(i, t) = s(j, t)$, a união dos vizinhos de $i$ e $j$ recebe a opinião de $i$.

### Variáveis dinâmicas de interesse
O **tempo de consenso**, definido como o período necessário para que o sistema alcance um estado estacionário, é uma métrica crucial na análise da dinâmica de consenso, bem como a **frequência da troca de opinião**. Durante a simulação, registramos tanto o tempo de consenso quanto a frequência de troca de opinião como indicadores-chave do comportamento do sistema. O histograma de ambas variáveis aleatórias são exibidos abaixo com a estimativa de densidade correspondente. Se faz necessária a utilização da escala log para visualização devido ao aspecto de cauda longa das distribuições.

![Histograma do Tempo de Consenso na escala logarítmica](consensus_hist.png)

![Histograma da Frequência de Troca de Opinião na escala logarítmica](frequency_hist.png)

### Inicialização dos nós
Os parâmetros para as redes e o modelo foram fixados para proporcionar um patamar conciso durante os testes com os algoritmos de aprendizado de máquina. Ao fixar esses parâmetros é possível focar no impacto de outras variáveis na análise. Dessa forma, as simulações contarão com as redes com um número de nós fixo, a saber, $N=1000$, além de uma porcentagem de nós com opiniões positivas $p = 0,2$. 

Além disso, adotamos três abordagens distintas de inicialização para os nós com opiniões positivas nas simulações. Primeiramente, a inicialização aleatória, atribuindo aleatoriamente opiniões positivas aos nós. Em seguida, adotamos a estratégia de inicialização inversa, na qual os nós com menor grau receberão opiniões positivas. Por fim, aplicaremos a inicialização direta, na qual os nós mais influentes na rede receberão opiniões positivas. É de suma importância simular o sistema com diferentes inicializações, possibilitando analisar como a importância das *features* são influenciadas em cada caso e compreender melhor como situações de consenso podem ser favorecidas.

## Caracterização de Redes
Buscamos caracterizar cada rede $i$ utilizando um vetor de features derivado de sua estrutura e denotado por $X_i=\{X_{i1}, X_{i2}, ...,X_{ik}\}$, em que $X_{ik}$ é a k-ésima métrica da rede $i$. Assim, foram utilizadas diversas medidas, incluindo o coeficiente de *clustering*, *closeness centrality*, *betweenness centrality*, *average shortest path lenght*, coeficiente de correlação de Pearson do grau, *information centrality*, *approximate current flow betweenness centrality* e *eigenvector centrality*, Entropia de Shannon e segundo momento do grau. Tais medidas, usadas coletivamente aqui, fornecem *insights* valiosos sobre a topologia, conectividade, eficiência, influência e organização em redes complexas \cite{costa2007characterization}. 

![Heatmap utilizando correlação de Spearman entre as features. É possível observar alta colinearidade entre diversas medidas.](heatmap.png)

Podemos dividir as métricas descritas acima entre três grandes grupos, sendo eles medidas de centralidade (*closeness centrality*, *betweenness centrality*, *average shortest path lenght*, *information centrality*, *approximate current flow betweenness centrality* e *eigenvector centrality*), de transitividade (*clustering*) e de conectividade (coeficiente de correlação de Pearson do grau, Entropia de Shannon e segundo momento do grau). Podemos obter um heatmap entre as features obtidas para as redes geradas utilizando a correlação de Spearman, uma medida que quantifica a colinearidade entre duas variáveis. Ao analisar o heatmap, vemos que há grande correlação linear entre diversas feautres, principalmente aquelas que pertencem aos mesmos grupos. Esse resultado é importante pois quando há informação mútua entre variáveis, o grau de influência no resultado de modelos de Aprendizado de Máquina é diminuido. 

## Aprendizado de Máquina
Nesse projeto assumimos que o tempo para alcançar consenso $Y_i$ e a frequência de mudança de opinião $C_i$ podem ser inferidos a partir do vetor de *features* $X_i$. A explicação abaixo foca na predição de $Y_i$ mas também é válida para $C_i$. 

$$
Y_i = f(X_i)+\delta
$$

Nosso objetivo é encontrar a função $f$ que relaciona $Y_i$ às métricas da rede. Trataremos predição de $Y_i$ como um problema de regressão em que $\delta$ é um termo que representa uma distribuição normal com média zero e desvio padrão $\sigma$. Esse termo representa a incerteza nos dados, que incluem as medidas que não foram incluídas no modelo e as flutuações aleatórias na simulação das redes e modelos.

### *Forward Selection* (FS)
*Forward Stepwise Selection* é uma maneira eficiente para selecionar *features*, que começa com um modelo sem preditores e adiciona variáveis uma a uma, até que os preditores exigidos estejam no modelo. De modo particular, em cada passo é adicionado o melhor preditor ao modelo. Considerando a alta colinearidade entre as variáveis explicativas, o FS desempenha um papel muito eficiente ao selecionar a melhor variável em cada passo sem descartar suas correlações.

pseudocodigo fs

### Coeficiente de Determinação (R2)
O coeficiente de determinação, $R2$, é uma métrica usada para medir o quão bem um modelo de regressão se ajusta aos dados \cite{johnson2017r2}. No entanto, quando adicionamos mais preditores ao modelo, o R2 pode aumentar mesmo que esses novos preditores não ajudem realmente a explicar a variação na variável dependente \cite{bishop2006pattern, murphy2012machine}. Para lidar com isso, utilizaremos o R2 ajustado, que leva em consideração o número de preditores e penaliza a inclusão daqueles que são irrelevantes. Esse ajuste fornece uma avaliação mais precisa de quão bem o modelo prevê o resultado. Isso garante uma avaliação mais confiável do desempenho do modelo.

formula r2

### Validação Cruzada
A fim de analisar os resultados utilizaremos o R2 no modelo de aprendizado de máquina, juntamente com técnicas descritas acima, como a validação cruzada e etapa de teste em um conjunto oculto de dados. Essa etapa busca garantir que o modelo foi capaz de generalizar com base nos dados de treinamento e consegue realizar boas previsões em dados novos.

fotinha validaçao cruzada


## Machine Learning
selecao empirica de features, selecao via forward selection, r2 score, regressao nao linear

# Resultados
Falar brevemente sobre a alta acurácia em cada um dos casos (random, direto e inverso)

## tabela com os resultados

## medidas mais importantes

# Conclusão
- pq as medidas mais importantes sao importantes
- quais as diferencas entre as inicializacoes diferentes
- regressao poisson vs xgboost e redes neurais
- Comparacao q-voter