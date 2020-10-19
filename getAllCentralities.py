import csv
from tulip import tlp
# The updateVisualization(centerViews = True) function can be called
# during script execution to update the opened views
# The pauseScript() function can be called to pause the script execution.
# To resume the script execution, you will have to click on the
# "Run script " button.
# The runGraphScript(scriptFile, graph) function can be called to launch
# another edited script on a tlp.Graph object.
# The scriptFile parameter defines the script name to call
# (in the form [a-zA-Z0-9_]+.py)
# The main(graph) function must be defined
# to run the script on the current graph
def main(graph):
    g = graph.addCloneSubGraph("clone")
    id_ = g['id']


    gDegree= graph.addCloneSubGraph('Degree')
    gBetweenness = graph.addCloneSubGraph("Betweenness Centrality")
    gPageRank = graph.addCloneSubGraph("Page Rank")
    gEccentricity = graph.addCloneSubGraph("Eccentricity")
    betweennessDs = tlp.getDefaultPluginParameters("Betweenness Centrality", g)
    betweennessDs['target']="nodes"

    
    allCentralities = [
        { 'Name':'Degree',  'max':True, 'graph': gDegree, 'currentAvgPath':0,'currLengthComponent':0 },
        { 'Name':'Betweenness Centrality', 'ds' :betweennessDs, 'max':True, 'graph': gBetweenness, 'currentAvgPath':0,'currLengthComponent':0 },
        { 'Name':'Page Rank',  'max':False, 'graph': gPageRank, 'currentAvgPath':0,'currLengthComponent':0 },
        { 'Name':'Eccentricity', 'max':False, 'graph':gEccentricity , 'currentAvgPath':0,'currLengthComponent':0 },
    ]
    
    with open('allCentralities.csv','w') as f:
        writer= csv.writer(f)
        
        writer.writerow(['nb_sommets','mesure#1','taille_composante#1','lg moyenne#1','mesure#2','taille_composante#2','lg moyenne#2','mesure#3','taille_composante#3','lg moyenne#3','mesure#4','taille_composante#4','lg moyenne#4','mesure#5','taille_composante#5','lg moyenne#5'])
        
        
        for i in range (100):
            for centrality in allCentralities:
                currGraph = graph.getDescendantGraph(centrality['Name'])

                if("ds" in centrality):
                    cent= tlp.DoubleProperty(currGraph)
                    currGraph.applyDoubleAlgorithm(centrality['Name'],centrality['ds'])
                else:
                    cent = currGraph.getDoubleProperty(centrality['Name'])
                    currGraph.applyDoubleAlgorithm(centrality['Name'], cent)
                    
                if( centrality['max']):
                    n = cent.getNodesEqualTo(cent.getNodeMax(currGraph), currGraph).next()
                else:
                    n = cent.getNodesEqualTo(cent.getNodeMin(currGraph), currGraph).next()

                currGraph.delNode(n)

                comp = tlp.ConnectedTest.computeConnectedComponents(currGraph)
                maxl = 0    
                for n in comp:
                    if( len(n) > maxl):
                        maxl = len(n)
                centrality['currentAvgPath']=tlp.averagePathLength(currGraph)
                centrality['currLengthComponent'] = maxl / currGraph.numberOfNodes()
            
            writer.writerow([i,
                'Degree',allCentralities[0]['currLengthComponent'],allCentralities[0]['currentAvgPath'],
                'Betweenness',allCentralities[1]['currLengthComponent'],allCentralities[1]['currentAvgPath'],
                'Page Rank',allCentralities[2]['currLengthComponent'],allCentralities[2]['currentAvgPath'],
                'Eccentricity',allCentralities[3]['currLengthComponent'],allCentralities[3]['currentAvgPath']])
                
            
    
     
