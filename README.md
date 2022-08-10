# Team Punistic Cogs

# Installation

[p] is your prefix

[p]repo add tpun-cogs https://github.com/batman202012/tpun

[p]cog install tpun-cogs <cog-name>
  
[p]load <cog-name>
  
  
  
  
# Cog list
  
  
# minecraft

Cog for checking the status' of minecraft servers  

[p]minecraft status <server>
Returns the amount of people on server and the ping
  
[p]minecraft ip <server>
Returns the server's ip
  
  
# pvc
  
Cog for creating private voice channels
  
[p]vc setup
Creates command channel for pvc and selects the channel's default joinable role (used for lock/unlock)

[p]vc create <name>
Creates a voice channel in the catergory the pvc command channel is in with name <name>
  
[p]vc gui
Opens a gui for voice channel creation
  
[p]vc delete
Deletes your private voice channel
  
[p]vc name
Returns the name of your private voice channel
  
[p]vc rename <name>
Renames your private voice channel to <name>

[p]vc region <int>
Changes your private voice channel region to <int>
The list of avaliable regions are as follow 0=Auto, 1=US West, 2=US East, 3=US South, 4=EU West, 5=EU Central, 6=Brazil, 7=Hong Kong, 8=Brazil, 9=Japan, 10=Russia, 11=Sydney, 12=South Africa
  
[p]vc lock
Prevents the roles used in vc setup from joining the channel
  
[p]vc unlock
Allows the roles used in vc setup to join the channel
  
[p]vc invite <user mention>
Invites a <user> to join your private voice channel
  
[p]vc limit <int>
Sets the user limit as <int> for your private voice channel, use 0 to set it to uncapped
  
[p]vc request <user mention>
Requests to join <user>'s private voice channel, only works when used on the channel's owner
  
[p]vc kick <user mention>
Kicks <user> from your private voice channel and removes their permissions to join
  
[p]vc mute <user mention>
Disables <user>'s permissions to speak/stream/use camera/type in vc text chat in your private voice channel

[p]vc unmute <user mention>
Enables <user>'s permissions to speak/stream/use camera/type in vc text chat in your private voice channel
  
[p]vc claim
Claims a private voice channel as yours if the owner is no longer present
  
[p]vc transfer <user mention>
Transfers private voice channel ownership to <user>

  
# reputation
  
Gives users +1 rep everytime someone thanks them

[p]repremove <user mention> <amount to remove>
Removes <amount> of reputation from <user>
  
[p]checkrep <user mention>
Checks the amount of rep <user> has

  
# rolebuy

Allows users to buy roles using redbot currency
  
[p]buy <role mention>
Buys <role> and removes currency from user

  
# usergate
  
Prevents user accounts that are under 7 days old from joining the server
  
  
# verifier
  
Verifies users using a gui
  
[p]verify <user mention>
Removes <user> unverified role and gives them their selected (from gui) verified role
