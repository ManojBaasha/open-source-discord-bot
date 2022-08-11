//import stuff
const { Client, GatewayIntentBits } = require('discord.js');
const { token } = require('./config.json');
const dotenv = require('dotenv');

//create client instance
const client = new Client({ intents : [GatewayIntentBits.Guilds] });
dotenv.config();

client.once('ready', () => {
    console.log('Ready!');
});

let fs = require("fs")
const readFileLines = filename =>
   fs.readFileSync(filename)
   .toString('UTF8')
   .split('\n');
let arr = readFileLines('questions.txt');


client.on('interactionCreate',async interaction => {
    if(!interaction.isChatInputCommand()) return;

    const {commandName} = interaction;

    if(commandName === 'ping'){
        await interaction.reply('pong');
    } else if(commandName === 'server'){
        await interaction.reply(`Server name: ${interaction.guild.name}\nTotal members: ${interaction.guild.memberCount}`);
    } else if(commandName === 'user'){
        await interaction.reply(`Your tag: ${interaction.user.tag}\nYour id: ${interaction.user.id}`);
    } else if(commandName === 'question'){
        await interaction.reply(`${arr[Math.floor(Math.random() * arr.length)]}`);
    }
    //more guild commands at https://discord.js.org/#/docs/main/stable/class/Guild
    //more user commands at https://discord.js.org/#/docs/main/stable/class/User
});





client.login(token)
