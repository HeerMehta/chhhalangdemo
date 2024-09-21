import React, { useState } from 'react';
import Message from './Message';
import InputBox from './InputBox';
import { handleChatQuery } from '../services/ChatService';

import './css/Chatbot.css';

const Chatbot = () => {
  const [messages, setMessages] = useState([]);

  const handleSendMessage = async (userMessage) => {
    const newMessages = [...messages, { type: 'user', text: userMessage }];
    setMessages(newMessages);

    const botResponse = await handleChatQuery(userMessage);
    setMessages([...newMessages, { type: 'bot', text: botResponse }]);
  };

  return (
    <div className="chatbot-container">
      <div className="chat-window">
        {messages.map((msg, index) => (
          <Message key={index} message={msg} />
        ))}
      </div>
      <InputBox onSendMessage={handleSendMessage} />
    </div>
  );
};

export default Chatbot;
