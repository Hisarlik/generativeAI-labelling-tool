import database
import pandas as pd
from sqlalchemy.orm import Session
from models import Base, Simplification
def run():

    with Session(database.engine) as session:
        diario_df = pd.read_csv("resources/dataset/openai_35_simplification.csv")
        for _, sentence in diario_df.iterrows():
            example = Simplification(original_sentence=sentence['text'],
                         model_simplification_sentence=sentence['openai_35'],
                         document_sentence_id=sentence['document_sentence_id'],
                         document_name=sentence['document'],
                         length_sentence=sentence['length'])
            session.add(example)
            print(example.document_sentence_id)

            session.commit()



if __name__ == '__main__':
    database.Base.metadata.create_all(database.engine)
    run()