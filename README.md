# Melzi

### Description

Melzi, named after Francesco Melzi, is a command-line utility that topologically 
sorts text based on conceptual dependency.

### Installation

For simplicity here's the oneliner. Run the following in your terminal:

`git clone https://github.com/AHBruns/Melzi.git && chmod +x Melzi/install.sh && ./Melzi/install.sh`

Once run, you'll likely have to restart your terminal. After this the utility
 can be called on any file or directory with the following 
 command: `melzi relative/path/to/input/file relative/path/to/output/file`.
 
 **NOTE: The output can overwrite existing files. So, be sure to write to 
 either a non-existent file or an existing file that you're okay with 
 overwriting.**
 

### Usage

TSort uses a simple domain-specific language to mark-up paragraphs. The 
TSort language is made up of statements. Each statement gets its own line; no 
sharing. Additionally, statements are tethered to their proceeding paragraph. 
That is, you should write your document like so:
```
PARAGRAPH A's STATMENTS

PARAGRAPH A

PARAGRAPH B's STATEMENTS

PARAGRAPH B

``` 
All TSort statements take the form `||| OPERATION ENTITY`.
 
The pipes are there to tell the parser that the line being parsed is a TSort statement, 
not a content line. So, ensure that you don't accidentally proceed any of 
your content lines with three pipes.

Now let's skip ahead and look at the entity part of a statement. In the 
TSort DSL entities are simply names for concepts being discussed in the 
content of the text.

For instance, if you had a paper about binary trees you 
might have an entity for the concept of a node, a linked list, a binary 
search tree, an OBST, and likely many other things as well. Entities are how 
TSort reasons about which how to order your paragraphs. Importantly, entities
 can include any character except for a newline.

Finally, the operation part of the statement can be any of the following:

- `DEC` : Used to declare a new entity.
- `DESC`: Used to denote that the proceeding paragraph describes an entity.
- `DEP` : Used to denote that the proceeding paragraph depends on an entity.

Operations are actions taken on entities. For an entity to be declared the 
statement `||| DEC ENTITY` must be used. Before an entity can be described or
 depended on, it must be declared. Declaring an entity does NOT implicitly 
 cause the proceeding paragraph to describe the entity. In other words,
```
||| DEC entity1
blah blah blah
blah blah blah
blah blah blah

||| DEP entity1
blah blah blah
blah blah blah
blah blah blah
```
has no valid ordering solution, but
```
||| DEC entity1
||| DESC entity1
blah blah blah
blah blah blah
blah blah blah

||| DEP entity1
blah blah blah
blah blah blah
blah blah blah
```
does. Look in the src/test.txt for examples on how to structure your 
documents.

### Hierarchical Structures

Many projects benefit from a hierarchical structure whose levels are each 
sorted independently of each other. A good example is a novel. One might want
 to sort the paragraphs of each chapter separately then sort the chapters 
 themselves. This can be achieved through targeting a directory instead of a 
 file with Melzi.
 
When Melzi is used on a directory it recursively traverses looking for 
files to sort. Each file is sorted individually then combined with the other
 files in its immediate directory structure and sorted again. This goes on 
 until Melzi has collated all the various files into a single output file.
 
For instance Melzi would sort the following structure
```
         ---- book ----
        |              |
    - chp1 -        - chp2 -
   |        |      |        |
sec1.txt sec2.txt sec1.txt sec2.txt
```
by first sorting `book/chp1/sec1.txt`, `book/chp1/sec2.txt`, `book/chp2/sec1
.txt`, and `book/chp2/sec2.txt` individually. Then sorting `book/chp1/sec1.txt`
and `book/chp1/sec2.txt` together where each file is it's own node. 
Then sorting `book/chp2/sec1.txt` and `book/chp2/sec2.txt` together where 
each file is it's own node. Then, finally, sorting The results of the two 
previous operations as individual nodes.

### Support

Please email me at alex.h.bruns@gmail.com with any questions. I can also be 
found on Twitter, @AlexHBruns.



