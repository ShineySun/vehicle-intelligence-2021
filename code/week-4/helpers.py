import numpy as np

# Calculate Euclidean distance between two 2-D points.
def distance(p1, p2):
    dx = p1['x'] - p2['x']
    dy = p1['y'] - p2['y']
    d = np.sqrt(dx ** 2 + dy ** 2)
    return d

def gaussian_distribution(x,y,ass_x, ass_y, sigma_x, sigma_y):
    return 1 / (2 * np.pi * sigma_x * sigma_y) * np.exp(-0.5*(np.power((x-ass_x)/sigma_x,2) + np.power((y-ass_y)/sigma_y,2)))
