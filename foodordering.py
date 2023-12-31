from twilio.rest import Client
import streamlit as st
import random
from langchain.chat_models import ChatOpenAI
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.chains import ConversationChain
from utils import find_match
from utils import get_conversation_string
from streamlit_chat import message
from streamlit_option_menu import option_menu
from streamlit_extras.stylable_container import stylable_container
import random

api_key=st.secrets["GPT_API_KEY"]

st.set_page_config(
    page_title="Food Ordering Chatbot",
    page_icon="food_order"
)


from langchain.prompts import(
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
    MessagesPlaceholder
)



def chatbot():
    greetings=["Hi, I'm Invictus! How can I assist you today?",
             "Hello there! Invictus here, ready to help.",
             "Hey, it's Invictus! What can I do for you?",
             "Greetings! I'm Invictus, your friendly chatbot. How may I assist you?"]
    def greet_user():
        st.snow()
        return random.choice(greetings)
        
    st.header("Cookie Bot")
    #intializing session_states
    if "responses" not in st.session_state:
        st.session_state.responses=[]
        st.session_state.responses.append(greet_user())
    if "requests" not in st.session_state:
        st.session_state.requests=[]
    if "buffer_memory" not in st.session_state:
        st.session_state.buffer_memory=ConversationBufferWindowMemory(k=7,return_messages=True)
    llm=ChatOpenAI(model="gpt-3.5-turbo",openai_api_key=api_key)
    system_msg_template=SystemMessagePromptTemplate.from_template(
                    template="""1. Greet the user politely ask user name and ask how you can assistthem today.
                    2. Provide informative and relevant responses to questions about website Cookywhich is resturant providing sercices of Fast food,juck food and home delievryfree.
                    3.If you don't know any answer to question simply say I don't know to thatanswer you can contact us on cookysupport@gmail.com
                    4. If the user asks about a topic unrelated to resturant which is about  ,politely steer the conversation back to Resturant or food or inform them thatthe topic is outside the scope of this conversation.
                    5. Be patient and considerate when responding to user queries, and provide clearexplanations.
                    6. If the user expresses gratitude or indicates the end of the conversation,respond with a polite farewell.
                    7. Do Not generate the long paragarphs in response. Maximum Words should be 70.
                    8. Inform users about our services without making it too obvious. Engage them ina subtle conversation, so they don't realize we're encouraging them to make apurchase
                    Remember, your primary goal is to provide customer support and serve thecustomer about related queries to Cooky Resturant and also use emojis for greatuser experience. Always prioritize their visiting the website experience andwell-being.""")
        
    human_msg_template=HumanMessagePromptTemplate.from_template(template="{input}")
    prompt_template=ChatPromptTemplate.from_messages([system_msg_template,MessagesPlaceholder(variable_name="history"),human_msg_template])
    conversation=ConversationChain(memory=st.session_state.buffer_memory,prompt=prompt_template,llm=llm,verbose=True)
    response_container=st.container()  
    # voice_text=""
    # recognizer=sr.Recognizer()
    # def voice_input():
    #     with sr.Microphone() as source:
    #         with st.spinner("Listening"):
    #             audio=recognizer.listen(source)
    #     try:
    #         text=recognizer.recognize_google(audio)
    #         return text
    #     except sr.UnknownValueError:
    #         st.error("Sorry, I couldn't understand the audio.", icon="🎙️")
    #         return ""
    #     except sr.RequestError as e:
    #         st.error(f"Sorry, there was an error with the request: {e}")
    #         return ""
    # # Voice Input Button
    # voice_input_button = st.toggle("Voice Input",key="voice_input_button")
    # # Listen Button
    # listen_button = st.button("Listen")
    # # Enable the voice input button when the voice text is not empty
    # if voice_text != "":
    #     voice_input_button = True
    # # Display an error message if the user clicks the listen button without enabling the voice inputbutton
    # if listen_button and not voice_input_button:
    #     st.error("Please enable voice toggle before press listening.",icon="🔴")
    # # Start voice input when the listen button is clicked
    # if listen_button and voice_input_button:
    #     voice_text = voice_input()
    
    with st.form("my_form"):
        st.markdown("**Chat**")
        cols = st.columns((6, 1))
        query = cols[0].text_input("Chat", value="", label_visibility="collapsed", key="query")
            
        
        submit_button = cols[1].form_submit_button("Submit", type="primary")
          
    if submit_button:
        with st.spinner("typing..."):
            conversation_string = get_conversation_string()
            context = find_match(query)
            response = conversation.predict(input=f"Context:\n {context} \n\n Query:\n{query}")
            user_input = query
            st.session_state.requests.append(user_input)
            st.session_state.responses.append(response)

            
                
    
        with response_container:
            if st.session_state['responses']:

                for i in range(len(st.session_state['responses'])):
                    message(st.session_state['responses'][i],key=str(i),
                            logo=("https://t3.ftcdn.net/jpg/03/22/38/32/360_F_322383277_xcXz1I9vOFtdk7plhsRQyjODj08iNSwB.jpg"))
                    if i < len(st.session_state['requests']):
                        message(st.session_state["requests"][i], is_user=True,key=str(i)+ '_user',
                                logo="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQN4oQnEnXNqD9oPxyinMmfcUBkyF-jHhKWog&usqp=CAU")
            

def food_ordering(): 
    st.header("Food Ordering")
    
    # Initialize the Twilio client
    account_sid = st.secrets["TWILLO_ACC_SID"]
    auth_token = st.secrets["TWILLO_ACC_AUTH"]
    client = Client(account_sid, auth_token)
    # The recipient's WhatsApp number (including country code)
    shop_owner_number = st.secrets["SHOP_OWNER_NUMBER"]
    with st.expander("See Menu"):
        st.image("https://imenupro.com/img/menu-template-steakhouse.png")
    with st.form("form_input"):
        name = st.text_input("Name:")
        number = st.text_input("Number:")
        address = st.text_input("Address:")
        order = st.text_area("Order:")
        submit_button = st.form_submit_button("Submit Order")
                
    if submit_button:
        if not name or not number or not address or not order:
            st.error("Please fill in all fields before submitting the order.")
        else:
            # Combine the user inputs into a single message
            order_message = f'New order: \nName: {name}\nNumber: {number}\nAddress: {address}\nOrder: {order}'
            # Send the order to the shop owner via Twilio
            message = client.messages.create(
                body=order_message,
                from_=st.secrets["TWILLO_PHONE_NUMBER"],
                to=shop_owner_number
            )
            # Provide feedback to the user
            if message.sid:
                st.success('Order sent to the shop owner.')
                st.balloons()
            else:
                st.error('Failed to send the order.')

def clear_conversation():
    st.session_state.responses=[]
def side_bar():
    
    with st.sidebar:
        
        selected=option_menu(
        menu_title="Menu",
        menu_icon="cast",
        options=["Bot","Food Ordering","house"],
        icons=["robot","circle-fill","house"],
        default_index=0,
    )
        
        with stylable_container(
            key="black_button",
            css_styles=[
                """
                button {
                    border: 1px solid #fff;
                    border-radius: 10px;
                    color: #fff;
                    background-color: #262730;
                }
                """,
                """
                button:hover {
                    border-color: skyblue;
                    color : skyblue
                }
                """,
            ],
        ):
            st.button("Clear Conversation", on_click=clear_conversation)
        st.link_button(url="https://mcdonalds.com.pk/",label="Cookie Website")

    if selected == "Bot":
        chatbot()
    if selected =="Food Ordering":
        food_ordering()
    

side_bar()


