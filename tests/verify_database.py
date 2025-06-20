import os

def parse_osi_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        design_dict = {}
        current_key = None
        list_values = []
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith('<DOCUMENT') or line.startswith('</DOCUMENT'):
                continue
            if line.startswith('-'):
                value = line.lstrip('- ').strip("'")
                if current_key:
                    list_values.append(value)
            else:
                if current_key and list_values:
                    if current_key == "Bolt.Diameter":
                        design_dict["KEY_D"] = list_values[0] if list_values else ""
                    elif current_key == "Bolt.Grade":
                        design_dict["KEY_GRD"] = list_values[0] if list_values else ""
                    elif current_key == "Connector.Plate.Thickness_List":
                        design_dict["KEY_PLATETHK"] = list_values[0] if list_values else ""
                    list_values = []
                if ':' in line:
                    key, value = [part.strip() for part in line.split(':', 1)]
                    current_key = key
                    if value:
                        key_map = {
                            "Connectivity *": "KEY_CONN",
                            "Member.Supporting_Section.Designation": "KEY_SUPTNGSEC",
                            "Member.Supported_Section.Designation": "KEY_SUPTDSEC",
                            "Member.Supporting_Section.Material": "KEY_SUPTNGSEC_MATERIAL",
                            "Member.Supported_Section.Material": "KEY_SUPTDSEC_MATERIAL",
                            "Load.Shear": "KEY_SHEAR",
                            "Load.Axial": "KEY_AXIAL",
                            "Bolt.Type": "KEY_TYP",
                            "Bolt.Bolt_Hole_Type": "KEY_DP_BOLT_HOLE_TYPE",
                            "Bolt.TensionType": "KEY_DP_BOLT_TYPE",
                            "Detailing.Bolt_Slip_Factor": "KEY_DP_BOLT_SLIP_FACTOR",
                            "Detailing.Edge_type": "KEY_DP_DETAILING_EDGE_TYPE",
                            "Detailing.Corrosive_Influences": "KEY_DP_DETAILING_CORROSIVE_INFLUENCES",
                            "Detailing.Gap": "KEY_DP_DETAILING_GAP",
                            "Design.Method": "KEY_DP_DESIGN_METHOD",
                            "Module": "KEY_MODULE",
                            "Connector.Material": "KEY_CONNECTOR_MATERIAL",
                            "Weld.Fab": "KEY_DP_WELD_FAB",
                            "Weld.Material_Grade_OverWrite": "KEY_DP_WELD_MATERIAL_G_O",
                        }
                        mapped_key = key_map.get(key, key)
                        design_dict[mapped_key] = value.strip("'")
                    else:
                        list_values = []
        
        if current_key and list_values:
            if current_key == "Bolt.Diameter":
                design_dict["KEY_D"] = list_values[0] if list_values else ""
            elif current_key == "Bolt.Grade":
                design_dict["KEY_GRD"] = list_values[0] if list_values else ""
            elif current_key == "Connector.Plate.Thickness_List":
                design_dict["KEY_PLATETHK"] = list_values[0] if list_values else ""
        
        return design_dict

osi_dir = r"C:\Visual Studio Code\FOSSEE OSDAG\Osdag\tests\fin_osi_files"
osi_files = ["FinPlateTest1.osi", "FinPlateTest2.osi", "FinPlateTest3.osi", "FinPlateTest4.osi"]

for osi_file in osi_files:
    print(f"\n{osi_file}:")
    file_path = os.path.join(osi_dir, osi_file)
    try:
        design_dict = parse_osi_file(file_path)
        for key, value in sorted(design_dict.items()):
            print(f"  {key}: {value}")
    except Exception as e:
        print(f"  Error: {e}")