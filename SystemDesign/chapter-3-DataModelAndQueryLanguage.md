# Data Model and Query Language

## Relational vs Document Databases

*   The main arguments in favor of the document data model are schema flexibility, better performance due to locality, and that for some applications it is closer to the data structures used by the application. The relational model counters by providing better support for joins, and many-to-one and many-to-many relationships.
*   If the data in your application has a **document-like structure** (i.e., a tree of one-to-manyrelationships, where typically the entire tree is loaded at once), then it’s probably a good idea touse a document model
*   The poor support for joins in document databases may or may not be a problem, depending on the application. 
*   if your application does use **many-to-many relationships**, the document model becomes less appealing.
*   For highly interconnected data, the document model is awkward, the relational model is acceptable, and graph models (see [“Graph-Like Data Models”](https://learning.oreilly.com/library/view/designing-data-intensive-applications/9781491903063/ch02.html#sec_datamodels_graph)) are the most natural

## Schema-on-read vs Schema-on-write

The schema-on-read approach is advantageous if the items in the collection don’t all have the same structure for some reason (i.e., the data is heterogeneous)—for example, because:

-   There are many different types of objects, and it is not practicable to put each type of object in its own table.
-   The structure of the data is determined by external systems over which you have no control and which may change at any time.

In situations like these, a schema may hurt more than it helps, and schemaless documents can be a much more natural data model.

### DATA LOCALITY FOR QUERIES

*   A document is usually stored as a single continuous string, encoded as JSON, XML, or a binary variant thereof (such as MongoDB’s BSON). If your application often needs to access the entire document (for example, to render it on a web page), there is a performance advantage to this *storage locality*. If data is split across multiple tables, like in [Figure 2-1](https://learning.oreilly.com/library/view/designing-data-intensive-applications/9781491903063/ch02.html#fig_billgates_relational), multiple index lookups are required to retrieve it all, which may require more disk seeks and take more time.
*   The locality advantage only applies if you need large parts of the document at the same time. The database typically needs to load the entire document, even if you access only a small portion of it, which can be wasteful on large documents. --**keep documents fairly small and avoid writes that increase the size of a document**

## Declarative Language VS Empirical Language

*   In a declarative query language, like SQL or relational algebra, you just specify the pattern of thedata you want—what conditions the results must meet, and how you want the data to be transformed (e.g.,sorted, grouped, and aggregated)—but not how to achieve that goal
*   It hides implementation detail, which makes it possible for performance improvement.

## MapReduce Querying

MapReduce is neither a declarative query language nor a fully imperative query API, but somewherein between: the logic of the query is expressed with snippets of code, which are called repeatedlyby the processing framework. It is based on the map (also known as collect) and reduce (alsoknown as fold or inject) functions that exist in many functional programming languages.

## Graph-Like Data Models

*   A graph consists of two kinds of objects: vertices (also known as nodes or entities) andedges (also known as relationships or arcs). Many kinds of data can be modeled as a graph.

*   *property graph* model (implemented by Neo4j, Titan, and InfiniteGraph) and the *triple-store* model (implemented by Datomic, AllegroGraph, and others). We will look at three declarative query languages for graphs: Cypher, SPARQL, and Datalog. Similar concepts appear in other graph query languages such as Gremlin [[36](https://learning.oreilly.com/library/view/designing-data-intensive-applications/9781491903063/ch02.html#Gremlin2013)] and graph processing frameworks like Pregel (see [Chapter 10](https://learning.oreilly.com/library/view/designing-data-intensive-applications/9781491903063/ch10.html#ch_batch)).

    ### Property Graphs

    ##### Example 2-2. Representing a property graph using a relational schema

    ```sql
    CREATE TABLE vertices (
        vertex_id   integer PRIMARY KEY,
        properties  json
    );
    
    CREATE TABLE edges (
        edge_id     integer PRIMARY KEY,
        tail_vertex integer REFERENCES vertices (vertex_id),
        head_vertex integer REFERENCES vertices (vertex_id),
        label       text,
        properties  json
    );
    
    CREATE INDEX edges_tails ON edges (tail_vertex);
    CREATE INDEX edges_heads ON edges (head_vertex);
    ```

*   In a triple-store, all information is stored in the form of very simple three-part statements:(subject, predicate, object). For example, in the triple (Jim, likes, bananas), Jim isthe subject, likes is the predicate (verb), and bananas is the object.

```
@prefix : <urn:example:>.
_:lucy     a       :Person.
_:lucy     :name   "Lucy".
_:lucy     :bornIn _:idaho.
_:idaho    a       :Location.
_:idaho    :name   "Idaho".
_:idaho    :type   "state".
_:idaho    :within _:usa.
_:usa      a       :Location.
_:usa      :name   "United States".
_:usa      :type   "country".
_:usa      :within _:namerica.
_:namerica a       :Location.
_:namerica :name   "North America".
_:namerica :type   "continent".
```