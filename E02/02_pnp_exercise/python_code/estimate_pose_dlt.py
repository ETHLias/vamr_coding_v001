import numpy as np

def estimatePoseDLT(p, P, K):
    # Estimates the pose of a camera using a set of 2D-3D correspondences
    # and a given camera matrix.
    # 
    # p  [n x 2] array containing the undistorted coordinates of the 2D points
    # P  [n x 3] array containing the 3D point positions
    # K  [3 x 3] camera matrix
    #
    # Returns a [3 x 4] projection matrix of the form 
    #           M_tilde = [R_tilde | alpha * t] 
    # where R is a rotation matrix. M_tilde encodes the transformation 
    # that maps points from the world frame to the camera frame

    

    # Convert 2D to normalized coordinates
    # TODO: Your code here
    # -------------------------------------------------------
    # Step 1: Homogenize coordinates
    P_3d = np.hstack((P, np.ones((P.shape[0], 1))))    # [X Y Z 1]
    p_2d = np.hstack((p, np.ones((p.shape[0], 1))))    # [u v 1]
    
    # Step 2: Normalize image coordinates (remove intrinsics)
    p_2d_normalized = np.linalg.inv(K) @ p_2d.T
    p_2d_normalized /= p_2d_normalized[2, :]           # divide by last coordinate
    

    # Build measurement matrix Q
    # TODO: Your code here
    # -------------------------------------------------------
    # Step 3: Build measurement matrix Q
    Q = []
    for i in range(P.shape[0]):
        X, Y, Z, _ = P_3d[i, :]
        x, y = p_2d_normalized[0, i], p_2d_normalized[1, i]

        row1 = [X, Y, Z, 1, 0, 0, 0, 0, -x*X, -x*Y, -x*Z, -x]
        row2 = [0, 0, 0, 0, X, Y, Z, 1, -y*X, -y*Y, -y*Z, -y]
        Q.append(row1)
        Q.append(row2)

    Q = np.array(Q)
            
    #print("Measurement Matrix Q:")
    #print(Q)

    # Solve for Q.M_tilde = 0 subject to the constraint ||M_tilde||=1
    # TODO: Your code here
    # -------------------------------------------------------
    # Step 4: Solve Qm = 0 with SVD
    U, S, Vt = np.linalg.svd(Q)
    M_tilde = Vt[-1, :].reshape(3, 4)   # projection matrix


    # Find the closest orthogonal matrix to R
    # https://en.wikipedia.org/wiki/Orthogonal_Procrustes_problem
    # TODO: Your code here
    # -------------------------------------------------------
    # Step 5: Extract [R_tilde | t_tilde]
    R_tilde = M_tilde[:, 0:3]
    t_tilde = M_tilde[:, 3]

    # Fix sign (ensure positive depth)
    if t_tilde[2] < 0:
        R_tilde = -R_tilde
        t_tilde = -t_tilde
    

    # Normalization scheme using the Frobenius norm:
    # recover the unknown scale using the fact that R_tilde is a true rotation matrix
    # TODO: Your code here
    # -------------------------------------------------------
    # Step 6: Recover scale and enforce orthogonality of R
    # Solve Orthogonal Procrustes problem: closest rotation matrix
    U_r, _, Vt_r = np.linalg.svd(R_tilde)
    R = U_r @ Vt_r

    # Enforce det(R) = +1
    if np.linalg.det(R) < 0:
        R = -R
        t_tilde = -t_tilde

    # Recover scale α using Frobenius norm
    alpha = np.linalg.norm(R_tilde, 'fro') / np.linalg.norm(R, 'fro')
    t = t_tilde / alpha


    # Build M_tilde with the corrected rotation and scale
    # TODO: Your code here
    # -------------------------------------------------------
    # Step 7: Rebuild final projection matrix
    M_final = np.hstack((R, t.reshape(-1, 1)))
    
    return M_final
    
    
    
    
