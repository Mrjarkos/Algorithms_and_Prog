import threading
import time

def thread_function(id):
    print(f"Thread {i}: starting")
    time.sleep(2)
    print(f"Thread {i}: finishing")

if __name__ == "__main__":
    
    n = 2
    print("===Secuencial===")
    init_time = time.time()
    for i in range(n):
        thread_function(i)
        
    end_time = time.time()-init_time
    print(f"Total time = {end_time}")
    
    print("===Paralelo===")
    threads = []
    ## Create threads
    init_time = time.time()
    for i in range(n):
        thread = threading.Thread(target=thread_function, args=(i,))
        threads.append(thread)
        thread.start()
    
    for thread in threads:    
        thread.join()
    end_time = time.time()-init_time
    print(f"Total time = {end_time}")