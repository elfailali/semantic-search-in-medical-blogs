#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Mapping is the process of defining how a document, and the fields it contains, are stored and indexed.


# In[ ]:


indexMapping = {
    "properties" : {
        "condition_label" : {
            "type" : "long"
        },
        "content" : {
            "type" : "text"
        },
        "description_vector" : {
            "type" : "dense_vector",
            "dims" : 768,
            "index" : True,
            "similarity" : "l2_norm" # dist euclid 
        },
    },
}

