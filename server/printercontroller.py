import serial
import time
import threading

STATES = ( "OFF",
           "STARTSTOP",
           "STANDBY",
           "READY",
           "FED",
           "PRINT",
           "CLEAR",
           "ERROR"
          )

class PrinterError(Exception):
    pass
          
class PrinterTimeout(Exception):
    pass
          
class StateThread(threading.Thread):
    def __init__(self, port):
        self.port = port
        self._kill = False
        self.state = None
        self.change_events = []
        self.change_condition = threading.Condition()
        
        super(StateThread, self).__init__()
        
    def kill(self):
        self._kill = True
    
    def register_change_event(self, event):
        self.change_events.append(event)
    
    def run(self):
        while(not self._kill):
            try:
                value = self.port.read()
                try:
                    value = int(value)
                except ValueError:
                    pass
                else:
                    new_state = STATES[int(value)]
                    if new_state != self.state:
                        self.state = new_state
                        print self.state
                        for evt in self.change_events:
                            evt.set()
            except serial.SerialTimeoutException:
                pass
    
class PrinterController(object):
    def __init__(self):
        for i in range(0, 100):
            try:
                self.port = serial.Serial("/dev/ttyUSB%d"%i, 9600, writeTimeout=10, timeout=1)
                break
            except serial.SerialException:
                pass
        else:
            raise Exception("Couldn't find arduino")
        
        self.port.setDTR(False)
        time.sleep(0.022)
        self.port.setDTR(True)
        time.sleep(1)
        
        self.state_thread = StateThread(self.port)
        self.change_event = threading.Event()
        self.state_thread.register_change_event(self.change_event)
        self.state_thread.start()
            
    def enable(self):
        self.port.write("1")
    
    def disable(self):
        self.port.write("0")
    
    def close(self):
        self.port.close()
        self.state_thread.kill()
        self.state_thread.join()
    
    def ready(self):
        return self.state_thread.state != None
    
    def wait_for_state(self, state, raise_error=True, timeout=None):
        if state not in STATES:
            raise ValueError("Invalid state")
    
        start = time.time()
        while(self.state_thread.state != state):
            if self.state_thread.state == "ERROR" and raise_error:
                raise PrinterError()
            elif(timeout and time.time()-start > timeout):
                raise PrinterTimeout()
            else:
                change_timeout = min(abs(timeout-(time.time()-start)), 1)
                self.wait_for_state_change(timeout=change_timeout)
    
    def wait_for_state_change(self, timeout=None):
        self.change_event.clear()
        self.change_event.wait(timeout=timeout)