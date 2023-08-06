from argparse import ArgumentParser, RawTextHelpFormatter
import codecs
from qiskit import QuantumCircuit

from user_configs import UserConfigs
from qiskit_back.c12sim_provider import C12SimProvider


def add_arguments():
    arg_parser.add_argument("--config", help="Use config file to get all data")

    arg_parser.add_argument(
        "--verbose",
        help="Added more information during the app execution (level 1)",
        const=True,
        nargs="?",
        default=None,
    )
    arg_parser.add_argument("--token", help="Token for user authentication to the remote server")

    qasm_group = arg_parser.add_mutually_exclusive_group()
    qasm_group.add_argument("--qasmcircuit", help="String of the qasm circuit to simulate.")
    qasm_group.add_argument("--qasmfile", help="Path to file containing qasm circuit to simulate.")


if __name__ == "__main__":
    arg_parser = ArgumentParser(formatter_class=RawTextHelpFormatter)
    add_arguments()
    args = arg_parser.parse_args()

    if args.config is None and args.token is None:
        raise ValueError("Input parameters have to be given via command line or configs.json file")

    user_configs: UserConfigs = None

    if args.config:
        user_configs = UserConfigs()
        # Overwrite from the command line
        if args.verbose is not None:
            user_configs.set_verbose(args.verbose)
        if args.token is not None:
            user_configs.set_token(args.token)

    else:
        user_configs = UserConfigs({"verbose": args.verbose, "token": args.token})

    provider = C12SimProvider(user_config=user_configs)
    backend = provider.get_backend("c12sim")

    circuit: QuantumCircuit = None

    if user_configs.get_verbose():
        print("Converting qasm string to qiskit quantum circuit...")

    if args.qasmcircuit is not None:
        qasm = codecs.decode(args.qasmcircuit, "unicode_escape")
        circuit = QuantumCircuit.from_qasm_str(qasm)
    elif args.qasmfile is not None:
        circuit = QuantumCircuit.from_qasm_file(args.qasmfile)
    else:
        raise ValueError("There is no qasm file or string given")

    if circuit is None:
        raise ValueError("There is a problem with qasm string or file (missing or wrong format")

    job = backend.run(circuit, shots=1024)
    print(f"Job Id: {job.job_id()}")
    try:
        job_result = job.result()
        print("Reuslt: ")
        print(job_result.get_counts())
    except Exception as e:
        print(e)
        print(f"Error occurred during the execution of a job {job.status()}")
