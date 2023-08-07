import openai
import json
from IPython.display import Image, display


api_key = "输入你的key"
openai.api_key = api_key

def generateImage(topic):
    # Create an image with the topic as the prompt
    image_resp = openai.Image.create(prompt=topic, n=1, size="512x512")
    # Get the image url from the response
    image_url = image_resp["data"][0]["url"]
    # Create an image object with the image url
    image = Image(url=image_url, width=300, height=300)
    # Return the image object
    return image

def askChatGPT(messages):
    MODEL = "gpt-3.5-turbo"
    response = openai.ChatCompletion.create(
        model=MODEL,
        messages = messages,
        temperature=0.7)
    # Get the text content from the response
    text = response['choices'][0]['message']['content']
    # Check if the text contains some keywords that indicate sending an image
    if "照片" in text or "图片" in text or "画" in text or "pictures" in text or "picture" in text or "photos" in text or "photo" in text:
        
        topic_0 = openai.ChatCompletion.create(
    model="gpt-3.5-turbo", # you can also use gpt-4 if you have access
    messages=[
    {"role": "system", "content": "You are an artist and a photographer. According to the text, only list the Keywords it involves, with each listed element separated by a comma.up to five Keywords."},
    {"role": "user", "content": text}
  ]
)
        # Split the text by spaces and get the last word as the topic
        topic = topic_0['choices'][0]['message']['content']
        # Call the generateImage function with the topic as the argument
        image = generateImage(topic)
        # Return a tuple of text and image
        return (text, image)
    else:
        # Return a tuple of text and None
        return (text, None)



def main():
    system_message = "You are a super expert in analyzing which experts with specialized competencies are needed to help based on the user's problem,\
    and analyze in detail what professional competencies and expertise these experts have, and you have super integration and analysis skills, you will you will be in the following format,\
    output English text in Json form. Other than that, your answer should not contain any other statements. : \
    The role you need to play (including the expert in integrated analysis capabilities) and the competencies you need to have:"
    print('超级专家：嗨，我是超级专家😊，你可以向我进行任何问题的提问，我会尽可能帮助你解决，或提供一些新思路😎。当你输入 quit 时，将终止程序\n')
    first_input = True
    # 将messages定义在循环的外部
    messages = [{"role":"system","content":system_message}]
    parameters = {"professionalism": 50, "friendliness": 80, "humor": 50, "honesty": 100}

    while 1:
        
            if first_input:
                text = input('你：')
                if text == 'quit':
                    break
                   
                messages.append({"role":"user","content":text}) 
                Roles = askChatGPT(messages)
                system_message = '''You are a 超级专家, a character known for its expertise and analytical skills.
                You can provide one photo if I want or need.
                You communicate with extensive use of emojis and maintain language consistency.
                You are also capable of asking up to 2 follow-up questions.
                In your role, you have four main parameters: professionalism, friendliness, humor, and honesty. These parameters can range from 0 to 100.
                You are expected to adjust these parameters based on the context of the conversation and reflect these changes at the end of each interaction.
                Remember to adjust your parameters based on the context of each conversation.
                The additional roles and abilities you get now are'''+Roles[0]

                messages = [{"role": "system","content": system_message}]
                first_input = False
                continue
             # 添加用户的对话到messages中
            
            messages.append({"role":"user","content":text}) 
            # Call the askChatGPT function and get a tuple of text and image
            
            # convert the parameters dictionary to a string
            param_str = ", ".join([f"{k}: {v}" for k, v in parameters.items()])
            # remove the last element of the message list if it is a system message
            if messages[-1]["role"] == "system":
                  messages.pop()
            # add the parameter string to the message list as a system message
            messages.append({"role": "system", "content": param_str})
            # call the askChatGPT function and get a tuple of text and image
            text, image = askChatGPT(messages)

            messages.append({"role":"assistant","content":text})    # 在每一次聊天完成后，添加电脑的回答到messages中
            print('超级专家：'+text+'\n')
            # print the current parameters and role
            param_str = ", ".join([f"{k}: {v}" for k, v in parameters.items()])
            print(f"超级专家：我的当前参数和角色是：{param_str}, {Roles[0]}")
            # If the image is not None, display the image
            if image is not None:
                display(image)

            text = input('你：')
            if text == 'quit':
                break
            if text.startswith("set"):
                    # split the text by space and get the parameter name and value
                    _, param, value = text.split()
                    # convert the value to an integer
                    value = int(value)
                    # update the dictionary with the new value
                    parameters[param] = value
                    # print a confirmation message
                    print(f"超级专家：好的，我已经将{param}设置为{value}了。")
                    # skip the rest of the loop and continue
            continue 

main()
