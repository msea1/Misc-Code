from typing import Any, Optional, Union, cast
from pydantic import BaseModel
import json
import csv
import re
from pathlib import Path
import os


class DataDefinition(BaseModel):
    data_key: str
    data_type: Optional[str] = None  # informal desc of type ("array of strings", "date", etc.)
    required: Optional[bool] = None  # required for ingestion
    description: Optional[str] = None
    examples: Optional[list[Any]] = None

    # INTERNAL ONLY — strip before sending to vendors
    request_if_missing: Optional[bool] = None  # TBD; ask provider to fill in this data (PRE-ABSTRACTION)
    must_be_present: Optional[bool] = None  # TBD; if missing, data should not be sent to abstractor (PRE-ABSTRACTION) 
    destination: Optional[str] = None  # e.g. ccdm_eob.patient, medical_provider.address_line_1 (POST-ABSTRACTION)
    import_details: Optional[str] = None  # technical notes for ingestion parser (POST-ABSTRACTION)
    comment: Optional[str] = None  # general notes, likely internal-only, about the piece of data


class DataGroupReference(BaseModel):
    ref: str  # name of a reusable group


class DataGroupDefinition(BaseModel):
    group_name: str
    description: Optional[str] = None

    # groups can contain either raw definitions or nested groups
    data_definitions: Optional[list[DataDefinition]] = None
    subgroups: Optional[list[Union["DataGroupDefinition", DataGroupReference]]] = None


class SchemaDefinition(BaseModel):
    name: str
    version: str
    description: Optional[str] = None
    vendor_instructions: Optional[list[str]] = None
    groups: list[DataGroupDefinition]


def to_vendor_json_old(schema: SchemaDefinition) -> dict:
    data = schema.model_dump(
        exclude={
            "groups": {
                "__all__": {
                    "data_definitions": {"__all__": {
                        "request_if_missing",
                        "must_be_present",
                        "destination",
                        "import_details",
                        "comment",
                    }},
                }
            }
        }
    )
    if "vendor_instructions" in data and data["vendor_instructions"]:
        data["vendor_instructions"] = [
            f"{i+1}. {instr}" for i, instr in enumerate(data["vendor_instructions"])
        ]
    return data


def sort_dict_old(d: dict|list, is_root=True) -> dict|list:
        root_order = ["name", "version", "description", "vendor_instructions", "groups"]
        group_order = ["group_name", "description", "data_definitions", "subgroups"]
        if isinstance(d, dict):
            keys = list(d.keys())
            preferred_order = root_order if is_root else group_order
            ordered_keys = [k for k in preferred_order if k in keys] + [k for k in sorted(keys) if k not in preferred_order]
            sorted_items = []
            for k in ordered_keys:
                v = d[k]
                # Recursively sort dicts/lists, is_root only for first pass
                if isinstance(v, dict):
                    v = sort_dict(v, is_root=False)
                elif isinstance(v, list):
                    v = [sort_dict(i, is_root=False) if isinstance(i, dict) else i for i in v]
                sorted_items.append((k, v))
            return dict(sorted_items)
        elif isinstance(d, list):
            return [sort_dict(i, is_root=False) if isinstance(i, dict) else i for i in d]
        else:
            return d


def sort_dict(d: dict | list, is_root=True) -> dict | list:
    """Sorts keys consistently for stable vendor output."""
    root_order = ["name", "version", "description", "vendor_instructions", "groups", "components"]
    group_order = ["group_name", "description", "data_definitions", "subgroups"]

    if isinstance(d, dict):
        keys = list(d.keys())
        preferred_order = root_order if is_root else group_order
        ordered_keys = [k for k in preferred_order if k in keys] + [
            k for k in sorted(keys) if k not in preferred_order
        ]
        return {k: sort_dict(d[k], is_root=False) if isinstance(d[k], (dict, list)) else d[k]
                for k in ordered_keys}
    elif isinstance(d, list):
        return [sort_dict(i, is_root=False) if isinstance(i, (dict, list)) else i for i in d]
    return d


