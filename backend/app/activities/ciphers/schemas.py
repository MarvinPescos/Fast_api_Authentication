from pydantic import Field, BaseModel
 
class ProccessTextResponse(BaseModel):
    """ Ciphered Text """
    result: str = Field(..., description="Ciphered Text")

class AtbashRequest(BaseModel):
    """ Atbash Request Schema"""
    text: str = Field(..., min_length=1)

class CaesarRequest(BaseModel):
    """ Caesar Request Schema"""
    text: str = Field(..., min_length=1)
    shift: int = Field(..., ge=1, le=25)

class VigenereRequest(BaseModel):
    """ Vigenere Request Schema"""
    text: str = Field(..., min_length=1)
    key: str = Field(..., min_length=1, pattern="^[a-zA-Z ]+$", description="Key must contain only letters and spaces")
    