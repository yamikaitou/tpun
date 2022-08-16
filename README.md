<div id="header" align="center">
  <img src="https://i.imgur.com/1heyRLg.gif" width="250"/>
</div>
<div id="badges" align="center">
<a href="https://discordapp.com/users/365398642334498816">
  <img src="https://img.shields.io/badge/Discord-blue?style=flat&logo=Discord&logoColor=white" alt="Discord"/>
</a>
</div>

<center><h1>Team Punistic Cogs</h1>

<div id="installation"><h2>Installation</h2></center>

<h3>
```
[p] is your prefix
```
</h3>
<br />
<h4>
```
[p]repo add tpun-cogs https://github.com/batman202012/tpun
```
</h4>
<br />
<h4>
```
[p]cog install tpun-cogs <cog-name>
```
</h4>
<br />
<h4>
```
[p]load <cog-name>
```
</h4>
<br /></div>

  <center><h2>Cog list</h2>
<br />

<div id="pvc"> <h3>PVC</h3>
<br />
 <h4>Cog for creating private voice channels</h4></center>
<br />
<h5>
```
[p]vc setup
```
</h5>
Creates command channel for pvc and selects the channel's default joinable role (used for lock/unlock)
<br /><br />
<h5>
```
[p]vc create <name>
```
</h5>
Creates a voice channel in the catergory the pvc command channel is in with name 'name'
<br /><br />
<h5>
```
[p]vc gui
```
</h5>
Opens a gui for voice channel creation
<br /><br /> 
<h5>
```
[p]vc delete
```
</h5>
Deletes your private voice channel
<br /><br />  
<h5>
```
[p]vc name
```
</h5>
Returns the name of your private voice channel
  <br /><br />
<h5>
```
[p]vc rename <name>
```
</h5>
Renames your private voice channel to 'name'
<h5>
```
[p]vc region <int>
```
</h5>
Changes your private voice channel region to 'int'
The list of avaliable regions are as follow 0=Auto, 1=US West, 2=US East, 3=US South, 4=EU West, 5=EU Central, 6=Brazil, 7=Hong Kong, 8=Brazil, 9=Japan, 10=Russia, 11=Sydney, 12=South Africa
<br /><br />  
<h5>
```
[p]vc lock
```
</h5>
Prevents the roles used in vc setup from joining the channel
 <br /><br /> 
<h5>
```
[p]vc unlock
```
</h5>
Allows the roles used in vc setup to join the channel
<br /><br />  
<h5>
```
[p]vc invite <user mention>
```
</h5>
Invites a 'user' to join your private voice channel
 <br /><br /> 
<h5>
```
[p]vc limit <int>
```
</h5>
Sets the user limit as 'int' for your private voice channel, use 0 to set it to uncapped
 <br /><br /> 
<h5>
```
[p]vc request <user mention>
```
</h5>
Requests to join "user"'s private voice channel, only works when used on the channel's owner
  <br /><br />
<h5>
```
[p]vc kick <user mention>
```
</h5>
Kicks 'user' from your private voice channel and removes their permissions to join
  <br /><br />
<h5>
```
[p]vc mute <user mention>
```
</h5>
Disables "user"'s permissions to speak/stream/use camera/type in vc text chat in your private voice channel
<br /><br />
<h5>
```
[p]vc unmute <user mention>
```
</h5>
Enables "user"'s permissions to speak/stream/use camera/type in vc text chat in your private voice channel
  <br /><br />
<h5>
```
[p]vc claim
```
</h5>
Claims a private voice channel as yours if the owner is no longer present
<br /><br />
<h5>
```
[p]vc transfer <user mention>
```
</h5>
Transfers private voice channel ownership to 'user'
<br /><br />
<h5>
```
[p]vc setup
```
</h5>
Command for setting up private voice channels in the server
<br /><br />
</div>
<span id="rep">
<center>
<h3>Reputation</h3>
<br />
<h4>Gives users +1 rep everytime someone thanks them</h4>
</center>
<br />
<h5>
```
[p]repremove <user mention> <amount to remove>
```
</h5>
Removes 'amount' of reputation from 'user'
<br /><br />  
<h5>
```
[p]checkrep <user mention>
```
</h5>
Checks the amount of rep 'user' has
<br /><br />
<span id="rolebuy"><center><h3>Rolebuy</h3>
<br />
<h4>Allows users to buy roles using redbot currency</h4></center>
<br />
<h5>
```
[p]buy <role mention>
```
</h5>
Buys 'role' and removes currency from user
<br /><br /></div>
<span id="usergate"><center><h3>Usergate</h3>
<br />
<h4>Prevents user accounts that are under 'days' old from joining the server</h4></center>
<br />
<h5>
```
[p]usergate <days>
```
</h5>
Sets the number of 'days' a user's account must exist
<br /><br />
</div>  
<span id="verifier"><center><h3>Verifier</h3>
<br />
<h4>Verifies users as a gender role using a gui</h4></center>
<br />  
<h5>
```
[p]verify <user mention>
```
</h5>
Removes 'user' unverified role and gives them their selected (from gui) verified role
<br /><br />
<h5>
```
[p]vsetup
```
</h5>
set the male, female, non-binary and unverified roles to use for verification
<br /><br />
</div>
