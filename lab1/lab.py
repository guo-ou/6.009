#!/usr/bin/env python3

import sys
import math
import base64
#import tkinter

from io import BytesIO
from PIL import Image as PILImage

## NO ADDITIONAL IMPORTS ALLOWED!

class Image:
    def __init__(self, width, height, pixels):
        self.width = width
        self.height = height
        self.pixels = pixels

    ## converts a (x,y) coordinate to a list index
    def convert_xy_to_index(self, x, y):
        '''
        Converts (x,y) coordinates to a 1D list index on [0,len(self.pixels)]
        '''
        index = 0
        index += y*self.width
        index += x
        return index

    def array_to_list(self, array):
        '''
        Takes an array (a list of lists in which each element is a
        column of the array) and returns a row major list of entries
        of the same pixel values.
        '''
        output = []
        for i in range(len(array[0])):
            for j in range(len(array)):
                output.append(array[j][i])

        return output


    def list_to_array(self, inp_list, width):
        '''
        Takes a row-major 1D array and returns a list
        of lists of which the elements are the columns
        of the pixel array.
        '''
        array_T = []
        row = []
        for i in range(len(inp_list)):
            row.append(inp_list[i])
            if len(row) == width:
                array_T.append(row)
                row = []

        ## transposing the row matrix -- easier than trying to construct the column array from scratch
        array = [[array_T[j][k] for j in range(len(array_T))] for k in range(len(array_T[0]))]

        return array


    def get_pixel(self, x, y):
        '''
        Grabs the pixel value from given (x,y) coordinate pixel -- indexed from
        (0,0) at top-left in row-major form. Calls self.convert_xy_to_index.
        '''
        index = self.convert_xy_to_index(x,y)
        return self.pixels[index]

    def set_pixel(self, x, y, c):
        '''
        Assigns a value c to a given (x,y) coordinate pixel. Calls self.convert_xy_to_index.
        '''
        index = self.convert_xy_to_index(x,y)
        self.pixels[index] = c

    def apply_per_pixel(self, func):
        '''
        Loops over all pixels and applies some single-argument function
        to the pixel value at each coordinate.
        '''
        result = Image.new(self.width, self.height)
        for x in range(result.width):
            for y in range(result.height):
                color = self.get_pixel(x, y)
                newcolor = func(color)
                result.set_pixel(x, y, newcolor)
        return result


    def invert(self, c):
        '''
        Inverts the pixel value.
        '''
        return 255-c

    def inverted(self):
        '''
        Calls self.apply_per_pixel with the function self.invert.
        '''
        return self.apply_per_pixel(self.invert)

    def clip(self, im):
        '''
        Clips the pixel values such that they are on [0,255],
        as per the lab documentation request.
        '''
        for y in range(im.height):
            for x in range(im.width):
                value = im.get_pixel(x,y)
                if value < 0:
                    value = 0
                if value > 255:
                    value = 255
                im.set_pixel(x,y,value)
        return im


    def lin_comb(self, kernel, local):
        '''
        Returns the "linear combintion" value for a given kernal
        and a given local matrix of the same size. "Local Matrix"
        refers to a 1D array representing the pixels surrounding a
        given (x,y) coordinate.
        '''
        value = 0
        for i in range(len(kernel)):
            value += kernel[i]*local[i]
        return value

    def find_matrix(self,x, y, kernel):
        '''
        Returns the "Local Matrix" referenced above. The first for
        loop creates a matrix of (x,y) coordinates. The second strips
        away all improper coordinates as per the edge effect rules and
        then grabs the corresponding pixel value. Calls self.get_pixel
        '''
        dim = int(((len(kernel)**(1/2))-1)/2)
        matrix = []
        for stepy in range(-dim, dim + 1):
            for stepx in range(-dim, dim + 1):
                matrix.append([x + stepx, y+stepy])


        for i in range(len(matrix)):
            ##Filter for edge effects (LEFT and ABOVE)
            if matrix[i][0] < 0:
                matrix[i][0] = 0
            if matrix[i][1] < 0:
                matrix[i][1] = 0
            ##Filter for edge effects (RIGHT and BELOW)
            if matrix[i][0] > self.width-1:
                matrix[i][0] = self.width-1
            if matrix[i][1] > self.height-1:
                matrix[i][1] = self.height-1

            matrix[i] = self.get_pixel(matrix[i][0], matrix[i][1])

        return matrix

    def correlate(self, x, y, kernel):
        '''
        Instantiates the local matrix for a given (x,y) coordinate.
        Returns the linear combination value for said matrix and a given kernel.
        '''
        local = self.find_matrix(x,y,kernel)

        return self.lin_comb(kernel, local)

    def correlated(self, kernel):
        '''
        Loops over all pixels and performs self.correlate on each.
        The method self.apply_per_pixel is omitted from this function
        as it does not simply allow for a kernel argument.
        '''
        height = self.height
        width = self.width

        new_img = self.new(width, height)
        new_img.pixels = []
        for y in range(height):
            for x in range(width):
                new_img.pixels.append(int(round(self.correlate(x,y,kernel))))
        return new_img


    def blurred(self, n):
        '''
        Generates a kernel given some blurring factor n,
        and uses this kernel to call self.correlated.
        '''
        kernel = []
        value = 1.0/(n**2) # such that sum(kernal) == 1
        for i in range(n**2):
            kernel.append(value)

        new_img = self.correlated(kernel)
        new_img.clip(new_img) #Always perform clipping after correlation as it is NOT completed in self.correlated
        return new_img

    def sharpened(self, n):
        '''
        Generates an appropriate kernel for sharpening.
        Because this correlation operation is linear, the
        two steps to sharpen (2*original and -1*blur) can be
        encompassed in one kernel. Say the first kernel is A and
        the second is B, then Ax + Bx = new image. However, given
        linearity, (A+B)x = new image as well. So the two kernels
        are summed and then fed into self.correlated.
        '''
        kernel = []
        value = -1.0/(n**2) ## Negative version of the blur kernal from self.blurred
        for i in range(n**2):
            kernel.append(value)

        ## Add the other kernal below
        ## Example:
        ## 0 0 0   -1/n^2 -1/n^2 -1/n^2
        ## 0 2 0 + -1/n^2 -1/n^2 -1/n^2 = final kernal
        ## 0 0 0   -1/n^2 -1/n^2 -1/n^2
        ## the first matrix is 2*"identity" kernal from the documentation
        kernel[int((n-1)/2) + int(n*(n-1)/2)] += 2

        new_img = self.correlated(kernel)
        new_img.clip(new_img) ## always clip after running self.correlated
        return new_img



    def orth_mag(self, im1, im2):
        '''
        Computes the value described in the documentation for self.edges.
        Returns an image with properly computed pixel values at each location.
        '''
        new_img = self.new(self.width, self.height)
        new_img.pixels = []

        for y in range(self.height): ##self, im1, and im2 all have same dimensions
            for x in range(self.width):
                pixel_1 = im1.get_pixel(x,y)
                pixel_2 = im2.get_pixel(x,y)
                final_pixel = int(round((pixel_1**2 + pixel_2**2)**(1/2)))
                new_img.pixels.append(final_pixel)

        return new_img


    def edges(self):
        '''
        Performs the edge finding algorithm defined in the documentation.
        Creates two images with each kernal, and then applies
        self.orth_mag to both, and returns a final image.
        '''

        ## Given kernels
        x_kernel = [-1,0,1,
                    -2,0,2,
                    -1,0,1]
        y_kernel = [-1,-2,-1,
                    0,0,0,
                    1,2,1]

        x_image = self.correlated(x_kernel)
        y_image = self.correlated(y_kernel)

        final_img = self.orth_mag(x_image, y_image)
        final_img.clip(final_img)
        return final_img

    def energy_map(self):
        '''
        Returns a list of columns corresponding to edge activity at each pixels.
        '''
        e_map = self.edges()
        array = self.list_to_array(e_map.pixels, self.width)
        return array

    def seam_carved(self, n):
        '''
        Takes n (number of columns to remove). Generates a list of values
        corresponding to the energy in each column and them removes the
        column from the set of image pixels.
        '''
        array_pixels = self.list_to_array(self.pixels, self.width) ## array of pixels from image in column form
        array = self.energy_map() ## array of edge values in column form
        energy_map = []

        for column in array:

            energy_map.append(sum(column))


        for iteration in range(n):
            lowest_index = energy_map.index(min(energy_map))

            energy_map.pop(lowest_index)
            array_pixels.pop(lowest_index)

        new_img = self.new(self.width - n, self.height)
        new_img.pixels = self.array_to_list(array_pixels)


        return new_img




    # Below this point are utilities for loading, saving, and displaying
    # images, as well as for testing.

    def __eq__(self, other):
        return all(getattr(self, i) == getattr(other, i)
                   for i in ('height', 'width', 'pixels'))

    @classmethod
    def load(cls, fname):
        """
        Loads an image from the given file and returns an instance of this
        class representing that image.  This also performs conversion to
        grayscale.

        Invoked as, for example:
           i = Image.load('test_images/cat.png')
        """
        with open(fname, 'rb') as img_handle:
            img = PILImage.open(img_handle)
            img_data = img.getdata()
            if img.mode.startswith('RGB'):
                pixels = [round(.299*p[0] + .587*p[1] + .114*p[2]) for p in img_data]
            elif img.mode == 'LA':
                pixels = [p[0] for p in img_data]
            elif img.mode == 'L':
                pixels = list(img_data)
            else:
                raise ValueError('Unsupported image mode: %r' % img.mode)
            w, h = img.size
            return cls(w, h, pixels)

    @classmethod
    def new(cls, width, height):
        """
        Creates a new blank image (all 0's) of the given height and width.

        Invoked as, for example:
            i = Image.new(640, 480)
        """
        return cls(width, height, [0 for i in range(width*height)])

    def save(self, fname, mode='PNG'):
        """
        Saves the given image to disk or to a file-like object.  If fname is
        given as a string, the file type will be inferred from the given name.
        If fname is given as a file-like object, the file type will be
        determined by the 'mode' parameter.
        """
        out = PILImage.new(mode='L', size=(self.width, self.height))
        out.putdata(self.pixels)
        if isinstance(fname, str):
            out.save(fname)
        else:
            out.save(fname, mode)
        out.close()

    def gif_data(self):
        """
        Returns a base 64 encoded string containing the given image as a GIF
        image.

        Utility function to make show_image a little cleaner.
        """
        buff = BytesIO()
        self.save(buff, mode='GIF')
        return base64.b64encode(buff.getvalue())

    def show(self):
        """
        Shows the given image in a new Tk window.
        """
        global WINDOWS_OPENED
        if tk_root is None:
            # if tk hasn't been properly initialized, don't try to do anything.
            return
        WINDOWS_OPENED = True
        toplevel = tkinter.Toplevel()
        # highlightthickness=0 is a hack to prevent the window's own resizing
        # from triggering another resize event (infinite resize loop).  see
        # https://stackoverflow.com/questions/22838255/tkinter-canvas-resizing-automatically
        canvas = tkinter.Canvas(toplevel, height=self.height,
                                width=self.width, highlightthickness=0)
        canvas.pack()
        canvas.img = tkinter.PhotoImage(data=self.gif_data())
        canvas.create_image(0, 0, image=canvas.img, anchor=tkinter.NW)
        def on_resize(event):
            # handle resizing the image when the window is resized
            # the procedure is:
            #  * convert to a PIL image
            #  * resize that image
            #  * grab the base64-encoded GIF data from the resized image
            #  * put that in a tkinter label
            #  * show that image on the canvas
            new_img = PILImage.new(mode='L', size=(self.width, self.height))
            new_img.putdata(self.pixels)
            new_img = new_img.resize((event.width, event.height), PILImage.NEAREST)
            buff = BytesIO()
            new_img.save(buff, 'GIF')
            canvas.img = tkinter.PhotoImage(data=base64.b64encode(buff.getvalue()))
            canvas.configure(height=event.height, width=event.width)
            canvas.create_image(0, 0, image=canvas.img, anchor=tkinter.NW)
        # finally, bind that function so that it is called when the window is
        # resized.
        canvas.bind('<Configure>', on_resize)
        toplevel.bind('<Configure>', lambda e: canvas.configure(height=e.height, width=e.width))


try:
    tk_root = tkinter.Tk()
    tk_root.withdraw()
    tcl = tkinter.Tcl()
    def reafter():
        tcl.after(500,reafter)
    tcl.after(500,reafter)
except:
    tk_root = None
WINDOWS_OPENED = False

if __name__ == '__main__':

    im = Image.load("Lebron_james_paddle.jpg")
    output = im.edges()
    output = output.sharpened(5)
    output.save("Lebron_final.jpg")
    output.show()


    # the following code will cause windows from Image.show to be displayed
    # properly, whether we're running interactively or not:
    if WINDOWS_OPENED and not sys.flags.interactive:
        tk_root.mainloop()