def to_vendor_json(schema: SchemaDefinition, components: dict[str, DataGroupDefinition]) -> dict:
    """
    Convert SchemaDefinition -> JSON-schema-like dict for vendors.
    - Includes top-level `components` with reusable groups
    - Emits $ref for DataGroupReference
    - Strips internal-only fields
    - Omits empty arrays / None values
    - Sorts keys consistently for stable output
    """
    # ----- Helpers -----
    def strip_internal(defn: DataDefinition) -> dict:
        d = defn.model_dump(
            exclude={
                "request_if_missing",
                "must_be_present",
                "destination",
                "import_details",
                "comment",
            }
        )
        return {k: v for k, v in d.items() if v not in (None, [], {})}

    def render_group(group: DataGroupDefinition | DataGroupReference) -> dict:
        if isinstance(group, DataGroupReference):
            return {"$ref": f"#/components/{group.ref}"}

        d: dict[str, Any] = {"group_name": group.group_name}
        if group.description:
            d["description"] = group.description
        if group.data_definitions:
            defs = [strip_internal(dd) for dd in group.data_definitions if dd]
            if defs:
                d["data_definitions"] = defs
        if group.subgroups:
            subs = [render_group(g) for g in group.subgroups if g]
            if subs:
                d["subgroups"] = subs
        return cast(dict[str, Any], sort_dict(d, is_root=False))

    def render_components() -> dict[str, Any]:
        comps: dict[str, Any] = {}
        for name, comp in components.items():
            d: dict[str, Any] = {"group_name": comp.group_name}
            if comp.description:
                d["description"] = comp.description
            if comp.data_definitions:
                defs = [strip_internal(dd) for dd in comp.data_definitions if dd]
                if defs:
                    d["data_definitions"] = defs
            if comp.subgroups:
                subs = [render_group(g) for g in comp.subgroups if g]
                if subs:
                    d["subgroups"] = subs
            comps[name] = sort_dict(d, is_root=False)
        return comps

    # ----- Root dict -----
    data: dict[str, Any] = {
        "name": schema.name,
        "version": schema.version,
    }
    if schema.description:
        data["description"] = schema.description
    if schema.vendor_instructions:
        data["vendor_instructions"] = [
            f"{i+1}. {instr}" for i, instr in enumerate(schema.vendor_instructions)
        ]
    if schema.groups:
        data["groups"] = [render_group(g) for g in schema.groups if g]
    if components:
        data["components"] = render_components()

    return cast(dict[str, Any], sort_dict(data, is_root=True))





# reusable components
amounts_schema = DataGroupDefinition(
    group_name="amounts",
    description="Monetary amounts associated with a claim",
    data_definitions=[
        DataDefinition(data_key="chargeAmount", data_type="float", required=True),
        DataDefinition(data_key="paidAmount", data_type="float"),
        DataDefinition(data_key="allowedAmount", data_type="float"),
    ],
)

components = {
    "AmountsSchema": amounts_schema,
}


example_schema = SchemaDefinition(
    name="Claims Abstraction",
    version="claims_abstraction_00001",
    description="Schema for medical & pharmacy claims",
    vendor_instructions=["Use the phrase 'no data found' when no data is present."],
    groups=[
    ],
)


# ===== Hard-coded components generated from abstraction_schema_required_fields.csv =====
# These were produced by running this script with EMIT_COMPONENT_CODE=1 and are now embedded
# so they're visible and importable without dynamic generation.

# ----- BEGIN GENERATED COMPONENT DEFINITIONS -----
abstractor_schema = DataGroupDefinition(
        group_name="abstractorSchema",
        data_definitions=[
            DataDefinition(data_key="abstractionRound", data_type="integer", required=False, description=None, examples=["1"], request_if_missing=None, must_be_present=None, destination=None, import_details=None, comment=None),
            DataDefinition(data_key="abstractionState", data_type="string", required=False, description=None, examples=["complete"], request_if_missing=None, must_be_present=None, destination=None, import_details=None, comment=None),
            DataDefinition(data_key="abstractorName", data_type="string", required=True, description=None, examples=["Henderson, Samuel"], request_if_missing=None, must_be_present=None, destination=None, import_details=None, comment="Please add description to schema: \"Full abstractor name as (last name, first name), not e-mail address, initials, etc.\""),
            DataDefinition(data_key="abstractionCompletionDateTime", data_type="string", required=True, description=None, examples=["2022-05-01"], request_if_missing=None, must_be_present=None, destination=None, import_details=None, comment=None),
            DataDefinition(data_key="abstractionDiscrepancies", data_type="string", required=False, description=None, examples=None, request_if_missing=None, must_be_present=None, destination=None, import_details=None, comment=None),
            DataDefinition(data_key="abstractionResolution", data_type="string", required=False, description=None, examples=None, request_if_missing=None, must_be_present=None, destination=None, import_details=None, comment=None)
        ]
)

