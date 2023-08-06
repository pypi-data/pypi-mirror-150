# Compspec Python

<p align="center">
  <img height="300" src="https://raw.githubusercontent.com/compspec/spec/main/img/compspec-circle.png">
</p>

A compspec (Composition spec) is a specification and model for comparing things. This means
that we take an abstract and simple approach to model complex systems as graphs (nodes
and relaionshps) and then can compare between graphs or extract corpora (groups of facts) to use later. 
Compspec python, the implementation here, is intended to provide a basic Python 
for using compspec for your own needs.

 - [The Spec](https://github.com/compspec/spec): read about the background, concepts, and design of the specification.

Conceptually, for a:

 - Diff: we will create two graphs and subtract one from the other
 - Composition: we will create one graph and display it
 

And the neat thing about this approach is that we can take a larger graph and break
it into smaller graphs, and test smaller graphs until we hit a result that suggests an incompatibility,
and stop. Given you are using subgraphs, it means that for some problem space we won't
get a listing of all the incompatible nodes, but we can be fairly sure that the combination
won't work because 1 incompatibility or difference is too much. Of course this design
and how the graphs are presented and tested can be tweaked for any particular problem space.
  
**under development**

## Usage

The core client here is intended to be used as an API, meaning you can derive
facts and relations and then run a model. It is intended for higher level libraries
to use this module for custom command line parsing of specific domain-oriented entities.

### Install

You can install locally

```bash
$ git clone git@github.com:compspec/compspec.git
$ cd compspec
$ pip install -e .
```

or from pypi:

```bash
$ pip install compspec
```

### Examples

For full examples, try running the scripts under [examples](examples) after you install
compspec. More complex examples (with DWARF, etc) are coming soon.

 - [Creating a basic graph](examples/basic-graph/run.py): (a composition)
 - [Calculating a Diff](examples/basic-diff/run.py): (a difference between two compositions)
 - [Combining Graphs](examples/combine-graphs/run.py)
 - [Calculating a DWARF diff](examples/dwarf): a set of more real world examples

```bash
$ python examples/basic-graph/run.py
$ python examples/basic-diff/run.py
$ python examples/combine-graphs/run.py
```
We also have an example that takes an iterative approach to compare groups:

```bash
$ python examples/python/tensorflow-module-example.py
$ python examples/python/tensorflow-function-example.py
$ python examples/python/tensorflow-example.py
```
That example is best if you are interested in breaking a problem space into
multiple graphs.


### Additional Functionality

Given that you have a graph:

```python
A = Graph()
for node_id, name, value in [
    ["id0", "func", "goodbye_world"],
    ["id1", "func", "hello_world"],
    ["id3", "parameter", "name"],
    ["id4", "default", "Squidward"],
]:
    A.new_node(name, value, node_id)

for fromid, relation, toid in [
    ["id1", "has", "id3"],
    ["id3", "has", "id4"],
    ["id3", "has", "id5"],
    ["id1", "has", "id6"],
    ["id6", "has", "id7"],
]:
    A.new_relation(fromid, toid, relation)
```

You can convert it to a dictionary:

```python
obj = A.to_dict()
```

And given that loaded (e.g., from json), we can then populate a new graph!

```python
g = Graph.from_dict(obj)
```

These are very simple operations to define graphs, and primarily the work is done
manually to create the nodes, relations, and identifiers. It is expected that specific
domains that intend to create graphs will load in some object (e.g., a binary file) and 
do this creation on behalf of the user.

## TODO

- look into Go library?
- we need to be able to print out the result (based on graph relationships)
- create compspec.yaml where we can explicitly define kinds of ABI breaks
