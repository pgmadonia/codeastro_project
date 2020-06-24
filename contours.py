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
    '''

    def __init__(self, file_name):
        self.file_name = file_name 
        self.image = img.imread(file_name) # numpy array of r-g-b values
        self.contours = img.imread(file_name) # image copy for including highligthed edges
        self.height= len(self.image)
        self.width = len(self.image[0])
        self.edges = np.zeros((self.height, self.width)) # numpy array with 1s as edges
     
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
            pixel_a - tuple: (r,g,b) values for pixel A  
            pixel_b - tuple: (r,g,b) values for pixel B
        '''
        return pixel_a.all() == pixel_b.all()

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
        # poison green: R-24 G-95 B-1
        for i in range(self.height): # 0 - 639
            for j in range(self.width): # 0 - 479
                if self.edges[i][j] == 1:
                    print(self.contours[i][j])
                    self.contours[i][j] = [1, 1, 1]
                else:
                    print(self.contours[i][j])
                    self.contours[i][j] = [0, 0, 0]  

     
image_to_process = Picture('pic3.png')

# print(len(image_to_process))
print(image_to_process)

image_to_process.find_edges()
image_to_process.highlight_edges()

# fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(10, 5))
# ax[0] = plt.imshow(image_to_process.contours)
# ax[1] = plt.imshow(image_to_process.image)

imgshow = plt.imshow(image_to_process.contours)

plt.show()

# print(image_to_process.contours)

# print(len(image_to_process.edges))
# print(len(image_to_process.edges[0]))
# print(len(image_to_process.image))
# print(len(image_to_process.image[0]))

# print(len(image_to_process.contours))
# print(len(image_to_process.contours[0]))
# print(type(img))