amounts_schema = DataGroupDefinition(
        group_name="amountsSchema",
        data_definitions=[
            DataDefinition(data_key="allowedCents", data_type="integer", required=False, description=None, examples=["12500"], request_if_missing=True, must_be_present=False, destination=None, import_details=None, comment="Re-request will be performed if, for a given occurrence of amountsSchema, the claim does not provide EITHER:\na) allowed, OR\nb) BOTH (patient overall responsibility OR ALL OF (coinsurance, copay, and deductible)) AND paid by insurance, OR\nc) [pharmacy claims only] BOTH paid by patient AND paid by insurance"),
            DataDefinition(data_key="billedCents", data_type="integer", required=False, description=None, examples=["15000"], request_if_missing=False, must_be_present=False, destination=None, import_details=None, comment=None),
            DataDefinition(data_key="patientOverallResponsibilityCents", data_type="integer", required=False, description=None, examples=["2500"], request_if_missing=True, must_be_present=False, destination=None, import_details=None, comment="Re-request will be performed if, for a given occurrence of amountsSchema, the claim does not provide EITHER:\na) allowed, OR\nb) BOTH (patient overall responsibility OR ALL OF (coinsurance, copay, and deductible)) AND paid by insurance, OR\nc) [pharmacy claims only] BOTH paid by patient AND paid by insurance"),
            DataDefinition(data_key="coinsuranceCents", data_type="integer", required=False, description=None, examples=["500"], request_if_missing=True, must_be_present=False, destination=None, import_details=None, comment="Re-request will be performed if, for a given occurrence of amountsSchema, the claim does not provide EITHER:\na) allowed, OR\nb) BOTH (patient overall responsibility OR ALL OF (coinsurance, copay, and deductible)) AND paid by insurance, OR\nc) [pharmacy claims only] BOTH paid by patient AND paid by insurance"),
            DataDefinition(data_key="copayCents", data_type="integer", required=False, description=None, examples=["2000"], request_if_missing=True, must_be_present=False, destination=None, import_details=None, comment="Re-request will be performed if, for a given occurrence of amountsSchema, the claim does not provide EITHER:\na) allowed, OR\nb) BOTH (patient overall responsibility OR ALL OF (coinsurance, copay, and deductible)) AND paid by insurance, OR\nc) [pharmacy claims only] BOTH paid by patient AND paid by insurance"),
            DataDefinition(data_key="deductibleCents", data_type="integer", required=False, description=None, examples=["0"], request_if_missing=True, must_be_present=False, destination=None, import_details=None, comment="Re-request will be performed if, for a given occurrence of amountsSchema, the claim does not provide EITHER:\na) allowed, OR\nb) BOTH (patient overall responsibility OR ALL OF (coinsurance, copay, and deductible)) AND paid by insurance, OR\nc) [pharmacy claims only] BOTH paid by patient AND paid by insurance"),
            DataDefinition(data_key="nonCoveredCents", data_type="integer", required=False, description=None, examples=["2500"], request_if_missing=False, must_be_present=False, destination=None, import_details=None, comment=None),
            DataDefinition(data_key="paidByInsuranceCents", data_type="integer", required=False, description=None, examples=["10000"], request_if_missing=True, must_be_present=False, destination=None, import_details=None, comment="Re-request will be performed if, for a given occurrence of amountsSchema, the claim does not provide EITHER:\na) allowed, OR\nb) BOTH (patient overall responsibility OR ALL OF (coinsurance, copay, and deductible)) AND paid by insurance, OR\nc) [pharmacy claims only] BOTH paid by patient AND paid by insurance"),
            DataDefinition(data_key="paidByPatientCents", data_type="integer", required=False, description=None, examples=["2500"], request_if_missing=True, must_be_present=False, destination=None, import_details=None, comment="Re-request will be performed if, for a given occurrence of amountsSchema, the claim does not provide EITHER:\na) allowed, OR\nb) BOTH (patient overall responsibility OR ALL OF (coinsurance, copay, and deductible)) AND paid by insurance, OR\nc) [pharmacy claims only] BOTH paid by patient AND paid by insurance")
        ]
)

