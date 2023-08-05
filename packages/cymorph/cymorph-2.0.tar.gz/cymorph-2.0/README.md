# CyMorph - non-parametric galaxy morphology package
_Updated and adjusted and repacked version of 1st CyMorph version:
https://github.com/rsautter/CyMorph & Paulo Barchi work_


## Installation
Dependencies:
```
pip install numpy scipy matplotlib seaborn sep
```
CyMorph can be installed with:
```
pip install cymorph
```

## Documentation
https://cymorph.readthedocs.io/

## Basic Usage


### Concentration
```
from cymorph.concentration import Concentration
c = Concentration(image, radius1, radius2) 
c.get_concentration()
```

### Asymmetry
```
from cymorph.asymmetry import Asymmetry
a = Asymmetry(image) 
a.get_pearsonr()
a.get_spearmanr()
a.get_collected_points_plot()
```

### Smoothness
```
from cymorph.smoothness import Smoothness
s = Smoothness(clean_image, segmented_mask, smoothing_degradation, butterworth_order) 
s.get_pearsonr() 
s.get_spearmanr()
s.get_smoothed_image()
s.get_collected_points_plot()
```


### Entropy
```
from cymorph.entropy import Entropy
e = Entropy(image, bins) 
e.get_entropy()
```


### G2
```
from cymorph.g2 import G2
g2 = G2(g2_modular_tolerance, g2_phase_tolerance, g2_position_tolerance) 
g2.get_g2()
g2.get_gradient_plot()
g2.get_asymmetry_gradient_plot()
```

### Contributors

- Igor Kolesnikov
- Vitor Sampaio
- Paulo Barchi
- Rubens Sautter