import React, { useState } from 'react';
// import './InputBox.css';

const InputBox = ({ onSendMessage }) => {
  const [inputValue, setInputValue] = useState('');

  const handleInputChange = (e) => {
    setInputValue(e.target.value);
  };

  const handleSendClick = () => {
    if (inputValue.trim()) {
      onSendMessage(inputValue);
      setInputValue('');
    }
  };

  return (
    <div className="input-box">
      <input
        type="text"
        value={inputValue}
        onChange={handleInputChange}
        placeholder="Ask something..."
      />
      <button onClick={handleSendClick}>Send</button>
    </div>
  );
};

export default InputBox;
