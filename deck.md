---
marp: true
theme: custom
paginate: true
size: 16:9
math: mathjax
style: @import url('https://unpkg.com/tailwindcss@^2/dist/utilities.min.css')
footer: by ChatGPT
---
    
<!-- _class: title -->
<!-- _footer: '' -->
<!-- _paginate: false -->
# Presentation by AI 
## Pretty cool, huh?
    
---
## Formula 
    

K-Means Clustering ist ein unsupervised Machine Learning Algorithmus, der verwendet wird, um Daten in Gruppen (Cluster) zu klassifizieren. Der Algorithmus funktioniert, indem er die Datenpunkte in K Cluster aufteilt und jedem Punkt eine Clusterzugehörigkeit zuweist.

Die mathematische Formel für K-Means Clustering lautet:

$$J(C_k) = \sum_{i=1}^K \sum_{x \in C_i} ||x - \mu_i||^2$$

wobei $C_k$ die Menge der K Cluster ist, $\mu_i$ der Mittelwert des i-ten Clusters ist und $||x - \mu_i||^2$ die Quadratsumme der Abweichung von x zu $\mu_i$ ist.
    