claim_note_item_schema = DataGroupDefinition(
        group_name="claimNoteItemSchema",
        data_definitions=[
            DataDefinition(data_key="message", data_type="string", required=False, description=None, examples=None, request_if_missing=None, must_be_present=None, destination=None, import_details=None, comment=None)
        ]
)

diagnosis_codes_schema = DataGroupDefinition(
        group_name="diagnosisCodesSchema",
        data_definitions=[
            DataDefinition(data_key="code", data_type="string", required=False, description=None, examples=["H66.002"], request_if_missing=True, must_be_present=False, destination=None, import_details=None, comment="For any diagnosis recorded, re-request will be performed if NEITHER code nor descriptoin is provided."),
            DataDefinition(data_key="description", data_type="string", required=False, description=None, examples=["Acute suppurative otitis media without spontaneous rupture of ear drum, left ear"], request_if_missing=True, must_be_present=False, destination=None, import_details=None, comment="For any diagnosis recorded, re-request will be performed if NEITHER code nor descriptoin is provided.")
        ]
)

medical_claim_line_item_schema = DataGroupDefinition(
        group_name="medicalClaimLineItemSchema",
        data_definitions=[
            DataDefinition(data_key="procedureCode", data_type="string", required=False, description=None, examples=["99213"], request_if_missing=True, must_be_present=False, destination=None, import_details=None, comment="Re-request will be performed if a line item contains NEITHER a procedure code nor a revenue code."),
            DataDefinition(data_key="procedureCodeDescription", data_type="string", required=False, description=None, examples=["Established patient office or other outpatient visit, 20-29 minutes"], request_if_missing=False, must_be_present=False, destination=None, import_details=None, comment=None),
            DataDefinition(data_key="procedureCodeModifiers", data_type="[string]", required=False, description=None, examples=[25], request_if_missing=False, must_be_present=False, destination=None, import_details=None, comment=None),
            DataDefinition(data_key="revenueCode", data_type="string", required=False, description=None, examples=["0450"], request_if_missing=True, must_be_present=False, destination=None, import_details=None, comment="Re-request will be performed if a line item contains NEITHER a procedure code nor a revenue code."),
            DataDefinition(data_key="serviceStartDate", data_type="string", required=False, description=None, examples=["2022-03-01"], request_if_missing=True, must_be_present=False, destination=None, import_details=None, comment="Re-request will be performed if a line item does not contain a service start date."),
            DataDefinition(data_key="serviceEndDate", data_type="string", required=False, description=None, examples=["2022-03-01"], request_if_missing=False, must_be_present=False, destination=None, import_details=None, comment=None),
            DataDefinition(data_key="adjudicationDecision", data_type="string", required=False, description=None, examples=["approved"], request_if_missing=True, must_be_present=False, destination=None, import_details=None, comment="Re-request will be performed if adjudication decision is not included at EITHER the overall claim or all line-item levels for a medical claim, unless payor is among those that only send us approved claims (Ops is compiling that list as of 8/2025)."),
            DataDefinition(data_key="quantity", data_type="integer", required=False, description=None, examples=["1"], request_if_missing=False, must_be_present=False, destination=None, import_details=None, comment=None),
            DataDefinition(data_key="nationalDrugCode", data_type="string", required=False, description=None, examples=["143988601"], request_if_missing=False, must_be_present=False, destination=None, import_details=None, comment=None),
            DataDefinition(data_key="page_and_line_number_reference", data_type="string", required=False, description=None, examples=["page 4"], request_if_missing=None, must_be_present=None, destination=None, import_details=None, comment=None)
        ],
        subgroups=[
            DataGroupDefinition(group_name="amounts",
        subgroups=[
            DataGroupReference(ref="amountsSchema")
        ]),
            DataGroupDefinition(group_name="auditLog",
        subgroups=[
            DataGroupReference(ref="abstractorSchema")
        ]),
            DataGroupDefinition(group_name="diagnosisCodes",
        subgroups=[
            DataGroupReference(ref="diagnosisCodesSchema")
        ])
        ]
)

