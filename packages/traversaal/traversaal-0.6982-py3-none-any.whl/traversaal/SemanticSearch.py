# traversaal/semantic_search.py

import warnings
import torch
from transformers import AutoTokenizer, AutoModel
import time
from sentence_transformers import SentenceTransformer
from openai.embeddings_utils import get_embedding, cosine_similarity


class SemanticSearch:
    def __init__(self):
        warnings.filterwarnings("ignore")  # Hide warnings
        self.model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")
        if not torch.cuda.is_available():
            print("Warning: No GPU found. Please add GPU to your notebook")
        else:
            print(
                """

  _______ .______    __    __      _______   ______    __    __  .__   __.  _______   __  
 /  _____||   _  \  |  |  |  |    |   ____| /  __  \  |  |  |  | |  \ |  | |       \ |  | 
|  |  __  |  |_)  | |  |  |  |    |  |__   |  |  |  | |  |  |  | |   \|  | |  .--.  ||  | 
|  | |_ | |   ___/  |  |  |  |    |   __|  |  |  |  | |  |  |  | |  . `  | |  |  |  ||  | 
|  |__| | |  |      |  `--'  |    |  |     |  `--'  | |  `--'  | |  |\   | |  '--'  ||__| 
 \______| | _|       \______/     |__|      \______/   \______/  |__| \__| |_______/ (__) 
                                                                                          

            
            """
            )
            self.model = self.model.to("cuda")

    def encode(self, text):
        with warnings.catch_warnings():
            embeddings = self.model.encode(text)

        return embeddings

    def encode_data(self, df):
        encoded_data = df.copy()
        print(
            """

.___________.__    __   __       _______.   .___  ___.      ___   ____    ____    .___________.    ___       __  ___  _______ 
|           |  |  |  | |  |     /       |   |   \/   |     /   \  \   \  /   /    |           |   /   \     |  |/  / |   ____|
`---|  |----|  |__|  | |  |    |   (----`   |  \  /  |    /  ^  \  \   \/   /     `---|  |----`  /  ^  \    |  '  /  |  |__   
    |  |    |   __   | |  |     \   \       |  |\/|  |   /  /_\  \  \_    _/          |  |      /  /_\  \   |    <   |   __|  
    |  |    |  |  |  | |  | .----)   |      |  |  |  |  /  _____  \   |  |            |  |     /  _____  \  |  .  \  |  |____ 
    |__|    |__|  |__| |__| |_______/       |__|  |__| /__/     \__\  |__|            |__|    /__/     \__\ |__|\__\ |_______|
                                                                                                                              
     _______.  ______   .___  ___.  _______    .___________.__  .___  ___.  _______                                           
    /       | /  __  \  |   \/   | |   ____|   |           |  | |   \/   | |   ____|                                          
   |   (----`|  |  |  | |  \  /  | |  |__      `---|  |----|  | |  \  /  | |  |__                                             
    \   \    |  |  |  | |  |\/|  | |   __|         |  |    |  | |  |\/|  | |   __|                                            
.----)   |   |  `--'  | |  |  |  | |  |____        |  |    |  | |  |  |  | |  |____ __ __ __                                  
|_______/     \______/  |__|  |__| |_______|       |__|    |__| |__|  |__| |_______(__(__(__)                                 
                                                                                                                              

        """
        )
        startTime = time.time()
        encoded_data["embedding"] = encoded_data["hotel_review"].apply(
            self.encode
        ) + encoded_data["hotel_description"].apply(self.encode)
        executionTime = time.time() - startTime
        print("Execution time in seconds: " + str(executionTime))
        return encoded_data

    def search(self, encoded_data, query):
        # query_embedding = embedder.encode(query,show_progress_bar=True)
        query_embedding = self.encode(query)
        encoded_data["score"] = encoded_data["embedding"].apply(
            lambda x: cosine_similarity(x, query_embedding.reshape(768, -1))
        )
        encoded_data = encoded_data.sort_values(by="score", ascending=False)

        # Get relevant reviews
        # encoded_data["relevant_reviews"] = encoded_data.apply(
        #     lambda row: self.get_relevant_reviews(
        #         row["id"], row["hotel_name"], encoded_data, query
        #     ),
        #     axis=1,
        # )

        relevant_results = encoded_data[["id", "hotel_name", "score", "hotel_review"]]
        relevant_results.rename(
            {"hotel_review": "relevant_review"}, axis="columns", inplace=True
        )

        return relevant_results

    def get_relevant_reviews(self, hotel_id, hotel_name, encoded_data, query):
        relevant_reviews = encoded_data[
            (encoded_data["id"] == hotel_id)
            & (encoded_data["hotel_name"] == hotel_name)
        ]["hotel_review"].tolist()
        return [review for review in relevant_reviews if query in review.lower()]
