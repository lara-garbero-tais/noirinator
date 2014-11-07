noirinator
==========

Python scripts to process individual Blender output images into a vectorized high-contrast single-file starting point for a comic book scene in SVG

3 stages:
-Optimizes the Blender output for tracing using PIL
-Traces using Potrace and Inkscape's model for grayscale
-Postprocesses back to non-destructive BN and joins SVGs
