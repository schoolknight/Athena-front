import sys,os
import subprocess
import time
from time import sleep
from concurrent import futures
import logging
import grpc
import sgx_pb2
import sgx_pb2_grpc

server_dir = os.path.dirname(__file__)
func_pool = os.path.join(server_dir, "app")

def sgx_func(id):
    start = time.time()
    #result = subprocess.run(func_pool, str(id)), capture_output=True, text = True)
    #print(result.stdout)
    sleep(3)
    exec_sec = int(time.time() - start)
    print(exec_sec)
    return 0

class SecureFuncService(sgx_pb2_grpc.SecureFuncServicer):

    def SGXFunc(self, request, context):
        response = sgx_pb2.FuncResult()
        response.value = sgx_func(request.value)
        return response

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    sgx_pb2_grpc.add_SecureFuncServicer_to_server(SecureFuncService(), server)
    server.add_insecure_port('localhost:7666')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    logging.basicConfig()
    serve()
