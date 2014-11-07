#Noir-Inator: a script to process individual Blender output images into a
#vectorized high-contrast single-file starting point for a comic book scene in SVG

#It responds to a very personal workflow and was intended for my own use

#Configuration in accompanying XML file, execution starts in line 96


import xml.etree.ElementTree as etree
from PIL import Image
import os


def bmpPreprocess(file, maxWidth = 1200):

    #This function optimizes the Blender output for tracing using PIL
    print 'Preprocessing ' + file + '...';

    #open image
    image = Image.open(file);

    width = image.size[0]; #note that Blender input is landscape so we use width as reference

    #convert to grayscale
    image = image.convert('L');

    #adjust size if needed
    if width > maxWidth:
        image.thumbnail((maxWidth,maxWidth), Image.ANTIALIAS);

    #save optimized version
    image.save(file);




def bmpTrace(file, steps = 8):

    #This function scripts tracing similar to the Inkscape "brightness steps" option using potrace
    #It is not yet implemented. Its output is a set of SVG files (provided for reference), 
    #each containing one of the original images and its raw tracing

    pass;




def svgPostProcessing(file, ns, background = 1, whiteLevels = 4):

    #This function postprocesses the trace, removing the original image and the background path(s)
    #It also removes shades to turn grayscale into black and white
    #Finally it inserts the relevant data in the general session SVG

    print 'Postprocessing ' + file + '...';

    #open SVG file
    document = etree.parse(file);
    svg = document.getroot();
    
    #find the main layer to work on
    layer = svg.find(ns + 'g');

    #remove original image from layer
    image = layer.find(ns + 'image');
    layer.remove(image);

    #identify relevant path group
    group = layer.find(ns + 'g');
    
    #delete number of background paths set in config
    for i in range(0,background):
        path = group.find(ns + 'path');
        group.remove(path);

    #turn grayscale into black and white
    #non-destructive, paths are not deleted but colored
    for counter, path in enumerate(group):
        if counter <= whiteLevels:
            path.set('style', "fill:#ffffff;fill-opacity:1");
        else:
            path.set('style', "fill:#000000;fill-opacity:1");

    #save svg
    document.write(file);
        
    #append relevant node to master svg
    masterLayer.append(group);

    #expand later: full rewrite of IDs to make them consecutive (low priority)
    





#### GENERAL PROCESSING AND CALLS #### 


#load config from XML file
settingsXML = etree.parse('noirinator.xml').getroot();
settings = {};

for element in settingsXML:
    settings[element.tag] = element.text;

    #expand later: strict validation for the XML (low priority)

#initialize empty master SVG
masterSvg = etree.parse('master.svg');
masterLayer = masterSvg.getroot().find(settings['xmlNamespace'] + 'g');

#read contents of input directory

for file in os.listdir(settings['inputDir']): 
    #expand later: warning if nothing was found here (low priority)

    if file.lower().endswith(".jpg"):

        bmpPreprocess(settings['inputDir'] + '/' + file, int(settings['imgMaxSize']));
        
        bmpTrace(file, int(settings['steps']));

        svgPostProcessing(  settings['processDir'] + '/' + file[:-3] + 'svg', 
                            settings['xmlNamespace'], 
                            int(settings['backgroundSteps']), 
                            int(settings['steps']) - int(settings['backgroundSteps']) - int(settings['blackSteps']) );


#expand later: align masterLayer children in 4:3 (medium priority)

#save final copy of master SVG
masterSvg.write('master.svg');

print 'Master SVG ready.';


