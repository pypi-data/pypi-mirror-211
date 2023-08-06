import numpy as np
import random
import math

from qiskit import QuantumCircuit
from qiskit.visualization import plot_histogram

from qgd_python.utils import get_unitary_from_qiskit_circuit
from qgd_python.gates.qgd_SX import qgd_SX
from scipy.stats import unitary_group
      

class Test_operations_squander:
    """This is a test class of the python iterface to compare the SQUANDER and the qiskit decomposition"""




    def test_SX_get_matrix(self):
        r"""
        This method is called by pytest. 
        Test to create an instance of U3 gate and compare with qiskit.
        """

        pi=np.pi

        for qbit_num in range(1,7):

            # target qbit
            target_qbit = qbit_num-1

            # creating an instance of the C++ class
            SX = qgd_SX( qbit_num, target_qbit )

	    #SQUANDER#

            # get the matrix                       
            SX_squander = SX.get_Matrix( )
      
	    #QISKIT

            # Create a Quantum Circuit acting on the q register
            circuit = QuantumCircuit(qbit_num)

            # Add the CNOT gate on control qbit and target qbit
            circuit.sx( target_qbit )

            # the unitary matrix from the result object
            SX_qiskit = get_unitary_from_qiskit_circuit( circuit )
            SX_qiskit = np.asarray(SX_qiskit)
        
            #the difference between the SQUANDER and the qiskit result        
            delta_matrix=SX_squander-SX_qiskit

            # compute norm of matrix
            error=np.linalg.norm(delta_matrix)

            #print("Get_matrix: The difference between the SQUANDER and the qiskit result is: " , np.around(error,2))
            assert( error < 1e-3 ) 


    def test_SX_apply_to(self):
        r"""
        This method is called by pytest. 
        Test to create an instance of U3 gate and compare with qiskit.
        """

        pi=np.pi

        for qbit_num in range(1,7):

            # target qbit
            target_qbit = qbit_num-1

            # creating an instance of the C++ class
            SX = qgd_SX( qbit_num, target_qbit )
        
            #create text matrix 
            test_matrix= np.identity( 2**qbit_num, dtype=complex )

	    #QISKIT      

            # Create a Quantum Circuit acting on the q register
            circuit = QuantumCircuit(qbit_num)

            # Add the CNOT gate on control qbit and target qbit
            circuit.sx( target_qbit )

            # the unitary matrix from the result object
            SX_qiskit = get_unitary_from_qiskit_circuit( circuit )
            SX_qiskit = np.asarray(SX_qiskit)

            # apply the gate on the input array/matrix 
            #SX_qiskit_apply_gate=np.matmul(SX_qiskit, test_matrix)

	    #SQUANDER

            SX_squander = test_matrix

            # apply the gate on the input array/matrix                
            SX.apply_to(SX_squander)       

            #the difference between the SQUANDER and the qiskit result        
            delta_matrix=SX_squander-SX_qiskit

            # compute norm of matrix
            error=np.linalg.norm(delta_matrix)

            #print("Apply_to: The difference between the SQUANDER and the qiskit result is: " , np.around(error,2))
            assert( error < 1e-3 ) 


