import base64
import binascii
import collections
import string
import urllib.parse
import discord
from discord.ext import commands

# Encoding/Decoding from various schemes.

import json
MORSE_CODE_DICT = json.load(open("lib/utils/morse.json"))

class Encoding(commands.Cog):
    """Simple Encryption/Decryption"""
    def __init__(self, bot):
        self.bot = bot
        self.hidden = False
 
    @commands.command(description = "Encode/Decode Morse values")
    async def morse(self,ctx, encode_or_decode, *,  message):
        if encode_or_decode == 'decode':
            message += " "
            decipher = ""
            citext = ""
            for letter in message:
                if letter != " ":
                    i = 0
                    citext += letter
                else:
                    i += 1
                    if i == 2:
                        decipher += " "
                    else:
                        decipher += list(MORSE_CODE_DICT.keys())[
                            list(MORSE_CODE_DICT.values()).index(citext)
                        ]
                        citext = ""
            embed = discord.Embed(title = "Morse Code",description = f"```{message}``` decoded is ```{decipher}```" ,color=discord.Colour.random())
            await ctx.send(embed = embed)

        if encode_or_decode == 'encode':
            message = message.upper()
            cipher = ""
            try:
                for letter in message:
                    if letter != " ":
                        cipher += MORSE_CODE_DICT[letter] + " "
                    else:
                        cipher += " "
            except KeyError:
                await ctx.send("I can only encode `A-Z`, `0-9` and some symbols")
                return
            embed = discord.Embed(title = "Morse Code",description = f"```{message}``` encoded is ```{cipher}```" ,color=discord.Colour.random())
            await ctx.send(embed = embed)


    @commands.command(description = "Encode/Decode b64 values", help = "b64 <`encode`/`decode`> <string>")
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def b64(self, ctx, encode_or_decode, *, string):
        byted_str = str.encode(string)
        
        if encode_or_decode == 'decode':
            decoded = base64.b64decode(byted_str).decode('utf-8')
            await ctx.send(decoded)
        
        if encode_or_decode == 'encode':
            encoded = base64.b64encode(byted_str).decode('utf-8').replace('\n', '')
            await ctx.send(encoded)
    
    @commands.command(description = "Encode/Decode b32 values", help = "b32 <`encode`/`decode`> <string>")
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def b32(self, ctx, encode_or_decode, *, string):
        byted_str = str.encode(string)

        if encode_or_decode == 'decode':
            decoded = base64.b32decode(byted_str).decode('utf-8')
            await ctx.send(decoded)
        
        if encode_or_decode =='encode':
            encoded = base64.b32encode(byted_str).decode('utf-8').replace('\n', '')
            await ctx.send(encoded)

    @commands.command(description = "Encode/Decode binary values", help = "binary <`encode`/`decode`> <string>")
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def binary(self, ctx, encode_or_decode, *, string):
        if encode_or_decode == 'decode':
            string = string.replace(" ", "")
            data = int(string, 2)
            decoded = data.to_bytes((data.bit_length() + 7) // 8, 'big').decode()
            await ctx.send(decoded)
        
        if encode_or_decode == 'encode':
            encoded = bin(int.from_bytes(string.encode(), 'big')).replace('b', '')
            await ctx.send(encoded)

    @commands.command(description = "Encode/Decode hex values", help = "hex <`encode`/`decode`> <string>")
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def hex(self, ctx, encode_or_decode, *, string):
        if encode_or_decode == 'decode':
            string = string.replace(" ", "")
            decoded = binascii.unhexlify(string).decode('ascii')
            await ctx.send(decoded)
        
        if encode_or_decode == 'encode':
            byted = string.encode()
            encoded = binascii.hexlify(byted).decode('ascii')
            await ctx.send(encoded)

    @commands.command(description = "Encode/Decode URL values", help = "url <`encode`/`decode`> <string>")
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def url(self, ctx, encode_or_decode, *, message):
        if encode_or_decode == 'decode':
            
            if '%20' in message:
                message = message.replace('%20', '(space)')
                await ctx.send(urllib.parse.unquote(message))
            else:
                await ctx.send(urllib.parse.unquote(message))
        
        if encode_or_decode == 'encode':
            await ctx.send(urllib.parse.quote(message))

def setup(bot):
    bot.add_cog(Encoding(bot))