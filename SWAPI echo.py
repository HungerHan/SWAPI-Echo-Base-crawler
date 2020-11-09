import json, requests

ENDPOINT = 'https://swapi.co/api'

PEOPLE_KEYS = ("url","name","height","mass","hair_color","skin_color","eye_color", "birth_year","gender","homeworld","species")
HOTH_KEYS = ("url","name","system_position","natural_satellites","rotation_period","orbital_period","diameter","climate","gravity","terrain","surface_water","population","indigenous_life_forms")
PLANET_KEYS = ("url","name","rotation_period","orbital_period","diameter","climate","gravity","terrain","surface_water","population")
STARSHIP_KEYS = ("url","starship_class","name","model","manufacturer","length","width","max_atmosphering_speed","hyperdrive_rating","MGLT","crew","passengers","cargo_capacity","consumables","armament")
SPECIES_KEYS = ("url","name","classification","designation","average_height","skin_colors","hair_colors", "eye_colors","average_lifespan","language")
VEHICLE_KEYS =  ("url","vehicle_class","name","model","manufacturer","length","max_atmosphering_speed","crew", "passengers","cargo_capacity","consumables","armament")

INPUTPLANET = 'swapi_planets-v1p0.json'
OUTPUTPLANET = 'swapi_planets_uninhabited-v1p1.json'

INPUTECHO = 'swapi_echo_base-v1p0.json'
OUTPUTECHO = 'swapi_echo_base-v1p1.json'

float_props = ('gravity', 'length', 'hyperdrive_rating', )
int_props = ('rotation_period', 'orbital_period', 'diameter', 'surface_water', 'population', 'height', 'mass', 'average_height', 'average_lifespan', 'max_atmosphering_speed', 'MGLT', 'crew', 'passengers', 'cargo_capacity') 
list_props = ('hair_color', 'skin_color','climate', 'terrain','skin_colors','hair_colors','eye_colors',)
dict_props = ('homeworld', 'species')

def read_json(filepath):
    """Given a valid filepath reads a JSON document and returns a dictionary.

    Parameters:
        filepath (str): path to file.
 
    Returns: 
        readjson_dict: dictionary representations of the decoded JSON document. 
    """
    with open(filepath, 'r', encoding='utf8') as read_obj:
        readjson_dict = json.load(read_obj)
        # print(f"type!!!{type(readjson_dict)}")
    return readjson_dict


def get_swapi_resource(url, params=None):
    """This function initiates an HTTP GET request to the SWAPI service 
    in order to return a representation of a resource. 

    Parameters:
        url (str) 
        params (dict)  # value pairs provided as search terms (e.g., {'search': 'yoda'} )
 
    Returns: 
        response: data fatched from the url + params
    """
    response=requests.get(url, params=params).json()
    return response

""" TEST
test=get_swapi_resource('https://swapi.co/api/planets/', 
            {'search': 'hoth'})['results'][0]['climate']
print(f"test={test}")
"""


def combine_data(default_data, override_data):
    """ This function creates a shallow copy of the default dictionary and 
        then updates the copy with key-value pairs from the 'override' dictionary. 
    Parameters:
        default_data (dict) 
        override_data (dict)
    Returns:
        combine_dict: a dictionary that combines the key-value pairs of both 
            the default dictionary and the override dictionary, 
            with override values replacing default values on matching keys.
    """
    #default_data.update(override_data)
    #return default_data
    combined_data = default_data.copy()  # shallow
    combined_data.update(override_data)  # in place

    return combined_data

"""TEST
dict1 = {'bookA': 1, 'bookB': 2, 'bookC': 3}
dict2 = {'bookC': 2, 'bookD': 4, 'bookE': 5}
test=combine_data(dict1, dict2)
print(test)
"""


def filter_data(data, filter_keys):
    """ This function applies a key name filter to a dictionary 
        in order to return an ordered subset of key-values. 
    Parameters:
        data (dict) 
        filter_keys (tuple)
    Returns:
        filter_dict: a filtered collection of key-value pairs to the caller. 
    """
    """
    filter_dict={}
    for key in filter_keys:
        if key in data.keys():
            filter_dict[key] = data[key]
        #else:
         #   filter_dict[key] = None
        
    return filter_dict
    """
    #print("In filter~~~")
    return {key: data[key] for key in filter_keys if key in data.keys()}

