from pyrogram import filters,enums,Client,idle
import os
import sys
import subprocess
import asyncio
import traceback
import io
from urllib.parse import urlparse 

API_ID = os.environ['API_ID']
API_HASH = os.environ['API_HASH']
STRING = os.environ['STRING']

user = Client('Ubot', 

        api_id=API_ID, 

        api_hash=API_HASH, 

        session_string=STRING,

        in_memory=True) 

 
asisstant = Client('asisstant',
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=AS_STRING,
        in_memory=True)
  



@user.on_message(filters.regex("^\.sh") & filters.user('me'))

@user.on_edited_message(filters.regex("^\.sh") & filters.user('me'))

async def shell(client, m):

    cmd = m.text.replace(".sh ","")

    if cmd == '.sh':

        return await user.edit_message_text(m.chat.id,text="No command to execute was given.",message_id=m.id)

    msg = await user. edit_message_text(m.chat.id,text="__Processing...__",message_id=m.id)

    shell = (await shell_exec(cmd))[0]

    if len(shell) > 3000:

        with open("shell_lucas.txt", "w") as file:

            file.write(shell)

        with open("shell_lucas.txt", "rb") as doc:

          if m.chat.is_forum == True:

            await user.send_document(m.chat.id,

                document=doc,

                file_name=doc.name,message_thread_id=m.topics.id)

          else:

            await user.send_document(m.chat.id,

                document=doc,

                file_name=doc.name)

          await user.delete_messages(m.chat.id, msg.id)

          try:

            os.remove("shell_lucas.txt")

          except:

            pass

    elif len(shell) != 0:

        await user.edit_message_text(m.chat.id,text=shell,message_id=m.id)

    else:

        await user.edit_message_text(m.chat.id,"No Reply",message_id=m.id)

@user.on_message(filters.regex("^\.run") & filters.user('me'))

@user.on_edited_message(filters.regex("^\.run") & filters.user('me'))

async def evaluation_cmd_t(client, m):

  cmd = m.text.replace(".run ","")

  if cmd == '.run':

    return await user.edit_message_text(m.chat.id,text="__No evaluate message!__",message_id=m.id)

  status_message = await user. edit_message_text(m.chat.id,text="__Processing eval pyrogram...__",message_id=m.id)

  old_stderr = sys.stderr

  old_stdout = sys.stdout

  redirected_output = sys.stdout = io.StringIO()

  redirected_error = sys.stderr = io.StringIO()

  stdout, stderr, exc = None, None, None

  try:

    await aexec(cmd, client, m)

  except Exception:

    exc = traceback.format_exc()

  stdout = redirected_output.getvalue()

  stderr = redirected_error.getvalue()

  sys.stdout = old_stdout

  sys.stderr = old_stderr

  evaluation = ""

  if exc:

    evaluation = exc

  elif stderr:

    evaluation = stderr

  elif stdout:

    evaluation = stdout

  else:

    evaluation = "Success"

  final_output = f"**EVAL**:\n`{cmd}`\n\n**OUTPUT**:\n`{evaluation.strip()}`\n"

  if len(final_output) > 4096:

    with open("LucasEval.txt", "w+", encoding="utf8") as out_file:

      out_file.write(final_output)

    await m.reply_document(document="LucasEval.txt",

                           caption=f"<code>{cmd[: 4096 // 4 - 1]}</code>",

                           disable_notification=True)

    await user.delete_messages(m.chat.id, status_message.id)

    os.remove("LucasEval.txt")

  else:

    await user.edit_message_text(m.chat.id,

                                text=final_output,

                                message_id=m.id)

async def aexec(code, c, m):

  exec("async def __aexec(c, m): " + "\n p = print" +

       "\n replied = m.reply_to_message" + "".join(f"\n {l_}"

                                                   for l_ in code.split("\n")))

  return await locals()["__aexec"](c, m)

async def shell_exec(code, treat=True):

    process = await asyncio.create_subprocess_shell(code, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.STDOUT)

    stdout = (await process.communicate())[0]

    if treat:

        stdout = stdout.decode().strip()

    return stdout, process



@asisstant.on_message(filters.chat(-1001549051935)) 
async def sharing(client,m): 
    text = m.text or m.caption 
    urls = [] 
    words = text.split() 
    for word in words: 
        url_components = urlparse(word) 
        if url_components.scheme and url_components.netloc: 
          urls.append(word) 
    jumlah = 0 
    for url in urls: 
        if urlparse(url).path in ['/ADITXROBOT','/SATUNUSAOFFICIAL_BOT']: 
            split_url = urlparse(url).query.split("=")[1] 
            query = f"/start {split_url}" 
            bot = str(urlparse(url).path.replace('/','')) 
            await asisstant.send_message(bot,query) 
            await asyncio.sleep(5) 
            async for message in asisstant.get_chat_history(bot,limit=1): 
            if message.video: 
                id = message.video.file_id 
                await asisstant.send_video("@aslibukansuci",video=id) 
                jumlah += 1 
    if jumlah >= 1: 
        await asisstant.send_message(1928677026,f'**Berhasil mengirim {jumlah} video ke Channel** @aslibukansuci')


asisstant.start()
user.start()
idle()
asisstant.stop()
user.stop()
