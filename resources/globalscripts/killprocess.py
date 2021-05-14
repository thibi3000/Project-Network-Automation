import psutil


def kill_virtualbox_related_proceses():
    '''Process kill function'''    
    for proc in psutil.process_iter():

        if any(procstr in proc.name() for procstr in\
            ['VirtualBox', 'vbox', 'Vbox']):
            print(f'Killing {proc.name()}')
            proc.kill()




