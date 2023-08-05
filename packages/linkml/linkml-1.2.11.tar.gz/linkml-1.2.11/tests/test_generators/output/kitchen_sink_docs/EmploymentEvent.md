
# Class: EmploymentEvent




URI: [ks:EmploymentEvent](https://w3id.org/linkml/tests/kitchen_sink/EmploymentEvent)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[Event],[Company]<employed%20at%200..1-%20[EmploymentEvent&#124;type:EmploymentEventType%20%3F;started_at_time(i):date%20%3F;ended_at_time(i):date%20%3F;is_current(i):boolean%20%3F],[Person]++-%20has%20employment%20history%200..*>[EmploymentEvent],[Event]^-[EmploymentEvent],[Person],[Company],[AnyObject])](https://yuml.me/diagram/nofunky;dir:TB/class/[Event],[Company]<employed%20at%200..1-%20[EmploymentEvent&#124;type:EmploymentEventType%20%3F;started_at_time(i):date%20%3F;ended_at_time(i):date%20%3F;is_current(i):boolean%20%3F],[Person]++-%20has%20employment%20history%200..*>[EmploymentEvent],[Event]^-[EmploymentEvent],[Person],[Company],[AnyObject])

## Parents

 *  is_a: [Event](Event.md)

## Referenced by Record

 *  **None** *[has employment history](has_employment_history.md)*  <sub>0..\*</sub>  **[EmploymentEvent](EmploymentEvent.md)**

## Attributes


### Own

 * [employed at](employed_at.md)  <sub>0..1</sub>
     * Range: [Company](Company.md)
     * in subsets: (subset A)
 * [EmploymentEvent➞type](EmploymentEvent_type.md)  <sub>0..1</sub>
     * Range: [EmploymentEventType](EmploymentEventType.md)

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
