import sys
    
if __name__ == "__main__":

    if len(sys.argv) < 5:
        print("You have to introduce all the values of a Kendall queue")
        
    A = str(sys.argv[1])
    S = str(sys.argv[2])
    C = int(sys.argv[3])
    N = int(sys.argv[4])