medical_claim_schema = DataGroupDefinition(
        group_name="medicalClaimSchema",
        data_definitions=[
            DataDefinition(data_key="claimId", data_type="string", required=False, description=None, examples=["XYZ12345"], request_if_missing=True, must_be_present=False, destination=None, import_details=None, comment=None),
            DataDefinition(data_key="serviceStartDate", data_type="string", required=False, description=None, examples=["2025-01-10"], request_if_missing=True, must_be_present=False, destination=None, import_details=None, comment="Re-request will be performed if service start date is lacking at BOTH the overall claim level AND for any line items included in a medical claim."),
            DataDefinition(data_key="serviceEndDate", data_type="string", required=False, description=None, examples=["2025-01-14"], request_if_missing=False, must_be_present=False, destination=None, import_details=None, comment=None),
            DataDefinition(data_key="adjudicationDecision", data_type="string", required=False, description=None, examples=["denied"], request_if_missing=True, must_be_present=False, destination=None, import_details=None, comment="Re-request will be performed if adjudication decision is not included at EITHER the overall claim or all line-item levels for a medical claim, unless payor is among those that only send us approved claims (Ops is compiling that list as of 8/2025)."),
            DataDefinition(data_key="page_and_line_number_reference", data_type="string", required=False, description=None, examples=["pages 2-4"], request_if_missing=None, must_be_present=None, destination=None, import_details=None, comment=None)
        ],
        subgroups=[
            DataGroupDefinition(group_name="auditLog",
        subgroups=[
            DataGroupReference(ref="abstractorSchema")
        ]),
            DataGroupDefinition(group_name="facility",
        subgroups=[
            DataGroupReference(ref="providerSchema")
        ]),
            DataGroupDefinition(group_name="providers",
        subgroups=[
            DataGroupReference(ref="providerSchema")
        ]),
            DataGroupDefinition(group_name="amounts",
        subgroups=[
            DataGroupReference(ref="amountsSchema")
        ]),
            DataGroupDefinition(group_name="diagnosisCodes",
        subgroups=[
            DataGroupReference(ref="diagnosisCodesSchema")
        ]),
            DataGroupDefinition(group_name="lineItems",
        subgroups=[
            DataGroupReference(ref="medicalClaimLineItemSchema")
        ]),
            DataGroupDefinition(group_name="notes",
        subgroups=[
            DataGroupReference(ref="ClaimNoteItemSchema")
        ])
        ]
)

