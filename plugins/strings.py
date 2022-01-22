
from pyrogram import __version__
from info import (
    OWNER_ID,
    CUSTOM_START_MESSAGE
)

if CUSTOM_START_MESSAGE:
    START_MESSAGE = CUSTOM_START_MESSAGE
else:
    START_MESSAGE = """<b>Hello {mention}</b>,
Mimi ni robot wa kuhifadhi media,text n.k,
unaweza kuvipata kwa kutuma neno kwenye group au ukiwa inline mode na nkuletea unachotaka hapo  hapo shart kiwe kwenye database ya admin husika,

bonyeza help kuweza kujua jinsi ya kuongeza data<b>(ni kwa admins waliopo kwenye database yetu tu ndiyo wataiona hii help button)</b> 

Jinsi ya kujiunga na maelezo zaidi bonyeza about batan
"""

HELP_MESSAGE = f"""<b><u>Main Commands</u></b>
○ <b>/add</b> <i>[neno la kutaftia data husika] [message or reply to message]</i>
    <i>ongeza data kwenye database Mfano /add soz</i>
    
○ <b>/delete</b> <i>[neno la data uliyotaka kufuta]</i>
    <i>kufuta data kutoka kwenye database Mfano /delete soz</i>
    
○ <b>/filters</b>
    <i>kuangalia data zote ulizotuma kwenye database</i>
    
○ <b>/admin</b>
    <i>kuangalua maendeleo yako kwenye huduma zetu</i>
   """ 
ABOUT_MESSAGE = f"""💥💥💥💥💥💥💥💥💥💥💥
         MWONGOZO MFUPI

Bot hii imetngenezwa na
<b>○ Imetengenezwa na: <a href='tg://user?id={OWNER_ID}'>HASSAN RANADHANI</a>

Ilikuweza kutumia huyu robot kwenye group lako bonyeza maneno Hassan Ramadhan haipo juu kisha tuma jina lako.

    🌸🌸Gharama🌸🌸
wiki ya kwanza ni ofa  ili kujifunza jinsi ya kumtumia lakini baada ya hapo ni sh 1000 kila wiki.
gharama hizi ni kwa ajili ya kulipia utumiaji Wa robot telegram

    🤷‍♂🤷‍♂Jinsi ya kumuunga
Ukishaongezwa kwenye list ya admin wetu utaarifiwa kisha baada ya hapo utatuma command /niunge kwenye magrup yako iliaweze kufanya kazi kwa data utakazo MPA.


Kwa msaada zaidi : <a href='https://t.me/+NlxxLyYIY1hiMWFk'>BONYEZA HAPA </a></b>
"""

MARKDOWN_HELP = """<b><u>Markdown Formatting</u></b>
○ <b>Bold Words</b> :
    format: <code>*Bold Text*</code>
    show as: <b>Bold Text</b>
    
○ <b>Italic Text</b>
    format: <code>_Italic Text_</code>
    show as: <i>Italic Text</i>
    
○ <b>Code Words</b>
    format: <code>`Code Text`</code>
    show as: <code>Code Text</code>
    
○ <b>Under Line</b>
    format: <code>__UnderLine Text__</code>
    show as: <u>UnderLine Text</u>
    
○ <b>StrikeThrough</b>
    format: <code>~StrikeThrough Text~</code>
    show as: <s>StrikeThrough Text</s>
    
○ <b>Hyper Link</b>
    format: <code>[Text](https://t.me/CodeXBotz)</code>
    show as: <a href='https://t.me/CodeXBotz'>Text</a>
    
○ <b>Buttons</b>
    <u>Url Button</u>:
    <code>[Button Text](buttonurl:https://t.me/CoddeXBotz)</code>
    <u>Alert Button</u>:
    <code>[Button Text](buttonalert:Alert Text)</code>
    <u>In Sameline</u>:
    <code>[Button Text](buttonurl:https://t.me/CodeXBotz:same)</code></i>
○ <b>Notes:</b>
    <i>Keep every Buttons in Seperate line when formating</i>
    <i>Your alert message text must be less than 200 characters, otherwise bot will ignore that button</i>
○ <b>Tip:</b> <i>You can add buttons for sticker and video note in /add command</i>"""
