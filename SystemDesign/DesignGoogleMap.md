# Design Google Map

*   Problem description

    *   Design a google map service

    *   Support display maps for certain cities(San Francisco, Seattle etc)

    *   Support tracking the user movement(GPS, telematics data)

    *   Support routing from place A to place B

    *   Support the place look up service [Bonus]

    *   Tracking of the traffic.[Bonus] 

        seatracking of traffic light etc 



*   Services
    *   Location services: track user's movement
    *   Navigation services
    *   Graph processing service: map rendering
    *   Look up service: basic information about cities, places, etc
*   Requirements
    *   low latency
    *   high reliability
    *   high scalability
*   1 billion MAU, 30 mins on google map, 10 cities, 5 routes, 3 navigation requests
*   Read/write ratio
    *   Location services: 1:1
    *   Navigation: 1 : 10 ^5
    *   Graph processing service: 10^5 : 1 
    *   Look up services: 10 ^5 : 1



*   Data storage:
    *   Redis
    *   MongoDB





## My thoughts

Business use cases:

1.   Map Grid rendering (given a location, render a grid)
     1.   PolygonID
     2.   Location
     3.   Neighbor polygon ID
2.   Location search (keywords search, elastice search)
     1.   Local business (Needs indexing, mongoDB)
          1.   Id, Name
          2.   Type
          3.   Addresss
          4.   polygonID
          5.   Nearby vertices
3.   Navigation
     1.   Algorithm: Dijkstra, Bellman-ford, A* algorithm 
     2.   Speed up: pull in all near by polygon information
     3.   Graph database(Neo4j or MySql, potgresGIS)
          1.   Road segments database (read heavy)
               1.   SegementID, directed
               2.   Vertices location
               3.   Name
               4.   Type
          2.   Vertices database:
               1.   VerticeID
               2.   location
     4.   Traffic databases (read/write heavy)
          1.   SegmentId -> traffic
     5.   Transit (read heavy)
     6.   Block data



