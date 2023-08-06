# NOBM
Benchmarking suite for non-linear optimization algorithms

---

**Version 1.0.1**

Testing suite aims to benchmark derivative-free optimization (DFO) algorithms mainly 'OMADS.py' and multidisciplinary
design optimization (MDO) algorithms


---
## License & copyright

© Ahmed H. Bayoumy 
---
---
## Installation

```commandline
$ pip install NOBM
```
---
## How to use

After installing the libraries listed in the `requirements.txt`, `NOBM` can be imported in the optimization solver code. 
For benchmarking `OMADS`, the path of the JSON template, which contains the problem setup, should be entered as an 
input argument to the `OMADS.py` call. 

```commandline
python BMDFO.py uncon .\tests
```

```commandline
from NOBM.toy import * 
```

