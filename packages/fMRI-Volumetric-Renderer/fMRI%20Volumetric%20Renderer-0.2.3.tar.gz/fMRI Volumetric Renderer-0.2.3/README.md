# fMRI-Volumetric-Renderer
A volumetric fMRI renderer for the web. Built using WebGL.

This project presents a method for visualizing volumetric MRI and fMRI data based on a discrete raytracing algorithm and OpenGL.
Data is pre-processed and then attached to the html template document, the renderer itself is written in html. This method presents a lightweight 
renderer that can be used to visualize fMRI data in a browser as well as in the output of a jupyter notebook.

## Python Render Pipeline Usage
```python
import nibabel as nib
import torch

import volume_plot_utils

#load an example nifti file
brainData = nib.load("data/sub-0x/func/subject-data-file.nii.gz")

#load the nifti data into a pytorch tensor
activationSequence = torch.tensor(brainData.get_fdata().T)

#use the displayVolume function to display the volumetric data in ipynb
displayVolume(activationSequence)
```

## General HTML Template Usage
The example python shows usage with pytroch and nibabel but html displays can be created from a template by substituting keywords from the template file:
see volume_plot_utils.py for more information


Interactive example:
https://kappnkrunch.github.io/fMRI-Volumetric-Renderer/example1.html

![Gif showing the renderer](view.gif "MRI view")
