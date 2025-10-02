import numpy as np

def reprojectPoints(P, M_tilde, K):
    # Reproject 3D points given a projection matrix
    #
    # P         [n x 3] coordinates of the 3d points in the world frame
    # M_tilde   [3 x 4] projection matrix
    # K         [3 x 3] camera matrix
    #
    # Returns [n x 2] coordinates of the reprojected 2d points

    
    # TODO: Your code here
    # Homogenize 3D points
    P_h = np.hstack((P, np.ones((P.shape[0], 1))))    # [X Y Z 1]
    
    # Project into camera
    p_h = (K @ M_tilde) @ P_h.T   # shape (3,n)
    
    # Normalize by depth (last row)
    p_h /= p_h[2, :]
    
    # Return in [n x 2]
    return p_h[:2, :].T


