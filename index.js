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

client.login(process.env.DISCORD_TOKEN)
