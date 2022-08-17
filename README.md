<div id="header" align="center">
  <img src="https://i.imgur.com/1heyRLg.gif" width="250"/>
</div>
<div id="badges" align="center">
<a href="https://discordapp.com/users/365398642334498816">
  <img src="https://img.shields.io/badge/Discord-blue?style=flat&logo=Discord&logoColor=white" alt="Discord"/>
</a>
</div>

<div id="Instalalation" align="center">

# Team Punistic Cogs

<br />
<br />

## Installation

<br />

</div>

- `
[p] is your prefix
`



<br />

1. `
[p]repo add tpun-cogs https://github.com/batman202012/tpun
`

<br />

2. `
[p]cog install tpun-cogs <cog-folder-name>
`

<br />

3. `
[p]load <cog-folder-name>
`

<br />


<div id="coglist" align="center">

## Cog list

<br />

</div>

- [Private Voice Channels](#pvc)

<br />

- [Reputation](#rep)

<br />

- [Role Buy](#rolebuy)

<br />

- [Usergate](#usergate)

<br />

- [Verifier](#verifier)

<br />
<br />

<div id="pvc" align="center">

## PVC 



<br />

### Cog for creating private voice channels

</div>

<div align="right">

[top](#coglist)

</div>

<br /> 

- `
[p]vc setup
`

##### Creates command channel for pvc and selects the channel's default joinable role (used for lock/unlock)

<br />
<br />

- `
[p]vc create <name>
`


##### Creates a voice channel in the catergory the pvc command channel is in with name 'name'

<br />
<br />

- `
[p]vc gui
`

##### Opens a gui for voice channel creation

<br />
<br /> 

- `
[p]vc delete
`

##### Deletes your private voice channel

<br />
<br />  

- `
[p]vc name
`

##### Returns the name of your private voice channel

<br />
<br />

- `
[p]vc list
`

##### Returns an embed of personal voice channel and owners

<br />
<br />

- `
[p]vc rename <name>
`

##### Renames your private voice channel to 'name'

<br />
<br />

- `
[p]vc region <int>
`

##### Changes your private voice channel region to 'int'
###### The list of avaliable regions are as follow 0=Auto, 1=US West, 2=US East, 3=US South, 4=EU West, 5=EU Central, 6=Brazil, 7=Hong Kong, 8=Brazil, 9=Japan, 10=Russia, 11=Sydney, 12=South Africa

<br />
<br /> 

- `
[p]vc lock
`

##### Prevents the roles used in vc setup from joining the channel

<br />
<br /> 

- `
[p]vc unlock
`

##### Allows the roles used in vc setup to join the channel

<br />
<br /> 

- `
[p]vc invite <user mention>
`

##### Invites a 'user' to join your private voice channel

<br />
<br /> 
<h5>

- `
[p]vc limit <int>
`

##### Sets the user limit as 'int' for your private voice channel, use 0 to set it to uncapped
<br />
<br /> 

- `
[p]vc request <user mention>
`

##### Requests to join "user"'s private voice channel, only works when used on the channel's owner

<br />
<br />
  
- `
[p]vc kick <user mention>
`

##### Kicks 'user' from your private voice channel and removes their permissions to join

<br />
<br />
  

- `
[p]vc mute <user mention>
`

##### Disables "user"'s permissions to speak/stream/use camera/type in vc text chat in your private voice channel

<br />
<br />

- `
[p]vc unmute <user mention>
`

##### Enables "user"'s permissions to speak/stream/use camera/type in vc text chat in your private voice channel

<br />
<br />
  
- `
[p]vc claim
`

##### Claims a private voice channel as yours if the owner is no longer present

<br />
<br />

- `
[p]vc transfer <user mention>
`

##### Transfers private voice channel ownership to 'user'

<br />
<br />

- `
[p]vc setup
`

##### Command for setting up private voice channels in the server

<br />
<br />

<div id="rep" align="center">

## Reputation

</div>

<br />

### Gives users +1 rep everytime someone thanks them

<div align="right">

[top](#coglist)

</div>

<br />

- `
[p]repremove <user mention> <amount to remove>
`

##### Removes 'amount' of reputation from 'user'

<br />
<br />  

- `
[p]checkrep <user mention>
`

##### Checks the amount of rep 'user' has

<br />
<br />

<div id="rolebuy" align="center">

## Rolebuy

<br />

### Allows users to buy roles using redbot currency

</div>

<div align="right">

[top](#coglist)

</div>

<br />

- `
[p]buy <role mention>
`

##### Buys 'role' and removes currency from user

<br />
<br />

<div id="usergate" align="center">

## Usergate

<br />

### Prevents user accounts that are under 'days' old from joining the server

<br />

</div>

<div align="right">

[top](#coglist)

</div>

<br /> 

- `
[p]usergate <days>
`

##### Sets the number of 'days' a user's account must exist

<br />
<br />

<div id="verifier" align="center">

## Verifier

<br />

### Verifies users as a gender role using a gui

</div>

<div align="right">

[top](#coglist)

</div>

<br /> 

- `
[p]verify <user mention>
`

##### Removes 'user' unverified role and gives them their selected (from gui) verified role

<br />
<br />

- `
[p]vsetup
`

##### set the male, female, non-binary and unverified roles to use for verification

<br />
<br />
