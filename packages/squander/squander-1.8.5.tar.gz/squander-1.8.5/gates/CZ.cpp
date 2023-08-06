/*
Created on Fri Jun 26 14:13:26 2020
Copyright (C) 2020 Peter Rakyta, Ph.D.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see http://www.gnu.org/licenses/.

@author: Peter Rakyta, Ph.D.
*/
/*! \file CZ.cpp
    \brief Class representing a CZ gate.
*/

#include "CZ.h"



using namespace std;


/**
@brief Nullary constructor of the class.
*/
CZ::CZ() {

        // number of qubits spanning the matrix of the gate
        qbit_num = -1;
        // the size of the matrix
        matrix_size = -1;
        // A string describing the type of the gate
        type = CZ_OPERATION;
        // The number of free parameters
        parameter_num = 0;

        // The index of the qubit on which the gate acts (target_qbit >= 0)
        target_qbit = -1;

        // The index of the qubit which acts as a control qubit (control_qbit >= 0) in controlled gates
        control_qbit = -1;


}


/**
@brief Constructor of the class.
@param qbit_num_in The number of qubits in the unitaries
@param target_qbit_in The identification number of the target qubit. (0 <= target_qbit <= qbit_num-1)
@param control_qbit_in The identification number of the control qubit. (0 <= target_qbit <= qbit_num-1)
*/
CZ::CZ(int qbit_num_in,  int target_qbit_in, int control_qbit_in) {


        // number of qubits spanning the matrix of the gate
        qbit_num = qbit_num_in;
        // the size of the matrix
        matrix_size = Power_of_2(qbit_num);
        // A string describing the type of the gate
        type = CZ_OPERATION;
        // The number of free parameters
        parameter_num = 0;

        if (target_qbit_in >= qbit_num) {
            std::stringstream sstream;
	    sstream << "The index of the target qubit is larger than the number of qubits" << std::endl;
	    print(sstream, 0);	    	            
            throw sstream.str();
        }
        // The index of the qubit on which the gate acts (target_qbit >= 0)
        target_qbit = target_qbit_in;


        if (control_qbit_in >= qbit_num) {
            std::stringstream sstream;
	    sstream << "The index of the control qubit is larger than the number of qubits" << std::endl;
	    print(sstream, 0);	    	
            throw sstream.str();
        }
        // The index of the qubit which acts as a control qubit (control_qbit >= 0) in controlled gates
        control_qbit = control_qbit_in;


}

/**
@brief Destructor of the class
*/
CZ::~CZ() {
}


/**
@brief Call to retrieve the gate matrix
@return Returns with the matrix of the gate
*/
Matrix
CZ::get_matrix() {

    Matrix CZ_matrix = create_identity(matrix_size);
    apply_to(CZ_matrix);

    return CZ_matrix;
}




/**
@brief Call to apply the gate on the input array/matrix CZ*input
@param input The input array on which the gate is applied
*/
void 
CZ::apply_to( Matrix& input ) {

    // the not gate of one qubit
    Matrix z_1qbit(2,2);
    z_1qbit[0].real = 1.0; z_1qbit[0].imag = 0.0; 
    z_1qbit[1].real = 0.0; z_1qbit[1].imag = 0.0;
    z_1qbit[2].real = 0.0; z_1qbit[2].imag = 0.0;
    z_1qbit[3].real = -1.0; z_1qbit[3].imag = 0.0;


    CNOT::apply_kernel_to(z_1qbit, input);

}



/**
@brief Call to apply the gate on the input array/matrix by input*CZ
@param input The input array on which the gate is applied
*/
void 
CZ::apply_from_right( Matrix& input ) {

    // the not gate of one qubit
    Matrix z_1qbit(2,2);
    z_1qbit[0].real = 1.0; z_1qbit[0].imag = 0.0; 
    z_1qbit[1].real = 0.0; z_1qbit[1].imag = 0.0;
    z_1qbit[2].real = 0.0; z_1qbit[2].imag = 0.0;
    z_1qbit[3].real = -1.0; z_1qbit[3].imag = 0.0;

    apply_kernel_from_right(z_1qbit, input);

}



/**
@brief Call to set the number of qubits spanning the matrix of the gate
@param qbit_num The number of qubits
*/
void CZ::set_qbit_num(int qbit_num) {
        // setting the number of qubits
        Gate::set_qbit_num(qbit_num);

}



/**
@brief Call to reorder the qubits in the matrix of the operation
@param qbit_list The reordered list of qubits spanning the matrix
*/
void CZ::reorder_qubits( vector<int> qbit_list) {

        Gate::reorder_qubits(qbit_list);

}



/**
@brief Call to create a clone of the present class
@return Return with a pointer pointing to the cloned object
*/
CZ* CZ::clone() {

    CZ* ret = new CZ( qbit_num, target_qbit, control_qbit );

    return ret;

}



