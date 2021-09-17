# Cell Transmission Model
### Numerical method to solve traffic flow system

The complex system of vehicular runoff is studied with different models. Some macroscopic, which consider traffic as a continuum fluid, and some microscopic, which consider the relation of a driver with adjacent vehicles.
Cell transmission model (CTM) is based on a class of macroscopic model called LWRs (Lighthill-Whitham-Richards model).

The variables of the each macroscopic model are:
* flow
* density
* mean speed

which are connnected together by the hydrodynamic flow relation:

<img src="https://render.githubusercontent.com/render/math?math=q(x,t) = \rho (x,t) v(x,t)">

The assunption of LWR models is that the flow is a funciton only of the density. The flow-density raltion is called _fundamental diagram_.
 CTM uses the simplest form of fundamental diagram, which has a triangular form

