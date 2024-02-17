# -*- coding: utf-8 -*-
#pragma execution_character_set("utf-8")

from openai import OpenAI
import time

client = OpenAI()

assistant  = client.beta.assistants.retrieve("asst_X1FYFTIy1Mw4mJPxp08eEHhJ")

thread = client.beta.threads.create()

message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="帮我看看属鼠的人2024年的运势",
)

run = client.beta.threads.runs.create(
  thread_id=thread.id,
  assistant_id=assistant.id,
)


while 1:
    run = client.beta.threads.runs.retrieve(
      thread_id=thread.id,
      run_id=run.id
    )

    if run.status == 'completed':
        messages = client.beta.threads.messages.list(
          thread_id=thread.id
        )
        print(messages)
        break
    elif run.status in ["in_progress"]:
        time.sleep(3)
        break
    else:
        print(run)
        break

client.close()