import os
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()

class RentalExtract(BaseModel):
    bhk: int | str = Field(description="Number of bedrooms in BHK format (e.g., 1, 2, 3, etc.)")
    furnishing: str = Field(description="Unfurnished / Semi-furnished / Furnished / Unknown")
    location: str = Field(description="Neighbourhood and city, if available")
    rent_amount: int = Field(description="Rent in INR (numeric, no commas)")
    deposit_amount: int = Field(description="Deposit in INR (numeric, no commas)")
    property_type: str = Field(description="Apartment / Flat / House / PG / Other")


model = ChatGroq(
    model = "llama-3.3-70b-versatile",
    temperature = 0
)

parser = PydanticOutputParser(pydantic_object=RentalExtract)

prompt = PromptTemplate(
    template = (
        """
        You extract structured rental listing details from a short message.
        From the text below, extract fields (Unknown if missing):
        - bhk (number)
        - furnishing (Unfurnished / Semi-furnished / Furnished)
        - location (neighbourhood, city)
        - rent_amount (numeric, INR, without commas)
        - deposit_amount (numeric, INR, without commas)
        - property_type (Apartment/Flat/House/PG/Other)

        Only return valid JSON with these keys exactly.

        Text: {text}
        """
    ), input_variables=["text"],
    partial_variables={"format_instructions": parser.get_format_instructions()}
    
)

def extract(text: str) -> RentalExtract:
    chain = prompt |  model | parser
    try: 
        result = chain.invoke({"text":text})
        return result
    except Exception as e:
        print("parsing failed", e)
        return RentalExtract(
            bhk="Unknown",
            furnishing="Unknown",
            location="Unknown",
            rent_amount="Unknown",
            deposit_amount="Unknown",
            property_type="Unknown",
        )
if __name__ == "__main__":
    sample_text = "2 BHK semi-furnished apartment in Pune available for 20,000 INR rent and 50,000 deposit."
    result = extract(sample_text)
    print(result)