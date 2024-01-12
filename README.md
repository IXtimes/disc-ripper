# Disc Ripper (A Python bot that interfaces scuffedly with the free video encoder Handbrake to rip MP4s off of discs)
As the long title stats, this is a scuffed Python disc ripper bot that interfaces with Handbrake to simplify disc ripping to just inserting a disc and letting it go. With text message support to notify you on the go.

I know this project will likely be largely unusable to some degree due to some oversight that I made, but incase your willing to work with the functioning heap that I made, here is something to consider with the executable that I provided in releases (if your smart enough feel free to compile your own version :p)
- This project has 2 functional modes: ripping a single feature length title, and ripping multiple episodic length titles.
- The bot INTERFACES with Handbrake, but any and all encoder settings to create the right MP4 qualities must be configured in Handbrake BEFORE running this program.
- This project allows for up to 2 instants of Handbrake to run encoding tasks (if your PC can handle it that is)
- On first execution the program may seem to crash, but this is due to a lack of a preference file existing in the same directory as the executable, so DONT WORRY if the program crashes initally.
- The preferences file should be self explainatory, but the Twilio information I believe *might* not be required, but its a case by case basis. If you want to utilize the abilty to send text messages for updates with the ripper bot create an account at Twilio.com (non spon)

If you have any insights to make this project ANY better (any Im sure theres plenty), feel free to either fork this project or reach out and I *might* get around to fixing it (Im a stressed CS college student, I got too much on my plate as is );)
Thanks for checking my first Python project out :)

