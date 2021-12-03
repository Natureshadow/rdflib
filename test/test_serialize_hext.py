from rdflib import Dataset, URIRef, Namespace, Literal, BNode
from test import TEST_DIR


def test_hext_01():
    d = Dataset()
    trig = """
            PREFIX ex: <http://example.com/>
            PREFIX owl: <http://www.w3.org/2002/07/owl#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

            ex:g1 {
                ex:s1
                    ex:p1 ex:o1 , ex:o2 ;
                    ex:p2 [
                        a owl:Thing ;
                        rdf:value "thingy" ;
                    ] ;
                    ex:p3 "Object 3" , "Object 4 - English"@en ;
                    ex:p4 "2021-12-03"^^xsd:date ;
                    ex:p5 42 ;
                    ex:p6 "42" ;
                .
            }

            ex:g2 {
                ex:s1
                    ex:p1 ex:o1 , ex:o2 ;
                .
                ex:s11 ex:p11 ex:o11 , ex:o12 .
            }

            # default graph triples
            ex:s1 ex:p1 ex:o1 , ex:o2 .
            ex:s21 ex:p21 ex:o21 , ex:o22 .

           """
    d.parse(data=trig, format="trig")
    out = d.serialize(format="hext")
    testing_lines = [
        [False, '["http://example.com/s1", "http://example.com/p1", "http://example.com/o2", "", "", "http://example.com/g2"]'],
        [False, '["http://example.com/s1", "http://example.com/p3", Object 3, "", "", "http://example.com/g1"]'],
        [False, '["http://example.com/s1", "http://example.com/p5", 42, "http://www.w3.org/2001/XMLSchema#integer", "", "http://example.com/g1"]'],
        [False, '"http://www.w3.org/1999/02/22-rdf-syntax-ns#value", thingy, "", "", "http://example.com/g1"]'],
        [False, '["http://example.com/s1", "http://example.com/p4", 2021-12-03, "http://www.w3.org/2001/XMLSchema#date", "", "http://example.com/g1"]']
    ]
    for line in out.splitlines():
        for test in testing_lines:
            if test[1] in line:
                test[0] = True

    assert all([x[0] for x in testing_lines])