pharmacy_claim_schema = DataGroupDefinition(
        group_name="pharmacyClaimSchema",
        data_definitions=[
            DataDefinition(data_key="claimId", data_type="string", required=False, description=None, examples=["ABC23456"], request_if_missing=True, must_be_present=False, destination=None, import_details=None, comment="Re-request will be performed if NEITHER claimId nor Rx number is provided for a pharmacy claim."),
            DataDefinition(data_key="adjudicationDecision", data_type="string", required=False, description=None, examples=["approved"], request_if_missing=True, must_be_present=False, destination=None, import_details=None, comment="Re-request will be performed if adjudication decision is not included, unless payor is among those that only send us approved claims (Ops is compiling that list as of 8/2025)."),
            DataDefinition(data_key="prescribingProviderName", data_type="string", required=False, description=None, examples=["Jones, Anthony"], request_if_missing=False, must_be_present=False, destination=None, import_details=None, comment=None),
            DataDefinition(data_key="prescribingProviderNPI", data_type="string", required=False, description=None, examples=["12345678"], request_if_missing=True, must_be_present=False, destination=None, import_details=None, comment=None),
            DataDefinition(data_key="fillLocationName", data_type="string", required=False, description=None, examples=["Uptown Cheyenne CVS #43"], request_if_missing=False, must_be_present=False, destination=None, import_details=None, comment=None),
            DataDefinition(data_key="fillLocationNPI", data_type="string", required=False, description=None, examples=["23456789"], request_if_missing=False, must_be_present=False, destination=None, import_details=None, comment=None),
            DataDefinition(data_key="fillDate", data_type="string", required=True, description=None, examples=["2025-02-20"], request_if_missing=True, must_be_present=True, destination=None, import_details=None, comment="A pharmacy claim will be ingested only if a fill date is provided, otherwise an error will be triggered.  Other claims within an abstraction file may still be ingested."),
            DataDefinition(data_key="nationalDrugCode", data_type="string", required=True, description=None, examples=["143988601"], request_if_missing=True, must_be_present=None, destination=None, import_details=None, comment="Abstraction will be performed only if EITHER NDC or label name is provided for a given pharmacy claim.."),
            DataDefinition(data_key="labelName", data_type="string", required=False, description=None, examples=["amoxicillin 200mg/5mL"], request_if_missing=False, must_be_present=None, destination=None, import_details=None, comment="Abstraction will be performed only if EITHER NDC or label name is provided for a given pharmacy claim.."),
            DataDefinition(data_key="daysSupply", data_type="integer", required=False, description=None, examples=["7"], request_if_missing=True, must_be_present=False, destination=None, import_details=None, comment=None),
            DataDefinition(data_key="quantityValue", data_type="number", required=False, description=None, examples=["210"], request_if_missing=True, must_be_present=False, destination=None, import_details=None, comment=None),
            DataDefinition(data_key="quantityUnits", data_type="number", required=False, description=None, examples=["mL"], request_if_missing=False, must_be_present=False, destination=None, import_details=None, comment=None),
            DataDefinition(data_key="rxNumber", data_type="string", required=False, description=None, examples=["CDE345678"], request_if_missing=True, must_be_present=False, destination=None, import_details=None, comment="Re-request will be performed if NEITHER claimId nor Rx number is provided for a pharmacy claim."),
            DataDefinition(data_key="pageAndLineNumberReference", data_type="string", required=False, description=None, examples=["page 5 line 2"], request_if_missing=None, must_be_present=None, destination=None, import_details=None, comment=None)
        ],
        subgroups=[
            DataGroupDefinition(group_name="amounts",
        subgroups=[
            DataGroupReference(ref="amountsSchema")
        ]),
            DataGroupDefinition(group_name="notes",
        subgroups=[
            DataGroupReference(ref="ClaimNoteItemSchema")
        ]),
            DataGroupDefinition(group_name="auditLog",
        subgroups=[
            DataGroupReference(ref="abstractorSchema")
        ])
        ]
)

provider_schema = DataGroupDefinition(
        group_name="providerSchema",
        data_definitions=[
            DataDefinition(data_key="name", data_type="string", required=False, description=None, examples=["Brown, Samantha"], request_if_missing=True, must_be_present=False, destination=None, import_details=None, comment="For any provider recorded, re-request will be performed if NEITHER provider name nor provider NPI is provided."),
            DataDefinition(data_key="npi", data_type="string", required=False, description=None, examples=["34567890"], request_if_missing=True, must_be_present=False, destination=None, import_details=None, comment="For any provider recorded, re-request will be performed if NEITHER provider name nor provider NPI is provided."),
            DataDefinition(data_key="providerType", data_type="enum", required=False, description=None, examples=["billing"], request_if_missing=False, must_be_present=False, destination=None, import_details=None, comment=None)
        ]
)

# ----- END GENERATED COMPONENT DEFINITIONS -----

# Mapping of component ref names to hard-coded DataGroupDefinition objects
GENERATED_COMPONENTS: dict[str, DataGroupDefinition] = {
    "abstractorSchema": abstractor_schema,
    "amountsSchema": amounts_schema,
    "ClaimNoteItemSchema": claim_note_item_schema,
    "diagnosisCodesSchema": diagnosis_codes_schema,
    "medicalClaimLineItemSchema": medical_claim_line_item_schema,
    "medicalClaimSchema": medical_claim_schema,
    "pharmacyClaimSchema": pharmacy_claim_schema,
    "providerSchema": provider_schema,
}


