import sys
import heapq
import engine

def generator(env):
    # for i in range(2):
    value = yield env.timeout(1, value=42)
    print(f"now={env.now}, value={value}")
    
if __name__ == "__main__":

    if len(sys.argv) < 5:
        print("You have to introduce all the values of a Kendall queue")
        exit
        
    A = str(sys.argv[1])
    S = str(sys.argv[2])
    C = int(sys.argv[3])
    N = int(sys.argv[4])