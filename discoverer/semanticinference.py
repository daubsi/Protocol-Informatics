import common
from peekable import peekable
from tokenrepresentation import TokenRepresentation

def perform_semantic_inference(cluster_collection, config):
    """
    This function performs semantic inference on a list of clusters given
    For each message in these clusters semantics are inferred by analyzing the token
    resp. its context.
    
    At the moment only two semantics are automatically inferred: numeric and IPv4 address
    
    TODO: Add more semantics, e.g. EOL identifier, lenght fields, ...
    """        
# Try to perform semantic inferences

# Walk through every cluster and check messages for obvious results
    cluster = cluster_collection.get_all_cluster()        
    for c in cluster:
        messages = c.get_messages()
        for message in messages:
            tokenlist = message.get_tokenlist()
            iterator = peekable(tokenlist)
            idx = 0
            while not iterator.isLast():
            #for tokenRepresentation in tokenlist:
                tokenRepresentation = iterator.next()
                tokenRepresentation.set_semantics([]) # Clear existing semantics from previous run
                token = tokenRepresentation.get_token()
                # Check whether it is numeric
                try:
                    isNumber = common.is_number(token)
                except TypeError:
                    print "Error checking token ", token, " for number semantics"
                    isNumber = False
                if isNumber:
                    tokenRepresentation.add_semantic("numeric")
                    c.add_semantics(idx,"numeric")
                    #print "Inferred semantic inference 'numeric' for token ", token
                    
                # Check whether it is an IP address
                if isinstance(token,str) and common.is_ipv4(token):
                    tokenRepresentation.add_semantic("ipv4 address")
                    c.add_semantics(idx,"ipv4 address")
                    #print "Inferred semantic inference 'ipv4 address' for token ", token
        
                # Check for carriage return identifiers
                # When 0d is followed by 0a we've got a CR-LF
                # Sensible? When 0d or 0a is the last token, we've got a single CR resp LF
                # In all other cases assume 0d/0a is just a hex value of the protocol
                if token == 0xd:
                    nextOne = iterator.peek()
                    if isinstance(nextOne, TokenRepresentation):
                        if nextOne.get_token() == 0xa:
                            inferred_formats = c.get_format_inference()
                            if inferred_formats[idx]=='const' and inferred_formats[idx+1]=='const':
                                tokenRepresentation.add_semantic("CR")
                                c.add_semantics(idx,"CR")
                                nextOne = iterator.next()
                                nextOne.set_semantics(["numeric","LF"])
                                c.add_semantics(idx+1, "LF")
                                idx += 1
                    
                idx +=1
        # Perform other tests like "is length field?"
        reference_message = messages[0]
        tokenlist = reference_message.get_tokenlist()
        idx = 0
        for tokenRepresentation in tokenlist:
            if tokenRepresentation.get_tokenType()=='binary' and idx+1<len(tokenlist):
                ref_value = tokenRepresentation.get_token()
                ref_next_length = tokenlist[idx+1].get_length()
                if not ref_value == ref_next_length: # This is no length field
                    continue
                ref_message_length = reference_message.get_length()
                is_length = True
                for message in messages:
                    cmp_value = message.get_tokenlist()[idx].get_token()
                    cmp_next_length = message.get_tokenlist()[idx+1].get_length()
                    cmp_message_length = message.get_length()
                    try:
                        diff_val = cmp_value - ref_value
                    except TypeError: # Could happen if a short text token is mistaken as a binary value
                        break
                    diff_next_length = cmp_next_length - ref_next_length
                    diff_msg_length = cmp_message_length - ref_message_length
                    if not (diff_val == diff_next_length == diff_msg_length):
                        is_length = False
                        break
                if is_length: # set "lengthfield" semantic for every message in the cluster at the given position
                    for message in messages: # TODO: What if there's only one message in the cluster? Sensible?
                        message.get_tokenlist()[idx].add_semantic("lengthfield")
                        c.add_semantics(idx,"lengthfield")
            idx += 1    

        
        
    