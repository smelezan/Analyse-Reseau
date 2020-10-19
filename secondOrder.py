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
    viewMetric = g.getDoubleProperty("viewMetric")
    eccentricity = g.getDoubleProperty("eccentricity")
    g.applyDoubleAlgorithm("Eccentricity", eccentricity)
    
    with open('eccentricity.csv','w') as f:
        writer= csv.writer(f)
        writer.writerow(['nb_sommets','mesure','taille_composante','lg moyenne'])
        
        for i in range (100):
            node = eccentricity.getNodesEqualTo(eccentricity.getNodeMin(g),g).next()
            g.delNode(node)
            comp = tlp.ConnectedTest.computeConnectedComponents(g)
            maxl = 0
            
            for n in comp:
                if( len(n) > maxl):
                    maxl = len(n)

            writer.writerow([i,'eccentricity',maxl/g.numberOfNodes(),tlp.averagePathLength(g)])
         
    
     
