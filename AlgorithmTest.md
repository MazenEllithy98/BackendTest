<!-- Algorithms
Give a pseudo code, time complexity, space complexity for each


Given the head of a singly linked list, return the middle node of the linked list. If there are two middle nodes, return the second middle node.
The number of nodes in the list is in the range [1, 100].

Examples:


Input: head = [1,2,3,4,5]
Output: [3,4,5]
Explanation: The middle node of the list is node 3.

Input: head = [1,2,3,4,5,6]
Output: [4,5,6]
Explanation: Since the list has two middle nodes with values 3 and 4, we return the second one. -->

<!-- Pseudo Code:  -->

function find_second_middle_node(head):
    <!-- Initialize two pointers at the head of the list -->
    slow = head
    fast = head

    <!-- Move the fast pointer two nodes at a time -->
    while fast != Null and fast.next != Null:
        slow = slow.next
        fast = fast.next.next

     <!-- Return the next node of the slow pointer, which is the second middle node -->
    return slow.next


<!-- Time Complexity: -->
the time complexity to find the middle node f a singly linked list using the above pseudocode is O(n), where n is the number of nodes in the list.

<!-- Space Complexity: -->
The space complexity of this algorithm is O(1) because we only use a constant amount of space to store the two pointers and their next nodes.