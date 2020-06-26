"""
This module recognizes shapes in pictures
"""
import numpy as np
import sys
np.set_printoptions(threshold=sys.maxsize)
import matplotlib.image as img
import matplotlib.pyplot as plt

# sample user interaction idea
# img = library.image('pic1.png')
# img_contour = img.draw_contours()

class Picture:
    """
    Runs through ``orbitize`` methods in a standardized way.

    Args:
        input_data: Either a relative path to data file or astropy.table.Table object
            in the orbitize format. See ``orbitize.read_input``
        sampler_str (str): algorithm to use for orbit computation. "MCMC" for
            Markov Chain Monte Carlo, "OFTI" for Orbits for the Impatient
        num_secondary_bodies (int): number of secondary bodies in the system.
            Should be at least 1.
        system_mass (float): mean total mass of the system [M_sol]
        plx (float): mean parallax of the system [mas]
        mass_err (float, optional): uncertainty on ``system_mass`` [M_sol]
        plx_err (float, optional): uncertainty on ``plx`` [mas]
        lnlike (str, optional): name of function in ``orbitize.lnlike`` that will
            be used to compute likelihood. (default="chi2_lnlike")
        system_kwargs (dict, optional): ``restrict_angle_ranges``, ``ref_tau_epoch``,
            ``results`` for ``orbitize.system.System``.
        mcmc_kwargs (dict, optional): ``num_temps``, ``num_walkers``, and ``num_threads``
            kwargs for ``orbitize.sampler.MCMC``

    Written: Sarah Blunt, 2018
    """

    def __init__(self, file_name, threshold = 0.1):
        """class __init__ method 

        Note:
            Do not include the `self` parameter in the ``Args`` section.

        Args:
            file_name (str): The name of the image file to be loaded as a Picture object.
            threshold (float): Threshold value to determine whether or not an edge is present. This is passed as an attribute and then called in by the highlight_edges_grad method. Default value is 0.1 .

        Attributes:
            file_name (str): file name of the loaded image
            image     (np.array): [R G B] values of each pixel in the image
            contours  (np.array): copy of the [R G B] values of each pixel in the image, will be used to draw the detected edge over the original image
            height    (int): height of the image in px 
            width     (int): width of the image in px
            edges     (np.array): array of zeros with same dimensions as the image. whenever an edge is found, the "color difference" value is stored in the corresponding pixel 
            threshold (float): threshold to the "color difference" to determine the presence of an edge
            alpha     (bool): True if the loaded image has an alpha channel, False otherwise
        """
        self.file_name = file_name 
        self.image = img.imread(file_name) # numpy array of r-g-b values
        self.contours = img.imread(file_name) # image copy for including highligthed edges
        self.height= len(self.image)
        self.width = len(self.image[0])
        self.edges = np.zeros((self.height, self.width)) # numpy array with 1s as edges
        self.threshold = threshold

        if len(self.image[0][0]) == 4:
            self.alpha = True
        else:
            self.alpha = False
     
    def __len__(self):
        """
        Special len method 
        
        Returns:
            int: total number of pixels            
        """
        return self.height * self.width

    def __str__(self):
        """
        Special str method 
        
        Returns:
            str: string with info on filename and image size            
        """
        return f'File name: {self.file_name}; width: {self.width}px, height: {self.height}px'

    def __del__(self):
        """
        Special del method 
        
        It deletes a picture object and prints a report of the deletion
        """
        print(f'I just deleted {self.file_name}')
    
    
    def assess_difference(self, pixel_a, pixel_b):
        """
        This function checks if two adjacent pixels have the exact same RGB value
        
        Args:
            pixel_a (float, list): [r,g,b] values for pixel A  
            pixel_b (float, list): [r,g,b] values for pixel B

        Returns:
            bool: True if the two pixel have the same RGB values 
        """
        
        return np.array_equal(pixel_a, pixel_b)

    def horizontal_scan(self, row_index):
        """
        This function performs a linear scan over a given row
        
        Args:
            row_index (int): index of row to scan in self.image 
        """
        for i in range(1, self.width):
            # compare each pixel to the previous one
            if not self.assess_difference(self.image[row_index][i-1], self.image[row_index][i]):
                self.edges[row_index][i] = 1
                
    def vertical_scan(self, col_index):
        '''
        This function performs a linear scan over a given column
        Args:
            col_index - index of column in self.image to scan
        '''
        
        for i in range(1, self.height):
            # compare each pixel to the previous one
            if not self.assess_difference(self.image[i-1][col_index], self.image[i][col_index]):
                self.edges[i][col_index] = 1
        
    def find_edges(self):
        '''
        ...
        '''
        for i in range(self.width):
            self.vertical_scan(i)
        
        for i in range(self.height):
            self.horizontal_scan(i)

    def highlight_edges(self): 
        '''
        '''       
        if self.alpha:
            for i in range(self.height): 
                for j in range(self.width): 
                    if self.edges[i][j] == 0:
                        # print(self.contours[i][j])
                        self.contours[i][j] = [0, 0, 0, 1]
                    else:
                        # print(self.contours[i][j])
                        self.contours[i][j] = [1, 1, 1, 1]
        else:     
            for i in range(self.height): 
                for j in range(self.width): 
                    if self.edges[i][j] == 0:
                        # print(self.contours[i][j])
                        self.contours[i][j] = [0, 0, 0]
                    else:
                        # print(self.contours[i][j])
                        self.contours[i][j] = [1, 1, 1]


    def assess_gradient(self, pixel_a, pixel_b):
        '''
        This function checks if two adjacent pixels have the exact same RGB value
        
        Args:
            pixel_a - list: [r,g,b] values for pixel A  
            pixel_b - list: [r,g,b] values for pixel B
        '''
        diff = np.abs(pixel_a - pixel_b).sum()
        # grad = diff / self.scale    

        return diff

    def horizontal_scan_grad(self, row_index):
        '''
        This function performs a linear scan over a given row
        
        Args:
            row_index - index of row in self.image to scan
        '''
        
        for i in range(1, self.width):
            # compare each pixel to the previous one
            hor_grad = self.assess_gradient(self.image[row_index][i-1], self.image[row_index][i])
            self.edges[row_index][i] = max(self.edges[row_index][i], hor_grad)
                
    def vertical_scan_grad(self, col_index):
        '''
        This function performs a linear scan over a given column
        Args:
            col_index - index of column in self.image to scan
        '''
        
        for i in range(1, self.height):
            # compare each pixel to the previous one
            vert_grad = self.assess_gradient(self.image[i-1][col_index], self.image[i][col_index])
            self.edges[i][col_index] = max(self.edges[i][col_index], vert_grad)

    def find_edges_grad(self):
        '''
        ...
        '''
        for i in range(self.width):
            self.vertical_scan_grad(i)
        
        for i in range(self.height):
            self.horizontal_scan_grad(i)

    def highlight_edges_grad(self): 
        '''
        '''       
        if self.alpha:
            for i in range(self.height): 
                for j in range(self.width): 
                    if self.edges[i][j] < self.threshold:
                        # print(self.contours[i][j])
                        self.contours[i][j] = [0, 0, 0, 1]  #drawing black
                    else:
                        # print(self.contours[i][j])
                        # if self.contours[i][j]
                        self.contours[i][j] = [1, 1, 1, 1]   #drawing the edge 
        else:     
            for i in range(self.height): 
                for j in range(self.width): 
                    if self.edges[i][j] < self.threshold:
                        # print(self.contours[i][j])
                        self.contours[i][j] = [0, 0, 0]
                    else:
                        # print(self.contours[i][j])
                        self.contours[i][j] = [1, 1, 1]


    def check_num_edges(self):
        '''
        '''
        tot_edges = 0
        for row in self.edges:
            tot_edges += sum(row)
        return tot_edges


    def paint_contours(self, grad = False):
        print('Working on the following image:')
        print(self)
        if grad: 
            self.find_edges_grad()
            print(f'I found {self.check_num_edges()} edges.')
            self.highlight_edges_grad()
        else:
            self.find_edges()   
            print(f'I found {self.check_num_edges()} edges.')
            self.highlight_edges()            
        
        plt.imshow(self.contours)
                    
                
# for th in np.linspace(0.1, 1., 10, endpoint=True):
#     print(f'Threshold is {th}')
#     image_to_process = Picture('pic6.png', threshold = th)


image_to_process = Picture('pic6.png')


image_to_process.paint_contours(grad=True)
plt.show()