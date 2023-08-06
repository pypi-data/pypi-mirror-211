from qiskit.circuit.random import random_circuit

TOKEN = "db0ccae9b0dfccba90a534ad40802d40aa57d395bdac4e3a0bfcaaa7db0a3c2f"
from c12simulator.qiskit_back.c12sim_provider import C12SimProvider

from c12simulator. import user_configs


provider = C12SimProvider(auth_token=TOKEN)
backend = provider.get_backend("c12sim")
circuit = random_circuit(5, 5, measure=False)
from qiskit.compiler import transpile

circuit = transpile(circuit, basis_gates=["id", "rx", "ry", "rz", "cx"])
job = backend.run(circuit, shots=1024)
print(job.status())
try:
    print(job.result(timeout=180))
except:
    print(job.status())
