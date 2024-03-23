# /***Data structure
# Write a pseudo code implementing Queue DS using Arrays.
# Give time complexity for Enqueue and Dequeue operations.
# Given that each element has a priority and we need to implement a Max Priority queue, outline the changes you’ll make to the above implementation and give expected time complexity.
# ***/

#initializing queue with fixed capacity

MAX_SIZE = 10
queue = [None] * MAX_SIZE
front = -1 
rear = -1

######### NORMAL QUEUE USING ARRAYS ###########
# Add an element to the queue (enqueue)
def enqueue(data):
    global rear
    if (rear == MAX_SIZE - 1):
        print("Queue is full. Cannot insert element.")
    else:
        if (front == -1):
            front = 0
        rear += 1
        queue[rear] = data

# Remove an element from the queue (dequeue)
def dequeue():
    global front
    if (front == -1):
        print("Queue is empty. Cannot remove element.")
    else:
        data = queue[front]
        front += 1
        if (front > rear):
            front = rear = -1
        return data


# time complexity for enqueue operation is O(1) because it simply involves incrementing the rear pointer and adding an element to the array 
# time complexity for dequeue operation is also O(1) because it involves incrementing the front pointer and returning the element at that position.





########## PRIORITY QUEUE ###########
#add an element to the queue (enqueue)
def enqueue(data , priority):
    global rear 
if(rear == MAX_SIZE -1 ):
    print("Queue is full , can't insert element")
else : 
    if(front == -1):
        front = 0
        rear +=1
        #insert the element in the correct position based on priority
        for i in range (rear , front -1 , -1):
            if queue[i-1][1] < priority:
                queue[i] = queue[i-1]
            else:
                break
            queue[i] = (data , priority)

#Remove an element from the queue (dequeue)
            def dequeue():
                global front 
                if (front == -1):
                    print("Queue is empty , can't remove eleemnt")
                else:
                    data , priority = queue[front]
                    front +=1
                    if (front > rear):
                        front = rear = -1
                        return data
# time complexity for enqueue operation is O(n) because we need to sort the queue based on priority values.
# time complexity for dequeue operation remains O(1)



