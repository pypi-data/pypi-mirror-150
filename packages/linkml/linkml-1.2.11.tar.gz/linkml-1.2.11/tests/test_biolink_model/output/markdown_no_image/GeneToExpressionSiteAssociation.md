
# Class: gene to expression site association


An association between a gene and an expression site, possibly qualified by stage/timing info.

URI: [biolink:GeneToExpressionSiteAssociation](https://w3id.org/biolink/vocab/GeneToExpressionSiteAssociation)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[Publication],[OntologyClass],[LifeStage],[AnatomicalEntity]<object%201..1-%20[GeneToExpressionSiteAssociation&#124;predicate:predicate_type;relation(i):uriorcurie;negated(i):boolean%20%3F;type(i):string%20%3F;category(i):category_type%20*;id(i):string;iri(i):iri_type%20%3F;name(i):label_type%20%3F;description(i):narrative_text%20%3F;source(i):label_type%20%3F],[GeneOrGeneProduct]<subject%201..1-++[GeneToExpressionSiteAssociation],[OntologyClass]<quantifier%20qualifier%200..1-++[GeneToExpressionSiteAssociation],[LifeStage]<stage%20qualifier%200..1-%20[GeneToExpressionSiteAssociation],[Association]^-[GeneToExpressionSiteAssociation],[GeneOrGeneProduct],[Attribute],[Association],[AnatomicalEntity],[Agent])](https://yuml.me/diagram/nofunky;dir:TB/class/[Publication],[OntologyClass],[LifeStage],[AnatomicalEntity]<object%201..1-%20[GeneToExpressionSiteAssociation&#124;predicate:predicate_type;relation(i):uriorcurie;negated(i):boolean%20%3F;type(i):string%20%3F;category(i):category_type%20*;id(i):string;iri(i):iri_type%20%3F;name(i):label_type%20%3F;description(i):narrative_text%20%3F;source(i):label_type%20%3F],[GeneOrGeneProduct]<subject%201..1-++[GeneToExpressionSiteAssociation],[OntologyClass]<quantifier%20qualifier%200..1-++[GeneToExpressionSiteAssociation],[LifeStage]<stage%20qualifier%200..1-%20[GeneToExpressionSiteAssociation],[Association]^-[GeneToExpressionSiteAssociation],[GeneOrGeneProduct],[Attribute],[Association],[AnatomicalEntity],[Agent])

## Parents

 *  is_a: [Association](Association.md) - A typed association between two entities, supported by evidence

## Referenced by Class


## Attributes


### Own

 * [gene to expression site association➞stage qualifier](gene_to_expression_site_association_stage_qualifier.md)  <sub>0..1</sub>
     * Description: stage at which the gene is expressed in the site
     * Range: [LifeStage](LifeStage.md)
     * Example: UBERON:0000069 larval stage
 * [gene to expression site association➞quantifier qualifier](gene_to_expression_site_association_quantifier_qualifier.md)  <sub>0..1</sub>
     * Description: can be used to indicate magnitude, or also ranking
     * Range: [OntologyClass](OntologyClass.md)
 * [gene to expression site association➞subject](gene_to_expression_site_association_subject.md)  <sub>1..1</sub>
     * Description: gene in which variation is correlated with the phenotypic feature
     * Range: [GeneOrGeneProduct](GeneOrGeneProduct.md)
 * [gene to expression site association➞object](gene_to_expression_site_association_object.md)  <sub>1..1</sub>
     * Description: location in which the gene is expressed
     * Range: [AnatomicalEntity](AnatomicalEntity.md)
     * Example: UBERON:0002037 cerebellum
 * [gene to expression site association➞predicate](gene_to_expression_site_association_predicate.md)  <sub>1..1</sub>
     * Description: expression relationship
     * Range: [PredicateType](types/PredicateType.md)

### Inherited from association:

 * [id](id.md)  <sub>1..1</sub>
     * Description: A unique identifier for an entity. Must be either a CURIE shorthand for a URI or a complete URI
     * Range: [String](types/String.md)
     * in subsets: (translator_minimal)
 * [iri](iri.md)  <sub>0..1</sub>
     * Description: An IRI for an entity. This is determined by the id using expansion rules.
     * Range: [IriType](types/IriType.md)
     * in subsets: (translator_minimal,samples)
 * [name](name.md)  <sub>0..1</sub>
     * Description: A human-readable name for an attribute or entity.
     * Range: [LabelType](types/LabelType.md)
     * in subsets: (translator_minimal,samples)
 * [description](description.md)  <sub>0..1</sub>
     * Description: a human-readable description of an entity
     * Range: [NarrativeText](types/NarrativeText.md)
     * in subsets: (translator_minimal)
 * [source](source.md)  <sub>0..1</sub>
     * Description: a lightweight analog to the association class 'has provider' slot, which is the string name, or the authoritative (i.e. database) namespace, designating the origin of the entity to which the slot belongs.
     * Range: [LabelType](types/LabelType.md)
     * in subsets: (translator_minimal)
 * [provided by](provided_by.md)  <sub>0..\*</sub>
     * Description: connects an association to the agent (person, organization or group) that provided it
     * Range: [Agent](Agent.md)
 * [has attribute](has_attribute.md)  <sub>0..\*</sub>
     * Description: connects any entity to an attribute
     * Range: [Attribute](Attribute.md)
     * in subsets: (samples)
 * [relation](relation.md)  <sub>1..1</sub>
     * Description: The relation which describes an association between a subject and an object in a more granular manner. Usually this is a term from Relation Ontology, but it can be any edge CURIE.
     * Range: [Uriorcurie](types/Uriorcurie.md)
 * [negated](negated.md)  <sub>0..1</sub>
     * Description: if set to true, then the association is negated i.e. is not true
     * Range: [Boolean](types/Boolean.md)
 * [qualifiers](qualifiers.md)  <sub>0..\*</sub>
     * Description: connects an association to qualifiers that modify or qualify the meaning of that association
     * Range: [OntologyClass](OntologyClass.md)
 * [publications](publications.md)  <sub>0..\*</sub>
     * Description: connects an association to publications supporting the association
     * Range: [Publication](Publication.md)
 * [association➞type](association_type.md)  <sub>0..1</sub>
     * Description: rdf:type of biolink:Association should be fixed at rdf:Statement
     * Range: [String](types/String.md)
 * [association➞category](association_category.md)  <sub>0..\*</sub>
     * Description: Name of the high level ontology class in which this entity is categorized. Corresponds to the label for the biolink entity type class.
 * In a neo4j database this MAY correspond to the neo4j label tag.
 * In an RDF database it should be a biolink model class URI.
This field is multi-valued. It should include values for ancestors of the biolink class; for example, a protein such as Shh would have category values `biolink:Protein`, `biolink:GeneProduct`, `biolink:MolecularEntity`, ...
In an RDF database, nodes will typically have an rdf:type triples. This can be to the most specific biolink class, or potentially to a class more specific than something in biolink. For example, a sequence feature `f` may have a rdf:type assertion to a SO class such as TF_binding_site, which is more specific than anything in biolink. Here we would have categories {biolink:GenomicEntity, biolink:MolecularEntity, biolink:NamedThing}
     * Range: [CategoryType](types/CategoryType.md)
     * in subsets: (translator_minimal)

## Other properties

|  |  |  |
| --- | --- | --- |
| **See also:** | | [https://github.com/monarch-initiative/ingest-artifacts/tree/master/sources/BGee](https://github.com/monarch-initiative/ingest-artifacts/tree/master/sources/BGee) |

