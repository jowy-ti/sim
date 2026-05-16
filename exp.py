import yaml

if __name__ == "__main__":

    with open("topology.yml", "r") as file:
        config = yaml.safe_load(file)

    # print(config['topology']['Queue0'][0]['next'])
    # print(config)
    # components = config['components']
    # for queue, attributes in components.items():
    #     print(queue)
    #     print(attributes)
    
    tpology = config['topology']

    for queue, attributes in tpology.items():
        print(queue)
        print(attributes)