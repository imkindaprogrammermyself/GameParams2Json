import json,os,threading,queue

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

input_file = os.path.join(__location__,'GameParams.json')
entites_dir = os.path.join(__location__,'entities')
        
def load_game_params(file):
    with open(file,'r') as f:
        game_params = json.load(f)
        f.close()
        return game_params

def get_entity_types(gparams):
    etypes = []
    for key in gparams:
        etype = gparams[key]['typeinfo']['type']
        if etype not in etypes:
            etypes.append(etype)
    return etypes

def entities_to_json(etype,gparams):
    entities = []
    for key in gparams:
        entity = gparams[key]
        if etype == entity['typeinfo']['type']:
            entities.append(entity)
    write_to = os.path.join(entites_dir,etype+'.json')
    with open(write_to,'w') as f:
        json.dump(entities,f,indent=4)
        f.close()
    #print('Done writing: %s.json'%etype,end='\n')

if not os.path.exists(entites_dir):
    os.mkdir(os.path.join(__location__,'entities'))
else:
    print('Path exists')

def write_entities_json(etypes,gparams):
    entity_threads = []
    for entity_type in etypes:
        th = threading.Thread(target=entities_to_json,args=(entity_type,gparams))
        th.start()
        entity_threads.append(th)

    for th in entity_threads:
        th.join()

print('Loading GameParams.json.')
game_params = load_game_params(input_file)
print('Getting entity types.')
entity_types = get_entity_types(game_params)
print('Writing entities to separate json files.')
write_entities_json(entity_types,game_params)
print('Done.')

