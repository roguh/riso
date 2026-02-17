# Preprocessor for Riso Printing

Riso printing creates imperfect copies of a digital image using large bottles of ink and a made of rice paper.

![_FEL9990_plus_9994 _2_15](https://github.com/user-attachments/assets/0ca48c78-7091-490a-b1da-63130514e1a3)

![M](https://github.com/user-attachments/assets/c1c88fa4-0200-4e4b-8799-24b60d81ac58)


The printer uses a thermal head to burn the digital image into rice paper, called the master stencil.
One stencil is required per ink color.
Some Riso workshops have up 16 different ink colors, which can be
combined to form any desired shade and creative effects like an oil painting.
Light colors are printed first, and the paper must be inserted into the machine to print each layer therefore imperfections are celebrated.

This is comparable to screenprinting where ink is pressed upon a stencil to create multiple prints.

理想 - Riso is Japanese for ideal.

## How to print a photo?

The Risograph printer prints one color at a time at any intensity, so a color image must be split into 3 separate grayscale images, each allowing for artistic input.

A simple way to convert an image for Riso printing is to split the image into CMYK channels (cyan, magenta, yellow, and black), and blend the black layer into each of the other layers.

This code takes a PNG image and splits it into 3 grayscale images, with a varying amount of the black color layer blended into the cyan, yellow, and magenta images.

## How to see what will be printed?

This code simulates the result of printing to a Risograph machine, depending on what colors of ink you have available.

It blends any number of images, blending each usingspecific ink colors.
I recommend color calibrating your monitor.

Simulation and fast iteration are fantastic for creative control, and trying out different limits.

# Variation explorer!

Imagine we replace the red,  green, and blue inks with different colors that are slightly or very different. Imagine we shift each color layer slightly. See any that stand out?

<img width="1650" height="865" alt="2026-02-16_22-59-15" src="https://github.com/user-attachments/assets/d3f2d707-bf84-43c2-93c7-da95d48f52ce" />

<img width="1601" height="923" alt="2026-02-16_22-53-05" src="https://github.com/user-attachments/assets/24f9cc53-419b-45e0-9ef0-dab788cc1d4d" />
