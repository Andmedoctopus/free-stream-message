import { useEffect, useState } from "react";

export const GetMessage = () => {
  const [text, setText] = useState<string>("");

  const speech = (textToRead: string) => {
    console.log("in speech", textToRead);
    if (textToRead) {
      let utterance = new SpeechSynthesisUtterance(textToRead);
      console.log(speechSynthesis);

      speechSynthesis.speak(utterance);
    }
  };

  useEffect(() => {
    const socket = new WebSocket(
      "ws://localhost:8000/ws/v1/message/streamer/c6d0c948-a4ee-4e8f-9267-96c3f362dd7a"
    );
    const handleMessage = (event: any) => {
      const receiveMessage = JSON.parse(event.data).message;
      setText(receiveMessage);
    };
    socket.addEventListener("message", handleMessage);
    return () => {
      socket.removeEventListener("message", handleMessage);
    };
  }, []);

  useEffect(() => {
    speech(text);
  }, [text]);

  const [inputValue, setInputValue] = useState("");

  return (
    <div>
      <h1 id="h1">{text}</h1>
      <button
        style={{ width: "200px", height: "40px", color: "red" }}
        onClick={() => {
          speech("hello hanna");
        }}
      >
        Tap me
      </button>
      <input
        type="text"
        name="input"
        value={inputValue}
        onChange={(event) => {
          setInputValue(event.target.value);
        }}
      ></input>
      <button
        style={{ width: "200px", height: "40px", color: "red" }}
        onClick={() => {
          setText(inputValue);
        }}
      >
        Go input
      </button>
    </div>
  );
};
