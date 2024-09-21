import React from 'react';
import './css/Message.css';

const Message = ({ message }) => {
  return (
    <div>
      <span>{message.text}</span>
    </div>
  );
};

export default Message;