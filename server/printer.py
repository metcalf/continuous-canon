import feedparser
import urllib2
import datetime
import signal
import Image

from subprocess import call

from stripeimage import stripe_image
from pipecontroller import PipeThread
from printercontroller import PrinterController

INPUT_PIPE_NAME =  "/dev/pcin"
OUTPUT_PIPE_NAME = "/dev/pcout"
CLEAR_ARGS = ["cancel", "-a"]
LP_ARGS = ["lp", "-o MediaType=Letter,matte", "-o position=top-right",  "striped.jpg"]
PATH_BASE = "images/%s-dd.%s"

# Check RSS feed
# Download image

RSS_PATH = "http://backend.deviantart.com/rss.xml?q=special%3Add&type=deviation&offset=0"
INCLUDE_SECTIONS = ("digitalart",
                    "photography",
                    "traditional",
                    "Contests",
                    "Fractal Art"
                    )

EXCLUDE_PATHS = (
                "animation",
                "digitalart/misc",
                "digitalart/paintings",
                "macabre",
                "horror",
                "cartoons",
                )

def parse_rss(url=RSS_PATH):
    feed = feedparser.parse(url)
    
    results = []
    for entry in feed.entries:
        term = entry.tags[0].term
        parts = term.split("/")
        if parts[0] in INCLUDE_SECTIONS:
            for path in EXCLUDE_PATHS:
                if path in term:
                    break
            else:
                results.append(
                    {
                        "title": entry.title,
                        "url": entry.media_content[0]["url"],
                        "tag": term,
                    }
                )
        
    return results

def get_dd():
    possibles = parse_rss()

    for possible in possibles:
        url = possible["url"]
        try:
            ext = url[url.rindex(".")+1:]
        except ValueError:
            continue
        
        
        path = PATH_BASE%(str(datetime.datetime.now().strftime("%Y%m%dT%H%M%S")), ext)
        try:
            data = urllib2.urlopen(url).read()
        except urllib2.URLError:
            continue
        
        f = open(path, "w+")
        try:
            f.write(data)
        finally:
            f.close()
         
        if "dpi" not in Image.open(path).info:
            continue

        return path
    
    return None    

def print_file(filename):
    stripe_image(filename)
    print "Striped"
    
    print "Calling %s"%" ".join(CLEAR_ARGS)
    call(CLEAR_ARGS)
    
    printer_controller = PrinterController()
    
    try:
        print "Waiting for arduino to reset"
        if not printer_controller.ready():
            printer_controller.wait_for_state_change(timeout=60.0)
        printer_controller.enable()
        
        print "Starting pipe thread"
        pipe_thread = PipeThread(INPUT_PIPE_NAME, OUTPUT_PIPE_NAME)           
        pipe_thread.start()
        
        print "Waiting for ready"
        printer_controller.wait_for_state("READY", timeout=60*10)
        
        print "Calling %s"%" ".join(LP_ARGS)
        call(LP_ARGS)
            
        try:
            print "Waiting for start"
            pipe_thread.started_event.wait(60.0)
            if not pipe_thread.started_event.is_set():
                raise RuntimeError("Could not start")
            print "Waiting for initial data send"
            pipe_thread.wait_feed.wait(60.0)
            if not pipe_thread.wait_feed.is_set():
                raise RuntimeError("Could not send")
            print "Waiting for print ready"
            printer_controller.wait_for_state("PRINT", timeout=60*5)
            pipe_thread.fed.set()
            print "Printing..."
            pipe_thread.wait_clear.wait(60.0*3)
            if not pipe_thread.wait_clear.is_set():
                raise RuntimeError("No clear")
            print "Waiting for clear..."
            printer_controller.wait_for_state("CLEAR", timeout=60)
            pipe_thread.cleared.set()
            print "Waiting for things to finish up"
            printer_controller.wait_for_state("STANDBY", timeout=60*5)
        finally:
            print "Closing pipes..."
            pipe_thread.close()
    finally:
        print "Closing ports..."
        try:
            printer_controller.disable()
        finally:
            printer_controller.close()
    
    print "Done!"
            
if __name__ == "__main__":
    path = get_dd()
    print_file(path)
