from node import Node
from art import *
from saveNode import *
import time
import os
import pickle
import numpy as np

#
# Dijkstra's Algorithm, By Kieron Pang
# MAIN FILE
# Started 29/07/2025, completed 7/08/2025
# Some sections have been AI assisted
#

def main():
    # lists
    nodes = []

    # welcome message
    print(art)
    time.sleep(0.5)
    print(text)
    time.sleep(1)


    # menu loop
    loop = True
    while loop == True:
        # display options
        print("1: Add Node")
        print("2: Add Edge")
        print("3: Remove Node")
        print("4: Remove Edge")
        print("5: Display Nodes")
        print("6: Display Edges")
        print("7: View Matrixes")
        print("8: Import File (binary)")
        print("9: Export File (Save)")
        print("10: Calculate Dijkstra's Algorithm")
        print("0: Exit")

        # user input and loop
        try: # for bad input
            userInput = int(input("What would you like to do? (Enter valid number): "))

            # condition
            if userInput >= 0 <= 9: # if valid number
                # 0 - Exit -----------------------------
                if userInput == 0:
                    loop = False # loop ends
                    
                # 1 - Add Node -----------------------------
                elif userInput == 1:
                    name = input("Enter Name of Node: ")
                    dup = False

                    for node in nodes:
                        if node.getName() == name:
                            dup = True
                            print("!!! Duplicate name detected.")
                            break
                    
                    if dup == False:
                        nodes.append(Node(name))

                        # confirm
                        print(f"\n* Node {name} has been successfully added!\n")

                    time.sleep(1)

                # 2 - Add Edge -----------------------------
                elif userInput == 2:                
                    core = input("What node to add an edge from?: ")
                    core2 = input("What node to add an edge to?: ")
                    found1 = False

                    # find from
                    for node in nodes:
                        if node.getName() == core:
                            found1 = True
                            node1 = node
                            break

                    if found1 == False:
                        print(f"* {core} does not exist.")

                    found2 = False

                    # find to
                    for node in nodes:
                        if node.getName() == core2 and node.getName() != core: # cannot equal first node
                            found2 = True
                            node2 = node
                            break    

                    if found2 == False:
                        print(f"* {core2} does not exist.")  

                    # check if edge exists
                    exist = False # edge does not exist
                    for x in node1.getEdge():
                        if x.getName() == node2.getName():
                            exist = True
                    
                    
                    # if both pass, add the edge
                    if exist == False:
                        if found1 == True and found2 == True:
                            # get weight first
                            try:
                                weight = int(input("Edge weight: "))

                                # edge is added (both ends)
                                node1.addEdge(node2, weight)
                                node2.addEdge(node1, weight)

                                # confirmation
                                print(f'\n* Node "{node1.getName()}" <---> Node "{node2.getName()}" added with weight {weight}.')

                            except Exception as e:
                                print("!!! Invalid weight, could not add edge.")
                                print(e)
                    
                    else:
                        print("!!! Edge already exists.")

                    print()
                    time.sleep(1)

                # 3 - Remove Node -----------------------------
                elif userInput == 3:
                    toRemove = input("Node to remove: ")
                    found = False

                    # find node in nodes list
                    for node in nodes:
                        if node.getName() == toRemove:
                            found = True
                            target_node = node
                            break

                    if not found:
                        print(f"* Node '{toRemove}' not found.")

                    else:
                        # Remove the target node from all other nodes' edge and weight lists
                        for node in nodes:
                            if target_node in node.edge:
                                index = node.edge.index(target_node)
                                node.edge.pop(index)
                                node.weight.pop(index)

                        # Remove the node itself
                        nodes.remove(target_node)
                        print(f"* Node '{toRemove}' and all its edges have been removed.")

                    time.sleep(1)

                # 4 - Remove Edge -----------------------------
                elif userInput == 4:
                    target1 = input("First node (edge from): ")
                    target2 = input("Second node (edge to): ")

                    save1 = None
                    save2 = None

                    # Find both nodes
                    for node in nodes:
                        if node.getName() == target1:
                            save1 = node
                        elif node.getName() == target2:
                            save2 = node

                    if save1 is not None and save2 is not None:
                        exists1 = save2 in save1.edge
                        exists2 = save1 in save2.edge

                        if exists1 and exists2:
                            # Remove edge from save1 to save2
                            index1 = save1.edge.index(save2)
                            save1.edge.pop(index1)
                            save1.weight.pop(index1)

                            # Remove edge from save2 to save1
                            index2 = save2.edge.index(save1)
                            save2.edge.pop(index2)
                            save2.weight.pop(index2)

                            print(f"* Edge between '{target1}' and '{target2}' removed.\n")
                        else:
                            print(f"!!! No edge exists between '{target1}' and '{target2}'.\n")
                    else:
                        print("!!! One or both nodes do not exist.")

                    time.sleep(1)
                            
                # 5 - Display Nodes -----------------------------
                elif userInput == 5:                
                    if len(nodes) != 0: # check at least one node exists
                        for node in nodes:
                            print("\n* Node: " + node.getName(), end=' ')

                        print()
                            
                    else:
                        print("\n* No nodes exist!")

                    time.sleep(1)

                # 6 - Display Edges -----------------------------
                elif userInput == 6:                
                    if len(nodes) != 0: # check at least one node exists
                        for node in nodes:
                            print("\n* Node: " + node.getName(), end=': ')
                            for x in node.getEdge():
                                print(x.getName(), end = ' ')

                        print()
                            
                    else:
                        print("\n* No edges exist!")

                    time.sleep(1)

                # 7 - View Matrixes ----------------------------- 
                elif userInput == 7: 
                    
                    # setup matrix   
                    size = len(nodes) 
                    matrix = np.zeros((size, size))

                    # build matrix
                    for node_idx in range(len(nodes)):
                        node = nodes[node_idx]
                        edges = node.getEdge()

                        for edge_idx in range(len(edges)):
                            connected_node = edges[edge_idx]
                            if connected_node in nodes:
                                pos = nodes.index(connected_node)
                                weight = node.getWeight(edge_idx)
                                matrix[node_idx][pos] = int(weight)             

                    # print header
                    print("\nAdjacency Matrix:\n")
                    print("      ", end='')  # space for row labels
                    for node in nodes:
                        print(f"{node.getName():>5}", end='')  # right-align column headers
                    print()

                    # print rows
                    for node_idx in range(len(nodes)):
                        print(f"{nodes[node_idx].getName():<6}", end='')  # row label, left-aligned
                        for val in matrix[node_idx]:
                            if val == 0:
                                print(f"{'--':>5}", end='')  # no connection
                            else:
                                print(f"{int(val):>5}", end='')  # connection weight
                        print()

                    time.sleep(1)
                
                # 8 - Import File (binary) -----------------------------
                elif userInput == 8:                
                    # check folder
                    if os.path.isdir("saves"):
                        name = input("Name of file to open: ")

                        # attempt to import
                        try:
                            with open("saves/" + name + ".pkl", "rb") as f:
                                nodes = pickle.load(f).getNodeList()
                        except:
                            print("!!! File does not exist!")
                        time.sleep(1)
                    else:
                        print("\n!!! No saves exist.\n")

                # 9 - Export File -----------------------------
                elif userInput == 9: 
                    # create the folder
                    if os.path.isdir("saves"):
                        pass               
                    else:
                        os.mkdir("saves")
                        print("* Folder 'saves' created succesfully!")

                        time.sleep(1)

                    # create object save file (based on a name and nodeslist)
                    name = input("Name of file to save as: ")
                    save = saveNode(name, nodes)
                    # print(save)

                    # check if file already exists
                    if os.path.exists ("saves/" + name + ".pkl"):
                        print("!!! File already exists (file not created).")

                    else:
                    # export
                        with open("saves/" + name + ".pkl", "wb") as f:
                            pickle.dump(save, f)
                        
                        # confirmation
                        print(f'\n"{name}" has been saved successfully!\n')
                    
                    time.sleep(1)

                # 10 - Calculate Dijkstra's Algorithm
                elif userInput == 10:
                    start_name = input("Start node: ")
                    end_name = input("End node: ")

                    start_node = None
                    end_node = None

                    # Find start and end nodes
                    for node in nodes:
                        if node.getName() == start_name:
                            start_node = node
                        if node.getName() == end_name:
                            end_node = node

                    if start_node is None:
                        print("Start node does not exist.\n")
                    elif end_node is None:
                        print("End node does not exist.\n")
                    else:
                        # Initialize Dijkstra data
                        unvisited = {node: float('inf') for node in nodes}
                        visited = {}
                        previous_nodes = {}

                        unvisited[start_node] = 0

                        while unvisited:
                            current_node = min(unvisited, key=unvisited.get)
                            current_distance = unvisited[current_node]

                            # Move current node to visited BEFORE early exit
                            visited[current_node] = current_distance
                            unvisited.pop(current_node)

                            if current_node == end_node:
                                break

                            for idx, neighbor in enumerate(current_node.edge):
                                if neighbor in visited:
                                    continue

                                weight = current_node.weight[idx]
                                new_distance = current_distance + weight

                                if new_distance < unvisited[neighbor]:
                                    unvisited[neighbor] = new_distance
                                    previous_nodes[neighbor] = current_node

                        # Reconstruct path
                        if end_node not in visited:
                            print("No path exists between the nodes.\n")
                        else:
                            path = []
                            current = end_node
                            while current != start_node:
                                path.insert(0, current.getName())
                                current = previous_nodes[current]
                            path.insert(0, start_node.getName())

                            print(f"Shortest path: {' -> '.join(path)}")
                            print(f"Total weight: {visited[end_node]}\n")

                    time.sleep(1)

                # gap for aesthetics
                print()

            # reset loop
            else:
                print("Please enter a number between 0 and 9")

        except:
            print("!!! Bad Input")
            #print("Error: " + e + "\n")

if __name__ == "__main__":
    main()