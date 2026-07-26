# RICAN

**Representational Isomorphic Coding for Arbitrary Numeration**

*A Fixed-Rate Binary Representation Framework for Finite Alphabets Using Continued-Fraction Convergents*

[![Python Version](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE.md)
[![Research](https://img.shields.io/badge/Research-DOI-blueviolet)](https://zenodo.org)
[![Paper](https://img.shields.io/badge/Paper-IEEE-red)](docs/RICAN_Paper.pdf)

---

## 📋 Table of Contents

1. [Qué es y qué no es RICAN](#qué-es-y-qué-no-es-rican)
2. [Descripción Científica](#descripción-científica)
3. [Publicación Académica](#publicación-académica)
4. [Quick Start](#quick-start)
5. [Ejemplos de Uso](#ejemplos-de-uso)
6. [Formato RJ03](#formato-rj03)
7. [Estructura del Repositorio](#estructura-del-repositorio)
8. [Reproducibilidad](#reproducibilidad)
9. [Roadmap](#roadmap)
10. [Citation](#citation)
11. [License](#license)
12. [Author](#author)

---

## 🧬 Qué es y qué no es RICAN

### ✅ Qué es RICAN

- Un **marco matemático** para representación binaria de tasa fija
- Un método **constructivo** para seleccionar tamaños de bloque mediante **fracciones continuas**
- Una **familia infinita** de representaciones para alfabetos finitos arbitrarios
- Un formato **autónomo y reversible** (RJ03)
- Una implementación **reproducible** en Python estándar

### ❌ Qué NO es RICAN

- NO es un compresor estadístico (no usa probabilidades)
- NO compite con Huffman, ANS, LZMA, gzip o xz
- NO explota redundancia de fuente
- NO requiere modelos de probabilidad ni entrenamiento

---

## 📐 Descripción Científica

RICAN aborda el problema de representar secuencias sobre alfabetos finitos utilizando **bits de longitud fija**.

Para un alfabeto de cardinalidad `B` y un bloque de longitud `K`, el número mínimo de bits requerido es:

```math
n(K) = ⌈K · log₂(B)⌉