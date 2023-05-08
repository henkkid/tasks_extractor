import os
import sys
import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

class HotReloader(PatternMatchingEventHandler):
    def __init__(self, app_path, patterns=None):
        super().__init__(patterns=patterns)
        self.app_path = app_path
        self.proc = None
    
    def start(self):
        self.proc = subprocess.Popen(['python', self.app_path])
    
    def stop(self):
        if self.proc is not None:
            self.proc.kill()
    
    def on_any_event(self, event):
        print(f'Detected change in {event.src_path}, reloading app...')
        self.stop()
        self.start()

if __name__ == '__main__':
    app_path = 'C:\Projecten\Taskanalyses'
    patterns = ['*.py', '*.ui']  # Add file patterns to watch here
    reloader = HotReloader(app_path, patterns)
    reloader.start()
    
    observer = Observer()
    observer.schedule(reloader, os.path.dirname(app_path), recursive=True)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    
    observer.join()