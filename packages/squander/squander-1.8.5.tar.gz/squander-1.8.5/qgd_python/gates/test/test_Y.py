import numpy as np
import random

from qiskit import QuantumCircuit
from qiskit.visualization import plot_histogram

from qgd_python.utils import get_unitary_from_qiskit_circuit
from qgd_python.gates.qgd_Y import qgd_Y
from scipy.stats import unitary_group


class Test_operations_squander:
    """This is a test class of the python iterface to compare the SQUANDER and the qiskit decomposition"""



    def test_Y_get_matrix(self):          
        r"""
        This method is called by pytest. 
        Test to create an instance of X gate and compare with qiskit.
        """

        pi=np.pi

        for qbit_num in range(1,7):

	    #SQUANDER#

            target_qbit=qbit_num-1

            Y = qgd_Y( qbit_num, target_qbit )

            # get the matrix                
            Y_squander = Y.get_Matrix( )

	    #QISKIT

            # Create a Quantum Circuit acting on the q register
            circuit = QuantumCircuit(qbit_num)

            # Add the CNOT gate on control qbit and target qbit
            circuit.y( target_qbit )

            # the unitary matrix from the result object
            Y_qiskit = get_unitary_from_qiskit_circuit( circuit )
            Y_qiskit = np.asarray(Y_qiskit)          
        
            #the difference between the SQUANDER and the qiskit result        
            delta_matrix=Y_squander-Y_qiskit

            # compute norm of matrix
            error=np.linalg.norm(delta_matrix)

            #print("Get_matrix: The difference between the SQUANDER and the qiskit result is: " , np.around(error,2))
            assert( error < 1e-3 ) 
           

    def test_Y_apply_to(self):
        r"""
        This method is called by pytest. 
        Test to create an instance of X gate and compare with qiskit.
        """

        pi=np.pi

        for qbit_num in range(1,7):

            # target qbit  
            target_qbit=qbit_num-1

            # creating an instance of the C++ class
            Y = qgd_Y( qbit_num, target_qbit )
   
            #create text matrix for apply_to 
            test_matrix= np.identity( 2**qbit_num, dtype=complex )

	    #QISKIT
            # Create a Quantum Circuit acting on the q register
            circuit = QuantumCircuit(qbit_num)

            # Add the CNOT gate on control qbit and target qbit
            circuit.y( target_qbit )

            # the unitary matrix from the result object
            Y_qiskit = get_unitary_from_qiskit_circuit( circuit )
            Y_qiskit = np.asarray(Y_qiskit)  
   
            # apply the gate on the input array/matrix  
            #Y_qiskit_apply_gate=np.matmul(Y_qiskit, test_matrix)

	    #SQUANDER

            Y_squander = test_matrix

            # apply the gate on the input array/matrix                
            Y.apply_to(Y_squander)          

            #the difference between the SQUANDER and the qiskit result        
            delta_matrix=Y_squander-Y_qiskit

            # compute norm of matrix
            error=np.linalg.norm(delta_matrix)

            #print("Apply_to: The difference between the SQUANDER and the qiskit result is: " , np.around(error,2))
            assert( error < 1e-3 ) 



