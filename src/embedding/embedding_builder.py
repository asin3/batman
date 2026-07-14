############################
#Imports
########################

import json
import sys

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:

    sys.path.insert(0, str(PROJECT_ROOT))

from sentence_transformers import SentenceTransformer

from src.knowledge.knowledge_repository import (

    KnowledgeRepository

)

##################################
#Load Repository
###################################

DOCUMENT_FOLDER = (

    PROJECT_ROOT

    / "data"

    / "class10"

    / "biology"

    / "textbook"

    / "staging"

    / "DOC000013"

)

repository = KnowledgeRepository(

    DOCUMENT_FOLDER

)

assets = repository.load_all()

chunks = assets["chunks"]

#############################
#Load Model
################################

model = SentenceTransformer(

    "all-MiniLM-L6-v2"

)

######################################
#Build Embeddings
#######################################

embeddings = model.encode(

    [

        chunk["content"]

        for chunk in chunks

    ],

    convert_to_numpy=True

)

#####################################
#Save
###################################
import numpy as np

np.save(

    DOCUMENT_FOLDER / "embeddings.npy",

    embeddings

)

########################################
#Manifest Update
#######################################

embeddings_created = True

########################################
#Reporting
########################################
