from pathlib import Path
import os

IN_FIFO_NAME = 'infifo'
OUT_FIFO_NAME = 'outfifo'

def main(): 
    failure, created = setupFIFOs({ IN_FIFO_NAME, OUT_FIFO_NAME })
    if failure is not None:
        print("FATAL: Failed to create FIFO '{}'".format(failure))
        return 1
    print('set up FIFOs')



#creates the for each element in the provided list. 
#returns None as the first element on success with the second element
#being the list of tuples it created. 
#on failure returns the path to the fifo it could not create as the first element
#and None as the second.
def setupFIFOs(fifoPaths):
    to_create = []
    for path in fifoPaths:
        if not Path(path).is_fifo(): to_create.append(path)

    failed_to_create= None; 
    fifos_created = []
    for path in to_create:
        try:
            os.mkfifo(path)
            fifos_created.append(path)
        except Exception as e:
            print('Could not create FIFO ' + path)
            print(e)
            failed_to_create = path 
            break

    if failed_to_create is not None:
        for path in fifos_created:
            os.unlink(path)

    return failed_to_create, fifos_created


main()
