"""
Rohit Suratekar
March 2018

Model based on ZFIN download file (March 2019)
Please check headers before using new files as ZFIN can add/remove columns
in future

"""


class DevelopmentalStage:
    def __init__(self, data: list):
        self.raw = data
        self.stage_id = data[0]
        self.stage_obo = data[1]
        self.stage_name = data[2]
        self.stage_begin = data[3]
        self.stage_end = data[4]
        self.time = data[3]
        self.index = data[1]

    def __str__(self):
        return self.stage_name


class AnatomyItem:
    def __init__(self, data):
        self.data = data
        data_split = data.split("\t")
        self.id = data_split[0].strip()
        self.name = data_split[1].strip()
        self.start_stage = data_split[2].strip()
        self.end_stage = data_split[3].strip()


class AnatomyRelation:
    def __init__(self, data):
        self.data = data
        data_split = data.split("\t")
        self.parent = data_split[0].strip()
        self.child = data_split[1].strip()
        self.relation = data_split[2].strip()


class ExpressionEntry:
    def __init__(self, data: list, stages: dict, anatomy: dict, relations: dict):
        self.raw = data
        self.gene_id = data[0]
        self.gene_symbol = data[1]
        self.fish_name = data[2]
        self.super_structure_id = data[3]
        self.super_structure_name = data[4]
        self.super_structure = anatomy[data[3]]
        self.parent_structure = anatomy[relations[data[3]].parent]
        self.sub_structure_id = data[5]
        self.sub_structure_name = data[6]
        self.start_stage = stages[data[7]]
        self.end_stage = stages[data[8]]
        self.assay = data[9]
        self.assay_mmo_id = data[10]
        self.publication_id = data[11]
        self.probe_id = data[12]
        self.antibody_id = data[13]
        self.fish_id = data[1]

    def is_there(self, value: str) -> bool:
        for d in self.raw:
            if value.strip().lower() in str(d).lower().strip():
                return True
        return False
