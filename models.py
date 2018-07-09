"""
All data sets are from https://zfin.org/downloads
on 6 July 2018

Expression headers
1. Gene ID 	2. Gene Symbol 	3. Fish Name 	4. Super Structure ID
5. Super Structure Name 	6. Sub Structure ID  	7. Sub Structure Name
8. Start Stage 	9. End Stage 	10. Assay 	11. Publication ID 	12. Probe ID
13. Antibody ID 	14. Fish ID

Ontology headers
1.Stage ID	2.Stage OBO ID	3.Stage Name	4.Begin Hours	5.End Hours

Anatomy Relationship
1.Parent Item ID	2.Child Item ID	3.Relationship Type ID

Anatomy items
1.Anatomy ID	2.Anatomy Name	3.Start Stage ID	4.End Stage ID

We added "ZFA:0100000	zebrafish anatomical entity	None	None" line to
anatomy database file to include missing entries
"""

all_dev_stages = {}
relations = {}
anatomy_items = {}


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


class DevStage:
    def __init__(self, data):
        self.data = data
        data_split = data.split("\t")
        self.stage_id = data_split[0]
        self.stage_obo = data_split[1]
        self.stage_name = data_split[2]
        self.stage_begin = data_split[3]
        self.stage_end = data_split[4]
        self.time = data_split[3]
        self.index = data_split[1]

    def __str__(self):
        return self.stage_name


with open("database\\anatomy_item_2018.07.06.txt") as f:
    for line in f:
        if len(line.split("\t")) > 0:
            a = AnatomyItem(line)
            anatomy_items[a.id] = a

with open("database\\anatomy_relationship_2018.07.06.txt") as f:
    for line in f:
        if len(line.split("\t")) > 0:
            r = AnatomyRelation(line.strip())
            relations[r.child] = r

with open("database\stage_ontology_2018.07.06.txt") as f:
    for line in f:
        if len(line.split("\t")) > 0:
            d = DevStage(line.strip())
            all_dev_stages[d.stage_name] = d


class DataObject:
    def __init__(self, data):
        self.data = data
        dp = data.split("\t")
        self.gene_id = dp[0]
        self.gene_symbol = dp[1]
        self.fish_name = dp[2]
        self.super_structure = anatomy_items[dp[3]]
        self.parent_structure = anatomy_items[relations[dp[3]].parent]
        self.sub_structure_id = dp[5]
        self.sub_structure_name = dp[6]
        self.start_stage = all_dev_stages[dp[7]]
        self.end_stage = all_dev_stages[dp[8]]
        self.assay = dp[9]
        self.publication = dp[10]
        self.probe = dp[11]
        self.antibody = dp[12]
        self.fish_id = dp[13]


def get_parent_structure(structure):
    dd = {}
    for key in anatomy_items:
        dd[anatomy_items[key].name] = anatomy_items[key]
    return anatomy_items[relations[dd[structure].id].parent]
