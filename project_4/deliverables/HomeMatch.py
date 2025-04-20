import os
import gradio as gr
os.environ["OPENAI_API_KEY"] = "sk-proj"

# For convertting the CSV string to a DataFrame
import pandas as pd
from io import StringIO

# For embedding and vector store
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma

from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import json

from langchain.chat_models import ChatOpenAI

from langchain.chains.query_constructor.schema import AttributeInfo
from langchain.retrievers.self_query.base import SelfQueryRetriever


def store_listings_in_vector_db(df_listing: pd.DataFrame)->Chroma:
    """"
    Store real estate listings in a vector database using Langchain and OpenAI."
    """

    # Combine the relevant fields into one document string for each listing
    def create_document(row):
        return (
            f"Neighborhood: {row['Neighborhood']}\n"
            f"Price: {row['Price']}\n"
            f"Bedrooms: {row['Bedrooms']}\n"
            f"Bathrooms: {row['Bathrooms']}\n"
            f"House Size: {row['House Size']}\n"
            f"Description: {row['Description']}\n"
            f"Neighborhood Description: {row['Neighborhood Description']}"
        )

    # Create a list of document texts
    documents = df_listing.apply(create_document, axis=1).tolist()

    # Use the row data as metadata for each document
    metadatas = df_listing.to_dict(orient="records")

    # Initialize OpenAIEmbeddings from Langchain
    embeddings = OpenAIEmbeddings()

    # Initialize the Chroma vector database collection with persistent storage.
    vectorstore = Chroma.from_texts(
        texts=documents,
        embedding=embeddings,
        metadatas=metadatas,
        collection_name="real_estate_listings",
    )

    return vectorstore


def get_retrievers(vectorstore:Chroma)->SelfQueryRetriever:
    """
    Get real estate recommendations based on buyer preferences using Langchain and OpenAI."
    """

    # Metadata fields of the real estate listings
    metadata_field_info = [
        AttributeInfo(name="Neighborhood", description="The neighborhood where the property is located.", type="string"),
        AttributeInfo(name="Price", description="The price of the property.", type="integer"),
        AttributeInfo(name="Bedrooms", description="The number of bedrooms in the property.", type="integer"),
        AttributeInfo(name="Bathrooms", description="The number of bathrooms in the property.", type="float"),
        AttributeInfo(name="House Size", description="The size of the house in square feet.", type="integer"),
        AttributeInfo(name="Description", description="A description of the property.", type="string"),
        AttributeInfo(name="NeighborhoodDescription", description="A description of the neighborhood.", type="string"),
    ] 

    document_content_description = "Real Estate Listings: Each listing contains information about the property, including neighborhood, price, number of bedrooms and bathrooms, house size, description, and neighborhood description."
    # Use a lower temperature for more deterministic output
    llm = ChatOpenAI(model_name = "chatgpt-4o-latest", temperature=0.2)

    retriever = SelfQueryRetriever.from_llm(
        llm, vectorstore, document_content_description, metadata_field_info, verbose=True)
    
    return retriever

def generate_personalized_listing_description(buyer_preference: str):
    """
    Given a buyer's preference, find the closest listing and generate a personalized description.
    Returns both the listing details and the personalized description.
    """
    # Retrieve similar listings using the buyer's preference
    similar_listings = retriever.invoke(buyer_preference)
    if not similar_listings:
        return "No similar listings found. Please try again with a different preference.", ""
    
    # Get the closest matching listing
    closest_listing = similar_listings[0].page_content

    # Define the prompt template to generate a personalized listing description.
    prompt_template = """
    You are a creative real estate assistant. Given the following listing details and a buyer's preference, generate a personalized listing description that highlights the aspects of the property aligning with the buyer's preferences, while preserving all factual details about the property. Do not modify any factual information.

    Listing:
    {listing}

    Buyer Preference:
    {buyer_preference}

    Personalized Description:
    """
    prompt = PromptTemplate(
        input_variables=["listing", "buyer_preference"],
        template=prompt_template
    )

    # Initialize the LLM for generating the description (adjust temperature for creativity)
    llm = ChatOpenAI(model_name="chatgpt-4o-latest", temperature=0.7)
    chain = LLMChain(llm=llm, prompt=prompt)

    personalized_description = chain.run(
        listing=closest_listing,
        buyer_preference=buyer_preference
    )

    return closest_listing, personalized_description

# Load the real estate listings CSV file
df_listings = pd.read_csv("data/real_estate_listings.csv")
vectorstore = store_listings_in_vector_db(df_listings)
retriever = get_retrievers(vectorstore)

# Build the Gradio interface
iface = gr.Interface(
    fn=generate_personalized_listing_description,
    inputs=gr.Textbox(lines=5, placeholder="Enter your buyer preference...", label="Buyer Preference"),
    outputs=[
        gr.Textbox(label="Closest Match Listing"),
        gr.Textbox(label="Personalized Description")
    ],
    title="Real Estate Recommendation",
    description="Enter your buyer preference to find the closest matching listing and receive a personalized description.",
    flagging_options=[]
)

iface.launch()