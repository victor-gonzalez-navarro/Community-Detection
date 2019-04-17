import networkx as nx
import matplotlib.pyplot as plt
import os
import numpy as np
import itertools
from igraph import *

from community import community_louvain

def jaccar_index(partition, ground_truth_partition):
    r1 = set(partition)
    r2 = set(ground_truth_partition)
    intersection_len = len(r1.intersection(r2))
    union_len = len(r1) + len(r2) - intersection_len
    jaccard = intersection_len / union_len
    return jaccard

colors = ['y','r','g','b','yellow','navy','chocolate','tan','midnightblue','tomato','olive','m','pink','c','lightblue',
          'burlywood','peru','brown','blueviolet','crimson','black'] * 15

# ------------------------------------------------------------------------------------------------------- READ RADATOOLS
# Read file Radatools
# Directory: cd Desktop/MAI/Sem2/CN/Lab/Lab3/radatools-5.0-mac/Communities_Detection
# Execute: sh Communities_Detection_Victor.sh
path = './Radatools'
files = []
for r, d, f in os.walk(path):
    for file in f:
        if '.log' not in file:
            # ------------------------------------------------------------------------------------ READ LABELS RADATOOLS
            fil = open('./Radatools/'+file, 'r')
            entra = False
            information = []
            for line in fil:
                if entra:
                    util_inf = line.split()
                    information = information + [util_inf[1:],]
                if line == '\n':
                    entra = True
            # --------------------------------------------------------------------------------------- READ LABELS MATLAB
            filM = open('./Matlab/' + file[:-4]+'.net', 'r')
            entraM = False
            informationM = []
            for lineM in filM:
                if entraM:
                    util_infM = lineM.split()
                    informationM = informationM + [util_infM[0], ]
                if lineM == '\n':
                    entraM = True
            # --------------------------------------------------------------------------------- READ GROUND TRUTH LABELS
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

            # ----------------------------------------------------------------------------------------- READ PAJEK GRAPH
            graph = file[:-3]+'net'
            G = nx.Graph(nx.read_pajek('A3-networks/'+graph))

            # ----------------------------------------------------------------------------------------- READ COORDINATES
            dictionary = G._node
            if len(list(dictionary[list(dictionary.keys())[0]].keys()))>1:
                position = dict()
                for item in list(G.nodes):
                    position[item] = np.array([dictionary[item]['x'], dictionary[item]['y']])
                print('*******************'+graph)
            else:
                print('*******[No coord]**'+graph)
                position = nx.kamada_kawai_layout(G)

            # -------------------------------------------------------------------------------------- COMPUTE COMMUNITIES
            # Community 1
            partitionC = community_louvain.best_partition(G)
            partitionC = [value for key, value in partitionC.items()]
            node_colorC = [colors[value] for value in partitionC]

            # Community 2
            if graph == 'airports_UW.net':
                G_com2 = read('Extra/' + graph)
            else:
                G_com2 = read('A3-networks/' + graph)
            comunity_2labels = G_com2.community_infomap()
            partitionI = comunity_2labels.membership
            node_colorI = [colors[value] for value in partitionI]

            # NetworkX
            #comp = nx.algorithms.community.centrality.girvan_newman(G)
            #comp2 = list(sorted(c) for c in next(comp))
            #partitionC = [-1] * len(G.node)
            #for it in range(len(comp2)):
            #    for it2 in range(len(comp2[it])):
            #        partitionC[list(G.nodes).index(comp2[it][it2])] = it

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
            partitionM = [-1]*len(G.node)
            for it in range(len(informationM)):
                partitionM[it] = int(informationM[it])-1
            node_colorM = [colors[value] for value in partitionM]

            # -------------------------------------------------------------------------------------------- PRINT RESULTS
            if graph != 'airports_UW.net':
                # Jaccard Index
                # JIC = str(round(jaccar_index(partitionC,ground_truth_partition),2))
                # JII = str(round(jaccar_index(partitionI,ground_truth_partition),2))
                # JIR = str(round(jaccar_index(partitionR,ground_truth_partition),2))
                # JIM = str(round(jaccar_index(partitionM,ground_truth_partition),2))
                # print('The Jaccard Index for Igraph is '+JIC)
                # print('The Jaccard Index for Igraph2 is '+JII)
                # print('The Jaccard Index for Radatools is '+ JIR)
                # print('The Jaccard Index for Matlab is '+ JIM)

                # Normalized mutual information
                NMIC = str(round(compare_communities(partitionC, ground_truth_partition, method='nmi'),2))
                NMII = str(round(compare_communities(partitionI, ground_truth_partition, method='nmi'),2))
                NMIR = str(round(compare_communities(partitionR, ground_truth_partition, method='nmi'),2))
                NMIM = str(round(compare_communities(partitionM, ground_truth_partition, method='nmi'),2))
                # print('The Normilized Mutual Information for Igraph is ' + NMIC)
                # print('The Normilized Mutual Information for Igraph2 is ' + NMII)
                # print('The Normilized Mutual Information for Radatools is ' + NMIR)
                # print('The Normilized Mutual Information for Matlab is ' + NMIM)

                # Variation of information
                VIC = str(round(compare_communities(partitionC, ground_truth_partition, method='vi'),2))
                VII = str(round(compare_communities(partitionI, ground_truth_partition, method='vi'),2))
                VIR = str(round(compare_communities(partitionR, ground_truth_partition, method='vi'),2))
                VIM = str(round(compare_communities(partitionM, ground_truth_partition, method='vi'),2))
                # print('The Variation of information for Igraph is ' + VIC)
                # print('The Variation of information for Igraph2 is ' + VII)
                # print('The Variation of information for Radatools is ' + VIR)
                # print('The Variation of information for Matlab is ' + VIM)

                # Rand Index
                RIC = str(round(compare_communities(partitionC, ground_truth_partition, method='rand'),2))
                RII = str(round(compare_communities(partitionI, ground_truth_partition, method='rand'),2))
                RIR = str(round(compare_communities(partitionR, ground_truth_partition, method='rand'),2))
                RIM = str(round(compare_communities(partitionM, ground_truth_partition, method='rand'),2))
                # print('The Rand Index for Igraph is ' + RIC)
                # print('The Rand Index for Igraph2 is ' + RII)
                # print('The Rand Index for Radatools is ' + RIR)
                # print('The Rand Index for Matlab is ' + RIM)
            else:
                NMIC = '-'
                NMII = '-'
                NMIR = '-'
                NMIM = '-'
                VIC = '-'
                VII = '-'
                VIR = '-'
                VIM = '-'
                RIC = '-'
                RII = '-'
                RIR = '-'
                RIM = '-'


            # -------------------------------------------------------------------------------------------- DRAW NETWORKS
            # C O M M U N I T Y
            fig = plt.figure(figsize=(20, 7))
            plt.subplot(1,5,1)
            nx.draw_networkx(G, pos=position, node_color=node_colorC, node_size=node_size,
                             with_labels=False, edge_color='gray')
            limits = plt.axis('off')
            plt.title('Igraph [Modularity-Louvain]'+'\n# Communities = '+str(len(set(partitionC)))+'\n[NMI]='+NMIC+'\n['
                                                                        'VI]=' +VIC + ' | [RI]=' + RIC,y=-0.13)

            # C O M M U N I T Y  2
            plt.subplot(1,5,2)
            nx.draw_networkx(G, pos=position, node_color=node_colorI, node_size=node_size,
                             with_labels=False, edge_color='gray')
            limits = plt.axis('off')
            plt.title('Igraph [InfoMap]'+'\n# Communities = '+str(len(set(partitionI)))+'\n[NMI]='+NMII+'\n['
                                                                        'VI]=' +VII + ' | [RI]=' + RII,y=-0.13)

            # G R O U N D   T R U T H
            plt.subplot(1, 5, 5)
            if file != 'airports_UW.txt':
                nx.draw_networkx(G, pos=position, node_color=node_colorT, node_size=node_size,
                             with_labels=False, edge_color='gray')
                plt.title('Ground Truth'+'\n# Communities = '+str(len(set(ground_truth_partition)))+'\n \n',y=-0.13)
            else:
                plt.title('Ground Truth')
            limits = plt.axis('off')

            # R A D A T O O L S
            mmm = len(set(node_colorR))
            plt.subplot(1,5,3)
            nx.draw_networkx(G, pos=position, node_color=node_colorR, node_size=node_size,
                             with_labels=False, edge_color='gray')
            limits = plt.axis('off')
            plt.title('Radatools [Modularity]'+'\n# Communities = '+str(len(set(partitionR)))+'\n[NMI]='+NMIR+'\n['
                                                                                'VI]=' +VIR + ' | [RI]=' + RIR,y=-0.13)

            # M A T L A B
            plt.subplot(1,5,4)
            nx.draw_networkx(G, pos=position, node_color=node_colorM, node_size=node_size,
                             with_labels=False, edge_color='gray')
            limits = plt.axis('off')
            plt.title('Matlab [Danon]'+'\n# Communities = '+str(len(set(partitionM)))+'\n[NMI]='+NMIM+'\n[VI]=' +VIM
                      + ' | [RI]=' + RIM,y=-0.13)

            plt.suptitle('Network: '+graph+'\n\n ',fontsize=16)
            fig.savefig('./Images/'+graph+'.png')
