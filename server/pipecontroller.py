import os
import fcntl
import stat
import threading

class PipeController(object):

    def __init__(self, in_name, out_name):
        self.in_name = in_name
        self.out_name = out_name
        self.reader_fd = None
        self.writer_fd = None
         
    def open_pipes(self):
        for (name, mode) in ((self.in_name, 0722), (self.out_name, 0744)):
            try:
                os.remove(name)
            except OSError as e:
                if e.errno != 2:
                    raise
            os.mkfifo(name)
            os.chmod(name, mode)

        self.reader_fd = os.open(self.in_name, os.O_NONBLOCK)
        self.writer_fd = os.open(self.out_name, os.O_WRONLY)
        print "pipes open"
    
    def close_pipes(self):
        if self.reader_fd:
            os.close(self.reader_fd)
            self.reader_fd = None
        if self.writer_fd:
            os.close(self.writer_fd)
            self.writer_fd = None
    
    def read(self):
        try:
            return os.read(self.reader_fd, 8192)
        except OSError as e:
            if e.errno != 11: # Resource temporarily unavailable
                return
                
    def write(self, data):
        os.write(self.writer_fd, data)

class PipeThread(threading.Thread):
    
    def __init__(self, in_name, out_name):
        self.pipe_controller = PipeController(in_name, out_name)

        self.fed = threading.Event()
        self.cleared = threading.Event()
        
        self.started_event = threading.Event()
        self.wait_feed = threading.Event()
        self.wait_clear = threading.Event()
        
        self.success = False
        self._kill = False
        
        super(PipeThread, self).__init__()
    
    def run(self):
        self.fed.clear()
        self.cleared.clear()
        self.started_event.clear()
        
        self.pipe_controller.open_pipes()
        
        try:
            self.started_event.set()
            
            iteration = 0
            done = False
            finish = False
            while(not done and not self._kill):
                data = self.pipe_controller.read()
                if data and len(data) > 0:
                    print "read %s"%data
                    if iteration == 3:
                        self.wait_feed.set()
                        self.fed.wait()
                        if self._kill:
                            return
                    elif len(data) == 64:
                        self.wait_clear.set()
                        self.cleared.wait()
                        if self._kill:
                            return
                        done = True
                    elif len(data) < 8192:
                        data = data[:-64]

                    print "writing"
                    self.pipe_controller.write(data)
                    print "written"
                    data = ""
                    iteration += 1
            
            if not self._kill:
                self.success = True
        finally:
            self.pipe_controller.close_pipes()
        
    def close(self):
        self._kill = True
        self.fed.set()
        self.cleared.set()
        self.pipe_controller.close_pipes()
