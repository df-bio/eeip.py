import argparse
import time

from eeip import ConnectionType, EEIPClient, RealTimeFormat

DEFAULT_SMC_ASSEMBLY_DATA_LEN = 36


def configure_client(client: EEIPClient, o_t_length: int, t_o_length: int) -> None:
    client.o_t_instance_id = 150
    client.o_t_length = o_t_length
    client.o_t_requested_packet_rate = 20_000
    client.o_t_realtime_format = RealTimeFormat.HEADER32BIT
    client.o_t_owner_redundant = False
    client.o_t_variable_length = False
    client.o_t_connection_type = ConnectionType.POINT_TO_POINT

    client.t_o_instance_id = 100
    client.t_o_length = t_o_length
    client.t_o_requested_packet_rate = 20_000
    client.t_o_realtime_format = RealTimeFormat.MODELESS
    client.t_o_owner_redundant = False
    client.t_o_variable_length = False
    client.t_o_connection_type = ConnectionType.POINT_TO_POINT

    client.configuration_assembly_instance_id = 105


def run_cycle(ip: str, hold_s: float, o_t_length: int, t_o_length: int) -> None:
    client = EEIPClient()
    client.register_session(ip)
    configure_client(client, o_t_length=o_t_length, t_o_length=t_o_length)

    client.forward_open()
    time.sleep(max(hold_s, 0.0))
    client.forward_close()
    client.unregister_session()


def main() -> None:
    parser = argparse.ArgumentParser(description="Open/close an SMC EEIP implicit connection")
    parser.add_argument("--ip", default="192.168.1.19", help="Target device IP")
    parser.add_argument("--cycles", type=int, default=5, help="Number of open/close cycles")
    parser.add_argument("--hold-s", type=float, default=0.5, help="Seconds to hold connection open")
    parser.add_argument(
        "--o-t-length",
        type=int,
        default=DEFAULT_SMC_ASSEMBLY_DATA_LEN,
        help="Originator->Target payload length bytes",
    )
    parser.add_argument(
        "--t-o-length",
        type=int,
        default=DEFAULT_SMC_ASSEMBLY_DATA_LEN,
        help="Target->Originator payload length bytes",
    )
    args = parser.parse_args()

    for index in range(args.cycles):
        print(f"[cycle {index + 1}/{args.cycles}] connecting to {args.ip}")
        started_at = time.monotonic()
        run_cycle(args.ip, args.hold_s, args.o_t_length, args.t_o_length)
        elapsed = time.monotonic() - started_at
        print(f"[cycle {index + 1}/{args.cycles}] success in {elapsed:.3f}s")


if __name__ == "__main__":
    main()
