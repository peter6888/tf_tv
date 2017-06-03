import subprocess, threading

class Command(object):
    def __init__(self, cmd):
        self.cmd = cmd
        self.process = None

    def run(self, timeout, waitTillFinish=True):
        def target():
            #print('Thread started')
            self.process = subprocess.Popen(self.cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = self.process.communicate()
            self.ret = self.ret if len(out) == 0 else out.decode('ascii')
        self.ret = ""
        thread = threading.Thread(target=target)
        thread.start()

        if not waitTillFinish:
            print("subprocess started, will finish by itself")
            return

        thread.join(timeout)
        if thread.is_alive():
            #print('Terminating process')
            self.process.terminate()
            thread.join()
        #print(self.process.returncode)
        print(self.ret)
        return self.ret

    def isRuning(self):
        processes = [line.split() for line in subprocess.check_output("tasklist").splitlines()]
        [processes.pop(e) for e in [0,1,2]]
        for task in processes:
            if task[0]==str.encode(self.cmd):
                return True
        return False

    def start(self):
        subprocess.Popen(self.cmd)
#c = WindowsCommand("dir")
#c.run(timeout=3)