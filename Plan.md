# Plan

## Prototype

Status:

TODO: get rid of the nasty table

+-----------------------+-----------------------+-----------------------+
| Item                  | Details               | ETA                   |
+-----------------------+-----------------------+-----------------------+
| Protocol Design       | Spec for full MQTT    | 2021-09-28            |
|                       | protocol              |                       |
+-----------------------+-----------------------+-----------------------+
| Gun 3D Design         | 3D print designs for: | 2021-10-02            |
+-----------------------+-----------------------+-----------------------+
| Prototype Hardware    | Build two prototypes: | 2021-10-16            |
+-----------------------+-----------------------+-----------------------+
| Game Server Software  | Basic test server,    | 2021-10-02            |
|                       | just one simple game: |                       |
|                       | Free For All          |                       |
+-----------------------+-----------------------+-----------------------+
| Launcher              | Basic command-line:   | 2021-10-02            |
+-----------------------+-----------------------+-----------------------+
| Monitor               | Simple GUI:           | 2021-10-02            |
+-----------------------+-----------------------+-----------------------+
| Gun                   | Basic test software:  | 2021-10-09            |
+-----------------------+-----------------------+-----------------------+
| FX Server             | Minimal:              | 2021-10-16            |
+-----------------------+-----------------------+-----------------------+
| Teams Game            | Teams: Server and Gun | 2021-10-23            |
|                       | Code                  |                       |
|                       |                       |                       |
|                       | Basic command-line    |                       |
|                       | launcher              |                       |
+-----------------------+-----------------------+-----------------------+
| Stramash Royal Game   | Stramash Royale:      | 2021-10-30            |
|                       | Server and Gun Code   |                       |
|                       |                       |                       |
|                       | Basic command-line    |                       |
|                       | launcher              |                       |
+-----------------------+-----------------------+-----------------------+

TODO Assess:

-   LED/receiver range -- well lit, darkness

-   Accuracy required for hit

-   3D-printed diffuser effectiveness

-   Laser brightness for smoke gen

-   Simple play-testing

-   Protocol

-   Networking speed etc

-   What happens when we pull the network cables etc?

-   Do we need a separate chip to do IR decoding, eg ATtiny85
    <https://github.com/fotisl/ir2i2c>

    -   ATtiny85 getting started
        <https://electronut.in/getting-started-with-attiny85-avr-programming/>
    -   Reasonable price from rs-online
    -   Even better from microchip direct?
        <https://www.microchipdirect.com/product/ATTINY85-20PU?productLoaded=true>
    -   Or just use a D1 mini?
        https://github.com/peterhinch/micropython-mqtt

### []{#anchor-4}Beta

Beta to be scoped out after prototype evaluation

-   Additional gun peripherals

    -   screen
    -   sound
    -   vibration
    -   RFID -- for position-based respawn, powerups etc
    -   capacitive sensing to ensure hand on gun, not covering sensor
    -   reset pin (short GND to EN?)

-   PCB changes

    -   Break out other gpios, power pins etc 'just in case' --
        upgradeable!
    -   Reset button -- short EN to ground?
    -   KF2510-2A and 4a connectors
    -   Go with bare module? Break out programming?
    -   Mounting holes
    -   Separate IC (eg ATtiny85) for IR decode? Or use ESP8266 with
        Peter Hinch's MQTT bridge?
    -   Peripherals
    -   Power supply/charger on board? TP4056? Or use LiFePO4 and
        dispense with?
    -   SMT? and get it assembled?
    -   Polyfuse for battery?

-   3D model changes

-   Software changes

    -   ESP32 monitors its voltage in main loop, squawks when getting
        low? Sleep if getting too low?

Additional games

Playtesting at Milestone

### []{#anchor-5}Version 1

To be scoped out after beta evaluation