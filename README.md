# pridebot
### version 1.1
A Discord bot that generates pride flag icons!
Built by tianders295

## Requirements:
* Python 3.6.0 or higher.
* The included flags folder, kept in `/src`
These modules need to be installed before you can run this.  
The name you type into `pip install` is given in inline code style.
* Discord.py `discord` - version 0.16.*
* NumPy `numpy`
* Pillow `pillow`
* Requests `requests`


## How to use:
### Commands:
Commands are listed like `!command parameter [attachment]`".

`!helpme` - DMs you this prompt.

`!flags` - Returns a list of flags.

`!prideflag flag [transparent PNG file]` - Superimposes the PNG file onto a 1000x1000 pride flag
of your choice. See below for a list of flags, or call `!flags`.

### Configuration Files:
In version 1.1, there are two configuration files: `config.txt` and `flaglist.txt` (all lowercase).
`config` *must* be present for the bot to run.
#### config.txt
`config` uses a not-very-special syntax for assigning keywords to pride flags.
Given a file named `lesbian.png`, the syntax would look something like this:
`lesbian: lesbian les`
#### flaglist.txt
Conversely, `flaglist` is just what the text for the `!flags` command should look like.
There's no special syntax, but it's recommended that you make your list readable.

### Flags:
The default flags included with this bot can be changed; these are just the ones included.
(Flags are listed as "Flag: list, of, keywords")

1. Lesbian:      lesbian, les, lez
2. Gay:          gay
3. Bisexual:     bisexual, bi
4. Pansexual:    pansexual, pan
5. Asexual:      asexual, ace
6. Transgender:  trans, transgender
7. Agender:      agender
8. Genderqueer:  genderqueer, gq
9. Nonbinary:    nonbinary, nb, enby
10. Bear:         bear
11. Twink:        twink
12. Butch:        butch
13. Femme:        femme 

## Special Thanks
Femme flag designed by [Noodle](http://noodle.tumblr.com)! (Link to design [here](http://noodle.tumblr.com/post/168070202366/noodle-an-idea-for-a-femme-flag-i-saw-some)) Be sure to credit them when using their design in your own instance!
