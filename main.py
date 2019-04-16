import networkx as nx
import matplotlib.pyplot as plt
import os
import numpy as np

from community import community_louvain

colors = ['y','r','g','b','yellow','navy','chocolate','tan','midnightblue','tomato','olive','m','pink','c','lightblue',
          'burlywood','peru','brown','blueviolet','crimson','black'] * 3

# ------------------------------------------------------------------------------------------------------- READ RADATOOLS
# Read file Radatools
# Directory: cd Desktop/MAI/Sem2/CN/Lab/Lab3/radatools-5.0-mac/Communities_Detection
# Execute: sh Communities_Detection_Victor.sh
path = './Radatools'
files = []
for r, d, f in os.walk(path):
    for file in f:
        if '.log' not in file:
            fil = open('./Radatools/'+file, 'r')
            entra = False
            information = []
            for line in fil:
                if entra:
                    util_inf = line.split()
                    information = information + [util_inf[1:],]
                if line == '\n':
                    entra = True
            # ------------------------------------------------------------------------------------ READ GROUND TRUTH
            if file != 'airports_UW.txt':
                if file == 'rb125.txt':
                    graph = file[:-4]+'-1'+ '.clu'
                elif file == 'zachary_unwh.txt' or file == 'dolphins.txt':
                    graph = file[:-4] + '-real' + '.clu'
                elif file == 'football.txt':
                    graph = file[:-4] + '-conferences' + '.clu'
                else:
                    graph = file[:-4] + '.clu'
                fil = open('./A3-networks/' + graph, 'r')
                ground_truth_partition = []
                entra = False
                for line in fil:
                    if entra:
                        ground_truth_partition.append(int(line))
                    entra = True

            # ------------------------------------------------------------------------------------ MAIN CODE
            graph = file[:-3]+'net'
            G = nx.Graph(nx.read_pajek('A3-networks/'+graph))

            # ------------------------------------------------------------------------------------ INI READ COORDINATES
            dictionary = G._node
            if len(list(dictionary[list(dictionary.keys())[0]].keys()))>1:
                position = dict()
                for item in list(G.nodes):
                    position[item] = np.array([dictionary[item]['x'], dictionary[item]['y']])
                print(graph)
            else:
                print('*******************'+graph)
                position = nx.kamada_kawai_layout(G)
            # ------------------------------------------------------------------------------------ FIN READ COORDINATES


            # Community
            partitionC = community_louvain.best_partition(G)
            partitionC = [value for key, value in partitionC.items()]
            node_colorC = [colors[value] for value in partitionC]

            if file != 'airports_UW':
                # Ground Truth
                node_colorT = [colors[value] for value in ground_truth_partition]
                node_size = 50
            else:
                node_size = 0.1

            # Radatools
            partitionR = [-1]*len(G.node)
            for it in range(len(information)):
                for it2 in range(len(information[it])):
                    partitionR[int(information[it][it2])-1] = it
            node_colorR = [colors[value] for value in partitionR]

            # Matlab
            # partitionM = community_louvain.best_partition(G)
            # node_colorM = [value for key, value in partitionM.items()]

            # Drawing
            # C O M M U N I T Y
            fig = plt.figure(figsize=(12, 6))
            plt.subplot(1,4,1)
            nx.draw_networkx(G, pos=position, node_color=node_colorC, node_size=node_size,
                             with_labels=False, edge_color='gray')
            limits = plt.axis('off')
            plt.title('Community'+'\n# Communities = '+str(len(set(partitionC))))

            # G R O U N D   T R U T H
            plt.subplot(1, 4, 4)
            if file != 'airports_UW.txt':
                nx.draw_networkx(G, pos=position, node_color=node_colorT, node_size=node_size,
                             with_labels=False, edge_color='gray')
                plt.title('Ground Truth'+'\n# Communities = '+str(len(set(ground_truth_partition))))
            else:
                plt.title('Ground Truth')
            limits = plt.axis('off')

            # R A D A T O O L S
            mmm = len(set(node_colorR))
            plt.subplot(1,4,2)
            nx.draw_networkx(G, pos=position, node_color=node_colorR, node_size=node_size,
                             with_labels=False, edge_color='gray')
            limits = plt.axis('off')
            plt.title('Radatools'+'\n# Communities = '+str(len(set(partitionR))))

            # M A T L A B
            plt.subplot(1,4,3)
            # nx.draw_networkx(G, pos = position, node_color = node_colorM, node_size = node_size,
            #                 with_labels = False, edge_color = 'gray')
            limits = plt.axis('off')
            #plt.xlabel('# Communities = '+str(len(set(partitionM))))
            plt.title('Matlab')

            plt.suptitle('Network: '+graph+'\n\n ',fontsize=16)
            fig.savefig('./Images/'+graph+'.png')