import textwrap
from typing import List

def remove_newlines(s : str) -> str:
    return s.replace('\n',"").replace('\xa0',"")

class Mask:

    def __init__(self, 
        company : str, 
        model : str, 
        niosh_approved: bool, 
        countries_of_origin: List[str], 
        eua_authorized: bool):
        self.company = remove_newlines(company)
        self.model = remove_newlines(model)
        self.niosh_approved = niosh_approved
        self.countries_of_origin = countries_of_origin
        self.eua_authorized = eua_authorized

    @classmethod
    def createAsAuthorizedImportedNonNioshRespiratorsManufacturedInChina(cls, 
        company : str, 
        model : str,
        countries_of_origin : List[str]):
        return cls(
            company=company,
            model=model,
            niosh_approved=False,
            countries_of_origin=countries_of_origin,
            eua_authorized=True
            )

    @classmethod
    def createAsNoLongerAuthorized(cls, 
        company : str, 
        model : str,
        countries_of_origin : List[str]):
        return cls(
            company=company,
            model=model,
            niosh_approved=False,
            countries_of_origin=countries_of_origin,
            eua_authorized=False
            )

    def __repr__(self): 
        return "%40s: %20s - EUA authorized: %8s - country: %20s" % (
            textwrap.shorten(self.company, width=40), 
            textwrap.shorten(self.model, width=20), 
            textwrap.shorten(str(self.eua_authorized), width=8),
            textwrap.shorten(','.join(self.countries_of_origin), width=20)
            )

    def __str__(self):
        return "%s: %s" % (self.company, self.model)

    def to_json(self):
        return {
            'company': self.company,
            'model': self.model
        }