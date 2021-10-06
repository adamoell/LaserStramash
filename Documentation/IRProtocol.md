# Infrared Protocol

Laser Stramash uses the standard NEC infrared remote protocol. This
protocol operates on a 38kHz carrier frequency, and is implemented at
near-infrared wavelengths around 940nm. Using this protocol allows for
very inexpensive IR peripherals, large team sizes, and detailed tracking
of who hit whom, and where.

Each time the gun fires, it transmits an NEC data packet, much as a TV
remote would. An NEC packet consists of a 16-bit *address* and a 16-bit
*command*. Laser Stramash uses the error-corrected NEC-8 version, where
each packet consists of an 8-bit address and its complement, and and
8-bit command and its complement. This allows for solid error detection.
Laser Stramash encodes the firing player's *team* in the address field,
and their *id* in the command field. This allows for up to 256 teams,
each with up to 256 players.

The prototype uses Peter Hinch's micropython_ir library for sending and
decoding NEC data.

## References

micropython_ir:

<https://github.com/peterhinch/micropython_ir>

NEC protocol details:

<https://www.sbprojects.net/knowledge/ir/nec.php>

**Caution**

The NEC protocol is very commonly used in infrared remotes. It may be as
well to cover the receivers of any IR-controlled equipment in or near
your play space!

