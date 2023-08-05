
# Class: MarriageEvent




URI: [ks:MarriageEvent](https://w3id.org/linkml/tests/kitchen_sink/MarriageEvent)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[WithLocation],[Place],[Person],[Person]<married%20to%200..1-%20[MarriageEvent&#124;started_at_time(i):date%20%3F;ended_at_time(i):date%20%3F;is_current(i):boolean%20%3F],[MarriageEvent]uses%20-.->[WithLocation],[Event]^-[MarriageEvent],[Event],[AnyObject])](https://yuml.me/diagram/nofunky;dir:TB/class/[WithLocation],[Place],[Person],[Person]<married%20to%200..1-%20[MarriageEvent&#124;started_at_time(i):date%20%3F;ended_at_time(i):date%20%3F;is_current(i):boolean%20%3F],[MarriageEvent]uses%20-.->[WithLocation],[Event]^-[MarriageEvent],[Event],[AnyObject])

## Parents

 *  is_a: [Event](Event.md)

## Uses Trait

 *  mixin: [WithLocation](WithLocation.md)

## Referenced by Record

 *  **None** *[has marriage history](has_marriage_history.md)*  <sub>0..\*</sub>  **[MarriageEvent](MarriageEvent.md)**

## Attributes


### Own

 * [married to](married_to.md)  <sub>0..1</sub>
     * Range: [Person](Person.md)

### Inherited from Event:

 * [started at time](started_at_time.md)  <sub>0..1</sub>
     * Range: [Date](Date.md)
 * [ended at time](ended_at_time.md)  <sub>0..1</sub>
     * Range: [Date](Date.md)
 * [is current](is_current.md)  <sub>0..1</sub>
     * Range: [Boolean](Boolean.md)
 * [metadata](metadata.md)  <sub>0..1</sub>
     * Description: Example of a slot that has an unconstrained range
     * Range: [AnyObject](AnyObject.md)

### Mixed in from WithLocation:

 * [in location](in_location.md)  <sub>0..1</sub>
     * Range: [Place](Place.md)
