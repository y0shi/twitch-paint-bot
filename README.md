# twitch-paint-bot

A bot in two acts.

## Act 1 - The Patron

The patron tells the painter what to paint.  Specifically, it attaches to a twitch channel (stream) and listens for commands, then sends them to the painter.

#### Main loop
- If not connected to the stream, connect.
- Listen for commands for N seconds.
  - Tally at most, 1 resquest from each user.
- Select the command with the highest number of votes.
  - If there's a tie, choose randomly.
- If no votes in M cycles, choose a random command
- Send the command to the painter

## Act 2 - The Painter

The painter listens for commands from the patron and does what it's told.  Each time the bot moves, it will also dispense paint onto the brush.

#### List of commands
- Move forward
- Turn right
- Turn left