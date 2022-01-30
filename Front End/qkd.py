from getpass import getpass
from qiskit.circuit import QuantumRegister, ClassicalRegister, QuantumCircuit
from qiskit.tools.compiler import execute
from quantuminspire.qiskit import QI
import numpy as np

def get_authentication():
    """Gets the authentication for connecting to the
       Quantum Inspire API.
    """
    print(‘Enter email:’)
    email = input()
    print(‘Enter password’)
    password =  getpass()
    return email, password 

if __name__ == '__main__':
    if 'authentication' not in vars().keys():
        authentication = get_authentication()
    QI.set_authentication_details(*authentication)
    qi_backend = QI.get_backend('QX single-node simulator')
    
    n_bits = 20
    
    user1bits = np.random.randint(2,size = n_bits)
    user1basis = np.random.choice(["X","Z"],size = n_bits)
    
    user2bits = np.random.randint(2,size = n_bits)
    user2basis = np.random.choice(["X","Z"],size = n_bits)
    
    def encode(bits,basis) :
    message = []
    assert len(bits) == len(basis)
    
    for i in range(len(bits)) :
        qc = QuantumCircuit(1,1)
        if basis[i] == "Z" :
            if bits[i] == 0:
                pass
            else :
                qc.x(0)
        else :
            if bits[i] == 0:
                qc.h(0)
            else :
                qc.x(0)
                qc.h(0)
        message.append(qc)
        
    return message

    message = encode(user1bits,user1basis)
    
    def measure(message, basis):
        qi_backend = QI.get_backend('QX single-node simulator')
        measurements = []
        for q in range(len(basis)):
            if basis[q] == "Z": 
                message[q].measure(0,0)
            else :
                message[q].h(0)
                message[q].measure(0,0)
            circuit = message[q]
            qi_job = execute(circuit, backend=qi_backend, shots=256)
            qi_result = qi_job.result()        
            measured_bit = int(qi_result.get_counts(circuit)[0])
            measurements.append(measured_bit)
        
        return measurements

    measurements = measure(message,user2basis)
    
    def common_bits(basis1,basis2,measured) :
    common = []
    for i in range(len(basis1)) :
        if basis1[i] == basis2[i] :
            common.append(measured[i])
    return common


    user1key = common_bits(user1basis,user2basis,user1bits)
    user2key = common_bits(user1basis,user2basis,measurements)
    
    assert user1key == user2key
    
    print("key = ",user1key)
    