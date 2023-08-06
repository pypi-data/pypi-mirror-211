from py_cli_interaction import must_parse_cli_string
import grpc
import time
import tqdm

import arizon_usb_apiserver.grpc.force_packet_pb2 as force_packet_pb2
import arizon_usb_apiserver.grpc.force_packet_pb2_grpc as force_packet_pb2_grpc


def test_grpc():
    endpoint = must_parse_cli_string("endpoint", "localhost:8080")
    
    channel = grpc.insecure_channel(endpoint)
    stub = force_packet_pb2_grpc.ForcePacketServiceStub(channel)

    response = stub.SetFIFOStatus(force_packet_pb2.ForceSetFIFOStatusRequest(
        status=True))
    print("SetStatus client received: " + str(response))

    response = stub.GetPacketStream(
        force_packet_pb2.ForcePacketRequest(timestamp=time.time_ns()))
    print("GetPacketStream client received: " + str(response))

    try:
        with tqdm.tqdm() as pbar:
            while True:
                data = next(response)
                if data.valid == False:
                    time.sleep(0.0005)
                    continue
                pbar.set_description(str(data.f) + ' - ' + str(data.index))
                pbar.update(1)
                # print)
    except KeyboardInterrupt as e:
        response.cancel()

    response = stub.SetFIFOStatus(force_packet_pb2.ForceSetFIFOStatusRequest(
        status=False))
    print("SetStatus client received: " + str(response))


if __name__ == '__main__':
    test_grpc()
