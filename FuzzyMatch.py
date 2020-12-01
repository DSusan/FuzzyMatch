from FuzzyMatchFuncs import *

def main():
    startTime = time.time()
    logging.basicConfig(format='%(asctime)s %(levelname)s {%(module)s} [%(funcName)s] %(message)s',
    level=logging.INFO, filename='Records.log', datefmt='%Y-%m-%d %H:%M:%S')
    
    if not (os.path.exists(mlDir)):
        logging.exception("Root directory not found")
        return
    for item in os.listdir(mlDir):
        try:
            d = os.path.join(mlDir, item)
            if os.path.isdir(d):
                #change
                childrenCategory.append(d+"\\Transform")
                #childrenCategory.append(d)
        except:
            logging.exception("File or Directory not found")
            print("File or Directory not found")
            return

    for chItem in childrenCategory:
        try:
            processFiles(Path(chItem))
        except OSError:
            logging.exception("File or Directory not found")
            print("File or Directory not found")
            return

    endTime = time.time()
    timerFunc(startTime, endTime)
    
if __name__ == '__main__':
    main()
    