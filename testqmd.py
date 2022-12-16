file = """
---
title: Presentation by AI
subtitle:  Pretty cool, huh?
author: by ChatGPT
lang: "De"
format: 
    revealjs: 
        theme: [simple, custom.scss]
        toc: false
        toc-title: "Inhaltsverzeichnis"
        toc-depth: 1
        number-sections: true
        number-depth: 1
        preview-links: true
        reference-location: document
from: markdown+emoji 
slide-number: c/t
jupyter: ml_openai
---


## Was ist eine Lineare Regression
### This is a subheader


**Lineare Regression** ist ein statistisches Modell, das verwendet wird, um die Beziehung zwischen einer abhängigen Variablen (Y) und einer oder mehreren unabhängigen Variablen (X) zu beschreiben. 

Die lineare Regressionsformel lautet: 

$$y = \beta_0 + \beta_1x_1 + \beta_2x_2 + ... + \beta_nx_n$$

wobei $y$ die abhängige Variable ist, $\beta_0$ der Konstante Faktor ist und $\beta_1$, $\beta_2$, ... , $\beta_n$ die Koeffizienten der unabhängigen Variablen $x_1$, $x_2$, ... , $x_n$ sind.



## Beispiel: seaborn
### This is a subheader


```python
import seaborn as sns
import numpy as np

# Generate random data
x = np.random.rand(50)
y = np.random.rand(50)

# Plot the scatterplot using seaborn
sns.scatterplot(x, y)
```
"""

file = file.replace("```python", "```{python}")
print(file)