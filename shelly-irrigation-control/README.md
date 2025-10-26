# Shelly Irrigation Control
Primarily created to read the zone statuses of a Shelly FK-06X irrigation controller then trigger a Shelly Pro 1 PM to activate an irrigation pump. This is functionality is not built-in with the FK-06X.

The Shelly Pro1PM relay is activated with a timer in seconds, the duration is defined in the environment. This is a failsafe to prevent the pump getting stuck on in the even the script crashes or a network drop out.