# Preprocessor for Riso Printing

Riso printing creates imperfect copies of a digital image using large bottles of ink and a made of rice paper.

<img width="300" alt="Riso style variation of a photograph" src="https://github.com/user-attachments/assets/0ca48c78-7091-490a-b1da-63130514e1a3" />

<img width="300" alt="Riso style variation of a photograph" src="https://github.com/user-attachments/assets/c1c88fa4-0200-4e4b-8799-24b60d81ac58" />


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

<img width="1650" height="865" alt="variations of a simple image" src="https://github.com/user-attachments/assets/d3f2d707-bf84-43c2-93c7-da95d48f52ce" />

<img width="1601" height="923" alt="variations of a landscape photograph" src="https://github.com/user-attachments/assets/24f9cc53-419b-45e0-9ef0-dab788cc1d4d" />





<!--- I'm not sure why I'd want to use 16 different ink colors. UPDATE I see it now

## GUI or CLI

Download and run the program and click around, or run it from the shell if you prefer command line interfaces, or need to batch process images.

TODO GUI
TODO screenshots
TODO batch demo
TODO animation in riso

### PROBLEMS
how to blend? CMYK uses subtractive, paint not pixels!
should i caree about color calibration or ICC profiles?
how does img subtraction work?
i tried so many combinations of blend, colorize, multiply, screen, add, subtract
https://prinfab.com/blog/simulating-a-screen-print-with-digital-print/ was difficult bc i dont know photoshop
https://graphicdesign.stackexchange.com/questions/55673/how-can-i-simulate-screen-printing-offset-colors-in-a-non-destructive-way PERFECT EXPLAIN

We set this layers Blend Mode to Screen. What this does is everything that is black will become the color we have chosen, everything that is white, will remain white. A 50% grey will look like a 50-50 mix of the color and white. Exactly what we want.
Bonus point is: If we double click on the Color Fill Layer we can change the color and immediately see the result in our image. This makes choosing spot color combinations for printing a lot easier.
Since this is inside a folder that is set to Multiply the effect of Screen won’t affect anything outside the folder (i.e. this won’t “screen” the other folders below)
Attention! The Blend Mode Screen handles transparency as if it would be black, which is confusing because we would rather assume to handle it as white. If your folder doesn’t have a solid white background, everything that is transparent will become the color you have chosen. To avoid this, but a white background at the end of each folder (e.g. by using a Color Fill set to white).
iterated with repl and lots of ctrl emacs jumping around to edit, some images i saved from the hektick process TODO

NOW I HAVE SPLIT UP AN IMAGE INTO GRAYSCALE LAYERS
COLORIZED EACH LAYER
AND BLENDED AS THOUGH THEY WERE PAINT!

now randomly shifting and randomizing hue/saturation for each ink color :)
as though the Riso layers had shifted or we had inks besides CMYK

TODO do i want Adobe RGB instead of srgb?


 -->
