"""Class to dectect edges in a picture"""
import numpy as np
import sys
np.set_printoptions(threshold=sys.maxsize)
import matplotlib.image as img
import matplotlib.pyplot as plt

# sample user interaction idea
# img = library.image('pic1.png')
# img_contour = img.draw_contours()

class Picture:
    """ Picture class.

    This class offers a series of methods to load in a picture using matplotlib.image and then find the edges between pixels with different colors in it.
    
    Note:
        Do not include the `self` parameter in the ``Args`` section.

    Args:
        file_name (str): The name of the image file to be loaded as a Picture object.
        threshold (float): Threshold value to determine whether or not an edge is present. 
            This is passed as an attribute and then called in by the highlight_edges_grad method. Default value is 0.1 .

    Attributes:
        file_name (str): file name of the loaded image
        image     (np.array): [R G B] values of each pixel in the image
        contours  (np.array): copy of the [R G B] values of each pixel in the image, will be used to draw the detected edge over the original image
        height    (int): height of the image in px 
        width     (int): width of the image in px
        edges     (np.array): array of zeros with same dimensions as the image. 
            Whenever an edge is found, value of the corresponding pixel is switched to 1 (if the highlight_edges method is called), 
            or the "color difference" value is stored in the corresponding pixel (if the highlight_edges_grad method is called).
        alpha     (bool): True if the loaded image has an alpha channel, False otherwise

    
    Written: Gullo, Mikulas, Paolo 2020
    """
    def __init__(self, file_name, threshold = 0.1):
        """ class __init__ method 
        """
        self.file_name = file_name 
        self.image = img.imread(file_name) # numpy array of r-g-b values
        self.contours = img.imread(file_name) # image copy for including highligthed edges
        self.height= len(self.image)
        self.width = len(self.image[0])
        self.edges = np.zeros((self.height, self.width)) # numpy array with 1s as edges

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
        This function performs a linear scan over a given row. It calls the assess_difference method on each couple of pixel in the row, 
            and every time this returns False it changes the corresponding pixel value to 1 in self.edges. 
        
        Args:
            row_index (int): index of row to scan in self.image 
        """
        for i in range(1, self.width):
            # compare each pixel to the previous one
            if not self.assess_difference(self.image[row_index][i-1], self.image[row_index][i]):
                self.edges[row_index][i] = 1
                
    def vertical_scan(self, col_index):
        """
        This function performs a linear scan over a given column. It calls the assess_difference method on each couple of pixel in the column,
            and every time this returns False it changes the corresponding pixel value to 1 in self.edges. 
        
        Args:
            col_index (int): index of column to scan in self.image 
        """
        
        for i in range(1, self.height):
            # compare each pixel to the previous one
            if not self.assess_difference(self.image[i-1][col_index], self.image[i][col_index]):
                self.edges[i][col_index] = 1
        
    def find_edges(self):
        """
        This method calls the vertical_scan and horizontal_scan methods to find edges within the image.

        """
        for i in range(self.width):
            self.vertical_scan(i)
        
        for i in range(self.height):
            self.horizontal_scan(i)

    def highlight_edges(self): 
        """
        highlight_edges

        This method cycles over the image rows and columns in self.edges. Whenever it finds a nonzero value, 
        it changes the corresponding pixel value in self.contours to [1,1,1] or [1,1,1,1] (depending on wether or not self.alpha is true). 
        """
        if self.alpha:
            for i in range(self.height): 
                for j in range(self.width): 
                    if self.edges[i][j] == 0:
                        # print(self.contours[i][j])
                        self.contours[i][j] = [0, 0, 0, 1]
                        # pass
                    else:
                        # print(self.contours[i][j])
                        self.contours[i][j] = [1, 1, 1, 1]
        else:     
            for i in range(self.height): 
                for j in range(self.width): 
                    if self.edges[i][j] == 0:
                        # print(self.contours[i][j])
                        self.contours[i][j] = [0, 0, 0]
                        # pass
                    else:
                        # print(self.contours[i][j])
                        self.contours[i][j] = [1, 1, 1]


    def assess_gradient(self, pixel_a, pixel_b):
        """
        This function measures the "color difference" between two adjacent pixels
        
        Args:
            pixel_a (float, list): [r,g,b] values for pixel A  
            pixel_b (float, list): [r,g,b] values for pixel B

        Returns:
            float: "color difference" between two pixels, defined as the sum of the absolute difference over the R, G and B parameters  
        """    
        diff = np.abs(pixel_a - pixel_b).sum()
        return diff

    def horizontal_scan_grad(self, row_index):
        """
        This function performs a linear scan over a given row. It calls the assess_gradient method on each couple of pixel in the row. For each pixel, it stores in self.edges the maximum value between the current value in self.edges and the "color difference" returned by assess_gradient. 
        
        Args:
            row_index (int): index of row to scan in self.image 
        """
        for i in range(1, self.width):
            # compare each pixel to the previous one
            hor_grad = self.assess_gradient(self.image[row_index][i-1], self.image[row_index][i])
            self.edges[row_index][i] = max(self.edges[row_index][i], hor_grad)
                
    def vertical_scan_grad(self, col_index):
        """
        This function performs a linear scan over a given column. It calls the assess_gradient method on each couple of pixel in the column. For each pixel, it stores in self.edges the maximum value between the current value in self.edges and the "color difference" returned by assess_gradient. 
        
        Args:
            col_index (int): index of column to scan in self.image 
        """
        for i in range(1, self.height):
            # compare each pixel to the previous one
            vert_grad = self.assess_gradient(self.image[i-1][col_index], self.image[i][col_index])
            self.edges[i][col_index] = max(self.edges[i][col_index], vert_grad)

    def find_edges_grad(self):
        """
        This method calls the vertical_scan_grad and horizontal_scan_grad methods to find edges within the image.
        """
        for i in range(self.width):
            self.vertical_scan_grad(i)
        
        for i in range(self.height):
            self.horizontal_scan_grad(i)

    def highlight_edges_grad(self, threshold): 
        """
        highlight_edges_grad

        This method cycles over the image rows and columns in self.edges. Whenever it finds a value above the threshold, 
        it changes the corresponding pixel value in self.contours to [1,1,1] or [1,1,1,1] (depending on wether or not self.alpha is true). 
        """       
        if self.alpha:
            for i in range(self.height): 
                for j in range(self.width): 
                    if self.edges[i][j] < threshold:
                        # print(self.contours[i][j])
                        self.contours[i][j] = [0, 0, 0, 1]  #drawing black
                        # pass
                    else:
                        # print(self.contours[i][j])
                        # if self.contours[i][j]
                        self.contours[i][j] = [1, 1, 1, 1]   #drawing the edge white 
                        # self.contours[i][j] = [0, 1, 0, 1]   #drawing the edge green
        else:     
            for i in range(self.height): 
                for j in range(self.width): 
                    if self.edges[i][j] < threshold:
                        # print(self.contours[i][j])
                        self.contours[i][j] = [0, 0, 0]
                        # pass
                    else:
                        # print(self.contours[i][j])
                        self.contours[i][j] = [1, 1, 1] #white
                        # self.contours[i][j] = [0, 1, 0] #green


    # def check_num_edges(self):
    #     '''
    #     '''
    #     tot_edges = 0
    #     for row in self.edges:
    #         tot_edges += sum(row)
    #     return tot_edges


    def paint_contours(self, grad = False, threshold = 0.1):
        """
        paint_contours

        This method runs the find_edges and highlight_edges methods over the image

        Args:
            grad (bool): if True, it will call the find_edges_grad and highlight_edges_grad methods instead. Default value is False 
            threshold (float): value over which a "color difference" detected by highlight_edges_grad is considered an edge
        """
        print('Working on the following image:')
        print(self)
        if grad: 
            self.find_edges_grad()
            # print(f'I found {self.check_num_edges()} edges.')
            self.highlight_edges_grad(threshold)
        else:
            self.find_edges()   
            # print(f'I found {self.check_num_edges()} edges.')
            self.highlight_edges()     

        fig = plt.figure(figsize=(10, 5))
        ax = fig.add_subplot(1,2,1)
        bx = fig.add_subplot(1,2,2)
        ax.imshow(self.image)
        bx.imshow(self.contours)
        ax.set_title('Original Image') 
        bx.set_title('Edge Contour') 
        plt.show()
        # plt.imshow(self.contours)
                    
                
# for th in np.linspace(0.1, 1., 10, endpoint=True):
#     print(f'Threshold is {th}')
#     image_to_process = Picture('pic6.png', threshold = th)

if __name__ == "__main__":
    image_to_process = Picture('pic1.png')
    image_to_process.paint_contours(grad=True)
    plt.show()