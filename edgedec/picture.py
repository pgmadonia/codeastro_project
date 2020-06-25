import numpy as np
import sys
np.set_printoptions(threshold=sys.maxsize)
import matplotlib.image as img
import matplotlib.pyplot as plt

# sample user interaction idea
# img = library.image('pic1.png')
# img_contour = img.draw_contours()

class Picture:
    '''
    This class conta
    '''

    def __init__(self, file_name, threshold = 0.1):
        self.file_name = file_name 
        self.image = img.imread(file_name) # numpy array of r-g-b values
        self.contours = img.imread(file_name) # image copy for including highligthed edges
        self.height= len(self.image)
        self.width = len(self.image[0])
        self.edges = np.zeros((self.height, self.width)) # numpy array with 1s as edges
        self.scale = 0.05 * min(self.height, self.width) # ~~~ from 0.8 (16px) to 120 (2400px)
        self.threshold = threshold

        if len(self.image[0][0]) == 4:
            self.alpha = True
        else:
            self.alpha = False
     
    def __len__(self):
        '''
        This function returns the total number of pixels            
        '''
        return self.height * self.width

    def __str__(self):
        return f'File name: {self.file_name}; width: {self.width}px, height: {self.height}px'

    def __del__(self):
        print(f'I just deleted {self.file_name}')
    
    
    def assess_difference(self, pixel_a, pixel_b):
        '''
        This function checks if two adjacent pixels have the exact same RGB value
        
        Args:
            pixel_a - list: [r,g,b] values for pixel A  
            pixel_b - list: [r,g,b] values for pixel B
        '''
        # print(type(pixel_a))
        # print(type(pixel_b))
 
        return np.array_equal(pixel_a, pixel_b)
        # return pixel_a == pixel_b #pixel_a[0] == pixel_b[0] and pixel_a[1] == pixel_b[1] and pixel_a[2] == pixel_b[2]   

    def horizontal_scan(self, row_index):
        '''
        This function performs a linear scan over a given row
        
        Args:
            row_index - index of row in self.image to scan
        '''
        
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
                    
                
for th in np.linspace(0.1, 1., 10, endpoint=True):
    print(f'Threshold is {th}')
    image_to_process = Picture('pic6.png', threshold = th)
    # image_to_process = Picture('donut.png')


    image_to_process.paint_contours(grad=True)
    plt.show()