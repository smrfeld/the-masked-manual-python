import textwrap
from typing import List, Dict
from enum import Enum

# Note:
# FDA approval + respirator N95 = surgical N95 respirator
# See definition of surgical N95:
# https://www.cdc.gov/niosh/npptl/topics/respirators/disp_part/N95list1.html
class RespiratorType(Enum):
    SURGICAL_MASK_EUA = 0
    SURGICAL_MASK_FDA = 1
    SURGICAL_MASK_FDA_POTENTIALLY_RECALLED = 2
    RESPIRATOR_EUA = 3
    RESPIRATOR_EUA_EXPIRED_AUTH = 4
    RESPIRATOR_N95_NIOSH = 5
    RESPIRATOR_N95_NIOSH_FDA = 6

    def __str__(self):
        return self.name

class ValveType(Enum):
    UNKNOWN = 0
    YES = 1 
    NO = 2
    NA = 3

    def __str__(self):
        return self.name

def remove_newlines(s_in : str) -> str:
    s = s_in
    # Note: strip() removes leading and trailing white space
    return s.replace('\n',"").replace('\xa0',"").strip()

class Mask:

    def __init__(self, 
        company : str, 
        model : str, 
        countries_of_origin: List[str], 
        respirator_type: RespiratorType,
        valve_type: ValveType):

        self.company = fix_phrase(remove_newlines(company))
        self.model = fix_phrase(remove_newlines(model))
        
        self.countries_of_origin = countries_of_origin
        self.respirator_type = respirator_type
        self.valve_type = valve_type
        
    @classmethod
    def createAsSurgicalMaskEua(cls,
        company : str, 
        model : str):
        return cls(
            company=company,
            model=model,
            countries_of_origin=[],
            respirator_type=RespiratorType.SURGICAL_MASK_EUA,
            valve_type=ValveType.NA
            )

    @classmethod
    def createAsSurgicalMaskFDA(cls,
        company : str, 
        model : str,
        recalled : bool):
        if recalled:
            respirator_type=RespiratorType.SURGICAL_MASK_FDA_POTENTIALLY_RECALLED
        else:
            respirator_type=RespiratorType.SURGICAL_MASK_FDA
        
        return cls(
            company=company,
            model=model,
            countries_of_origin=[],
            respirator_type=respirator_type,
            valve_type=ValveType.NA
            )

    @classmethod
    def createAsAuthorizedImportedNonNioshRespirators(cls, 
        company : str, 
        model : str,
        countries_of_origin : List[str]):
        return cls(
            company=company,
            model=model,
            countries_of_origin=countries_of_origin,
            respirator_type=RespiratorType.RESPIRATOR_EUA,
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
            countries_of_origin=countries_of_origin,
            respirator_type=RespiratorType.RESPIRATOR_EUA_EXPIRED_AUTH,
            valve_type=ValveType.UNKNOWN
            )

    @classmethod
    def createAsNioshApprovedN95(cls,
        company : str,
        model : str,
        fda_approved : bool,
        valve_type : ValveType):
        if fda_approved:
            respirator_type = RespiratorType.RESPIRATOR_N95_NIOSH_FDA
        else:
            respirator_type = RespiratorType.RESPIRATOR_N95_NIOSH

        return cls(
            company=company,
            model=model,
            countries_of_origin=[],
            respirator_type=respirator_type,
            valve_type=valve_type
        )

    def __str__(self):
        return "%40s: %40s - %40s" % (
            textwrap.shorten(self.company, width=40), 
            textwrap.shorten(self.model, width=40), 
            textwrap.shorten(str(self.respirator_type), width=40)
            )

    def __repr__(self): 
        return "%s: %s" % (self.company, self.model)

    def to_json(self) -> Dict[str,str]:
        d = {
            'company': self.company,
            'model': self.model,
            'countries_of_origin': self.countries_of_origin,
            'respirator_type': str(self.respirator_type),
            'valve_type': str(self.valve_type)
        }

        return d

def fix_phrase(s_in : str) -> str:
    s = s_in

    # Duplicates - case does not matter in the list on the RHS
    duplicates : Dict[str, List[str]] = {}
    duplicates["ACME FILTER MASK INC."] = ["ACME AUTOMATIC DISPOSABLE"]

    # Ensure lowercase on RHS
    duplicates = { key: [x.lower() for x in vals] for key,vals in duplicates.items() }

    # Replace duplicate
    for key, vals in duplicates.items():
        if s.lower() in vals:
            s = key
    
    # Also fix small errors
    nonsense_words = [
        "fzco",
        "ltda",
        "pte",
        "2000",
        "kgaa",
        "m",
        "i/e",
        "unltd."
    ]
    sp = s.split()
    i_sp = 0
    while i_sp < len(sp):
        if sp[i_sp].lower() in nonsense_words:
            del sp[i_sp]
        else:
            i_sp += 1
    s = " ".join(sp)

    # Ensure that:
    # Space always precedes ( and follows )
    s = s.replace('(',' (').replace(')',') ').replace('  ', ' ')

    # Correct
    corrected_words = [
        "Inc.",
        "Co.",
        "Ltd.",
        "LLC",
        "Medical",
        "Equipment",
        "Company",
        "Protective",
        "Products",
        "Audio",
        "Visual",
        "International",
        "Automatic",
        "Disposable",
        "Dealers"
        "Pro",
        "Tech",
        "American",
        "Convertors",
        "Div.",
        "Seal",
        "Threshold",
        "Healthcare",
        "Resources",
        "Surgicals",
        "Hospital",
        "Disposables",
        "Surgical",
        "Dressings",
        "Medicines",
        "Prod.",
        "Corp."
        "i/e",
        "Health",
        "Creative",
        "Contract",
        "Equipments",
        "Golden",
        "Leaves",
        "Development",
        "Technology",
        "Tech.",
        "Sci.",
        "Intelligent",
        "Industries",
        "for",
        "the",
        "and",
        "Blind",
        "Innovative",
        "Outsourcing",
        "Solutions",
        "Johnson",
        "Assoc.",
        "Packaging",
        "Group",
        "Incorporated",
        "Scientific",
        "Mfg.",
        "Mining",
        "Minnesota",
        "Modern",
        "Pennsylvania",
        "Association",
        "Protect",
        "Guard",
        "Filter",
        "Absorbent",
        "Cotton",
        "Automatic",
        "Disposable",
        "Mask",
        "Surgical",
        "Disposable",
        "Anti-for",
        "Face",
        "Reliable",
        "Cone",
        "Protector",
        "Laser",
        "Plus",
        "Dispos.",
        "Surg.",
        "Pro",
        "Certified",
        "Safety",
        "China",
        "Clinical",
        "Cardiovascular",
        "Green",
        "Cross",
        "Gloves",
        "Bandage",
        "Material",
        "Lancaster",
        "County",
        "Textile",
        "Corp.",
        "Precision",
        "Instrument"
    ]
    corrected_words_lower = [ x.lower().replace('.','').replace(',','') for x in corrected_words ]
    sp = s.split()
    for i, word in enumerate(sp):
        word_lower = word.lower().replace('.','').replace(',','')
        
        if word_lower in corrected_words_lower:
            idx = corrected_words_lower.index(word_lower)
            sp[i] = corrected_words[idx]
            
        # Capitalize the first letter, no matter what
        if i == 0:
            sp[i] = sp[i][0].capitalize() + sp[i][1:]

    s = " ".join(sp)

    # Remove trailing comma
    if len(s) > 0 and s[-1] == ',':
        s = s[:-2]

    return s