if __name__ == "__main__":
    # Helper functions to build schema from CSV ------------------------------
    def camel_to_snake(name: str) -> str:
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        s2 = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1)
        return s2.replace("__", "_").lower()

    def level_to_var(level_name: str) -> str:
        # Strip trailing "Schema" (case-insensitive), convert to snake_case, ensure suffix _schema
        base = re.sub(r"schema$", "", level_name, flags=re.IGNORECASE)
        snake = camel_to_snake(base)
        if not snake.endswith("_schema"):
            snake = f"{snake}_schema"
        return snake
    def _to_bool(val: Optional[str]) -> Optional[bool]:
        if val is None:
            return None
        s = str(val).strip().lower()
        if s in ("y", "yes", "true"):
            return True
        if s in ("n", "no", "false"):
            return False
        if s in ("n/a", ""):
            return None
        if s.startswith("y ("):
            return True
        if s.startswith("n ("):
            return False
        return None

    ref_pattern = re.compile(r"^(?:array of\s+)?([A-Za-z0-9_]+Schema)", re.IGNORECASE)

    def parse_examples(val: Optional[str]) -> Optional[list[Any]]:
        if val is None:
            return None
        s = str(val).strip()
        if not s or s.lower() == "(see comment)":
            return None
        # Try to parse JSON array if it looks like one, else return as single example string
        if s.startswith("[") and s.endswith("]"):
            try:
                parsed = json.loads(s)
                return parsed if isinstance(parsed, list) else [parsed]
            except Exception:
                return [s]
        return [s]

    def build_from_csv(csv_path: str) -> tuple[SchemaDefinition, dict[str, DataGroupDefinition]]:
        rows: list[dict[str, str]] = []
        with open(csv_path, newline="") as f:
            reader = csv.DictReader(f)
            for r in reader:
                rows.append(r)

        # Group rows by level
        by_level: dict[str, list[dict[str, str]]] = {}
        for r in rows:
            level = (r.get("level") or "").strip()
            if not level:
                continue
            by_level.setdefault(level, []).append(r)

        # Build components for every non-root level
        components: dict[str, DataGroupDefinition] = {}

        def make_group(level_name: str, level_rows: list[dict[str, str]]) -> DataGroupDefinition:
            group_defs: list[DataDefinition] = []
            subgroups: list[Union[DataGroupDefinition, DataGroupReference]] = []

            for r in level_rows:
                key = (r.get("key") or "").strip()
                if not key:
                    continue
                dtype = (r.get("data_type") or "").strip()
                comment = (r.get("comment") or "").strip() or None
                examples = parse_examples(r.get("examples"))
                req_ing = _to_bool(r.get("required_for_ingestion"))
                req_abs = _to_bool(r.get("required_for_abstraction"))
                re_req = _to_bool(r.get("re-request_if_missing") or r.get("re-request_if_missing"))

                # Detect references to other schemas
                m = ref_pattern.match(dtype)
                if m:
                    ref_schema = m.group(1)  # e.g. amountsSchema
                    # Wrap reference so we preserve the field name as a subgroup with its own name
                    subgroups.append(
                        DataGroupDefinition(
                            group_name=key,
                            subgroups=[DataGroupReference(ref=ref_schema)],
                        )
                    )
                    continue

                # Plain definition
                group_defs.append(
                    DataDefinition(
                        data_key=key,
                        data_type=dtype or None,
                        required=req_ing,
                        description=None,  # No separate description column; keeping None
                        examples=examples,
                        request_if_missing=re_req,
                        must_be_present=req_abs,
                        comment=comment,
                    )
                )

            return DataGroupDefinition(
                group_name=level_name,
                data_definitions=group_defs or None,
                subgroups=subgroups or None,
            )

        for level, level_rows in by_level.items():
            if level == "root":
                continue
            components[level] = make_group(level, level_rows)

        # Root group
        root_rows = by_level.get("root", [])
        root_group = make_group("root", root_rows)

        schema = SchemaDefinition(
            name="Claims Abstraction (Generated)",
            version="claims_abstraction_generated_0001",
            description="Schema generated from abstraction_schema_required_fields.csv",
            vendor_instructions=None,
            groups=[root_group],
        )
        return schema, components

    def generate_component_vars_from_csv(csv_path: str) -> dict[str, DataGroupDefinition]:
        """Create globals like `amounts_schema` for each non-root level in the CSV.
        Returns a dict of var_name -> DataGroupDefinition.
        """
        _, comps = build_from_csv(csv_path)
        created: dict[str, DataGroupDefinition] = {}
        for comp_key, comp_val in comps.items():
            var_name = level_to_var(comp_key)
            globals()[var_name] = comp_val
            created[var_name] = comp_val
        return created

    # Build from CSV in this workspace and print vendor JSON -----------------
    csv_path = str(Path(__file__).with_name("abstraction_schema_required_fields.csv"))
    if Path(csv_path).exists():
        generated_schema, generated_components = build_from_csv(csv_path)
        created_vars = generate_component_vars_from_csv(csv_path)

        # Optional: emit Python code for components for hard-coding
        if os.environ.get("EMIT_COMPONENT_CODE") == "1":
            def q(s: Optional[str]) -> str:
                return "None" if s is None else json.dumps(s)

            def ser_examples(ex: Optional[list[Any]]) -> str:
                if not ex:
                    return "None"
                return json.dumps(ex)

            def ser_datadef(dd: DataDefinition) -> str:
                parts = [
                    f"data_key={q(dd.data_key)}",
                    f"data_type={q(dd.data_type)}",
                    f"required={"None" if dd.required is None else ("True" if dd.required else "False")}",
                    f"description={q(dd.description)}",
                    f"examples={ser_examples(dd.examples)}",
                    f"request_if_missing={"None" if dd.request_if_missing is None else ("True" if dd.request_if_missing else "False")}",
                    f"must_be_present={"None" if dd.must_be_present is None else ("True" if dd.must_be_present else "False")}",
                    f"destination={q(dd.destination)}",
                    f"import_details={q(dd.import_details)}",
                    f"comment={q(dd.comment)}",
                ]
                return "DataDefinition(" + ", ".join(parts) + ")"

            def ser_group_inline(g: DataGroupDefinition | DataGroupReference) -> str:
                if isinstance(g, DataGroupReference):
                    return f"DataGroupReference(ref=\"{g.ref}\")"
                body: list[str] = [f"group_name={q(g.group_name)}"]
                if g.description is not None:
                    body.append(f"description={q(g.description)}")
                if g.data_definitions is not None:
                    dd_list = ",\n            ".join(ser_datadef(dd) for dd in g.data_definitions)
                    body.append(f"data_definitions=[\n            {dd_list}\n        ]")
                if g.subgroups is not None:
                    sub_list = ",\n            ".join(ser_group_inline(sg) for sg in g.subgroups)
                    body.append(f"subgroups=[\n            {sub_list}\n        ]")
                return "DataGroupDefinition(" + ",\n        ".join(body) + ")"

            print("# ----- BEGIN GENERATED COMPONENT DEFINITIONS -----")
            for comp_key in sorted(generated_components.keys()):
                comp = generated_components[comp_key]
                var_name = level_to_var(comp_key)
                print(f"{var_name} = DataGroupDefinition(\n        " + ",\n        ".join([
                    f"group_name=\"{comp.group_name}\""
                ] + ([f"description={q(comp.description)}"] if comp.description is not None else []) +
                ([f"data_definitions=[\n            {',\n            '.join(ser_datadef(dd) for dd in comp.data_definitions)}\n        ]"] if comp.data_definitions else []) +
                ([f"subgroups=[\n            {',\n            '.join(ser_group_inline(g) for g in comp.subgroups)}\n        ]"] if comp.subgroups else [])
                ) + "\n)\n")
            print("# ----- END GENERATED COMPONENT DEFINITIONS -----")
        else:
            # Build components dict keyed by ref names (unchanged)
            vendor_json = to_vendor_json(generated_schema, components=generated_components)
            print(json.dumps(vendor_json, indent=4))

            # Brief summary of created variables
            print("\n# Created component variables:")
            for vn in sorted(created_vars.keys()):
                print(f"- {vn}")
    else:
        # Fallback to example if CSV not found
        vendor_json = to_vendor_json(example_schema, components=components)
        print(json.dumps(vendor_json, indent=4))
