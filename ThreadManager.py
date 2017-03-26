import threading
import time

class ThreadManager(threading.Thread):
    def __init__(self, server):
        super(ThreadManager, self).__init__()
        self.client_threads = []
        self.server = server
        self._stop = threading.Event()

    def run(self):
        while True:
            print "Thread Manager Starting"
            # Get Current Time
            current_time = time.time()
            # Loop through all tracked threads in system
            for thread in self.client_threads:
                # Check if the thread is inactive
                if int(current_time - thread.last_activity) > 1:
                    # Signal thread to stop
                    print thread.addr, " is being stopped"
                    thread.stop()
                    
            # Sleep to give priority to system over management
            print "Thread Manager Sleeping"
            time.sleep(5)

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()

    def add_thread(self, thread):
        self.client_threads.append(thread)
