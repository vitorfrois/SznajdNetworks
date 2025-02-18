---
title: Prediction of the Sznajd model through network topology 
author:
- Vítor Amorim Fróis
documentclass: article
format: pdf
link-citations: true
lang: en
refs: |
   ::: {#refs}
   :::
abstract: |
    This paper presents a Machine Learning approach to predict Sznajd model dynamical variables in complex networks through topological features: the consensus time and opinion change frequency. Exploring the convergence between topology and dynamics, this paper introduces a solid method using traditional learning algorithms for the prediction and answers questions related to polarization mechanisms in social interactions. Leveraging ???? topological measures of the underlying networks, we verify that the ???? and ???? emerge as the most important predictors for these outcomes.
bibliography: [references.bib]
---

\tableofcontents

# Outline

## Introduction
- Introduction to complex systems, social dynamics and polarization
- Motivate through real examples (brazil and usa)
- Ising, Q-voter and Sznajd 
- Hypothesis: Topology can be a huge factor of influence 
- Finish briefly explaining the proposed methodology and improvements since the last article

## Methods
- Random Network Generation
- Sznajd model simulation
- Network characterization
- Machine Learning: R2, Forward Selection, Cross Validation, Data Normalization, Non-Linear Regression, Random Forests 

## Results
- Prediction of Dynamical Variables
- Feature importance through random forest
- Regression analysis in proposed method

## Conclusion
- Compared to the last related published paper, this one presents a more robust method
- Analysis of the coeficients (we cant tell that much, but here they are)
- Future works: how can we adapt traditional learning methods to the node prediction, given that we expect a iid assumption 

The interaction between simple ruled components of a system can create complex patterns and features like emergence, scale-free distributions and heterogeinity. Emerging phenomena are present in complex systems and characterized by the spontaneous result of the interaction between millions of components that constitute the system. An big example of emergence occours during asian southeast night, when fireflies from all over the region adjust its blinking frequency accordingly to their neighbors. The effect is expanded past the whole system until they all blink in synchrony.   

In the context of social dynamics, mathematical models that seek to reproduce human behaviour in networks, emergency can be characterized as an phenomena related to polarization [@maia2021emergence]. Here, we define polarization as the opinion fragmentation, a state opposed to consensus. Many studies show that polarization can have deep influence in political environment, as seen in violent and anti-democratic rallies that took place in January 8th 2023 at Brasilia [@interian2023polarization;@layton2021polarization]. Given this, is very important to study polarization aiming to reduce discord scenarios.

Statistical physics developed tools for the study of many interacting particle systems, which are adopted with ease by social dynamics academics. Ersnt Ising found the exact solution for a paramagnetic model, 

