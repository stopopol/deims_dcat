import deims
# pip install rdflib

def generate_dcat(site_record):

    import os
    from rdflib import Graph, URIRef, Literal, BNode
    from rdflib.namespace import CSVW, DC, DCAT, DCTERMS, DOAP, FOAF, ODRL2, ORG, OWL, \
                           PROF, PROV, RDF, RDFS, SDO, SH, SKOS, SOSA, SSN, TIME, \
                           VOID, XMLNS, XSD

    # relevant attributes from json

    # check functionality of BNode
    # https://www.w3.org/TR/vocab-dcat-3/#Property:resource_identifier

    id_suffix = site_record.get('id').get('suffix')
    title = Literal(site_record.get('title'))
    issued = Literal(site_record.get('created'))
    modified = Literal(site_record.get('changed'))
    site_url = URIRef("http://www.deims.org/" + uuid)
    abstract = Literal(site_record.get('attributes').get('general').get('abstract'))
    coordinates = Literal(site_record.get('attributes').get('geographic').get('coordinates'))

    # iterable objects
    contacts = site_record.get('attributes').get('contact').get('siteManager')
    metadataCreators = site_record.get('attributes').get('contact').get('metadataProvider')
    observedProperties = site_record.get('attributes').get('focusDesignScale').get('observedProperties')

    g = Graph()

    # https://rdflib.readthedocs.io/en/stable/intro_to_creating_rdf.html

    g.add((site_url, RDF.type, DCAT.Dataset))
    g.add((site_url, DCTERMS['title'], title))
    g.add((site_url, DCTERMS["license"], URIRef("https://creativecommons.org/licenses/by-nc/4.0/")))
    g.add((site_url, DCTERMS['issued'], issued))
    g.add((site_url, DCTERMS['modified'], modified))
    g.add((site_url, DCTERMS['language'], Literal("en")))
    g.add((site_url, DCTERMS['description'], abstract))
    g.add((site_url, DCTERMS['identifier'], Literal(site_url)))
    g.add((site_url, DCTERMS['Location'], coordinates))
    g.add((site_url, DCAT['landingPage'], URIRef(site_url)))

    # for fields with n properties
    if contacts is not None:
        for contact in contacts:
            g.add((site_url, DCAT['contactPoint'], Literal(contact.get('name'))))

    if metadataCreators is not None:
        for metadata_creator in metadataCreators:
            g.add((site_url, DCTERMS['creator'], Literal(metadata_creator.get('name'))))
            
    if observedProperties is not None:
        for observedProperty in observedProperties:
            g.add((site_url, DCAT['keyword'], Literal(observedProperty.get('label'))))
            #g.add((site_url, DCAT['keyword'], URIRef(observedProperty.get('uri'))))

    # export to xml
    base_dir = os.getcwd() + '/dcat_files'
    filename = id_suffix + '.ttl'
    destination_path = os.path.join(base_dir, filename)

    g.serialize(destination=destination_path, format='turtle')

    # check validator 
    # https://www.itb.ec.europa.eu/shacl/dcat-ap.de/upload
    
# list of all LTER Europe sites
for uuid in deims.getListOfSites(network="4742ffca-65ac-4aae-815f-83738500a1fc", verified_only=True):
    generate_dcat(deims.getSiteById(uuid))
