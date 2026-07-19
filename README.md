# photo-mosaic

A Python-based image processing tool that uses the Python Imaging Library (PIL/Pillow) to create a photomosaic based o dictionary of source images.

A photomosaic (or photographic mosaic) is a large image composed of hundreds or thousands of smaller photographs (tiles).

## Features

* **Image Pixelation:** Pixelates an image by dividing it into squares and then getting the average RGB values for those squares.
* **Color Distance Matching:** Uses a 3D Pythagorean/Euclidean distance formula ($$\text{Distance} = \sqrt{(R_2 - R_1)^2 + (G_2 - G_1)^2 + (B_2 - B_1)^2}$$) to find the best matching source image for a given square.
* **Caching System:** Saves and loads pre-calculated data (source image RGB values) to minimise run time.
---

## Requirements

- Python
- Pillow (library for image processing)


A big thanks to Robert Heaton.