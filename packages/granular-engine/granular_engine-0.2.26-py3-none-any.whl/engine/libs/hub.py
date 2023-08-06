from engine.connections import Callisto, Dione


def get_artifacts(url, last=False, best=False):
    if 'https://engine.granular.ai/' in url:
        if 'projects' in url and 'experiments' in url:
            if '&' not in url:
                url = url.replace('https://engine.granular.ai/', '')
                info = url.split('/')
                org_slug = info[1]
                experiment_id = info[4].split('=')[-1]
                
                callisto = Callisto()
                org_id = callisto.get_org_id_from_slug(org_slug=org_slug)

                dione = Dione(callisto, org_id)
                artifacts = dione.get_artifacts(experiment_id)
                artifacts = sorted(artifacts, key=lambda d: d['step'])

                if last:
                     artifacts.reverse()
                     for artifact in artifacts:
                         if 'checkpoint' in artifact['metadata']: 
                            return artifact
                else:
                    return artifacts
            else:
                print ("Please choose only one experiment to retrieve its artifacts.")
        else:
            print ("This is not a correct GeoEngine experiment URL.")
    else:
        print ("This is not a url from https://engine.granular.ai")

def get_last_weight(url):
    artifact = get_artifacts(url, last=True)
    if artifact:
        return artifact['metadata']['checkpoint'], artifact['experimentId']
    
def get_best_weight(url):
    if 'https://engine.granular.ai/' in url:
        if 'projects' in url and 'experiments' in url:
            if '&' not in url:
                url = url.replace('https://engine.granular.ai/', '')
                info = url.split('/')
                org_slug = info[1]
                experiment_id = info[4].split('=')[-1]
                
                callisto = Callisto()
                org_id = callisto.get_org_id_from_slug(org_slug=org_slug)

                dione = Dione(callisto, org_id)
                experiment = dione.get_experiment_by_id(experiment_id)
                if experiment['bestModel']:
                    return experiment['bestModel'], experiment['id']
            else:
                print ("Please choose only one experiment to retrieve its artifacts.")
        else:
            print ("This is not a correct GeoEngine experiment URL.")
    else:
        print ("This is not a url from https://engine.granular.ai")