dict1 = {'bookA': 1, 'bookB': 2, 'bookC': 3, 'bookD': 6}
dict2 = ('bookE', 'bookC', 'bookA', 'bookD')
#test12=filter_data(dict1, dict2)
#print(test12)


def is_unknown(value):
    """ This function applies a case-insensitive truth value 
        test for string values that equal unknown or n/a .
    Parameters:
        value (str)
    Returns:
        True if a match is obtained
    """
    value=value.strip().lower()
    if value == "unknown" or value == "n/a":
        #print(f"{value}TRUE")
        return True
    else:
        #print(f"{value}FALSE")
        return False

def convert_string_to_float(value):
    """This function attempts to convert a string to a floating point value. 
    Parameters:
        value (str)
    Returns:
        value: If unsuccessful the function returns the value unchanged. 
    """
    value=value.split(' ')
    for val in value:
        try:     
            return float(val) 
        except ValueError:     
            return val 


def convert_string_to_int(value):
    """ This function attempts to convert a string to a floating point int. 
    Parameters:
        value (str)
    Returns:
        value: If unsuccessful the function returns the value unchanged. 
    """
    value=value.split(' ')
    for val in value:
        try:     
            return int(val) 
        except ValueError:     
            return val 


def convert_string_to_list(value, delimiter=','):
    """ This function converts a string of delimited text values to a list. 
        The function will split the passed in string using the provided delimiter 
        and return the resulting list to the caller. 
    Parameters:
        value (str) 
        delimiter (str)
    Returns:
        str2list: return the resulting list to the caller. 
    """
    str2list=[]
    value=value.split(delimiter)
    for val in value:
        if ' ' in val:
            val = val.strip(' ')
            str2list.append(val)
        else:
            str2list.append(val)
    return str2list


def clean_data(entity):
    """ This function converts dictionary string values to more appropriate types 
        such as float , int , list , or, in certain cases, None . 
    Parameters:
        entity (dict)
    Returns:
        clean_dict: a dictionary with 'cleaned' values to the caller
    """
    
    
    #print(entity)
    """
    if 'gender' in entity.keys():
        print("PEOPLE_KEYS")
        entity=filter_data(entity, PEOPLE_KEYS)
    elif 'surface_water' in entity.keys():
        print("PLANET_KEYS")
        entity=filter_data(entity, PLANET_KEYS)
    elif 'starship_class' in entity.keys():
        print("STARSHIP_KEYS")
        entity=filter_data(entity, STARSHIP_KEYS)
    elif 'classification' in entity.keys():
        entity=filter_data(entity, SPECIES_KEYS)
    elif 'vehicle_class' in entity.keys():
        entity=filter_data(entity, VEHICLE_KEYS)
    else:
        print("ELSE")
    """
    clean_dict={}
    if 'gender' in entity:
        #print("PEOPLE_KEYS")
        entity=filter_data(entity, PEOPLE_KEYS)
    elif 'surface_water' in entity:
        #print("PLANET_KEYS")
        entity=filter_data(entity, HOTH_KEYS)
    elif 'starship_class' in entity:
        #print("STARSHIP_KEYS")
        entity=filter_data(entity, STARSHIP_KEYS)
    elif 'classification' in entity:
        entity=filter_data(entity, SPECIES_KEYS)
    elif 'vehicle_class' in entity:
        entity=filter_data(entity, VEHICLE_KEYS)
    else:
        #print("ELSE")
        1 == 1


    for key, value in entity.items():
        #print(f"key: {key} -- value: {value}-- {type(value)}")
        if type(value) == str:
            if is_unknown(value):
                #print("NA")
                clean_dict[key] = None
            elif key in int_props:
                #print("INT")
                clean_dict[key] = convert_string_to_int(value)
            elif key in float_props:
                #print("FLOAT")
                if key == 'gravity':
                    value = value.rstrip()
                clean_dict[key] = convert_string_to_float(value)
            elif key in list_props:
                #print("LIST")
                clean_dict[key] = convert_string_to_list(value)
            
            elif key in dict_props:
                #print("DICT")
                if key == 'homeworld':
                    home_dict = get_swapi_resource(value)
                    home_dict = filter_data(home_dict, PLANET_KEYS)
                    clean_dict[key] = clean_data(home_dict)
                """
                elif key == 'species':
                    spec_dict = get_swapi_resource(value[0])
                    spec_dict = filter_data(spec_dict, SPECIES_KEYS)
                    clean_dict[key] = clean_data(spec_dict)
                """
            else:
                #print("str")
                clean_dict[key] = value
            
        else:
            #print("ELSE")
            if key == 'species':
                #print("SPECIES!!!")
                spec_dict = get_swapi_resource(value[0])
                spec_dict = filter_data(spec_dict, SPECIES_KEYS)
                #spec_dict=list(spec_dict)
                """
                dictlist=[]
                for key, value in spec_dict.items():
                    temp = [key,value]
                    dictlist.append(temp)
                """
                spec_dict=clean_data(spec_dict)
                spec_list=[]
                spec_list.append(spec_dict)
                #print(f"SPECIES DICT:{spec_dict}")
                #print(f"type {type(spec_dict)}")
                #print(f"combine data{combine_data(clean_dict, spec_dict)}")
                clean_dict['species']=spec_list
                #clean_dict[key] = clean_data(spec_dict)
                #clean_dict[key] = None
            
            else:
                clean_dict[key] = value
            """
            if key == 'homeworld':
                print("HOMEWORLD!!!")
                home_dict = get_swapi_resource(value)
                home_dict = filter_data(home_dict, PLANET_KEYS)
                clean_dict[key] = clean_data(home_dict)
            elif key == 'species':
                spec_dict = get_swapi_resource(value[0])
                spec_dict = filter_data(spec_dict, SPECIES_KEYS)
                clean_dict[key] = clean_data(spec_dict)
            """
    return clean_dict
