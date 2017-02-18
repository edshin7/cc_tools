import cc_data
import cc_dat_utils
import json


# default string value of json file to read
default_json_file = "data/edwardsh_cc1.json"

# opens input_json_file to read out data
json_data = open(default_json_file).read()

# loads json file to decode
json_file = json.loads(json_data)

# strong name of new dat file
dat_output_name = "data/edwardsh_cc1.dat"


# makes dat file from json file
def make_dat_from_json(json_file, dat_output_name):
    # cc_file made from a given json file
    cc_file = make_cc_from_json(json_file)
    
    return cc_dat_utils.write_cc_data_to_dat(cc_file, dat_output_name)


# makes a cc_data file from given json file
def make_cc_from_json(json_file):
    data = cc_data.CCDataFile()

    for level in json_file["levels"]:
        new_level = cc_data.CCLevel()

        new_level.level_number = level["level number"]
        new_level.time = level["time"]
        new_level.num_chips = level["chip number"]
        new_level.upper_layer = level["upper layer"]
        new_level.lower_layer = level["lower layer"]

        fields = make_field_from_optional(level["optional fields"])

        for field in fields:
            new_level.add_field(field)

        data.add_level(new_level)


    return data


# makes a list of fields from a a json file's optional fields list
def make_field_from_optional(optional_fields):
    fields = []

    for field in optional_fields:
        new_field = None

        # title field
        if(field["field type"] == 3):
            new_field = cc_data.CCMapTitleField(field["title"])

        # traps field
        elif(field["field type"] == 4):
            traps = []
            locations = field["traps"]
            for location in locations:
                bx = location["bx"]
                by = location["by"]
                tx = location["tx"]
                ty = location["ty"]
                control = cc_data.CCTrapControl(bx, by, tx, ty)
                traps.append(control)

            new_field = cc_data.CCTrapControlsField(traps)

        # cloning machine field
        elif(field["field type"] == 5):
            machines = []
            locations = field["cloning machines"]
            for location in locations:
                bx = location["bx"]
                by = location["by"]
                tx = location["tx"]
                ty = location["ty"]
                control = cc_data.CCCloningMachineControl(bx, by, tx, ty)
                machines.append(control)

            new_field = cc_data.CCCloningMachineControlsField(machines)

        # encoded password field
        elif(field["field type"] == 6):
            new_field = cc_data.CCEncodedPasswordField(field["password"])

        # hint field
        elif(field["field type"] == 7):
            new_field = cc_data.CCMapHintField(field["hint"])

        # monsters / moving objects field
        elif(field["field type"] == 10):
            monsters = []
            locations = field["monsters"]

            for location in locations:
                x = location["x"]
                y = location["y"]
                coordinate = cc_data.CCCoordinate(x, y)
                monsters.append(coordinate)

            new_field = cc_data.CCMonsterMovementField(monsters)

        fields.append(new_field)

    return fields


# print(make_cc_from_json(json_file))


# dat_output = make_dat_from_json(json_file, dat_output_name)









