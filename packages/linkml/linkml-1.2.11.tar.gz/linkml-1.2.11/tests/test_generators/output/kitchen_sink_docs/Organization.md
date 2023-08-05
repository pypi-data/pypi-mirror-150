
# Class: Organization




URI: [ks:Organization](https://w3id.org/linkml/tests/kitchen_sink/Organization)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[Organization&#124;id:string;name:string%20%3F;aliases:string%20*]uses%20-.->[HasAliases],[Organization]^-[Company],[HasAliases],[Company])](https://yuml.me/diagram/nofunky;dir:TB/class/[Organization&#124;id:string;name:string%20%3F;aliases:string%20*]uses%20-.->[HasAliases],[Organization]^-[Company],[HasAliases],[Company])

## Identifier prefixes

 * ROR

## Uses Trait

 *  mixin: [HasAliases](HasAliases.md)

## Children

 * [Company](Company.md)

## Referenced by Record


## Attributes


### Own

 * [id](id.md)  <sub>1..1</sub>
     * Range: [String](String.md)
 * [name](name.md)  <sub>0..1</sub>
     * Range: [String](String.md)

### Mixed in from HasAliases:

 * [➞aliases](hasAliases__aliases.md)  <sub>0..\*</sub>
     * Range: [String](String.md)
