import textwrap
from typing import List, Dict
from enum import Enum

# Note:
# FDA approval + N95 = surgical N95
# See definition of surgical N95:
# https://www.cdc.gov/niosh/npptl/topics/respirators/disp_part/N95list1.html
class RespiratorType(Enum):
    UNKNOWN = 0
    N95 = 1
    SURGICAL_N95 = 2

    def __str__(self):
        return self.name

class ValveType(Enum):
    UNKNOWN = 0
    YES = 1 
    NO = 2

    def __str__(self):
        return self.name

def remove_newlines(s : str) -> str:
    # Note: strip() removes leading and trailing white space
    return s.replace('\n',"").replace('\xa0',"").strip()

def fix_duplicate_companies(s : str) -> str:
    if s == "3M Company":
        return "3M"
    else:
        return s

class Mask:

    def __init__(self, 
        company : str, 
        model : str, 
        niosh_approved: bool, 
        countries_of_origin: List[str], 
        eua_authorized: bool,
        respirator_type: RespiratorType,
        valve_type: ValveType):
        self.company = fix_duplicate_companies(remove_newlines(company))
        self.model = remove_newlines(model)
        self.niosh_approved = niosh_approved
        self.countries_of_origin = countries_of_origin
        self.eua_authorized = eua_authorized
        self.respirator_type = respirator_type
        self.valve_type = valve_type

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
            eua_authorized=True,
            respirator_type=RespiratorType.UNKNOWN,
            valve_type=ValveType.UNKNOWN
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
            eua_authorized=False,
            respirator_type=RespiratorType.UNKNOWN,
            valve_type=ValveType.UNKNOWN
            )

    @classmethod
    def createAsNioshApprovedN95(cls,
        company : str,
        model : str,
        respirator_type : RespiratorType,
        valve_type : ValveType):
        return cls(
            company=company,
            model=model,
            niosh_approved=False,
            countries_of_origin=[],
            eua_authorized=False,
            respirator_type=respirator_type,
            valve_type=valve_type
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

    def to_json(self) -> Dict[str,str]:
        d = {
            'company': self.company,
            'model': self.model,
            'niosh_approved': self.niosh_approved,
            'eua_authorized': self.eua_authorized,
            'countries_of_origin': self.countries_of_origin,
            'respirator_type': str(self.respirator_type),
            'valve_type': str(self.valve_type)
        }

        return d