ddd={
      "name": "Hoth",
      "system_position": 6,
      "natural_satellites": 3,
      "rotation_period": 23,
      "orbital_period": 549,
      "diameter": 7200,
      "climate": [
        "frozen"
      ],
      "gravity": 1.1,
      "terrain": [
        "tundra",
        "ice caves",
        "mountain ranges"
      ],
      "surface_water": 100,
      "population": None,
      "indigenous_life_forms": [
        "Tauntaun",
        "Wampa"
      ],
      "url": "https://swapi.co/api/planets/4/"
}
ccc={
      "name": "Leia Organa", 
            "height": "150", 
            "mass": "49", 
            "hair_color": "brown", 
            "skin_color": "light", 
            "eye_color": "brown", 
            "birth_year": "19BBY", 
            "gender": "female", 
            "homeworld": "https://swapi.co/api/planets/2/", 
            "films": [
                "https://swapi.co/api/films/2/", 
                "https://swapi.co/api/films/6/", 
                "https://swapi.co/api/films/3/", 
                "https://swapi.co/api/films/1/", 
                "https://swapi.co/api/films/7/"
            ], 
            "species": [
                "https://swapi.co/api/species/1/"
            ], 
            "vehicles": [
                "https://swapi.co/api/vehicles/30/"
            ], 
            "starships": [], 
            "created": "2014-12-10T15:20:09.791000Z", 
            "edited": "2014-12-20T21:17:50.315000Z", 
            "url": "https://swapi.co/api/people/5/"
}
#test=clean_data(ccc)
#print(f"clean_dict {test}")


def assign_crew(starship, crew):
    """ This function assigns crew members to a starship. 
        Each crew key defines a role (e.g., pilot , copilot , astromech_droid ) 
        that must be used as the new starship key (e.g., starship['pilot'] ). 
        The crew value (dict) represents the crew member 
        (e.g., Han Solo, Chewbacca). 
    Parameters:
        starship (dict) 
        crew (dict)
    Returns:
        starship: an updated starship with one or 
        more new crew member key-value pairs added to the caller. 
    """
   
    return combine_data(starship, crew)



def write_json(filepath, data):
    """ capable of writing SWAPI data to a target JSON document file. 
    Parameters:
        filepath (str) 
        data
    Returns:
        None
    """
    with open(filepath, 'w', encoding='utf8') as writeobj:
        json.dump(data, writeobj)



