# Main program modules
from handbrake_module import handbrake_series, handbrake_single

def print_title():
    print("==================================================================================================")
    print("  ____             ____      ____        ____                 ____     ____   U _____ u   ____     ")
    print(" |  _\"\\    ___    / __\"| uU /\"___|    U |  _\"\\ u     ___    U|  _\"\\ uU|  _\"\\ u\\| ___\"|/U |  _\"\\ u  ")
    print("/| | | |  |_\"_|  <\\___ \\/ \\| | u       \\| |_) |/    |_\"_|   \\| |_) |/\\| |_) |/ |  _|\"   \\| |_) |/  ")
    print("U| |_| |\\  | |    u___) |  | |/__       |  _ <       | |     |  __/   |  __/   | |___    |  _ <    ")
    print(" |____/ uU/| |\\u  |____/>>  \\____|      |_| \\_\\    U/| |\\u   |_|      |_|      |_____|   |_| \\_\\  ")
    print("  |||_.-,_|___|_,-.)(  (__)_// \\\\       //   \\\\_.-,_|___|_,-.||>>_    ||>>_    <<   >>   //   \\\\_  ")
    print(" (__)_)\\_)-' '-(_/(__)    (__)(__)     (__)  (__)\\_)-' '-(_/(__)__)  (__)__)  (__) (__) (__)  (__) ")
    print("==================================================================================================")
    
print_title()
print("Designed by: Xander Corcoran (IXtimes)\n")
print("Enter what mode you wish to rip discs in:")
print("1. Single title per disc (for movies)")
print("2. Multiple titles per disc (for episodes of a show)")
input = int(input("Enter the number of the option here: "))
if(input == 1):
    handbrake_single.rip_single()
elif(input == 2):
    handbrake_series.rip_series()