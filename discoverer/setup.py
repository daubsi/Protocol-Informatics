from message import Message
from clustercollection import ClusterCollection

class Setup:
    

    def __init__(self,flowBasedSequences, config):
        if flowBasedSequences==None:
            print "FATAL: No sequences loaded yet"
            return False

        self.cluster_collection = ClusterCollection()    
        for i in flowBasedSequences:
                flowInfo = flowBasedSequences[i]
                for seq in flowInfo.sequences:
                    newMessage = Message(seq.message, config) # Used message instead of sequence now
                    self.cluster_collection.add_message_to_cluster(newMessage)
                    #print newMessage.get_payload()
                    #print "Tokenlist of ", seq.sequence, " = ", newMessage.get_tokenrepresentation_string()
                    # Cluster message
                    
                    #===============================================================
                    # newrep = newMessage.get_tokenrepresentation()
                    # if not cluster.has_key(newrep):
                    #    cluster.update({newrep: [newMessage]})
                    # else:
                    #    l = cluster.get(newrep)
                    #    l.append(newMessage)
                    #    cluster.update({newrep: l})
                    #===============================================================
         
        
        
    def __repr__(self):
        return "%s" % self.cluster_collection
    
    def get_cluster_collection(self):
        
        return self.cluster_collection
    
    def debug(self):
        cluster = self.cluster_collection.get_all_cluster()        
        # Print cluster
        for c in cluster:
            keys = c.keys()
            for key in keys:
                l = c.get(key)
                print "Key:", key, " Elements: ", l  
            
        