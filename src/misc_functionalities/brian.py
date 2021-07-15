import random

async def generate_words(message):
    m_word = random.choice(open('src/misc_functionalities/brian/mlist.txt').readlines())
    r_word = random.choice(open('src/misc_functionalities/brian/rlist.txt').readlines())
    await message.channel.send(m_word + r_word)