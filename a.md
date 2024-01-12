---
marp:true
theme: gaia
footer：|2022/2/19'
paginate: true
size: 16:9
math: katex
marp: true
---

# Math Formula in Markdown

## Inline Math Formulas:

Euler's identity, arguably the most beautiful relation in mathematics, can be written inline like this: $e^{i\pi} + 1 = 0$

## Display Style Math Formulas:

For a more complicated formula like the quadratic equation, it's better to give it a line on its own with display style:

$$
x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}
$$
---

And a matrix:

$$
\begin{bmatrix}
  a_{11} & a_{12} \\
  a_{21} & a_{22} 
\end{bmatrix}
$$

You can even write sum or product series:

$$
\sum_{i=0}^{n} i^2
$$

$$
\prod_{i=1}^{n} i = n!
$$