def main():
    """"Entry point. This program will interact with local file assets and the     
    API to create two data files required by Rebel Alliance Intelligence.

    Parameters:        
        None

    Returns:        
        None 
    """
    
    plante_list={}
    plante_list=read_json(INPUTPLANET)

    uninhabited_list=[] # hold uninhabited planet data
    new_dict={}
    for plante in plante_list:
        if is_unknown(plante['population']) == True:
            #print(plante["population"])
            new_dict=filter_data(plante, PLANET_KEYS)
            new_dict=clean_data(new_dict)
            uninhabited_list.append(new_dict)
        
    write_json(OUTPUTPLANET, uninhabited_list)
    
# swapi_echo_base-v1p1.json
    echo_base = read_json(INPUTECHO)

    swapi_hoth = get_swapi_resource('https://swapi.co/api/planets/',{'search':'hoth'})['results'][0]
    echo_base_hoth = echo_base["location"]["planet"]
    hoth = combine_data(echo_base_hoth, swapi_hoth)
    filter_hoth = filter_data(hoth, HOTH_KEYS)
    clean_hoth = clean_data(filter_hoth)
    echo_base['location']['planet'] = clean_hoth

    # 6.4.2 Garrison commander
    echo_base_commander = echo_base['garrison']['commander']
    echo_base_commander = clean_data(echo_base_commander)
    echo_base['garrison']['commander'] = echo_base_commander

    # 6.4.3 Corellian Smuggler Dash Rendar
    echo_base_Smuggler = echo_base["visiting_starships"]["freighters"][1]["pilot"]
    echo_base_Smuggler = clean_data(echo_base_Smuggler)
    echo_base["visiting_starships"]["freighters"][1]["pilot"] = echo_base_Smuggler
    
    #6.4.4 Snowspeeder
    swapi_vehicles_url = f"{ENDPOINT}/vehicles/"
    swapi_snowspeeder = get_swapi_resource(swapi_vehicles_url, {'search': 'snowspeeder'})['results'][0]
    
    echo_base_snowspeeder = echo_base['vehicle_assets']['snowspeeders'][0]['type']
    
    snowspeeder = combine_data(echo_base_snowspeeder, swapi_snowspeeder)
    snowspeeder = filter_data(snowspeeder, VEHICLE_KEYS)
    snowspeeder= clean_data(snowspeeder)
    echo_base['vehicle_assets']['snowspeeders'][0]['type'] = snowspeeder

    #6.4.5 T-65 X-wing, GR-75 medium transport, and Millennium Falcon
    # T-65 X-wing
    swapi_starships_url = f"{ENDPOINT}/starships/"
    swapi_Xwing = get_swapi_resource(swapi_starships_url, {'search': ' t-65 x-wing' })['results'][0]
    
    echo_base_Xwing = echo_base["starship_assets"]["starfighters"][0]['type']
    Xwing = combine_data(echo_base_Xwing, swapi_Xwing)
    print(f"Xwing{Xwing}")
    Xwing  = filter_data(Xwing, STARSHIP_KEYS)
    print(f"filter Xwing{Xwing}")
    Xwing  = clean_data(Xwing)
    print(f"clean Xwing{Xwing}")
    echo_base["starship_assets"]["starfighters"][0]['type'] = Xwing
    print(echo_base["starship_assets"]["starfighters"][0]['type'])
    # GR-75 medium transport
    swapi_transport = get_swapi_resource(swapi_starships_url, {'search': 'gr-75 medium transport'})['results'][0]

    echo_base_transport = echo_base["starship_assets"]["transports"][0]['type']
    transport = combine_data(echo_base_transport, swapi_transport)
    transport = filter_data(transport, STARSHIP_KEYS)
    transport = clean_data(transport)
    echo_base["starship_assets"]["transports"][0]['type'] = transport
    # Millennium Falcon
    swapi_Falcon = get_swapi_resource(swapi_starships_url, {'search': "millennium Falcon"})['results'][0]
    
    echo_base_Falcon = echo_base["visiting_starships"]["freighters"][0]
    
    Falcon = combine_data(echo_base_Falcon, swapi_Falcon)
    Falcon = filter_data(Falcon, STARSHIP_KEYS)
    Falcon = clean_data(Falcon)
    echo_base["visiting_starships"]["freighters"][0]  = Falcon

    #6.4.6 Assign crew to the Millennium Falcon
    swapi_people_url = f"{ENDPOINT}/people/"
    han = get_swapi_resource(swapi_people_url, {'search': 'han solo'})['results'][0]
    han = filter_data(han, PEOPLE_KEYS)
    han = clean_data(han)

    che = get_swapi_resource(swapi_people_url, {'search': 'chewbacca'})['results'][0]
    che = filter_data(che, PEOPLE_KEYS)
    che = clean_data(che)

    m_falcon=echo_base['visiting_starships']['freighters'][0]
    m_falcon = assign_crew(m_falcon, {'pilot': han, 'copilot': che})
    echo_base['visiting_starships']['freighters'][0] = m_falcon


    #6.5 Update evacuation plan
    evac_plan = echo_base['evacuation_plan']
    # total people
    num_people=0
    for key,value in echo_base["garrison"]['personnel'].items():
        num_people=num_people+value
    evac_plan['max_base_personnel']=num_people
    evac_plan['max_available_transports']=echo_base["starship_assets"]["transports"][0]["num_available"]
    evac_plan['passenger_overload_multiplier']=echo_base["evacuation_plan"]["passenger_overload_multiplier"]
     # Available transport
    num_trans = echo_base['starship_assets']['transports'][0]['num_available']
    # overload capacity
    multi=echo_base['evacuation_plan']['passenger_overload_multiplier']
    capa = 90
    evac_plan['max_passenger_overload_capacity']=capa*multi*num_trans


    # Hope transport
    evac_transport=(echo_base["starship_assets"]['transports'][0]['type']).copy()
    evac_transport["name"]= "Bright Hope"
    # passengers
    evac_transport['passenger_manifest'] = []

    Leia = get_swapi_resource(swapi_people_url, {'search': "leia organa"})['results'][0]
    Leia = filter_data(Leia, PEOPLE_KEYS)
    Leia = clean_data(Leia)
    evac_transport['passenger_manifest'].append(Leia)

    droid = get_swapi_resource(swapi_people_url, {'search': 'c-3po'})['results'][0]
    droid = filter_data(droid, PEOPLE_KEYS)
    droid = clean_data(droid)
    evac_transport['passenger_manifest'].append(droid)

    # Escorts
    evac_transport['escorts'] = []
    luke_x_wing=(echo_base["starship_assets"]["starfighters"][0]['type']).copy()
    print(echo_base["starship_assets"]["starfighters"][0]['type'])
    wedge_x_wing=(echo_base["starship_assets"]["starfighters"][0]['type']).copy()
    # luke_x_wing
    luke = get_swapi_resource(swapi_people_url, {'search': 'luke skywalker'})['results'][0]
    luke = filter_data(luke, PEOPLE_KEYS)
    luke = clean_data(luke)

    R2 = get_swapi_resource(swapi_people_url, {'search': 'r2-d2'})['results'][0]
    R2 = filter_data(R2, PEOPLE_KEYS)
    R2 = clean_data(R2)

    luke_x_wing = assign_crew(luke_x_wing, {'pilot': luke, 'astromech_droid': R2})
    evac_transport['escorts'].append(luke_x_wing)

    # wedge_x_wing
    Wedge = get_swapi_resource(swapi_people_url, {'search': 'wedge antilles'})['results'][0]
    Wedge = filter_data(Wedge, PEOPLE_KEYS)
    Wedge = clean_data(Wedge)

    R5 = get_swapi_resource(swapi_people_url, {'search': 'r5-d4'})['results'][0]
    R5 = filter_data(R5, PEOPLE_KEYS)
    R5 = clean_data(R5)

    wedge_x_wing = assign_crew(wedge_x_wing, {'pilot': Wedge, 'astromech_droid': R5})
    evac_transport['escorts'].append(wedge_x_wing)
    

    evac_plan['transport_assignments'].append(evac_transport)
    echo_base['evacuation_plan']=evac_plan

    write_json(OUTPUTECHO, echo_base)


if __name__ == '__main__':
    main()
