<h1># Team Punistic Cogs</h1>

<h2># Installation</h2>

<h3>[p] is your prefix</h3>

<h4>[p]repo add tpun-cogs https://github.com/batman202012/tpun</h4>

<h4>[p]cog install tpun-cogs 'cog-name'</h4>
  
  <h4>[p]load 'cog-name'</h4>
  
  
  
  
  <h2># Cog list</h2>
  
  
  <h3># minecraft</h3>

<h4>Cog for checking the status' of minecraft servers</h4>

  <h5>[p]minecraft status 'server'</h5>
Returns the amount of people on server and the ping
  
    <h5>[p]minecraft ip 'server'</h5>
Returns the server's ip
  
  
      <h3># pvc</h3>
  
      <h4>Cog for creating private voice channels</h4>
  
<h5>[p]vc setup</h5>
Creates command channel for pvc and selects the channel's default joinable role (used for lock/unlock)

  <h5>[p]vc create 'name'</h5>
Creates a voice channel in the catergory the pvc command channel is in with name 'name'
  
<h5>[p]vc gui</h5>
Opens a gui for voice channel creation
  
<h5>[p]vc delete</h5>
Deletes your private voice channel
  
<h5>[p]vc name</h5>
Returns the name of your private voice channel
  
<h5>[p]vc rename 'name'</h5>
Renames your private voice channel to 'name'

<h5>[p]vc region 'int'</h5>
Changes your private voice channel region to 'int'
The list of avaliable regions are as follow 0=Auto, 1=US West, 2=US East, 3=US South, 4=EU West, 5=EU Central, 6=Brazil, 7=Hong Kong, 8=Brazil, 9=Japan, 10=Russia, 11=Sydney, 12=South Africa
  
<h5>[p]vc lock</h5>
Prevents the roles used in vc setup from joining the channel
  
<h5>[p]vc unlock</h5>
Allows the roles used in vc setup to join the channel
  
<h5>[p]vc invite 'user mention'</h5>
Invites a 'user' to join your private voice channel
  
<h5>[p]vc limit 'int'</h5>
Sets the user limit as 'int' for your private voice channel, use 0 to set it to uncapped
  
<h5>[p]vc request 'user mention'</h5>
Requests to join "user"'s private voice channel, only works when used on the channel's owner
  
<h5>[p]vc kick 'user mention'</h5>
Kicks 'user' from your private voice channel and removes their permissions to join
  
<h5>[p]vc mute 'user mention'</h5>
Disables "user"'s permissions to speak/stream/use camera/type in vc text chat in your private voice channel

<h5>[p]vc unmute 'user mention'</h5>
Enables "user"'s permissions to speak/stream/use camera/type in vc text chat in your private voice channel
  
<h5>[p]vc claim</h5>
Claims a private voice channel as yours if the owner is no longer present
  
<h5>[p]vc transfer 'user mention'</h5>
Transfers private voice channel ownership to 'user'

  
<h3># reputation</h3>
  
<h4>Gives users +1 rep everytime someone thanks them</h4>

<h5>[p]repremove 'user mention' 'amount to remove'</h5>
Removes 'amount' of reputation from 'user'
  
<h5>[p]checkrep 'user mention'</h5>
Checks the amount of rep 'user' has

  
<h3># rolebuy</h3>

<h4>Allows users to buy roles using redbot currency</h4>
  
<h5>[p]buy 'role mention'</h5>
Buys 'role' and removes currency from user

  
<h3># usergate</h3>
  
<h4>Prevents user accounts that are under 7 days old from joining the server</h4>
  
  
<h3># verifier</h3>
  
<h4>Verifies users using a gui</h4>
  
<h5>[p]verify 'user mention'</h5>
Removes 'user' unverified role and gives them their selected (from gui) verified role
