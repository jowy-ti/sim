
class Event:
    def __init__(self, id, curBlk, nxtBlk, moveTime, priority_Level):
        self.id = int(id)
        self.curBlk = int(curBlk)
        self.nxtBlk = int(nxtBlk)
        self.moveTime = moveTime
        self.priority_Level = int(priority_Level)


    # Crucial for heapq / sorting
    def __lt__(self, other):
        if self.moveTime == other.moveTime:
            # Secondary sort by priority level if times are equal
            return self.priority_Level < other.priority_Level
        return self.moveTime < other.moveTime
    
    def update_blocks(self, new_current, new_next):
        self.curBlk = new_current
        self.nxtBlk = new_next

    def __repr__(self):
        return f"Event(id={self.id}, time={self.moveTime:.2f}, path={self.curBlk}->{self.nxtBlk})"