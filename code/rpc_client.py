from __future__ import print_function
import logging
import grpc
import sgx_pb2
import sgx_pb2_grpc

def run():
    with grpc.insecure_channel('166.111.131.17:7666') as channel:
        stub = sgx_pb2_grpc.SecureFuncStub(channel)
        response = stub.SGXFunc(sgx_pb2.FuncId(value=1))
    print("Secure function executed: " + str(response.value))
if __name__ == '__main__':
    logging.basicConfig()
    run()
