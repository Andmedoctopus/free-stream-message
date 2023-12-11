import { useState } from "react";

export const SendMessage = () => {
  const [inputValue, setInputValue] = useState("");

  const sendMessage = () => {
    fetch("http://localhost:8000/api/v1/messages/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: inputValue }),
    });
  };

  const onInputMassageChange = (event: any) => {
    setInputValue(event.target.value);
  };
  return (
    <div>
      <h1>Insert your Message</h1>
      <div>
        <input
          type="text"
          name="inputText"
          value={inputValue}
          onChange={onInputMassageChange}
        ></input>
        <button onClick={sendMessage}>Send Message</button>
      </div>
    </div>
  );
};
