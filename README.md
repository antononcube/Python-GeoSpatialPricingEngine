# GeoSpatialPricingEngine

Python package with an Object-Oriented Programming (OOP) framework for the creation and calibration of Geo-spatial pricing engines.

---

## Installation

From [PyPI.org](https://pypi.org):

```
pip install GeoSpatialPricingEngine
```

---

## Design


### The Geo-Spatial Pricing Problem 

Let us define the Geo-Spatial Pricing Problem (GSPP) in most general terms:

**Definition GSSP:** Create a mathematical artifact that approximates prices of deliveries of goods 
between different geographical locations using a generic pricing formula and using 
a relatively small, sparse pricing dataset. 

The "pricing landscape" (or "manifold of prices") is expected to be non-linear in terms of 
start and destination locations, distances, routes, and Geo-spatial directions.

Here is a _simplified_, but concrete definition in which the "pricing landscape" is 
approximated with a set of formulas that have the same form. 
That set of formulas is the "mathematical artifact." 

**Definition GSSP1:** The price of the transport of goods from the geographical point $g_1$ to geographical point $g_2$ is determined by: 
  - Geo-coordinates of $g_1$ and $g_2$
  - The length $d(g_1, g_2)$ of a route taken between $g_1$ and $g_2$
  - An offset of the price $s(g_1)$ ("start location flat rate")
  - An offset of the price $e(g_2)$ ("destination location flat rate")
  - A coefficient $k(g_1, g_2)$ multiplying the distance $d(g_1, g_2)$ 
  - The _generic_ formula of the price is:
$$
  p(g_1, g_2)=s(g_1) + e(g_2) + k(g_1, g_2) * d(g_1, g_2) 
$$

A more complicated formulation extends GSSP1 by including the routes between the Geo-locations in
the price derivation. For example, routes can reflect geographical elevation changes, fuel pricing landscape,
population, or weather conditions. 

GSSP has the following properties:

- The pricing is not symmetric in any of the Geo-spatial directions
  - Generally, $p(g_1, g_2) \neq p(g_2, g_1)$ 
- Proximity of start- or end locations does not imply price proximity 
  - Consider two deliveries of goods starting at the same location $g_0$ and finishing different locations $g_1$ and $g_2$ 
  - The distance $d(g_1, g_2)$ is very small compared to $d(g_0, g_1)$ and $d(g_0, g_2)$, e.g., $d(g_1, g_2) ≤ 0.02 * d(g_0, g_1)$ 
  - Though, the prices difference can be significant, e.g., $p(g_0, g_1) ≥ 1.2 * p(g_0, g_2)$
- Routes can have lengths significantly larger than the corresponding over-air distances.  

*TBF...*

-----

## Methodology

A possible solution GSPP can be seen re-implementation of Multi-dimensional Quantile Regression (QR) 
using specially designed basis functions. From the GSPP formulation above it follows that 
routes between start and end locations are ignored and only distances over the air are used then 
QR is applied in a six-dimensional space. 

Python and [Google OR-Tools](https://developers.google.com/optimization) are chosen in order to have a general design and implementation
that can be _transferred_ to other programming languages and optimization systems in them.

Large Language Models (LLMs) are used to generate large part of the code with suitable LLM prompts.
Project's documentation and LLM prompts are created and collected with the aim to be able to reproduce
the implementation of the solution framework using LLMs.

Fake pricing datasets of different types are specially generated in order test and exemplify 
different aspects of GSPP and the solution provided by the framework.  

*TBF...*

----

## Solution outline

- The geographical area of interest (e.g. USA) is covered with a regular or irregular grid of adjacent cells.
- Pricing methods are broken down into different levels of scope:
  - Policy (Geo-spatial-temporal)
  - Strategy (Geo-spatial)
  - Special rules (tactical, for concrete locations, goods, or transport)

*TBF...*

----

## References

*TBD...*
